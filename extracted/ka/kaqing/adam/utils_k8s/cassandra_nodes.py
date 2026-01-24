from adam.config import Config
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_session import ReplSession

# utility collection on cassandra nodes; methods are all static
class CassandraNodes:
    def exec(pod_name: str,
             namespace: str,
             command: str,
             show_out = True,
             throw_err = False,
             shell = '/bin/sh',
             backgrounded = False,
             log_file = None,
             history = True,
             text_color: str = None,
             job_id: str = None) -> PodExecResult:
        r: PodExecResult = Pods.exec(pod_name, "cassandra", namespace, command, show_out = show_out, throw_err = throw_err, shell = shell, backgrounded = backgrounded, log_file=log_file, text_color=text_color, job_id=job_id)

        if history and r and r.log_file:
            # entry = f':tail {r.log_file}'

            ReplSession().append_history(r.log_file)

        return r

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