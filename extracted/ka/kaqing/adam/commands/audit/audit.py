import click

from adam.commands import extract_trailing_options, validate_args
from adam.commands.audit.completions_l import completions_l
from adam.commands.audit.audit_repair_tables import AuditRepairTables
from adam.commands.audit.audit_run import AuditRun
from adam.commands.audit.show_last10 import ShowLast10
from adam.commands.audit.show_slow10 import ShowSlow10
from adam.commands.audit.show_top10 import ShowTop10
from adam.commands.command import Command
from adam.commands.intermediate_command import IntermediateCommand
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_athena import Athena
from adam.utils_context import Context

class Audit(IntermediateCommand):
    COMMAND = 'audit'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Audit, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)
        self.schema_read = False

    def command(self):
        return Audit.COMMAND

    def required(self):
        return ReplState.L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            r = None
            if len(args) > 0:
                r = self.intermediate_run(cmd, state, args, self.cmd_list(), display_help=False)

            if not r or isinstance(r, str) and r == 'command-missing':
                with extract_trailing_options(args, '&') as (args, backgrounded):
                    with validate_args(args, state, default='select * from audit order by ts desc limit 10') as sql:
                        ctx = Context.new(cmd, show_out=True, backgrounded=backgrounded)
                        ctx.log2(sql)
                        Athena.run_query(sql, ctx=ctx)

            return state

    def completion(self, state: ReplState):
        if state.device != ReplState.L:
            return {}

        return completions_l()

    def cmd_list(self):
        return [AuditRepairTables(), AuditRun(), ShowLast10(), ShowSlow10(), ShowTop10()]

    def help(self, state: ReplState):
        return super().help(state, 'run SQL queries on Athena audit database', command='[audit] [<sql-statements>]')

class AuditCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Audit.COMMAND, Audit().cmd_list(), show_cluster_help=False)