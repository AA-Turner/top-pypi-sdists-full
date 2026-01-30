import json
from typing import Union

from adam.app_session import AppSession
from adam.apps import Apps
from adam.utils_context import Context
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_k8s.app_clusters import AppClusters
from adam.utils_k8s.app_pods import AppPods

def app_cd_dirs(state: ReplState):
    if state.app_app:
        return ['..'] + AppPods.pod_names(state.namespace, state.app_env, state.app_app)
    elif state.app_env:
        return ['..'] + [app[0].split('-')[1] for app in Apps.apps(state.app_env)]
    else:
        return [env[0] for env in Apps.envs()]

class AppRestHandler:
    def __init__(self, state: ReplState, forced = False):
        self.state = state
        self.forced = forced

    def __enter__(self):
        return self.post

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def post(self, args: list[str]) -> Union[ReplState, str]:
        if not args:
            return 'arg missing'

        t_f = args[0].split('.')
        if len(t_f) < 2:
            return 'arg missing'

        state = self.state

        payload, valid = Apps().payload(t_f[0], t_f[1], args[1:] if len(args) > 1 else [])
        if not valid:
            log2('Missing one or more action arguments.')
            return state

        if payload:
            try:
                payload = json.loads(payload)
            except json.decoder.JSONDecodeError as e:
                log2(f'Invalid json argument: {e}')
                return state

        AppSession.run(state.app_env, state.app_app, state.namespace, t_f[0], t_f[1], payload=payload, forced=self.forced)

        return state

class AppPodService:
    def __init__(self, handler: 'AppHandler'):
        self.handler = handler

    def exec(self, command: str, ctx: Context = Context.NULL) -> Union[PodExecResult, list[PodExecResult]]:
        state = self.handler.state

        if state.app_pod:
            return AppPods.exec(state.app_pod, state.namespace, command, shell='bash', ctx=ctx)
        elif state.app_app:
            pods = AppPods.pod_names(state.namespace, state.app_env, state.app_app)
            return AppClusters.exec(pods, state.namespace, command, action='bash', shell='bash', ctx=ctx)

        return []

    def post(self, args: list[str], forced=False) -> Union[ReplState, str]:
        state = self.handler.state

        if not args:
            return 'arg missing'

        t_f = args[0].split('.')
        if len(t_f) < 2:
            return 'arg missing'

        payload, valid = Apps().payload(t_f[0], t_f[1], args[1:] if len(args) > 1 else [])
        if not valid:
            log2('Missing one or more action arguments.')
            return state

        if payload:
            try:
                payload = json.loads(payload)
            except json.decoder.JSONDecodeError as e:
                log2(f'Invalid json argument: {e}')
                return state

        AppSession.run(state.app_env, state.app_app, state.namespace, t_f[0], t_f[1], payload=payload, forced=forced)

        return state

class AppHandler:
    def __init__(self, state: ReplState):
        self.state = state

    def __enter__(self):
        return AppPodService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
