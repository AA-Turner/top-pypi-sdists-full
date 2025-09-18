from kubernetes import client

# utility collection on config maps; methods are all static
class ConfigMaps:
    def create(name: str, namespace: str, data: dict[str, str], labels: dict[str, str] = {}):
        v1 = client.CoreV1Api()

        metadata = client.V1ObjectMeta(
            name=name,
            namespace=namespace,
            labels=labels
        )

        configmap = client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=metadata,
            data=data
        )

        try:
            api_response = v1.create_namespaced_config_map(body=configmap, namespace=namespace)
            # print(f"ConfigMap '{name}' created successfully in namespace '{namespace}'.")
            # print(api_response)
        except client.ApiException as e:
            # print(f"Error creating ConfigMap: {e}")
            raise e

    def delete_with_selector(namespace: str, label_selector: str):
        v1 = client.CoreV1Api()

        ret = v1.list_namespaced_config_map(namespace=namespace, label_selector=label_selector)
        for i in ret.items:
            v1.delete_namespaced_config_map(name=i.metadata.name, namespace=namespace)