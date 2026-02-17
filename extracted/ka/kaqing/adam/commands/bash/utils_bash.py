from adam.commands.devices.devices import device
from adam.utils_repl.repl_state import ReplState
from adam.utils_context import NULL

class BashHandler:
    def __init__(self, s0: ReplState, s1: ReplState):
        self.s0 = s0
        self.s1 = s1

    def __enter__(self):
        return self.exec

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def exec(self, args: list[str], ctx = NULL):
        return device(self.s1).bash(self.s0, self.s1, args, ctx=ctx)