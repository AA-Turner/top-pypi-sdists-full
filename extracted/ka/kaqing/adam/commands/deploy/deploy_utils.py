from typing import Callable
from adam.app_session import AppSession
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.services import Services
from adam.utils import log2

def deploy_frontend(name: str, namespace: str, label_selector: str):
    app_session: AppSession = AppSession.create('c3', 'c3', namespace)
    port = 7678
    labels = gen_labels(label_selector)
    creating('service', lambda: Services.create_service(name, namespace, port, labels, labels=labels))
    creating('ingress', lambda: Ingresses.create_ingress(name, namespace, app_session.host, '/c3/c3/ops($|/)', port, annotations={
        'kubernetes.io/ingress.class': 'nginx',
        'nginx.ingress.kubernetes.io/use-regex': 'true',
        'nginx.ingress.kubernetes.io/rewrite-target': '/'
    }, labels=labels))

    return f'https://{app_session.host}/c3/c3/ops'

def undeploy_frontend(namespace: str, label_selector: str):
    deleting('ingress', lambda: Ingresses.delete_ingresses(namespace, label_selector=label_selector))
    deleting('service', lambda: Services.delete_services(namespace, label_selector=label_selector))

def gen_labels(label_selector: str):
    kv = label_selector.split('=')
    return {kv[0]: kv[1]}

def creating(name: str, body: Callable[[], None]):
    log2(f'Creating {name}...', nl=False)
    body()
    log2(' OK')

def deleting(name: str, body: Callable[[], None]):
    try:
        log2(f'Deleting {name}...', nl=False)
        body()
        log2(' OK')
    except Exception as e:
        log2(e)