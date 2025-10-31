#!/usr/bin/env python3
"""
Prometheus 配置文件生成脚本
根据用户配置的 IP 地址生成对应的 prometheus.yml
"""

import yaml
import os
import argparse
from typing import List, Dict, Any

class QuoteString(str):
    """自定义字符串类，用于强制 YAML 输出时使用单引号"""
    pass

def quote_str_representer(dumper, data):
    """自定义 YAML 表示器，确保字符串使用单引号"""
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style="'")

# 注册自定义表示器
yaml.add_representer(QuoteString, quote_str_representer)

def generate_prometheus_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据配置数据生成 Prometheus 配置
    """
    
    prometheus_config = {
        'global': {
            'scrape_interval': '15s',
            'evaluation_interval': '15s'
        },
        'scrape_configs': [
            {
                'job_name': 'prometheus',
                'static_configs': [
                    {
                        'targets': [QuoteString(f"{config_data.get('prometheus_host', 'localhost')}:{config_data.get('prometheus_port', 9105)}")]
                    }
                ]
            },
            {
                'job_name': 'vllm_pd_cluster',
                'static_configs': []
            }
        ]
    }
    
    # 添加 prefill 目标
    prefill_ips = config_data.get('prefill_ips', [])
    if prefill_ips:
        prometheus_config['scrape_configs'][1]['static_configs'].append({
            'targets': [QuoteString(f"{ip}:{config_data.get('prefill_port', 8100)}") for ip in prefill_ips],
            'labels': {
                'role': 'prefill'
            }
        })
    
    # 添加 decode 目标
    decode_ips = config_data.get('decode_ips', [])
    decode_ports = config_data.get('decode_ports', list(range(8200, 8208)))  # 8200-8207
    
    if decode_ips and decode_ports:
        decode_targets = []
        for ip in decode_ips:
            for port in decode_ports:
                decode_targets.append(QuoteString(f"{ip}:{port}"))
        
        prometheus_config['scrape_configs'][1]['static_configs'].append({
            'targets': decode_targets,
            'labels': {
                'role': 'decode'
            }
        })
    
    return prometheus_config

def load_config(config_file: str) -> Dict[str, Any]:
    """
    从 YAML 配置文件加载配置
    """
    if not os.path.exists(config_file):
        # 如果配置文件不存在，创建默认配置模板
        default_config = {
            'prometheus_host': 'localhost',
            'prometheus_port': 9105,
            'prefill_ips': ['10.0.0.1'],
            'prefill_port': 8100,
            'decode_ips': ['10.0.0.2', '10.0.0.3'],
            'decode_ports': [8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207]
        }
        
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        print(f"已创建默认配置文件: {config_file}")
        print("请修改配置文件中的 IP 地址后重新运行脚本")
        return default_config
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def save_config(config: Dict[str, Any], output_file: str):
    """
    保存 Prometheus 配置到文件
    """
    with open(output_file, 'w') as f:
        f.write("# Prometheus 配置文件\n")
        f.write("# 由配置生成脚本自动生成，请勿手动修改\n\n")
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Prometheus 配置已生成: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='生成 Prometheus 配置文件')
    parser.add_argument('-c', '--config', default='prometheus_config.yaml', 
                       help='输入配置文件路径 (默认: prometheus_config.yaml)')
    parser.add_argument('-o', '--output', default='prometheus.yml', 
                       help='输出配置文件路径 (默认: prometheus.yml)')
    parser.add_argument('--show-only', action='store_true', 
                       help='只显示配置而不保存到文件')
    
    args = parser.parse_args()
    
    # 加载用户配置
    config_data = load_config(args.config)
    
    # 生成 Prometheus 配置
    prometheus_config = generate_prometheus_config(config_data)
    
    if args.show_only:
        # 只显示配置内容
        print("生成的 Prometheus 配置:")
        print("=" * 50)
        print(yaml.dump(prometheus_config, default_flow_style=False, sort_keys=False, allow_unicode=True))
    else:
        # 保存到文件
        save_config(prometheus_config, args.output)
        
        # 显示生成的配置摘要
        print("\n配置摘要:")
        print(f"- Prometheus 监控端口: {config_data.get('prometheus_port', 9105)}")
        print(f"- Prefill 节点: {len(config_data.get('prefill_ips', []))} 个")
        print(f"- Decode 节点: {len(config_data.get('decode_ips', []))} 个")
        print(f"- 每个 Decode 节点的端口数: {len(config_data.get('decode_ports', []))}")

if __name__ == '__main__':
    main()
