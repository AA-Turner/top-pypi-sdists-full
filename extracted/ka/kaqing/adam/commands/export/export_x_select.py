from adam.commands import extract_trailing_options, validate_args
from adam.commands.command import Command
from adam.commands.export.completions_x import completions_x
from adam.commands.export.export_databases import export_db
from adam.repl_state import ReplState, RequiredState
from adam.utils_async_job import AsyncJobs
from adam.utils_context import Context

class ExportXSelect(Command):
    COMMAND = 'xelect'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ExportXSelect, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ExportXSelect.COMMAND

    def required(self):
        return RequiredState.EXPORT_DB

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with validate_args(args, state, name='SQL statement') as query:
                    with export_db(state) as dbs:
                        dbs.sql(f'select {query}', ctx=Context.new(cmd, backgrounded))

                    return state

    def completion(self, state: ReplState):
        if state.device != ReplState.C:
            return {}

        if not state.export_session:
            return {}

        # add only xelect completions to c: drive from lark
        return {ExportXSelect.COMMAND: completions_x(state)[ExportXSelect.COMMAND]}

    def help(self, state: ReplState):
        return super().help(state, 'run queries on export database', command='xelect...')