from adam.utils_context import NULL
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.pod_exec_result import PodExecResult

# utility collection on cassandra nodes; methods are all static
class CassandraNodes:
    host_ids_by_pod = {}

    def exec(pod_name: str,
             namespace: str,
             command: str,
             throw_err = False,
             shell = '/bin/sh',
             ctx = NULL) -> PodExecResult:

        if not ctx.debug:
            ctx.log(Pods.get_command_printable(pod_name, "cassandra", namespace, command, shell, ctx=ctx))

        r: PodExecResult = Pods.exec(pod_name, "cassandra", namespace, command, throw_err = throw_err, shell = shell, ctx=ctx)

        if not ctx.debug:
            r.log(ctx)

        return r