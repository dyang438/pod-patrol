####

## Prerequisites

- Docker installed and running
- kubectl CLI tool installed
- k3d installed (lightweight local Kubernetes cluster based on k3s)

## Setup Instructions

### 1. Install dependencies

Install kubectl (CLI tool used to interact with Kubernetes clusters)

```bash
brew install kubectl
```

Install docker desktop from this link: https://www.docker.com/products/docker-desktop/

Then install k3d (lightweight wrapper to run Kubernetes in Docker)

```bash
brew install k3d
```

### 2. Create a k3d Cluster

First, create a new k3d cluster with the following command:

```bash
k3d cluster create parity-cluster
```

Verify the cluster is running:

```bash
k3d cluster list
kubectl cluster-info
```

### 2. Apply the Faulty Deployment

Deploy the faulty application:

```bash
kubectl apply -f faulty-deploy.yaml
```

### 3. Observe the Deployment

VERY IMPORTANT: if you see pods stuck in ContainerCreating State, please see the Troubleshooting section below.
Watch as pods start to spin up:

```bash
# Initial deployment
kubectl get pods -l app=faulty-app

# After a few moments...
kubectl get pods -l app=faulty-app
```

You should see the pods transition to a `CrashLoopBackOff` state after a few restarts.

View detailed information about the failing pods:

```bash
kubectl describe pods -l app=faulty-app
```

Check the logs of the failing container:

```bash
kubectl logs -l app=faulty-app
```

## Understanding What's Happening

The `faulty-deploy.yaml` file includes several intentional issues:

1. The container deliberately exits with an error code: `exit 1`
2. It references a non-existent ConfigMap key (`MISSING_KEY`) which is marked as optional so the container can start
3. The container exits shortly after starting, triggering Kubernetes to restart it
4. After multiple restart attempts in rapid succession, Kubernetes puts the pod in `CrashLoopBackOff` state

## Cleanup

When you're done with the demo, delete the deployment and cluster:

```bash
kubectl delete -f faulty-deploy.yaml
k3d cluster delete parity-cluster
```

## Troubleshooting

### Pods Stuck in ContainerCreating State

If pods get stuck in `ContainerCreating` state (longer than 1-2 minutes), do the following:

```bash
# Check if DNS resolution works
docker exec k3d-parity-cluster-server-0 nslookup registry-1.docker.io

# If it fails, update DNS configuration to use Google's DNS
docker exec k3d-parity-cluster-server-0 sh -c "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"

# Verify DNS resolution now works
docker exec k3d-parity-cluster-server-0 nslookup registry-1.docker.io
```
