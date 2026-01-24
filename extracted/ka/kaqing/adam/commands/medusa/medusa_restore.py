from datetime import datetime
from functools import partial

from adam.commands import validate_args
from adam.commands.command import Command, InvalidArgumentsException
from adam.commands.medusa.utils_medusa import medusa_backup_names
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils import tabulize, log2, log_exc

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

        with self.validate(args, state) as (args, state):
            ns = state.namespace
            dc: str = StatefulSets.get_datacenter(state.sts, ns)
            if not dc:
                return state

            def msg(missing: bool):
                if missing:
                    log2('\n* Missing Backup Name')
                    log2('Usage: qing restore <backup> <sts@name_space>\n')
                else:
                    log2('\n* Backup job name is not valid.')

                tabulize(CustomResources.medusa_show_backupjobs(dc, ns),
                         lambda x: f"{x['metadata']['name']}\t{x['metadata']['creationTimestamp']}\t{x['status'].get('finishTime', '')}",
                         header='NAME\tCREATED\tFINISHED',
                         separator='\t',
                         to=2)

            with validate_args(args, state, msg=partial(msg, True)) as bkname:
                if not (job := CustomResources.medusa_get_backupjob(dc, ns, bkname)):
                    msg(False)
                    raise InvalidArgumentsException()

                if not input(f"Restoring from {bkname} created at {job['metadata']['creationTimestamp']}. Please enter Yes to continue: ").lower() in ['y', 'yes']:
                    return state

                with log_exc(lambda e: "Exception: MedusaRestore failed: %s\n" % e):
                    now_dtformat = datetime.now().strftime("%Y-%m-%d.%H.%M.%S")
                    rtname = 'medusa-' + now_dtformat + '-restore-from-' + bkname
                    CustomResources.create_medusa_restorejob(rtname, bkname, dc, ns)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {id: None for id in medusa_backup_names(state)}, auto_key='medusa.backups')

    def help(self, state: ReplState):
        return super().help(state, 'start a restore job')