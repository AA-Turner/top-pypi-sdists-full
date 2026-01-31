from adam.commands.bash.bash_completer import BashCompleter
from adam.commands.command import Command
from adam.commands.devices.device import Device
from adam.commands.postgres.postgres_databases import PostgresDatabases, pg_path
from adam.commands.postgres.utils_postgres import pg_database_names, pg_table_names, postgres
from adam.repl_state import ReplState
from adam.utils import wait_log
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

class DevicePostgres(Command, Device):
    COMMAND = f'{ReplState.P}:'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DevicePostgres, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DevicePostgres.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        state.device = ReplState.P

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'move to Postgres Operations device')

    def pod(self, state: ReplState) -> str:
        pod, _ = PostgresDatabases.pod_and_container(state.namespace)
        return pod

    def pod_names(self, state: ReplState) -> list[str]:
        return [self.pod(state)]

    def default_container(self, state: ReplState) -> str:
        _, container = PostgresDatabases.pod_and_container(state.namespace)
        return container

    def ls(self, cmd: str, state: ReplState, ctx: Context = Context.NULL):
        if state.pod_targetted:
            self.bash(state, state, ['ls'])
            return

        with pg_path(state) as (host, database):
            if database:
                tabulize(pg_table_names(state),
                         header='NAME',
                         separator=',',
                         ctx=ctx.copy(show_out=True))
            elif host:
                tabulize(pg_database_names(state),
                         header='DATABASE',
                         separator=',',
                         ctx=ctx.copy(show_out=True))
            else:
                self.show_pg_hosts(state, ctx=ctx)

    def show_pg_hosts(self, state: ReplState, ctx: Context = Context.NULL):
        if state.namespace:
            tabulize(PostgresDatabases.hosts(state),
                     lambda p: f'{p.host},{p.endpoint()}:{p.port()},{p.username()},{p.password()}',
                     header='NAME,ENDPOINT,USERNAME,PASSWORD',
                     separator=',',
                     ctx=ctx.copy(show_out=True))
        else:
            tabulize(PostgresDatabases.hosts(state),
                     lambda p: f'{p.host},{p.namespace},{p.endpoint()}:{p.port()},{p.username()},{p.password()}',
                     header='NAME,NAMESPACE,ENDPOINT,USERNAME,PASSWORD',
                     separator=',',
                     ctx=ctx.copy(show_out=True))

    def cd(self, dir: str, state: ReplState):
        if dir == '':
            state.pg_path = None
            return

        with pg_path(state) as (host, database):
            if dir == '..':
                if database:
                    database = None
                else:
                    host = None
            else:
                tks = dir.split('@')
                if not host:
                    host = tks[0]
                else:
                    database = tks[0]

                if len(tks) > 1:
                    state.namespace = tks[1]

            if database:
                state.pg_path = f'{host}/{database}'
            else:
                state.pg_path = host

    def cd_completion(self, cmd: str, state: ReplState, default: dict = {}):
        return {cmd: {d: None for d in self.direct_dirs(cmd, state, default=default)}}

    def direct_dirs(self, cmd: str, state: ReplState, default: dict = {}) -> list[str]:
        with pg_path(state) as (host, database):
            if database:
                return ['..']
            elif host:
                return ['..'] + [p for p in pg_database_names(state)]
            else:
                return [p for p in PostgresDatabases.host_names(state.namespace)]

    def pwd(self, state: ReplState):
        words = []

        with pg_path(state) as (host, database):
            if host:
                words.append(f'host/{host}')
            if database:
                words.append(f'database/{database}')

            return '\t'.join([f'{ReplState.P}:>'] + (words if words else ['/']))

    def try_fallback_action(self, chain: Command, state: ReplState, cmd: str):
        with pg_path(state) as (_, database):
            if not database:
                database = PostgresDatabases.default_db()

            if database:
                return True, chain.run(f'pg {cmd}', state)

        return False, None

    def enter(self, _: ReplState):
        wait_log('Inspecting postgres database instances...')

    def show_tables(self, state: ReplState, ctx: Context = Context.NULL):
        tabulize(PostgresDatabases.tables(state, default_schema=True),
                 lambda d: d['name'],
                 separator=',',
                 ctx=ctx.copy(show_out=True))

    def show_table_preview(self, state: ReplState, table: str, rows: int, ctx: Context = Context.NULL):
        PostgresDatabases.run_sql(state, f'select * from {table} limit {rows}', ctx=ctx)

    # def bash(self, s0: ReplState, s1: ReplState, args: list[str], ctx: Context = Context.NULL):
        # pod, container = PostgresDatabases.pod_and_container(s1.namespace)
        # log2(f'Running on {pod}(container:{container})...')

        # return super().bash(s0, s1, args, ctx=ctx)

    def bash_target_changed(self, s0: ReplState, s1: ReplState):
        return s0.pg_path != s1.pg_path

    def exec_no_dir(self, command: str, state: ReplState, ctx: Context = Context.NULL):
        with postgres(state) as pod:
            return pod.exec(command, ctx.copy(show_out=True, show_verbose=True))

    def exec_with_dir(self, command: str, session_just_created: bool, state: ReplState, ctx: Context = Context.NULL):
        with postgres(state) as pod:
            return pod.exec(command, ctx=ctx.copy(show_out=not session_just_created, show_verbose=not session_just_created))

    def bash_completion(self, cmd: str, state: ReplState, default: dict = {}):
        return {cmd: BashCompleter(lambda: [])}