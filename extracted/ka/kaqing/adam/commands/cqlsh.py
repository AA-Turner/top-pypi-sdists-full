import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.cql_utils import run_cql
from adam.repl_state import ReplState, RequiredState
from adam.utils import log, log2

class Cqlsh(Command):
    COMMAND = 'cql'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Cqlsh, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def command(self):
        return Cqlsh.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        opts = []
        cqls = []
        for arg in args:
            if arg.startswith('--'):
                opts.append(arg)
            elif arg != '-e':
                cqls.append(arg)
        if not cqls:
            if state.in_repl:
                log2('Please enter cql statement. e.g. select host_id from system.local')
            else:
                log2('* CQL statement is missing.')
                log2()
                Command.display_help()

            return 'no-cql'

        cql = ' '.join(cqls)
        return run_cql(state, cql, opts, show_out=True)

    def completion(self, state: ReplState) -> dict[str, any]:
        if state.sts or state.pod:
            return {Cqlsh.COMMAND: None} | {
                'delete': {'from': None},
                'insert': {'into': None},
                'select': None,
                'update': None,
            }

        return {}

    def help(self, _: ReplState) -> str:
        return f'[{Cqlsh.COMMAND}] <cql-statements>\t run cqlsh with queries'

class CqlCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('  e.g. qing cql <cluster or pod> select host_id from system.local')
        log()
        log('Advanced Usages:')
        log('  1. Use -- to specify what arguments are passed to the cqlsh.')
        log('  2. Use "" to avoid expansion on shell variables.')
        log('  3. Use ; to use multiple CQL statements')
        log()
        log('  e.g. qing cql <cluster or pod> -- "consistency quorum; select * from system.local" --request-timeout=3600')
        log()

        ClusterOrPodCommandHelper.cluter_or_pod_help()