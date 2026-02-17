from adam.commands.command import Command
from adam.commands.command_filter import CommandFilter
from adam.utils_repl.repl_commands import ReplCommands
from adam.utils_repl.repl_state import ReplState
from adam.utils_tabulize import tabulize

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

        with self.context() as (_, ctx):
            def section(cmds : list[Command]):
                sorted_cmds = sorted(cmds, key=lambda cmd: cmd.command())
                return [f'  {c.help(state)}' for c in sorted_cmds if c.help(state)]

            def filters(cmds : list[CommandFilter]):
                sorted_cmds = sorted(cmds, key=lambda cmd: cmd.command())
                return [f'  {c.help(state)}' for c in sorted_cmds if c.help(state)]

            lines = []
            lines.append('NAVIGATION\tALIAS')
            lines.append('  a: | c: | l: | p: | x:\t\tswitch to another operational device: App, Cassandra, Audit, Postgres or Export')
            lines.extend(section(ReplCommands.navigation()))
            lines.append('CASSANDRA')
            lines.extend(section(ReplCommands.cassandra_ops()))
            lines.append('POSTGRES')
            lines.extend(section(ReplCommands.postgres_ops()))
            lines.append('APP')
            lines.extend(section(ReplCommands.app_ops()))
            lines.append('EXPORT DB')
            lines.extend(section(ReplCommands.export_ops()))
            lines.append('AUDIT')
            lines.extend(section(ReplCommands.audit_ops()))
            lines.append('TOOLS')
            lines.extend(section(ReplCommands.tools()))
            lines.append('COMMAND FILTERS')
            lines.extend(filters(ReplCommands.filters()))
            lines.append('')
            lines.extend(section(ReplCommands.exit()))

            tabulize(lines, separator='\t', ctx=ctx)

            return lines

    def completion(self, _: ReplState):
        return {Help.COMMAND: None}

    def help(self, state: ReplState):
        return None