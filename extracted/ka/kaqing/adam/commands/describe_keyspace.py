import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.cql_utils import keyspaces, parse_cql_desc_tables, run_cql
from adam.config import Config
from adam.pod_exec_result import PodExecResult
from adam.repl_state import ReplState, RequiredState
from adam.utils import log, log2

class DescribeKeyspace(Command):
    COMMAND = 'describe keyspace'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DescribeKeyspace, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def required(self):
        return RequiredState.CLUSTER

    def command(self):
        return DescribeKeyspace.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not args:
            if state.in_repl:
                log2('Please enter keyspace name')
            else:
                log2('* keyspace name is missing.')
                log2()
                Command.display_help()

            return 'missing-keyspace'

        r: list[PodExecResult] = run_cql(state, f'describe keyspace {args[0]}', show_out=True, on_any=True)
        if not r:
            log2('No pod is available')
            return 'no-pod'

        # do not continue to cql route
        return state

    def completion(self, state: ReplState) -> dict[str, any]:
        if state.sts:
            state.wait_log("Inspecting Cassandra Keyspaces...")
            return super().completion(state, {ks: None for ks in keyspaces(state.sts, state.namespace)})

        return {}

    def help(self, _: ReplState) -> str:
        return f'{DescribeKeyspace.COMMAND} <keyspace-name>\t describe Cassandra keyspace'