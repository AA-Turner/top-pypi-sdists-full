from adam.commands.command import Command
from adam.utils_k8s.jobs import Jobs
from adam.repl_state import ReplState, RequiredState

class RepairLog(Command):
    COMMAND = 'repair log'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RepairLog, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RepairLog.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            ns = state.namespace
            Jobs.get_logs('cassrepair-'+state.sts, ns)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'get repair job logs')