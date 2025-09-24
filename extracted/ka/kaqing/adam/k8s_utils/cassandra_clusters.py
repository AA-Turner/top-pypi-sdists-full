from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
import sys
from typing import TypeVar

from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.pod_exec_result import PodExecResult
from adam.utils import log2
from .statefulsets import StatefulSets
from .pods import Pods
from .kube_context import KubeContext

T = TypeVar('T')

# utility collection on cassandra clusters; methods are all static
class CassandraClusters:
    def exec(statefulset: str, namespace: str, command: str, action: str = 'action', max_workers=0, show_out=True, on_any = False) -> list[PodExecResult]:
        def body(executor: ThreadPoolExecutor, pod: str, namespace: str, show_out: bool):
            if executor:
                return executor.submit(CassandraNodes.exec, pod, namespace, command, False, False,)

            return CassandraNodes.exec(pod, namespace, command, show_out=show_out)

        def post(result, show_out: bool):
            if KubeContext.show_out(show_out):
                print(result.command)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    log2(result.stderr, file=sys.stderr)

            return result

        return StatefulSets.on_cluster(statefulset, namespace, body, post=post, action=action, max_workers=max_workers, show_out=show_out, on_any=on_any)