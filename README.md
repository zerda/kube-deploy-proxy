# Description
In the kubernetes cluster, provide a proxy to update image version of deployment.

It's used in continuous deployment scenario, to avoid exposing Kubernetes API Server to Internet.

# Installation
1. Fill `AUTH_TOKEN` value with random string in base64 format, in `doc/kubernetes-example.yaml` file.
1. Apply to cluster, `kubectl apply -f doc/kubernetes-example.yaml`

# Patch the deployment
```bash
curl --request PATCH \
  --url 'http://k8s-node:32320/namespaces/default/deployments/nginx-debug/containers/nginx?image=gcr.io/google_containers/nginx-slim:0.22' \
  --header 'authorization: Bearer 563f4f2f-d33c-4087-b014-ba8b0a3f63fc'
```
