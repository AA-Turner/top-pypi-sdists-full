import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.nodetool_commands import NODETOOL_COMMANDS
from adam.config import Config
from adam.k8s_utils.cassandra_clusters import CassandraClusters
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.repl_state import ReplState, RequiredState
from adam.utils import log

class NodeTool(Command):
    COMMAND = 'nodetool'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(NodeTool, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return NodeTool.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        user, pw = state.user_pass()
        command = f"nodetool -u {user} -pw {pw} {' '.join(args)}"

        if state.pod:
            return CassandraNodes.exec(state.pod, state.namespace, command, show_out=True)
        elif state.sts:
            return CassandraClusters.exec(state.sts, state.namespace, command, action='nodetool', show_out=True)

    def completion(self, state: ReplState):
        if state.pod or state.sts:
            return {NodeTool.COMMAND: {'help': None} | {c: None for c in NODETOOL_COMMANDS}}

        return {}

    def help(self, _: ReplState):
        return f'{NodeTool.COMMAND} <sub-command>\t run nodetool with arguments'

class NodeToolCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Sub-Commands:')

        cmds = ''
        for c in NODETOOL_COMMANDS:
            if cmds:
                cmds += ', '
            cmds += c
            if len(cmds) > Config().get('nodetool.commands_in_line', 40):
                log('  ' + cmds)
                cmds = ''

        if len(cmds) > 0:
            log('  ' + cmds)
        log()
        ClusterOrPodCommandHelper.cluter_or_pod_help()