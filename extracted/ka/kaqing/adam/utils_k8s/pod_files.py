import os
import re
from kubernetes import client
from kubernetes.stream import stream
from kubernetes.stream.ws_client import ERROR_CHANNEL

from adam.config import Config
from adam.repl_session import ReplSession
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods
from adam.utils import GeneratorStream, PodLogFile, log_exc
from adam.utils_local import local_downloads_dir, local_exec

from websocket._core import WebSocket

def creating_dir(pod_name: str,
                    container: str,
                    namespace: str,
                    dir_or_file: str,
                    is_file = False,
                    ctx: Context = Context.NULL):
    return PodFiles.creating_dir(pod_name, container, namespace, dir_or_file, is_file, ctx)

# utility collection on pods filesystem; methods are all static
class PodFiles:
    pods_cmder_written = set()
    Pods.creating_dir = creating_dir

    def cmder(pod_name: str, container: str, namespace: str):
        script = PodFiles.creating_dir(pod_name, container, namespace, Config().get('job.cmder.path', '/tmp/q/cmder.sh'), is_file=True)

        key = f'{namespace}.{container}.{pod_name}'
        if key not in Pods.pods_cmder_written:
            cmd_file_content = Config().get('job.cmder.content', "($1; echo QING_$?) > $2 2> $3 &")
            Pods.exec(pod_name, container, namespace, f"echo '{cmd_file_content}' > {script} && chmod a+x {script}")
            Pods.pods_cmder_written.add(key)

        return script

    def log_file_from_template(log_file: str, pod_name: str):
        if not log_file:
            return None

        pod_suffix = pod_name
        if pod_name:
            if groups := re.match(r'.*-(.*)', pod_name):
                pod_suffix = f'-{groups[1]}'
            elif groups := re.match(r'.*_(.*)', pod_name):
                pod_suffix = f'-{groups[1]}'

        if not pod_suffix.startswith('-'):
            pod_suffix = f'-{pod_suffix}'

        return log_file.replace('{pod}', pod_suffix)

    def read_file(pod_name: str, container: str, namespace: str, file_path: str):
        v1 = client.CoreV1Api()

        resp = stream(
            v1.connect_get_namespaced_pod_exec,
            name=pod_name,
            namespace=namespace,
            container=container,
            command=["cat", file_path],
            stderr=True, stdin=False,
            stdout=True, tty=False,
            _preload_content=False, # Important for streaming
        )

        s: WebSocket = resp.sock
        try:
            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    yield resp.read_stdout()

            with log_exc():
                # get the exit code from server
                error_output = resp.read_channel(ERROR_CHANNEL)
        except Exception as e:
            raise e
        finally:
            resp.close()
            if s and s.sock and Pods._TEST_POD_CLOSE_SOCKET:
                with log_exc():
                    s.sock.close()

    def download_file(pod_name: str, container: str, namespace: str, from_path: str, to_path: str = None):
        if not to_path:
            to_path = f'{local_downloads_dir()}/{os.path.basename(from_path)}'

        bytes = PodFiles.read_file(pod_name, container, namespace, from_path)
        with open(to_path, 'wb') as f:
            for item in GeneratorStream(bytes):
                f.write(item)

        ReplSession().append_history(f':tail {to_path}')

        return to_path

    _dirs_created = set()

    def creating_dir(pod_name: str,
                     container: str,
                     namespace: str,
                     dir_or_file: str,
                     is_file = False,
                     ctx: Context = Context.NULL):
        dir = dir_or_file
        if is_file:
            dir = os.path.dirname(dir_or_file)

        key = f'{dir}@{pod_name}'
        if key not in PodFiles._dirs_created:
            PodFiles._dirs_created.add(key)
            Pods.exec(pod_name, container, namespace, f'mkdir -p {dir}', shell='bash', ctx=ctx)

        return dir_or_file

    def find_files(pod: str, container: str, namespace: str, pattern: str, mmin: int = 0, remote = False, capture_pid = False, ctx: Context = Context.NULL):
        log_files: list[PodLogFile] = []

        stdout = ''
        if not remote:
            # find . -maxdepth 1 -type f -name '*'
            dir = os.path.dirname(pattern)
            base = os.path.basename(pattern)
            cmd = ['find', dir, '-name', base]
            if mmin:
                cmd += ['-mmin',  f'-{mmin}']

            cmd += ["-exec", "stat", "-c", "'%n %s'", "{}", "\;"]

            stdout = local_exec(cmd, show_out=ctx.debug).stdout
        else:
            dir = os.path.dirname(pattern)
            base = os.path.basename(pattern)
            cmd = f"find {dir} -name '{base}'"
            if mmin:
                cmd = f'{cmd} -mmin -{mmin}'

            cmd += " -exec stat -c '%n %s' {} \;"
            if capture_pid:
                cmd += " -exec tail -n 1 {} \;"

            stdout = Pods.exec(pod, container, namespace, cmd, shell='bash', ctx=ctx).stdout

        # /tmp/q/logs/21085209.err 58
        # nohup: can't execute 'sdfsfsf': No such file or directory
        # /tmp/q/logs/21085209.log 7
        # QING:466607:0
        # /tmp/q/logs/21142322.log 632
        # (4 rows)
        # /tmp/q/logs/21142322.pid 14
        # QING:477894:0

        f: PodLogFile = None
        for line in stdout.split('\n'):
            line = line.strip(' \r')
            if line:
                if line.startswith('QING:'):
                    if f:
                        if groups := re.match(r'^QING:(\d+):(\d+)$', line):
                            f.pid=groups[1]
                            f.exit_code = groups[2]
                        elif groups := re.match(r'^QING:(\d+)', line):
                            f.pid=groups[1]
                else:
                    tokens = line.split(' ')
                    if len(tokens) == 2 and tokens[0].startswith('/') and tokens[1].isdigit():
                        f = PodLogFile(tokens[0], pod, size=tokens[1])
                        log_files.append(f)

        return log_files

# def creating_dir(pod_name: str,
#                     container: str,
#                     namespace: str,
#                     dir_or_file: str,
#                     show_out = False,
#                     is_file = False):
#     return PodFiles.creating_dir(pod_name, container, namespace, dir_or_file, show_out, is_file)
    # dir = dir_or_file
    # if is_file:
    #     dir = os.path.dirname(dir_or_file)

    # key = f'{dir}@{pod_name}'
    # if key not in PodFiles._dirs_created:
    #     PodFiles._dirs_created.add(key)
    #     Pods.exec(pod_name, container, namespace, f'mkdir -p {dir}', show_out=show_out, shell='bash')

    # return dir_or_file