from adam.commands.command import Command
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils import log_exc
from adam.utils_tabulize import tabulize

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

        with self.validate(args, state) as (args, state):
            ns = state.namespace
            dc = StatefulSets.get_datacenter(state.sts, ns)
            if not dc:
                return state

            with log_exc(lambda e: "Exception: MedusaShowBackupJobs failed: %s\n" % e):
                CustomResources.clear_caches()

                tabulize(CustomResources.medusa_show_backupjobs(dc, ns),
                         lambda x: f"{x['metadata']['name']}\t{x['metadata']['creationTimestamp']}\t{x['status'].get('finishTime', '') if 'status' in x else 'unknown'}",
                         header='NAME\tCREATED\tFINISHED',
                         separator='\t',
                         err=True,
                         ctx=self.context())

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show Medusa backups')