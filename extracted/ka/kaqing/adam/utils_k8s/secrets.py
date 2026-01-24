import base64
import functools
import re
from typing import cast
from kubernetes import client
from kubernetes.client import V1Secret

from adam.config import Config
from adam.utils import log2, wait_log

# utility collection on secrets; methods are all static
class Secrets:
    @functools.lru_cache()
    def list_secrets(namespace: str = None, name_pattern: str = None):
        wait_log('Inspecting Cassandra Instances...')

        secrets_names = []

        v1 = client.CoreV1Api()
        try:
            if name_pattern:
                name_pattern = name_pattern.replace('{namespace}', namespace if namespace else '')

            if namespace:
                secrets = v1.list_namespaced_secret(namespace)
            else:
                secrets = v1.list_secret_for_all_namespaces()

            for item in cast(list[V1Secret], secrets.items):
                name: str = item.metadata.name
                if name_pattern:
                    if re.match(name_pattern, name):
                        if not namespace:
                            name = f'{name}@{item.metadata.namespace}'
                        secrets_names.append(name)
        except client.ApiException as e:
            log2(f"Error listing secrets: {e}")
            raise e

        return secrets_names

    def get_user_pass(sts_or_pod_name: str, namespace: str, secret_path: str = 'cql.secret'):
        # cs-d0767a536f-cs-d0767a536f-default-sts ->
        # cs-d0767a536f-superuser
        # cs-d0767a536f-reaper-ui
        user = 'superuser'
        if secret_path == 'reaper.secret':
            user = 'reaper-ui'
        groups = re.match(Config().get(f'{secret_path}.cluster-regex', r'(.*?-.*?)-.*'), sts_or_pod_name)
        secret_name = Config().get(f'{secret_path}.name', '{cluster}-' + user).replace('{cluster}', groups[1], 1)

        secret = Secrets.get_data(namespace, secret_name)
        password_key = Config().get(f'{secret_path}.password-item', 'password')

        return (secret_name, secret[password_key])

    def get_data(namespace: str, secret_name: str):
        v1 = client.CoreV1Api()
        try:
            secret = v1.read_namespaced_secret(secret_name, namespace)

            return {key: base64.b64decode(value).decode("utf-8") for key, value in secret.data.items()}
        except client.ApiException as e:
            log2(f"Error reading secret: {e}")
            # raise e

        return None