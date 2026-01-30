from adam.commands.command import Command
from adam.commands.export.export_sessions import export_session
from adam.repl_state import ReplState, RequiredState
from adam.utils_context import Context

class CleanUpAllExportSessions(Command):
    COMMAND = 'clean up all export sessions'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CleanUpAllExportSessions, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return CleanUpAllExportSessions.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with export_session(state) as sessions:
                sessions.clean_up_all(Context.new(show_out=True))

            return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'clean up all export sessions')