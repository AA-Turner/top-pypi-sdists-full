from kubernetes import client

from adam.config import Config
from adam.utils import debug, log2

# utility collection on ingresses; methods are all static
class Ingresses:
    def get_host(name: str, namespace: str):
        api = client.NetworkingV1Api()
        try:
            ingress = api.read_namespaced_ingress(name=name, namespace=namespace)
            return ingress.spec.rules[0].host
        except client.ApiException as e:
            print(f"Error getting Ingresses: {e}")

    def create_ingress(name: str, namespace: str, host: str, path: str, port: int, annotations: dict[str, str] = {},  labels: dict[str, str] = {}, path_type = "ImplementationSpecific"):
        api = client.NetworkingV1Api()

        body = client.V1Ingress(
            api_version="networking.k8s.io/v1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(name=name, annotations=annotations, labels=labels),
            spec=client.V1IngressSpec(
                rules=[client.V1IngressRule(
                    host=host,
                    http=client.V1HTTPIngressRuleValue(
                        paths=[client.V1HTTPIngressPath(
                            path=path,
                            path_type=path_type,
                            backend=client.V1IngressBackend(
                                service=client.V1IngressServiceBackend(
                                    port=client.V1ServiceBackendPort(
                                        number=port,
                                    ),
                                    name=name)
                                )
                        )]
                    )
                )]
            )
        )

        api.create_namespaced_ingress(
            namespace=namespace,
            body=body
        )

    def delete_ingresses(namespace: str, ingresses: list[client.V1Ingress] = None, label_selector = None, dry = False):
        if ingresses:
            for ingress in ingresses:
                Ingresses.delete_ingress(ingress.metadata.name, namespace, dry=dry)

        if label_selector:
            ingresses = Ingresses.get_ingresses_by_label(namespace, label_selector)
            for ingress in ingresses:
                Ingresses.delete_ingress(ingress.metadata.name, namespace, dry=dry)

    def delete_ingress(name: str, namespace: str, dry = False):
        api = client.NetworkingV1Api()

        try:
            if dry:
                log2(f"200 Ingress '{name}' in namespace '{namespace}' deleted successfully.")
            else:
                api.delete_namespaced_ingress(name=name, namespace=namespace)
                debug(f"200 Ingress '{name}' in namespace '{namespace}' deleted successfully.")
        except client.ApiException as e:
            log2(f"Error deleting Ingress: {e}")

    def get_ingresses_by_label(namespace: str, label_selector) -> list[client.V1Ingress]:
        api = client.NetworkingV1Api()

        try:
            if namespace:
                ingresses = api.list_namespaced_ingress(
                    namespace=namespace,
                    label_selector=label_selector
                )
            else:
                ingresses = api.list_ingress_for_all_namespaces(
                    label_selector=label_selector
                )

            return ingresses.items
        except client.ApiException as e:
            log2(f"Error fetching Ingresses: {e}")
            return []