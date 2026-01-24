from datetime import datetime

from adam.commands import validate_args
from adam.commands.command import Command
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils import log2

class MedusaBackup(Command):
    COMMAND = 'backup'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(MedusaBackup, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return MedusaBackup.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            ns = state.namespace
            sts = state.sts
            now_dtformat = datetime.now().strftime("%Y-%m-%d.%H.%M.%S")
            with validate_args(args, state, default='medusa-' + now_dtformat + 'full-backup-' + sts) as bkname:
                dc = StatefulSets.get_datacenter(state.sts, ns)
                if not dc:
                    return state

                try:
                    CustomResources.create_medusa_backupjob(bkname, dc, ns)
                except Exception as e:
                    log2("Exception: MedusaBackup failed: %s\n" % e)
                finally:
                    CustomResources.clear_caches()

                return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'start a backup job')