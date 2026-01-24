import copy

from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState

class Ls(Command):
    COMMAND = 'ls'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Ls, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Ls.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            if len(args) > 0:
                arg = args[0]
                if arg in ['p:', 'c:'] and arg != f'{state.device}:':
                    state = copy.copy(state)
                    state.device = arg.replace(':', '')

            Devices.of(state).ls(cmd, state)

            return state

    def completion(self, state: ReplState):
        return super().completion(state, {'&': None}, pods=Devices.of(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'list apps, envs, clusters, nodes, pg hosts/databases or export databases', args='[device:]')