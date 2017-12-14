import datetime
import os

from flask import Flask, request, jsonify, json, Response
from kubernetes import client, config
from kubernetes.config.incluster_config import SERVICE_HOST_ENV_NAME


def json_default(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        return value.__dict__


app = Flask(__name__)

if SERVICE_HOST_ENV_NAME in os.environ:
    config.load_incluster_config()
else:
    config.load_kube_config()


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


@app.route('/namespaces/<namespace>/deployments/<deployment>/containers/<container>', methods=['PATCH'])
def deploy(namespace, deployment, container):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return jsonify(response_object), 401
        if not auth_token or auth_token != os.environ.get('AUTH_TOKEN'):
            response_object = {
                'status': 'fail',
                'message': 'Bearer token incorrect.'
            }
            return jsonify(response_object), 401

    image = request.args.get('image')
    if not image:
        response_object = {
            'status': 'fail',
            'message': 'image argument required.'
        }
        return jsonify(response_object), 400

    apps = client.AppsV1beta1Api()
    patch = {"spec": {"template": {"spec": {"containers": [{"name": container, "image": image}]}}}}
    data = apps.patch_namespaced_deployment(deployment, namespace, patch)

    return Response(json.dumps(data.status, default=json_default), content_type="application/json")


if __name__ == '__main__':
    app.run()
