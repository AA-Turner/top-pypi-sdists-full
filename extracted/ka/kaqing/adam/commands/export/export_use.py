from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.export.export_databases import export_db
from adam.repl_state import ReplState
from adam.utils import log2

class ExportUse(Command):
    COMMAND = 'use'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ExportUse, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ExportUse.COMMAND

    def required(self):
        return [ReplState.C]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, at_least=0) as session:
                if not session:
                    state.export_session = None

                    log2('Export database is unset.')

                    return state

                state.export_session = session

                with export_db(state) as dbs:
                    dbs.show_database()

                return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'use export database', args='<export-database-name>')