import sys
from typing import TypeVar

from adam.utils_apps.app_pods import AppPods
from adam.utils_concurrent import parallelize
from adam.utils_context import NULL
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_k8s.pod_exec_result import PodExecResult

T = TypeVar('T')

# utility collection on app clusters; methods are all static
class AppClusters:
    def exec(pods: list[str],
             namespace: str,
             command: str,
             action: str = 'action',
             on_any = False,
             shell = '/bin/sh',
             ctx = NULL) -> list[PodExecResult]:
        samples = 1 if on_any else sys.maxsize
        with parallelize(pods,
                         msg='d`Running|Ran ' + action + ' command onto {size} pods') as exec:
            results: list[PodExecResult] = exec.sample(lambda pod: AppPods.exec(pod, namespace, command, False, shell, ctx=ctx), samples=samples)
            for result in results:
                if KubeContext.show_out(ctx.show_out):
                    ctx.log(result.command)
                    if result.stdout:
                        ctx.log(result.stdout)
                    if result.stderr:
                        ctx.log2(result.stderr)

            return results