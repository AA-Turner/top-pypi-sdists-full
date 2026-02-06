from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState
from adam.utils_context import Context

class BashHandler:
    def __init__(self, s0: ReplState, s1: ReplState):
        self.s0 = s0
        self.s1 = s1

    def __enter__(self):
        return self.exec

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def exec(self, args: list[str], ctx: Context = Context.NULL):
        return Devices.of(self.s1).bash(self.s0, self.s1, args, ctx=ctx)