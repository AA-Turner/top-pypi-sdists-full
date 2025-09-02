from datetime import datetime

from adam.commands.command import Command
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.k8s_utils.custom_resources import CustomResources
from adam.config import Config
from adam.utils import lines_to_tabular, log2

class MedusaRestore(Command):
    COMMAND = 'restore'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(MedusaRestore, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return MedusaRestore.COMMAND

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

        if len(args) == 1:
            bkname = args[0]
            job = CustomResources.medusa_get_backupjob(dc, ns, bkname)
            if not job:
                log2('\n* Backup job name is not valid.')
                bklist = [f"{x['metadata']['name']}\t{x['metadata']['creationTimestamp']}\t{x['status'].get('finishTime', '')}" for x in CustomResources.medusa_show_backupjobs(dc, ns)]
                log2(lines_to_tabular(bklist, 'NAME\tCREATED\tFINISHED', separator='\t'))

                return state

            if not input(f"Restoring from {bkname} created at {job['metadata']['creationTimestamp']}. Please enter Yes to continue: ").lower() in ['y', 'yes']:
                return state
        else:
            bklist = [f"{x['metadata']['name']}\t{x['metadata']['creationTimestamp']}\t{x['status'].get('finishTime', '')}" for x in CustomResources.medusa_show_backupjobs(dc, ns)]
            log2('\n* Missing Backup Name')
            log2('Usage: qing medusa restore <backup> <sts@name_space>\n')
            log2(lines_to_tabular(bklist, 'NAME\tCREATED\tFINISHED', separator='\t'))
            return state

        now_dtformat = datetime.now().strftime("%Y-%m-%d.%H.%M.%S")
        rtname = 'medusa-' + now_dtformat + '-restore-from-' + bkname
        try:
            print('SEAN doing')
            # CustomResources.create_medusa_restorejob(rtname, bkname, dc, ns)
        except Exception as e:
            log2("Exception: MedusaRestore failed: %s\n" % e)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            ns = state.namespace
            dc = StatefulSets.get_datacenter(state.sts, ns)
            if not dc:
                return {}

            if Config().get('medusa.restore-auto-complete', False):
                leaf = {id: None for id in [f"{x['metadata']['name']}" for x in CustomResources.medusa_show_backupjobs(dc, ns)]}

                return super().completion(state, leaf)
            else:
                return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{MedusaRestore.COMMAND}\t start a restore job'