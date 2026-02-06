from adam.commands import extract_options, validate_args
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra, cassandra_tables as get_tables
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2, log_exc
from adam.utils_context import Context

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

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--include-reaper') as (args, include_reaper):
                with validate_args(args, state, name='gc grace in seconds') as arg_str:
                    excludes = [e.strip(' \r\n') for e in Config().get(
                        'cql.alter-tables.excludes',
                        'system_auth,system_traces,reaper_db,system_distributed,system_views,system,system_schema,system_virtual_schema').split(',')]
                    batching = Config().get('cql.alter-tables.batching', True)
                    tables = get_tables(state, on_any=True)
                    for k, v in tables.items():
                        if k not in excludes or k == 'reaper_db' and include_reaper:
                            if batching:
                                # alter table <table_name> with GC_GRACE_SECONDS = <timeout>;
                                cql = ';\n'.join([f'alter table {k}.{t} with {arg_str}' for t in v])
                                with log_exc(True):
                                    with cassandra(state) as pods:
                                        pods.cql(cql, on_any=True, ctx=Context.new(cmd, show_out=True))
                                    continue
                            else:
                                for t in v:
                                    with log_exc(True):
                                        # alter table <table_name> with GC_GRACE_SECONDS = <timeout>;
                                        cql = f'alter table {k}.{t} with {arg_str}'
                                        with cassandra(state) as pods:
                                            pods.cql(cql, on_any=True, ctx=Context.new(cmd, show_out=True))
                                        continue

                            log2(f'{len(v)} tables altered in {k}.')

                    # do not continue to cql route
                    return state

    def completion(self, _: ReplState) -> dict[str, any]:
        # auto completion is taken care of by lark completer
        return {}

    def help(self, state: ReplState) -> str:
        return super().help(state, 'alter schema on all tables', args='with <param=value>,... [--include-reaper]')