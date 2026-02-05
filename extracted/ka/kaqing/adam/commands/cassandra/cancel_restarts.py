from adam.commands import validate_args
from adam.commands.command import Command
from adam.utils_cassandra.node_scheduler import NodeScheduler
from adam.utils_context import Context
from adam.repl_state import ReplState, RequiredState
from adam.utils import duration
from adam.utils_repl.set_completer import SetCompleter
from adam.utils_tabulize import tabulize

class CancelRestarts(Command):
    COMMAND = 'cancel restarts'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CancelRestarts, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return CancelRestarts.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state, apply=False) as (args, state):
            with validate_args(args, state, name='pod name'):
                pods = self.comma_separated_args(args)

                ctx = self.context()
                canceled = list(NodeScheduler.cancel_restarts(state, pods, ctx=ctx).items())
                canceled = sorted(canceled, key=lambda p: p[1])

                ctx.log('Canceled restarts:')
                tabulize(canceled,
                         fn=lambda p: f'{p[0][0]}\t{p[0][1]}\t{duration(p[1])} ago',
                         header='POD\tNAMESPACE\tSCHEDULED',
                         separator='\t',
                         ctx=ctx)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: SetCompleter(NodeScheduler.restarts(ctx=Context.NULL)))

    def help(self, state: ReplState):
        return super().help(state, 'cancel restart request on Cassandra nodes', args='<pod-name>,...')