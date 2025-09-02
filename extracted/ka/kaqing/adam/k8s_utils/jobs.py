from kubernetes import client
from time import sleep
from .pods import Pods
from adam.utils import log2

# utility collection on jobs; methods are all static
class Jobs:
    def create(job_name: str, namespace: str, image: str, image_pull_secret: str, env: dict[str, any], env_from: dict[str, any],
                volume_name: str, pvc_name: str, mount_path: str, command: list[str]=None):
        envs = []
        for k, v in env.items():
            envs.append(client.V1EnvVar(name=k.upper(), value=str(v)))
        for k, v in env_from.items():
            envs.append(client.V1EnvVar(name=k.upper(), value_from=client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(key=k, name=v))))
        template = Pods.create_pod_spec(job_name, image, image_pull_secret, envs, volume_name, pvc_name, mount_path, command)
        spec = client.V1JobSpec(template=client.V1PodTemplateSpec(spec=template), backoff_limit=1, ttl_seconds_after_finished=300)
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=spec)

        try:
            client.BatchV1Api().create_namespaced_job(body=job, namespace=namespace)
            log2(f"Job {job_name} created in {namespace}")
        except Exception as e:
            log2("Exception when calling BatchV1Apii->create_namespaced_job: %s\n" % e)
        return

    def get_job_pods(job_name: str, namespace: str):
        pods = client.CoreV1Api().list_namespaced_pod(namespace=namespace, label_selector=f'job-name={job_name}')
        return pods

    def delete(job_name: str, namespace: str, wait=True):
        try:
            client.BatchV1Api().delete_namespaced_job(name=job_name, namespace=namespace, propagation_policy='Background')
            if wait:
                while True:
                    pods = Jobs.get_job_pods(job_name, namespace).items
                    if not pods:
                        return
                    sleep(5)
            log2(f"Job {job_name} in {namespace} deleted.")
        except Exception as e:
            log2("Exception when calling BatchV1Apii->delete_namespaced_job: %s\n" % e)
        return

    def get_logs(job_name: str, namespace: str):
        v1 = client.CoreV1Api()
        try:
            pod_name = Jobs.get_job_pods(job_name, namespace).items[0].metadata.name
            log2(v1.read_namespaced_pod_log(name=pod_name, namespace=namespace))
        except Exception as e:
            log2("Exception when calling CorV1Apii->list_namespaced_pod, cannot find job pod: %s\n" % e)