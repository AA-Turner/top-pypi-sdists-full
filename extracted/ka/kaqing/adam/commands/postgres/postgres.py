import click

from adam.commands import extract_trailing_options, validate_args
from adam.commands.command import Command
from adam.commands.intermediate_command import IntermediateCommand
from adam.commands.postgres.postgres_databases import pg_path
from adam.commands.postgres.completions_p import psql0_completions, completions_p
from adam.commands.postgres.utils_postgres import pg_table_names, postgres
from adam.utils_context import Context
from .postgres_ls import PostgresLs
from .postgres_preview import PostgresPreview
from adam.repl_state import ReplState
from adam.utils import ExecResult, log, log2, log_timing

class Postgres(IntermediateCommand):
    COMMAND = 'pg'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Postgres, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Postgres.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with validate_args(args, state, name='SQL statement') as sql:
                    if not state.pg_path:
                        if state.in_repl:
                            log2('Enter "use <pg-name>" first.')
                        else:
                            log2('* pg-name is missing.')

                        return state

                    r: ExecResult = None
                    with postgres(state) as pod:
                        r = pod.sql(args, ctx=Context.new(cmd, backgrounded, show_out=True, history=Context.PODS))

                    if not backgrounded and r:
                        log(r.stdout)
                        log2(r.stderr)

                    return state

    def cmd_list(self):
        return [PostgresLs(), PostgresPreview(), PostgresPg()]

    def completion(self, state: ReplState):
        if state.device != state.P:
            return {}

        with pg_path(state) as (host, database):
            if database:
                if pg_table_names(state):
                    with log_timing('psql_completions'):
                        return completions_p(state)
            elif host:
                return psql0_completions(state)

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'run queries on Postgres databases', command='[pg] <sql-statements>')

class PostgresCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Postgres.COMMAND, Postgres().cmd_list(), show_cluster_help=True)
        log('PG-Name:  Kubernetes secret for Postgres credentials')
        log('          e.g. stgawsscpsr-c3-c3-k8spg-cs-001')
        log('Database: Postgres database name within a host')
        log('          e.g. stgawsscpsr_c3_c3')

# No action body, only for a help entry and auto-completion
class PostgresPg(Command):
    COMMAND = 'pg'

    def command(self):
        return PostgresPg.COMMAND