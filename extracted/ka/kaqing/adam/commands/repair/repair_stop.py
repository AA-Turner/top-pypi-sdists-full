from adam.commands.command import Command
from adam.k8s_utils.jobs import Jobs
from adam.repl_state import ReplState, RequiredState
from adam.config import Config

class RepairStop(Command):
    COMMAND = 'repair stop'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RepairStop, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RepairStop.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        ns = state.namespace
        Jobs.delete('cassrepair-'+state.sts, ns)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{RepairStop.COMMAND}\t delete a repair job'