# Prefill/Decode Disaggregation Grafana Dashboard Usage Guide

1. "./start_docker.sh" to setup docker
2. After enter docker, modify and update prometheus_config.yaml to update the prefill/decode IPs to actual server IP, and then run "generate_config_file.sh" to generate my_prometheus.yml config file
3. Run "./run.sh" to start both Prometheus and Grafana service
4. After step3 runs successfully, open browser to access "http://localhost:3000" in local server or "http://IP_Address:3000"(replace IP_Address with the IP Grafana server is running)
    You will need to login using the default credentials.

    username: admin
    password: admin

    The next step is to configure the data source for Grafana to scrape metrics from. Click on the "Data Source" button, select Prometheus, and specify the Prometheus url localhost:9105. If the dashboard does not display data, under the Other section for the Data Source, change the HTTP method to GET.

5. Import Grafana Dashboard
    After setup the Grafana server, then you can import a Grafana Dashboard through uploading a dashboard JSON file in the Grafana UI under Home > Dashboards > Import dashboard. You can use a file like - vLLM_PD_Cluster_Monitoring.json. Open the dashboard, and you will see different panels displaying the metrics data.

