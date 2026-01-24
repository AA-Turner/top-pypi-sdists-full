from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.export.export_sessions import export_session
from adam.repl_state import ReplState, RequiredState

class CleanUpExportSessions(Command):
    COMMAND = 'clean up export sessions'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CleanUpExportSessions, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return CleanUpExportSessions.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='export session', separator=',') as session_names:
                with export_session(state) as sessions:
                    sessions.clean_up(session_names)

                return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'clean up export sessions', args='<export-session-name>,...')