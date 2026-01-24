from adam.commands.command import Command
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils import tabulize, log_exc

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

        with self.validate(args, state) as (args, state):
            ns = state.namespace
            dc = StatefulSets.get_datacenter(state.sts, ns)
            if not dc:
                return state

            with log_exc(lambda e: "Exception: MedusaShowRestoreJobs failed: %s\n" % e):
                tabulize(CustomResources.medusa_show_restorejobs(dc, ns),
                         header='NAME\tCREATED\tFINISHED',
                         separator='\t',
                         to=2)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show Medusa restores')