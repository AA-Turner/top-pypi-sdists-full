import sys
from typing import TypeVar

from adam.config import Config
from adam.utils_async_job import AsyncJobs
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils import log, log2, log_to_pods, pod_log_dir
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets

T = TypeVar('T')

# utility collection on cassandra clusters; methods are all static
class CassandraClusters:
    def exec(sts: str,
             namespace: str,
             command: str,
             action: str = 'action',
             max_workers=0,
             show_out=True,
             on_any = False,
             shell = '/bin/sh',
             backgrounded = False,
             log_file = None,
             history=True,
             text_color: str = None,
             job_id: str = None) -> list[PodExecResult]:

        pods = StatefulSets.pod_names(sts, namespace)
        samples = 1 if on_any else sys.maxsize
        if (backgrounded or command.endswith(' &')) and not log_file:
            pod_suffix = None
            dir = None
            if log_to_pods():
                pod_suffix = ''
                dir = pod_log_dir()

            if not job_id:
                job_id = AsyncJobs.new_id()
            log_file = AsyncJobs.pod_log_file(command, job_id=job_id, pod_suffix=pod_suffix, dir=dir)

        msg = 'd`Running|Ran ' + action + ' command onto {size} pods'
        with Pods.parallelize(pods, max_workers, samples, msg, action=action) as exec:
            results: list[PodExecResult] = exec.map(lambda pod: CassandraNodes.exec(pod, namespace, command, False, False, shell, backgrounded, log_file, history, text_color, job_id))
            for result in results:
                if show_out and not Config().is_debug():
                    log(result.command, text_color=text_color)
                    if result.stdout:
                        log(result.stdout, text_color=text_color)
                    if result.stderr:
                        log2(result.stderr, text_color=text_color)

            return results

    def pod_names_by_host_id(sts: str, ns: str):
        pods = StatefulSets.pods(sts, ns)

        return {CassandraNodes.get_host_id(pod.metadata.name, ns): pod.metadata.name for pod in pods}
