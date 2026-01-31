from adam.commands.command import Command
from adam.commands.devices.device_export import DeviceExport
from adam.commands.export.export_databases import export_db
from adam.repl_state import ReplState

class ShowExportDatabases(Command):
    COMMAND = 'show export databases'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowExportDatabases, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowExportDatabases.COMMAND

    def required(self):
        return [ReplState.C, ReplState.X]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with export_db(state) as dbs:
                dbs.show_databases(self.context())

            return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'list export databases')