import functools
from typing import List
from kubernetes import client

from adam.config import Config
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_session import ReplSession

# utility collection on app pods; methods are all static
class AppPods:
    @functools.lru_cache()
    def pod_names(namespace: str, env: str, app: str):
        if not env or not app:
            return []

        return [pod.metadata.name for pod in AppPods.app_pods(namespace, env, app)]

    def app_pods(namespace: str, env: str, app: str) -> List[client.V1Pod]:
        v1 = client.CoreV1Api()

        env_key = Config().get('app.env', 'c3__env-0')
        app_key = Config().get('app.app', 'c3__app-0')
        label_selector = f'applicationGroup=c3,{env_key}=0{env}0,{app_key}=0{app}0'

        return v1.list_namespaced_pod(namespace, label_selector=label_selector).items

    def exec(pod_name: str,
             namespace: str,
             command: str,
             throw_err = False,
             shell = '/bin/sh',
             ctx: Context = Context.NULL) -> PodExecResult:
        container = Config().get('app.container-name', 'c3-server')
        r = Pods.exec(pod_name, container, namespace, command, throw_err = throw_err, shell = shell, ctx = ctx)

        if r:
            if ctx.show_out:
                ctx.log2(command, verbose=True)
                ctx.log(r.stdout)
                ctx.log2(r.stderr)

            if r.log_file:
                ReplSession().append_history(f':tail {r.log_file}')

        return r