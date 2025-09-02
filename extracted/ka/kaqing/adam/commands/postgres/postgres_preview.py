from adam.commands.command import Command
from adam.commands.ls import Ls
from adam.commands.preview_table import PreviewTable
from adam.repl_state import ReplState, RequiredState

class PostgresPreview(Command):
    COMMAND = 'pg preview'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(PostgresPreview, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return PostgresPreview.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state, RequiredState.PG_DATABASE):
            return state

        state.device = ReplState.P

        PreviewTable().run(f'preview {" ".join(args)}', state)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{PostgresPreview.COMMAND}\t preview postgres table'