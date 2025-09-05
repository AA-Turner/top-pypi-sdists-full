from adam.app_session import AppSession
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.services import Services
from adam.utils import log2

def deploy_frontend(name: str, namespace: str, label_selector: str):
    app_session: AppSession = AppSession.create('c3', 'c3', namespace)
    port = 7678
    labels = gen_labels(label_selector)
    Services.create_service(name, namespace, port, labels, labels=labels)
    # Services.create_service(name, namespace, port, {"run": "ops"})
    Ingresses.create_ingress(name, namespace, app_session.host, '/c3/c3/ops($|/)', port, annotations={
        'kubernetes.io/ingress.class': 'nginx',
        'nginx.ingress.kubernetes.io/use-regex': 'true',
        'nginx.ingress.kubernetes.io/rewrite-target': '/'
    }, labels=labels)

    return f'https://{app_session.host}/c3/c3/ops'

def undeploy_frontend(namespace: str, label_selector: str):
    Ingresses.delete_ingresses(namespace, label_selector=label_selector)
    Services.delete_services(namespace, label_selector=label_selector)

def gen_labels(label_selector: str):
    kv = label_selector.split('=')
    return {kv[0]: kv[1]}