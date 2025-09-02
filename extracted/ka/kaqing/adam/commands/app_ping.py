from adam.commands.command import Command
from adam.repl_state import ReplState, RequiredState
from adam.app_session import AppSession

class AppPing(Command):
    COMMAND = 'app ping'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(AppPing, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return AppPing.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state, app_required=RequiredState.APP_APP):
            return state

        _, forced = Command.extract_options(args, '--force')

        AppSession.run(state.app_env, state.app_app, state.namespace, 'Echo', 'echoStatic', forced= forced)

        return state

    def completion(self, state: ReplState):
        if state.app_app:
            return super().completion(state, {'--force': None})

        return {}

    def help(self, _: ReplState):
        return f"{AppPing.COMMAND} [--force]\t ping app server with Echo.echoStatic()"