from adam.config import Config
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.secrets import Secrets
from adam.pod_exec_result import PodExecResult

# utility collection on cassandra nodes; methods are all static
class CassandraNodes:
    def exec(pod_name: str, namespace: str, command: str, show_out = True, throw_err = False) -> PodExecResult:
        return Pods.exec(pod_name, "cassandra", namespace, command, show_out, throw_err)

    def get_host_id(pod_name: str, ns: str):
        try:
            user, pw = Secrets.get_user_pass(pod_name, ns)
            command = f'echo "SELECT host_id FROM system.local; exit" | cqlsh --no-color -u {user} -p {pw}'
            result: PodExecResult = CassandraNodes.exec(pod_name, ns, command, show_out=Config().is_debug())
            next = False
            for line in result.stdout.splitlines():
                if next:
                    return line.strip(' ')
                if line.startswith('----------'):
                    next = True
                    continue
        except Exception as e:
            return str(e)

        return 'Unknown'