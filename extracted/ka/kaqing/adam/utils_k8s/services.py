from typing import List
from kubernetes import client

from adam.config import Config
from adam.utils import debug, log2

from .kube_context import KubeContext

# utility collection on services; methods are all static
class Services:
    def list_services(label_selector=None) -> List[client.V1Service]:
        v1 = client.CoreV1Api()
        if ns := KubeContext.in_cluster_namespace():
            services = v1.list_namespaced_service(ns, label_selector=label_selector)
        else:
            services = v1.list_service_for_all_namespaces(label_selector=label_selector)

        return services.items

    def list_svc_name_and_ns(label_selector=None):
        return [(service.metadata.name, service.metadata.namespace) for service in Services.list_services(label_selector=label_selector)]

    def list_svc_names(label_selector=None, show_namespace = True):
        if show_namespace:
            return [f"{svc}@{ns}" for svc, ns in Services.list_svc_name_and_ns(label_selector=label_selector)]
        else:
            return [f"{svc}" for svc, _ in Services.list_svc_name_and_ns(label_selector=label_selector)]

    def create_service(name: str, namespace: str, port: int, selector: dict[str, str], labels: dict[str, str] = {}):
        v1 = client.CoreV1Api()
        body = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=name,
                labels=labels
            ),
            spec=client.V1ServiceSpec(
                selector=selector,
                ports=[client.V1ServicePort(
                    port=port,
                    target_port=port
                )]
            )
        )
        # Creation of the Deployment in specified namespace
        # (Can replace "default" with a namespace you may have created)
        v1.create_namespaced_service(namespace=namespace, body=body)

    def delete_services(namespace: str, services: list[client.V1Service] = None, label_selector = None, dry = False):
        if services:
            for service in services:
                Services.delete_service(service.metadata.name, namespace, dry=dry)

        if label_selector:
            services = Services.list_services(label_selector)
            for service in services:
                Services.delete_service(service.metadata.name, namespace, dry=dry)

    def delete_service(name: str, namespace: str, dry = False):
        try:
            v1 = client.CoreV1Api()

            delete_options = client.V1DeleteOptions()

            if dry:
                log2(f"200 Service '{name}' in namespace '{namespace}' deleted successfully.")
            else:
                api_response = v1.delete_namespaced_service(
                    name=name,
                    namespace=namespace,
                    body=delete_options
                )
                debug(f"200 Service '{name}' in namespace '{namespace}' deleted successfully.")
        except client.ApiException as e:
            log2(f"Error deleting Service '{name}': {e}")
        except Exception as e:
            log2(f"An unexpected error occurred: {e}")