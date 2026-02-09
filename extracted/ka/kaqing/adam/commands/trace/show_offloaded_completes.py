from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.sql.async_executor import AsyncExecutor
from adam.utils_tabulize import tabulize

class ShowOffloadedCompletes(Command):
    COMMAND = 'show offloaded completes'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowOffloadedCompletes, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowOffloadedCompletes.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            pending, processed, first, last = AsyncExecutor.entries_in_queue()
            lines = []
            for k, v in processed.items():
                lines.append(f'{k}\t{v:2.2f}')
            for k in pending:
                lines.append(f'{k}\tpending')
            lines += [
                f'---------------------------',
                f'duration\t{last-first:2.2f}'
            ]

            tabulize(lines,
                     header='key\tduration(in sec)',
                     separator='\t',
                     ctx=self.context())

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show offloaded completes')