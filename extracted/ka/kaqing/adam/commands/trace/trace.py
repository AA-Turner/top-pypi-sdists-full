from adam.commands.command import Command
from adam.commands.trace.trace_completes import TraceCompletes
from adam.commands.trace.trace_timings import TraceTimings
from adam.commands.intermediate_command import IntermediateCommand

class Trace(IntermediateCommand):
    COMMAND = 'trace'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Trace, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Trace.COMMAND

    def cmd_list(self):
        return [TraceTimings(), TraceCompletes()]