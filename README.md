# Description
In the kubernetes cluster, setup a proxy to update image version of deployment.

It's used in continuous deployment scenario, to avoid exposing Kubernetes API Server to Internet.

# Installation
1. Replace `AUTH_TOKEN` value with random string in base64 format, in `doc/manifests/secret.yaml` file.
1. Replace or remove `host` and `tls` values in `doc/manifests/ingress.yaml` file.
1. Apply all manifests to to cluster, `kubectl apply -f doc/manifests/`.

# Patch the deployment
```bash
curl --request PATCH \
  --url 'https://deploy-proxy.example.com/namespaces/default/deployments/nginx-debug/containers/nginx?image=gcr.io/google_containers/nginx-slim:0.22' \
  --header 'authorization: Bearer SOME-PRIVATE-TOKEN'
```
