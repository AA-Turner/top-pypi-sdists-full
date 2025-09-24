import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.cql_utils import parse_cql_desc_tables, run_cql
from adam.config import Config
from adam.pod_exec_result import PodExecResult
from adam.repl_state import ReplState, RequiredState
from adam.utils import log, log2

class AlterTables(Command):
    COMMAND = 'alter tables with'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(AlterTables, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def required(self):
        return RequiredState.CLUSTER

    def command(self):
        return AlterTables.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not args:
            if state.in_repl:
                log2('Please enter gc grace in seconds. e.g. alter gc-grace-seconds 3600')
            else:
                log2('* gc grace second is missing.')
                log2()
                Command.display_help()

            return 'missing-arg'

        args, include_reaper = Command.extract_options(args, '--include-reaper')
        arg_str = ' '.join(args)

        r: list[PodExecResult] = run_cql(state, 'describe tables', show_out=False, on_any=True)
        if not r:
            log2('No pod is available')
            return 'no-pod'

        excludes = [e.strip(' \r\n') for e in Config().get(
            'cql.alter-tables.excludes',
            'system_auth,system_traces,reaper_db,system_distributed,system_views,system,system_schema,system_virtual_schema').split(',')]
        batching = Config().get('cql.alter-tables.batching', True)
        tables = parse_cql_desc_tables(r[0].stdout)
        for k, v in tables.items():
            if k not in excludes or k == 'reaper_db' and include_reaper:
                if batching:
                    # alter table <table_name> with GC_GRACE_SECONDS = <timeout>;
                    cql = ';\n'.join([f'alter table {k}.{t} with {arg_str}' for t in v])
                    try:
                        run_cql(state, cql, [], show_out=Config().is_debug(), on_any=True)
                    except Exception as e:
                        log2(e)
                        continue
                else:
                    for t in v:
                        try:
                            # alter table <table_name> with GC_GRACE_SECONDS = <timeout>;
                            cql = f'alter table {k}.{t} with {arg_str}'
                            run_cql(state, cql, [], show_out=Config().is_debug(), on_any=True)
                        except Exception as e:
                            log2(e)
                            continue

                log2(f'{len(v)} tables altered in {k}.')

        # do not continue to cql route
        return state

    def completion(self, state: ReplState) -> dict[str, any]:
        if state.sts:
            ps = Config().get('cql.alter-tables.gc-grace-periods', '3600,86400,864000,7776000').split(',')
            return super().completion(state, {
                'GC_GRACE_SECONDS': {'=': {p.strip(' \r\n'): {'--include-reaper': None} for p in ps}},
            })

        return {}

    def help(self, _: ReplState) -> str:
        return f'{AlterTables.COMMAND} <param = value> [--include-reaper] \t alter on all tables'