"""Helper functions for kubeconfig autopop from Rancher"""
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

import requests
import yaml


class ClusterInfo(NamedTuple):
    id: str
    name: str


class ProjectInfo(NamedTuple):
    id: str
    name: str
    cluster: str
    display_name: str


_MESSAGE_401 = 'Unauthorized. Check your bearer token and try again'  # pylint: disable=invalid-name
_MESSAGE_404 = 'Invalid URL. Check your Rancher endpoint and try again'  # pylint: disable=invalid-name
# pylint: disable=invalid-name
_MESSAGE_403 = 'Forbidden. Try creating a new auth token. If the issue persists, notify your cluster administrator.'
# pylint: disable=invalid-name
_MESSAGE_500 = ('Server error. MosaicML platform had an issue processing your request. '
                'Please notify your cluster administrator.')


def retrieve_clusters(
    endpoint: str,
    auth_token: str,
) -> List[ClusterInfo]:

    _GET_CLUSTER_MESSAGE = 'Error retrieving cluster info'

    headers = {'Authorization': 'Bearer ' + auth_token}

    resp = requests.request('GET', endpoint + '/v3/clusters', headers=headers, timeout=10)

    if resp.status_code == 401:
        raise RuntimeError(f'{_GET_CLUSTER_MESSAGE}: {_MESSAGE_401}')

    if resp.status_code == 404:
        raise RuntimeError(f'{_GET_CLUSTER_MESSAGE}: {_MESSAGE_404}')

    return [ClusterInfo(item['id'], item['name']) for item in resp.json()['data'] if item['state'] == 'active']


def generate_cluster_config(
    endpoint: str,
    auth_token: str,
    clusters: List[ClusterInfo],
    namespace: Optional[str] = None,
    kube_config_path: Optional[Path] = None,
) -> Path:

    headers = {'Authorization': 'Bearer ' + auth_token}
    if not kube_config_path:
        kube_config_path = Path.home().joinpath('.kube', 'config')
    kube_config_path.parent.mkdir(parents=True, exist_ok=True)

    if kube_config_path.exists():
        with open(kube_config_path, 'r', encoding='utf-8') as f:
            kubeconfig = yaml.safe_load(f)
    else:
        kubeconfig = {
            'apiVersion': 'v1',
            'kind': 'Config',
            'clusters': [],
            'users': [],
            'contexts': [],
        }

    for cluster in clusters:
        if cluster.id == 'local':
            continue

        resp = requests.request('POST',
                                endpoint + '/v3/clusters/' + cluster.id + '?action=generateKubeconfig',
                                headers=headers,
                                timeout=10)

        _GET_KUBECONFIG_MESSAGE = f'Error creating kubeconfig for cluster {cluster.name}'
        if resp.status_code == 401:
            raise RuntimeError(f'{_GET_KUBECONFIG_MESSAGE}: {_MESSAGE_404}')

        if resp.status_code == 404:
            raise RuntimeError(f'{_GET_KUBECONFIG_MESSAGE}: {_MESSAGE_404}')

        if resp.status_code == 500:
            raise RuntimeError(f'{_GET_KUBECONFIG_MESSAGE}: {_MESSAGE_500}')

        config = yaml.safe_load(resp.json()['config'])

        if namespace:
            config['contexts'][0]['context']['namespace'] = namespace

        kubeconfig = merge_kubeconfigs(config, kubeconfig)

        kubeconfig.setdefault('current-context', kubeconfig['contexts'][0]['name'])

        with open(kube_config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(kubeconfig, f)

    return kube_config_path


def merge_kubeconfigs(source: Dict[str, Any], dest: Dict[str, Any]) -> Dict[str, Any]:
    """Merge details from source into dest and return the updated dest
    """

    for ii in range(len(source['clusters'])):
        updated_cluster = False
        updated_user = False
        updated_context = False

        for cl in dest['clusters']:
            if cl['name'] == source['clusters'][ii]['name']:
                cl['cluster'] = source['clusters'][ii]['cluster']
                updated_cluster = True
                break

        for cl in dest['users']:
            if cl['name'] == source['users'][ii]['name']:
                cl['user'] = source['users'][ii]['user']
                updated_user = True
                break

        for cl in dest['contexts']:
            if cl['name'] == source['contexts'][ii]['name']:
                cl['context'] = source['contexts'][ii]['context']
                updated_context = True
                break

        if not updated_cluster:
            dest['clusters'].append(source['clusters'][ii])

        if not updated_user:
            dest['users'].append(source['users'][ii])

        if not updated_context:
            dest['contexts'].append(source['contexts'][ii])

    return dest


def retrieve_projects(
    endpoint: str,
    auth_token: str,
) -> List[ProjectInfo]:

    headers = {'Authorization': 'Bearer ' + auth_token}

    resp = requests.request('GET', endpoint + '/v3/projects', headers=headers, timeout=10)

    _GET_PROJECTS_MESSAGE = 'Error getting available projects'
    if resp.status_code == 401:
        raise RuntimeError(f'{_GET_PROJECTS_MESSAGE}: {_MESSAGE_401}')

    if resp.status_code == 404:
        raise RuntimeError(f'{_GET_PROJECTS_MESSAGE}: {_MESSAGE_404}')

    return [
        ProjectInfo(proj['id'], proj['id'].split(':')[1], proj['id'].split(':')[0], proj['name'])
        for proj in resp.json()['data']
    ]


def configure_namespaces(
    endpoint: str,
    auth_token: str,
    projects: List[ProjectInfo],
    namespace_name: str,
):
    headers = {'Authorization': 'Bearer ' + auth_token}

    for project in projects:
        payload = {
            'type': 'namespace',
            'metadata': {
                'annotations': {
                    'field.cattle.io/containerDefaultResourceLimit': '{}',
                },
                'labels': {},
            },
            'disableOpenApiValidation': False
        }

        payload['metadata']['annotations']['field.cattle.io/projectId'] = project.id
        payload['metadata']['labels']['field.cattle.io/projectId'] = project.name
        payload['metadata']['name'] = namespace_name

        resp = requests.request('POST',
                                endpoint + '/k8s/clusters/' + project.cluster + '/v1/namespaces',
                                headers=headers,
                                data=json.dumps(payload),
                                timeout=10)

        _CREATE_NAMESPACE_MESSAGE = f'Error creating namespace {namespace_name} on cluster {project.cluster}'
        if resp.status_code == 401:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_401}')

        if resp.status_code == 403:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_403}')

        if resp.status_code == 404:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_404}')

        if resp.status_code == 500:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_500}')
