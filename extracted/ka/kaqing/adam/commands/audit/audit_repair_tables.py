import time

from adam.commands import validate_args
from adam.commands.command import Command
from adam.config import Config
from adam.rdbms.utils_athena import Athena
from adam.utils_context import NULL
from adam.utils_log import log2
from adam.commands.audit.utils_audits import AuditMeta, Audits, audit
from adam.utils_repl.repl_state import ReplState

class AuditRepairTables(Command):
    COMMAND = 'audit repair'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(AuditRepairTables, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)
        self.auto_repaired = False

    def command(self):
        return AuditRepairTables.COMMAND

    def required(self):
        return ReplState.L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with validate_args(args, state, default=Config().get('audit.athena.repair-partition-tables', 'audit').split(',')) as tables:
                    meta = Audits.get_meta()
                    self.repair(tables, meta, ctx=ctx)

                return state

    def completion(self, state: ReplState):
        # trigger auto repair if on l: drive
        if state.device == ReplState.L:
            if not self.auto_repaired:
                if hours := Config().get('audit.athena.auto-repair.elapsed_hours', 12):
                    with audit() as submit:
                        submit(lambda: self.auto_repair(hours))

        return {}

    def auto_repair(self, hours: int):
        self.auto_repaired = True

        meta: AuditMeta = Audits.get_meta()
        if meta.partitions_last_checked + hours * 60 * 60 < time.time():
            tables = Config().get('audit.athena.repair-partition-tables', 'audit').split(',')
            self.repair(tables, meta, show_sql=True)
            log2(f'Audit tables have been auto-repaired.')

    def repair(self, tables: list[str], meta: AuditMeta, show_sql = False, ctx = NULL):
        with audit() as submit:
            for table in tables:
                if show_sql:
                    ctx.log(f'MSCK REPAIR TABLE {table}')

                submit(Athena.query, f'MSCK REPAIR TABLE {table}', None,)
            submit(Audits.put_meta, Audits.PARTITIONS_ADDED, meta,)

    def help(self, state: ReplState):
        return super().help(state, 'run MSCK REPAIR to discover new partitions')