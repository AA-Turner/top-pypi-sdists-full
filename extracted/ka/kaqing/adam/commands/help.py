from adam.commands.command import Command
from adam.repl_commands import ReplCommands
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log

class Help(Command):
    COMMAND = 'help'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Help, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Help.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        def section(cmds : list[ReplCommands]):
            return [f'  {c.help(state)}' for c in cmds if c.help(state)]

        lines = []
        lines.append('NAVIGATION')
        lines.append('  a: | c: | p:\t switch to another operational device: App, Cassandra or Postgres')
        lines.extend(section(ReplCommands.navigation()))
        lines.append('CHECK CASSANDRA')
        lines.extend(section(ReplCommands.cassandra_check()))
        lines.append('CASSANDRA OPERATIONS')
        lines.extend(section(ReplCommands.cassandra_ops()))
        lines.append('TOOLS')
        lines.extend(section(ReplCommands.tools()))
        lines.append('APP')
        lines.extend(section(ReplCommands.app()))
        lines.append('')
        lines.extend(section(ReplCommands.exit()))

        log(lines_to_tabular(lines, separator='\t'))

        return lines

    def completion(self, _: ReplState):
        return {Help.COMMAND: None}

    def help(self, _: ReplState):
        return None