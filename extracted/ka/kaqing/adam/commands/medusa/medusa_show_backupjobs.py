from adam.commands.command import Command
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.k8s_utils.custom_resources import CustomResources
from adam.utils import lines_to_tabular, log2


class MedusaShowBackupJobs(Command):
    COMMAND = 'show backups'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(MedusaShowBackupJobs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return MedusaShowBackupJobs.COMMAND

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
            bklist = [f"{x['metadata']['name']}\t{x['metadata']['creationTimestamp']}\t{x['status'].get('finishTime', '')}" for x in CustomResources.medusa_show_backupjobs(dc, ns)]
            log2(lines_to_tabular(bklist, 'NAME\tCREATED\tFINISHED', separator='\t'))
        except Exception as e:
            log2("Exception: MedusaShowBackupJobs failed: %s\n" % e)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{MedusaShowBackupJobs.COMMAND}\t start a restore job'