from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.export.exporter import export
from adam.commands.export.utils_export import state_with_pod
from adam.repl_state import ReplState, RequiredState

class ImportSession(Command):
    COMMAND = 'import session'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ImportSession, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ImportSession.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with validate_args(args, state, name='export session') as spec:
                    with state_with_pod(state) as state:
                        with export(state) as exporter:
                            exporter.import_session(spec, ctx=ctx)

                            return state

    def completion(self, state: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'import tables in session to SQLite(or Athena)', args='<export-session-name>')