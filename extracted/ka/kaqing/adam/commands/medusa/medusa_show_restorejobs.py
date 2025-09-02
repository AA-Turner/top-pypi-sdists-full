from adam.commands.command import Command
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.k8s_utils.custom_resources import CustomResources
from adam.utils import lines_to_tabular, log2

class MedusaShowRestoreJobs(Command):
    COMMAND = 'show restores'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(MedusaShowRestoreJobs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return MedusaShowRestoreJobs.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)
        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        ns = state.namespace
        dc = StatefulSets.get_datacenter(state.sts, ns)
        if not dc:
            return state

        try:
            rtlist = CustomResources.medusa_show_restorejobs(dc, ns)
            log2(lines_to_tabular(rtlist, 'NAME\tCREATED\tFINISHED', separator='\t'))
        except Exception as e:
            log2("Exception: MedusaShowRestoreJobs failed: %s\n" % e)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{MedusaShowRestoreJobs.COMMAND}\t start a restore job'