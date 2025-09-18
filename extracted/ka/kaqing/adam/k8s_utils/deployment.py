from kubernetes import client

from adam.k8s_utils.pods import Pods
from adam.k8s_utils.volumes import ConfigMapMount

# utility collection on deployments; methods are all static
class Deployments:
    def delete_with_selector(namespace: str, label_selector: str, grace_period_seconds: int = None):
        v1 = client.AppsV1Api()

        ret = v1.list_namespaced_deployment(namespace=namespace, label_selector=label_selector)
        for i in ret.items:
            v1.delete_namespaced_deployment(name=i.metadata.name, namespace=namespace, grace_period_seconds=grace_period_seconds)

    def create_deployment_spec(name: str, image: str, image_pull_secret: str,
                               envs: list, container_security_context: client.V1SecurityContext,
                               volume_name: str, pvc_name:str, mount_path:str,
                               command: list[str]=None, sa_name=None, labels: dict[str, str] = {},
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

    def create(namespace: str, deployment_name: str, image: str,
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