from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time

from metaflow.exception import MetaflowException
from metaflow.metaflow_config import KUBERNETES_NAMESPACE
from .pod_killer import PodKiller


CLIENT_REFRESH_INTERVAL_SECONDS = 300


class KubernetesClientException(MetaflowException):
    headline = "Kubernetes client error"


class KubernetesClient(object):
    def __init__(self):
        try:
            # Kubernetes is a soft dependency.
            from kubernetes import client, config
        except (NameError, ImportError):
            raise KubernetesClientException(
                "Could not import module 'kubernetes'.\n\nInstall Kubernetes "
                "Python package (https://pypi.org/project/kubernetes/) first.\n"
                "You can install the module by executing - "
                "%s -m pip install kubernetes\n"
                "or equivalent through your favorite Python package manager."
                % sys.executable
            )
        self._refresh_client()
        self._namespace = KUBERNETES_NAMESPACE

    def _refresh_client(self):
        from metaflow_extensions.outerbounds.plugins.auth_server import get_token
        from kubernetes import client

        config = client.Configuration()
        token_info = get_token("/generate/k8s")
        config.host = token_info["endpoint"]
        config.api_key["authorization"] = "Bearer " + token_info["token"]
        config.verify_ssl = False  # TODO: FIX THIS
        client.Configuration.set_default(config)
        self._client = client
        self._client_refresh_timestamp = time.time()

    def get(self):
        if (
            time.time() - self._client_refresh_timestamp
            > CLIENT_REFRESH_INTERVAL_SECONDS
        ):
            self._refresh_client()

        return self._client

    def _find_active_pods(self, flow_name, run_id=None, user=None):
        def _request(_continue=None):
            # handle paginated responses
            return self._client.CoreV1Api().list_namespaced_pod(
                namespace=self._namespace,
                # limited selector support for K8S api. We want to cover multiple statuses: Running / Pending / Unknown
                field_selector="status.phase!=Succeeded,status.phase!=Failed",
                limit=1000,
                _continue=_continue,
            )

        results = _request()

        if run_id is not None:
            # handle argo prefixes in run_id
            run_id = run_id[run_id.startswith("argo-") and len("argo-") :]

        while results.metadata._continue or results.items:
            for pod in results.items:
                match = (
                    # arbitrary pods might have no annotations at all.
                    pod.metadata.annotations
                    and pod.metadata.labels
                    and (
                        run_id is None
                        or (pod.metadata.annotations.get("metaflow/run_id") == run_id)
                        # we want to also match pods launched by argo-workflows
                        or (
                            pod.metadata.labels.get("workflows.argoproj.io/workflow")
                            == run_id
                        )
                    )
                    and (
                        user is None
                        or pod.metadata.annotations.get("metaflow/user") == user
                    )
                    and (
                        pod.metadata.annotations.get("metaflow/flow_name") == flow_name
                    )
                )
                if match:
                    yield pod
            if not results.metadata._continue:
                break
            results = _request(results.metadata._continue)

    def list(self, flow_name, run_id, user):
        results = self._find_active_pods(flow_name, run_id, user)

        return list(results)

    def kill_pods(self, flow_name, run_id, user, echo):
        # Create PodKiller instance
        killer = PodKiller(self._client, echo, self._namespace)

        # Process all matching jobs and jobsets based on their outcomes
        (
            job_jobset_results,
            num_jobs,
            num_jobsets,
        ) = killer.process_matching_jobs_and_jobsets(flow_name, run_id, user)

        if job_jobset_results:
            successful_operations = sum(1 for result in job_jobset_results if result)
            echo(
                f"Found and processed {num_jobs} jobs and {num_jobsets} jobsets, {successful_operations} operations successful\n"
            )
        else:
            echo("No matching jobs or jobsets found for run *%s*" % run_id)

    def job(self, **kwargs):
        from metaflow.plugins.kubernetes.kubernetes_job import KubernetesJob

        return KubernetesJob(self, **kwargs)

    def jobset(self, **kwargs):
        from metaflow.plugins.kubernetes.kubernetes_job import KubernetesJobSet

        return KubernetesJobSet(self, **kwargs)
