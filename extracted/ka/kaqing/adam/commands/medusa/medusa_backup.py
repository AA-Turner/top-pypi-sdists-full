from datetime import datetime
import re

from adam.commands.command import Command
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.k8s_utils.custom_resources import CustomResources
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
        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        ns = state.namespace
        sts = state.sts
        now_dtformat = datetime.now().strftime("%Y-%m-%d.%H.%M.%S")
        bkname = 'medusa-' + now_dtformat + 'full-backup-' + sts
        if len(args) == 1:
            bkname = str(args[0])
        groups = re.match(r'^(.*?-.*?-).*', sts)
        dc = StatefulSets.get_datacenter(state.sts, ns)
        if not dc:
            return state

        try:
            CustomResources.create_medusa_backupjob(bkname, dc, ns)
        except Exception as e:
            log2("Exception: MedusaBackup failed: %s\n" % e)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{MedusaBackup.COMMAND}\t start a backup job'