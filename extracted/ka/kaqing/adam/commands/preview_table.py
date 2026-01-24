from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState, RequiredState

class PreviewTable(Command):
    COMMAND = 'preview'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(PreviewTable, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return PreviewTable.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.PG_DATABASE, ReplState.L, RequiredState.EXPORT_DB]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, at_least=1) as table:
                Devices.of(state).preview(table, state)

            return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'preview table', args='TABLE')