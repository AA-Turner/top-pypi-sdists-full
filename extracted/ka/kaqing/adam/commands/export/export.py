from adam.commands import extract_options
from adam.commands.command import Command
from adam.commands.export.exporter import export
from adam.repl_state import ReplState, RequiredState

class ExportTables(Command):
    COMMAND = 'export'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ExportTables, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ExportTables.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            # remove & if present
            with self.context(args) as (args, ctx):
                with extract_options(args, '--export-only') as (args, export_only):
                    with export(state) as exporter:
                        exporter.export(args, export_only=export_only, ctx=ctx)

                        return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'export tables to Sqlite, Athena or CSV file', args='TABLE...')