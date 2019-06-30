import datetime
import os

from flask import Flask, request, jsonify, json, Response
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.config.incluster_config import SERVICE_HOST_ENV_NAME

from auth import bearer_required


def json_default(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    elif callable(getattr(value, 'to_dict', None)):
        return value.to_dict()
    else:
        return value.__dict__


app = Flask(__name__)

if SERVICE_HOST_ENV_NAME in os.environ:
    config.load_incluster_config()
else:
    config.load_kube_config()

auth_token = os.environ.get('AUTH_TOKEN')
if not auth_token:
    raise EnvironmentError('Environment Variables `AUTH_TOKEN` is required')


@app.route('/')
def index():
    return 'Hello Kubernetes!'


@app.route('/info', methods=['GET'])
def info():
    return jsonify({})


@app.route('/health')
def health():
    core = client.CoreApi()
    ret = core.get_api_versions()
    return jsonify({'versions': ret.versions})


@app.route('/namespaces/<namespace>/deployments', methods=['GET'])
@bearer_required(auth_token)
def list_deployments(namespace):
    apps = client.AppsV1beta1Api()
    try:
        data = apps.list_namespaced_deployment(namespace)
        return Response(json.dumps(data.items, default=json_default), mimetype='application/json')
    except ApiException as e:
        return str(e), e.status


@app.route('/namespaces/<namespace>/deployments/<deployment>/containers/<container>', methods=['PATCH'])
@bearer_required(auth_token)
def deploy(namespace, deployment, container):
    image = request.args.get('image')
    if not image:
        response_object = {
            'status': 'failed',
            'message': 'image argument required.'
        }
        return jsonify(response_object), 400

    apps = client.AppsV1beta1Api()
    patch = {"spec": {"template": {"spec": {"containers": [{"name": container, "image": image}]}}}}
    try:
        data = apps.patch_namespaced_deployment(deployment, namespace, patch)
        return Response(json.dumps(data.status, default=json_default), mimetype='application/json')
    except ApiException as e:
        return str(e), e.status


if __name__ == '__main__':
    app.run()
