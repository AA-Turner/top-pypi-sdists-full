import click

from adam.commands import extract_trailing_options
from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.cql.completions_c import completions_c
from adam.commands.cql.utils_cql import cassandra
from adam.repl_state import ReplState, RequiredState
from adam.utils import log
from adam.utils_context import Context

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

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with cassandra(state) as pods:
                    pods.cql(args, ctx=Context.new(cmd, show_out=True, backgrounded=backgrounded, history=Context.PODS))

    def completion(self, state: ReplState) -> dict[str, any]:
        if state.device != state.C:
            return {}

        if state.sts or state.pod:
            return completions_c(state)

        return {}

    def help(self, state: ReplState) -> str:
        return super().help(state, 'run cqlsh with queries', command='[cql] <cql-statement>;...', args='[&]')

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