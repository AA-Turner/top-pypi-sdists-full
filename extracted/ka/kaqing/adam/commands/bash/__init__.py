from adam.commands.bash.utils_bash import BashHandler
from adam.repl_state import ReplState

def bash(s0: ReplState, s1: ReplState):
    return BashHandler(s0, s1)