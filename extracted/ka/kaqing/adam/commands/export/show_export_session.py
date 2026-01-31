from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.export.export_sessions import export_session
from adam.repl_state import ReplState, RequiredState

class ShowExportSession(Command):
    COMMAND = 'show export session'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowExportSession, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowExportSession.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='export session') as session:
                with export_session(state) as sessions:
                    sessions.show_session(session, self.context())

            return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'show export session', args='<export-session-name>')