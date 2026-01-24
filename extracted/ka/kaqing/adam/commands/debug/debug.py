from adam.commands.command import Command
from adam.commands.debug.debug_completes import DebugCompletes
from adam.commands.debug.debug_timings import DebugTimings
from adam.commands.intermediate_command import IntermediateCommand

class Debug(IntermediateCommand):
    COMMAND = 'debug'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Debug, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Debug.COMMAND

    def cmd_list(self):
        return [DebugTimings(), DebugCompletes()]