from kubernetes import client

from adam.utils_context import NULL
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.volumes import ConfigMapMount
from adam.utils_log import log_exc

# utility collection on deployments; methods are all static
class Deployments:
    def delete_with_selector(namespace: str, label_selector: str, grace_period_seconds: int = None):
        v1 = client.AppsV1Api()

        ret = v1.list_namespaced_deployment(namespace=namespace, label_selector=label_selector)
        for i in ret.items:
            v1.delete_namespaced_deployment(name=i.metadata.name, namespace=namespace, grace_period_seconds=grace_period_seconds)

    def create_deployment_spec(name: str,
                               image: str,
                               image_pull_secret: str,
                               envs: list,
                               container_security_context: client.V1SecurityContext,
                               volume_name: str,
                               pvc_name:str,
                               mount_path:str,
                               command: list[str]=None,
                               sa_name=None,
                               labels: dict[str, str] = {},
                               config_map_mount: ConfigMapMount = None):
        return client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels=labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=Pods.create_pod_spec(name, image, image_pull_secret, envs, container_security_context,
                                          volume_name, pvc_name, mount_path, command=command, sa_name=sa_name,
                                          restart_policy="Always", config_map_mount=config_map_mount),
            ),
        )

    def create(namespace: str,
               deployment_name: str,
               image: str,
               command: list[str] = None,
               secret: str = None,
               env: dict[str, any] = {},
               container_security_context: client.V1SecurityContext = None,
               labels: dict[str, str] = {},
               volume_name: str = None,
               pvc_name: str = None,
               mount_path: str = None,
               sa_name=None,
               config_map_mount: ConfigMapMount = None):
        v1 = client.AppsV1Api()
        envs = []
        for k, v in env.items():
            envs.append(client.V1EnvVar(name=str(k), value=str(v)))
        deployment = Deployments.create_deployment_spec(deployment_name, image, secret, envs,
                                                        container_security_context, volume_name, pvc_name,
                                                        mount_path, command=command, sa_name=sa_name, labels=labels,
                                                        config_map_mount=config_map_mount)
        return v1.create_namespaced_deployment(
            namespace=namespace,
            body=client.V1Deployment(spec=deployment, metadata=client.V1ObjectMeta(
                name=deployment_name,
                labels=labels
            ))
        )

    def update_image(namespace: str,
                     deployment_name: str,
                     container_name: str,
                     image: str,
                     ctx = NULL):
        api_instance = client.AppsV1Api()

        body = {
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": container_name,
                                "image": image
                            }
                        ]
                    }
                }
            }
        }

        with log_exc():
            # Patch the deployment
            api_response = api_instance.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=body
            )
            ctx.log2(f"Deployment '{deployment_name}' image updated successfully to '{image}'")

            return True
            # Optional: Add an annotation to record the change reason
            # body_annotation = {"metadata": {"annotations": {"kubernetes.io/change-cause": f"Updated image to {new_image_name}"}}}
            # api_instance.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=body_annotation)
        # except ApiException as e:
        #     print(f"Error updating deployment: {e}")

        return False