from adam.commands.command import Command
from adam.commands.cli_commands import CliCommands
from adam.repl_state import ReplState, RequiredState
from adam.utils import lines_to_tabular, log

class ShowKubectlCommands(Command):
    COMMAND = 'show cli-commands'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowKubectlCommands, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowKubectlCommands.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        if not self.validate_state(state):
            return state

        v = CliCommands.values(state, collapse=True)
        # node-exec-?, nodetool-?, cql-?, reaper-exec, reaper-forward, reaper-ui, reaper-username, reaper-password
        cmds = [
            f'bash,{v["node-exec-?"]}',
            f'nodetool,{v["nodetool-?"]}',
            f'cql,{v["cql-?"]}',
        ]

        if 'reaper-exec' in v:
            cmds += [
                f'reaper,{v["reaper-exec"]}',
                f',{v["reaper-forward"]}  * should be run from your laptop',
                f',{v["reaper-ui"]}',
                f',{v["reaper-username"]}',
                f',{v["reaper-password"]}',
            ]

        cmds += [f'{k},{v0}' for k, v0 in v.items() if k.startswith('pg-')]

        log(lines_to_tabular(cmds, separator=','))

        return cmds

    def completion(self, state: ReplState):
        if not state.sts:
            return {}

        return super().completion(state)

    def help(self, _: ReplState):
        return f"{ShowKubectlCommands.COMMAND}\t show kubectl commands"