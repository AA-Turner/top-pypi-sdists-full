from abc import abstractmethod
from typing import Callable

from adam.commands.command import Command
from adam.config import Config
from adam.utils_repl.repl_state import ReplState

class CommandFilter:
    @abstractmethod
    def command(self) -> str:
        pass

    @abstractmethod
    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], ReplState, str]:
        pass

    def applicable_commands(self, commands: list[Command]) -> list[Command]:
        return commands

    def process_config(self, state: ReplState, cmd: str, word: str, config_key: str, value = True, default = False) -> tuple[Callable[[], None], ReplState, str]:
        if (pre := f'{word} ') and cmd.startswith(pre):
            cmd = cmd[len(pre):]
            final_value = Config().get(config_key, default=default)

            Config().set(config_key, value)

            return lambda results: Config().set(config_key, final_value), state, cmd

        return None, state, cmd

    def help(self, _: ReplState, desc: str = None, command: str = None):
        if not desc:
            return None

        if not command:
            command = self.command()
        return f'{command}\t\t{desc}'