# Shimon Assignment

# Installation
## Prerequisites
1. Curl
1. Docker
1. Minikube
1. Helm
1. [k6](https://k6.io/)


## Kubernetes

### Create Cluster
```bash
minikube start -n 3
```
### Install Nginx Ingress
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.metrics.enabled=true \
  --set-string controller.podAnnotations."prometheus\.io/scrape"="true" \
  --set-string controller.podAnnotations."prometheus\.io/port"="10254" \
  --set controller.extraArgs."metrics-per-host"=false
```
### Install Prometheus
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --create-namespace \
  --namespace kube-prometheus-stack
```
### Install Keda
```bash
helm repo add kedacore https://kedacore.github.io/charts

helm repo update

helm install keda kedacore/keda --namespace keda --create-namespace
```

### Install Mongo
```bash
helm install mongo charts-to-deploy/mongo
```
### Install Kafka
```bash
helm install kafka charts-to-deploy/kafka
```
### Install Customers-Management-API
```bash
helm install customers-management-api charts-to-deploy/customers-management-api
```
### Install Customers-Facing-Server
```bash
helm install customer-facing-server charts-to-deploy/customer-facing-server
```
### Install Scale Objects
```bash
helm install scale charts-to-deploy/scale
```


### Expose the Ingress Through Your Localhost
```bash
kubectl port-forward service/ingress-nginx-controller -n ingress-nginx 8080:80
```

</br></br>

# Test the Application
Before testing the application, please ensure that all pods are running. You can check this with the following command (it may take about 7 minutes):
```bash
kubectl get all --namespace default
```

#### Send Data to Kafka via Curl:
```bash
curl -X POST http://localhost:8080/buy \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Shimon",
    "userid": "Shimi123",
    "price": 56.0
  }'
```
#### Get the Data from the API Service
```bash
curl http://127.0.0.1:8080/getAllUserBuys 
```

### Test Keda via K6
```bash
k6 run --summary-trend-stats="min,avg,med,p(90),p(99),max,count" --summary-time-unit=ms k6.js
```
</br>

### Please Ensure That You Are Not Connected to a VPN/Office Network, as it may cause IP duplication and prevent the cluster from working.
