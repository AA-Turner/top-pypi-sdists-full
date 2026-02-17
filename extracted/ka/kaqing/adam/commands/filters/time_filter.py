from typing import Callable
from adam.commands.command_filter import CommandFilter
from adam.utils_repl.repl_state import ReplState

class TimeFilter(CommandFilter):
    def command(self) -> str:
        return 'time'

    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], ReplState, str]:
        return super().process_config(state, cmd, self.command(), 'debugs.timings', value='on', default='off')

    def help(self, state: ReplState) -> str:
        return super().help(state, 'run command with timing debug on', command='time <command>...')