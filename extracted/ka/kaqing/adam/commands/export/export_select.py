from adam.commands.command import Command
from adam.commands.export.completions_x import completions_x
from adam.repl_state import ReplState, RequiredState

# No action body, only for a help entry and auto-completion
class ExportSelect(Command):
    COMMAND = 'select_on_x'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ExportSelect, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ExportSelect.COMMAND

    def required(self):
        return RequiredState.EXPORT_DB

    def completion(self, state: ReplState):
        if state.device != ReplState.X:
            return {}

        if state.export_session:
            return completions_x(state)

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'run queries on export database', command='<sql-select-statements>')