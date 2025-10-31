#!/bin/bash

cd /workspace/prometheus-2.52.0.linux-amd64 
cp ../my_prometheus.yml .
nohup ./prometheus --config.file=./my_prometheus.yml --storage.tsdb.path=./vllm_pd_cluster_data --web.listen-address=:9105  > prometheus_vllm_pd_cluster.log 2>&1 &

sleep 10

cd /workspace/grafana-v11.0.0
nohup ./bin/grafana-server &


