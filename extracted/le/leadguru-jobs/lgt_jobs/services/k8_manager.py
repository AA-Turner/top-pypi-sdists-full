import json
import logging as log
import os

from kubernetes import config
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.rest import ApiException


class K8Manager:

    def __init__(self):
        with open(os.environ.get('K8_CONFIG'), 'r') as k8_config:
            config.load_kube_config_from_dict(json.loads(k8_config.read()))

    @staticmethod
    def delete_bots(namespace: str):
        api_instance = CoreV1Api()
        pod_names_to_delete = ['lgt-slack-bots-v2', 'lgt-discord-bots', 'lgt-bg-worker']
        pods = api_instance.list_namespaced_pod(namespace)
        pods_to_delete = [pod.metadata.name for pod in pods.items for name in pod_names_to_delete
                          if name in pod.metadata.name]
        for pod in pods_to_delete:
            try:
                api_instance.delete_namespaced_pod(pod, namespace)
                log.info(f'Killed pod: {pod}')
            except ApiException as e:
                log.error(str(e))