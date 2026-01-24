import sys
from typing import TypeVar

from adam.utils_k8s.app_pods import AppPods
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils import log, log2
from adam.utils_k8s.pods import Pods
from .kube_context import KubeContext

T = TypeVar('T')

# utility collection on app clusters; methods are all static
class AppClusters:
    def exec(pods: list[str],
             namespace: str,
             command: str,
             action: str = 'action',
             max_workers=0,
             show_out=True,
             on_any = False,
             shell = '/bin/sh',
             backgrounded = False) -> list[PodExecResult]:
        samples = 1 if on_any else sys.maxsize
        msg = 'd`Running|Ran ' + action + ' command onto {size} pods'
        with Pods.parallelize(pods, max_workers, samples, msg, action=action) as exec:
            results: list[PodExecResult] = exec.map(lambda pod: AppPods.exec(pod, namespace, command, False, False, shell, backgrounded))
            for result in results:
                if KubeContext.show_out(show_out):
                    log(result.command)
                    if result.stdout:
                        log(result.stdout)
                    if result.stderr:
                        log2(result.stderr)

            return results