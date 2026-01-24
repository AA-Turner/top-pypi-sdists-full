from adam.commands.command import Command
from adam.commands.fs.ls import Ls
from adam.repl_state import ReplState, RequiredState

class PostgresLs(Command):
    COMMAND = 'pg ls'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(PostgresLs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return PostgresLs.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            state.device = ReplState.P

            Ls().run('ls', state)

            return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'list postgres hosts, databases or tables')