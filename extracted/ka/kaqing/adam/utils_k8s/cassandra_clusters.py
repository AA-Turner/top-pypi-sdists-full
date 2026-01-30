import sys

from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets

# utility collection on cassandra clusters; methods are all static
class CassandraClusters:
    def exec(sts: str,
             namespace: str,
             command: str,
             action: str = 'action',
             max_workers=0,
             on_any = False,
             shell = '/bin/sh',
             ctx: Context = Context.NULL) -> list[PodExecResult]:

        pods = StatefulSets.pod_names(sts, namespace)
        samples = 1 if on_any else sys.maxsize

        msg = 'd`Running|Ran ' + action + ' command onto {size} pods'
        with Pods.parallelize(pods, max_workers, samples, msg, action=action) as exec:
            results: list[PodExecResult] = exec.map(lambda pod: CassandraNodes.exec(pod, namespace, command, False, shell, ctx.copy(show_out=False)))
            if not ctx.debug:
                for result in results:
                    ctx.log(result.command)
                    result.log(ctx)
            return results

    def pod_names_by_host_id(sts: str, ns: str):
        pods = StatefulSets.pods(sts, ns)

        return {CassandraNodes.get_host_id(pod.metadata.name, ns): pod.metadata.name for pod in pods}
