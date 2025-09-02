import json

from adam.apps import Apps
from adam.commands.command import Command
from adam.repl_state import ReplState, RequiredState
from adam.app_session import AppSession
from adam.utils import log2

class App(Command):
    COMMAND = 'app'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(App, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return App.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state, app_required=RequiredState.APP_APP):
            return state

        args, forced = Command.extract_options(args, '--force')

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

    def completion(self, state: ReplState):
        if state.app_app:
            return super().completion(state, {'--force': None})

        return {}

    def help(self, _: ReplState):
        return f"{App.COMMAND} [--force]\t post app API query with type and function"