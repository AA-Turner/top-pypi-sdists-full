from abc import abstractmethod

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper
from adam.repl_state import ReplState
from adam.utils import tabulize, log, log2

class IntermediateCommand(Command):
    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        return self.intermediate_run(cmd, state, args, self.cmd_list())

    def completion(self, state: ReplState):
        return {}

    @abstractmethod
    def cmd_list(self):
        pass

    def intermediate_run(self, cmd: str, state: ReplState, args: list[str], cmds: list['Command'], separator='\t', display_help=True):
        state, _ = self.apply_state(args, state)

        if state.in_repl:
            if display_help:
                tabulize(cmds, lambda c: c.help(state), separator=separator)

            return 'command-missing'
        else:
            # head with the Chain of Responsibility pattern
            if not self.run_subcommand(cmd, state):
                if display_help:
                    log2('* Command is missing.')
                    Command.display_help()
                return 'command-missing'

        return state

    def run_subcommand(self, cmd: str, state: ReplState):
        cmds = Command.chain(self.cmd_list())
        return cmds.run(cmd, state)

    def intermediate_help(super_help: str, cmd: str, cmd_list: list['Command'], separator='\t', show_cluster_help=False):
        log(super_help)
        log()
        log('Sub-Commands:')

        tabulize(cmd_list, lambda c: c.help(ReplState()).replace(f'{cmd} ', '  ', 1), separator=separator)
        if show_cluster_help:
            log()
            ClusterCommandHelper.cluster_help()