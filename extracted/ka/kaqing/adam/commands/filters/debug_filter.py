from typing import Callable
from adam.commands.command_filter import CommandFilter
from adam.repl_state import ReplState

class DebugFilter(CommandFilter):
    def command(self) -> str:
        return 'debug'

    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], str]:
        return super().process_config(state, cmd, self.command(), 'debug')

    def help(self, state: ReplState) -> str:
        return super().help(state, 'run command with debug on', command='debug <command>...')