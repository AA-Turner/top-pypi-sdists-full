import sys

from adam.utils_cassandra.cassandra_nodes import CassandraNodes
from adam.utils_concurrent import parallelize
from adam.utils_context import NULL
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s.k8s_context import K8sContext

# utility collection on cassandra clusters; methods are all static
class CassandraClusters:
    def exec(sts: str,
             namespace: str,
             command: str,
             action: str = 'action',
             on_any = False,
             shell = '/bin/sh',
             samples = sys.maxsize,
             pods: list[str] = None,
             k8s: K8sContext = K8sContext.NULL,
             ctx = NULL) -> list[PodExecResult]:
        results: list[PodExecResult] = []

        if not pods:
            pods = k8s.running_pods(sts, namespace)
            if not pods:
                # no pod was reported as runnning; just try with the non-running pods
                pods = k8s.pod_names(sts, namespace)

        if on_any:
            samples = 1

        with parallelize(pods,
                          msg='d`Running|Ran ' + action + ' command onto {size} pods') as exec:
            if samples == sys.maxsize:
                rs = exec.collect(lambda pod: CassandraNodes.exec(pod, namespace, command, False, shell, ctx.copy(show_out=False)))
            else:
                rs = exec.sample(lambda pod: CassandraNodes.exec(pod, namespace, command, False, shell, ctx.copy(show_out=False)), samples=samples)

            results.extend(rs)

        if not ctx.debug:
            for r in results:
                ctx.log(r.command)
                r.log(ctx)

        return results