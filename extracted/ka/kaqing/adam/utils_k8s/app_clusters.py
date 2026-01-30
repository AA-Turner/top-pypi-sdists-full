import sys
from typing import TypeVar

from adam.utils_context import Context
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
             on_any = False,
             shell = '/bin/sh',
             ctx: Context = Context.NULL) -> list[PodExecResult]:
        samples = 1 if on_any else sys.maxsize
        msg = 'd`Running|Ran ' + action + ' command onto {size} pods'
        with Pods.parallelize(pods, max_workers, samples, msg, action=action) as exec:
            results: list[PodExecResult] = exec.map(lambda pod: AppPods.exec(pod, namespace, command, False, shell, ctx=ctx))
            for result in results:
                if KubeContext.show_out(ctx.show_out):
                    ctx.log(result.command)
                    if result.stdout:
                        ctx.log(result.stdout)
                    if result.stderr:
                        ctx.log2(result.stderr)

            return results