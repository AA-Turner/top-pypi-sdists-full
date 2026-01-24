from adam.app_session import AppSession
from adam.utils import ing
from adam.utils_k8s.ingresses import Ingresses
from adam.utils_k8s.services import Services

def deploy_frontend(name: str, namespace: str, label_selector: str):
    app_session: AppSession = AppSession.create('c3', 'c3', namespace)
    port = 7678
    labels = gen_labels(label_selector)
    with ing('Creating service'):
        Services.create_service(name, namespace, port, labels, labels=labels)
    with ing('Creating ingress'):
        Ingresses.create_ingress(name, namespace, app_session.host, '/c3/c3/ops($|/)', port, annotations={
            'kubernetes.io/ingress.class': 'nginx',
            'nginx.ingress.kubernetes.io/use-regex': 'true',
            'nginx.ingress.kubernetes.io/rewrite-target': '/'
        }, labels=labels)

    return f'https://{app_session.host}/c3/c3/ops'

def undeploy_frontend(namespace: str, label_selector: str):
    with ing('Deleting ingress'):
        Ingresses.delete_ingresses(namespace, label_selector=label_selector)
    with ing('Deleting service'):
        Services.delete_services(namespace, label_selector=label_selector)

def gen_labels(label_selector: str):
    kv = label_selector.split('=')
    return {kv[0]: kv[1]}