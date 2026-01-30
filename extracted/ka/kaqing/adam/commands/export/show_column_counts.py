from adam.commands import extract_trailing_options, validate_args
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra_table_names
from adam.commands.export.export_databases import ExportDatabases, export_db
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils_async_job import AsyncJobs
from adam.utils_context import Context

class ShowColumnCounts(Command):
    COMMAND = 'show column counts on'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowColumnCounts, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowColumnCounts.COMMAND

    def required(self):
        return RequiredState.EXPORT_DB

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with validate_args(args, state, name='SQL statement') as table:
                    with export_db(state) as dbs:
                        query = Config().get(f'export.column_counts_query', 'select id, count(id) as columns from {table} group by id')
                        query = query.replace('{table}', table)
                        dbs.sql(query, state.export_session, Context.new(backgrounded=backgrounded))

            return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {t: None for t in ExportDatabases.table_names(state.export_session)}, auto_key='x.tables')

    def help(self, state: ReplState):
        return super().help(state, 'show column count per id', args='<export-table-name>')