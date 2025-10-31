#!/bin/bash

apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    nano \
    htop \
    tree \
    git \
    ssh \
    sudo \
    net-tools \
    iputils-ping \
    dnsutils \
    iproute2 \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release \
    zip \
    unzip \
    jq \
    file \
    tmux \
    screen \
    rsync 

cd /workspace
wget https://github.com/prometheus/prometheus/releases/download/v2.52.0/prometheus-2.52.0.linux-amd64.tar.gz
tar -xvzf prometheus-2.52.0.linux-amd64.tar.gz

wget https://dl.grafana.com/oss/release/grafana-11.0.0.linux-amd64.tar.gz
tar -zxvf grafana-11.0.0.linux-amd64.tar.gz

pip3 install PyYAML
