from abc import abstractmethod
from typing import Callable

from adam.config import Config
from adam.repl_state import ReplState

class CommandFilter:
    @abstractmethod
    def command(self) -> str:
        pass

    @abstractmethod
    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], str]:
        pass

    def process_config(self, state: ReplState, cmd: str, word: str, config_key: str, value = True, default = False) -> tuple[Callable[[], None], str]:
        if (pre := f'{word} ') and cmd.startswith(pre):
            cmd = cmd[len(pre):]
            final_value = Config().get(config_key, default=default)

            Config().set(config_key, value)

            return lambda: Config().set(config_key, final_value), cmd

        return None, cmd

    def help(self, _: ReplState, desc: str = None, command: str = None):
        if not desc:
            return None

        if not command:
            command = self.command()
        return f'{command}\t\t{desc}'