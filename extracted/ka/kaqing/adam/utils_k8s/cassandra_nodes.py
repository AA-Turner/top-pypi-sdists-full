from adam.utils_context import Context
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.pod_exec_result import PodExecResult

# utility collection on cassandra nodes; methods are all static
class CassandraNodes:
    host_ids_by_pod = {}

    def exec(pod_name: str,
             namespace: str,
             command: str,
             throw_err = False,
             shell = '/bin/sh',
             ctx: Context = Context.NULL) -> PodExecResult:

        if not ctx.debug:
            ctx.log(Pods.get_command_printable(pod_name, "cassandra", namespace, command, shell, ctx=ctx))

        r: PodExecResult = Pods.exec(pod_name, "cassandra", namespace, command, throw_err = throw_err, shell = shell, ctx=ctx)

        if not ctx.debug:
            r.log(ctx)

        return r

    def get_host_id(pod_name: str, ns: str, ctx: Context = Context.NULL):
        try:
            user, pw = Secrets.get_user_pass(pod_name, ns)
            command = f'echo "SELECT host_id FROM system.local; exit" | cqlsh --no-color -u {user} -p {pw}'
            result: PodExecResult = CassandraNodes.exec(pod_name, ns, command, ctx.copy(show_out=ctx.debug))
            next = False
            for line in result.stdout.splitlines():
                if next:
                    host_id =line.strip(' ')
                    CassandraNodes.host_ids_by_pod[pod_name] = host_id
                    return host_id

                if line.startswith('----------'):
                    next = True
                    continue
        except Exception as e:
            pass
            # return str(e)

        if pod_name in CassandraNodes.host_ids_by_pod:
            return CassandraNodes.host_ids_by_pod[pod_name]

        return 'Unknown'