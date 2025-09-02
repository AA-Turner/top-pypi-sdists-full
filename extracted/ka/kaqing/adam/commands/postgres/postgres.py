import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper
from .postgres_ls import PostgresLs
from .postgres_preview import PostgresPreview
from .postgres_session import PostgresSession
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log, log2

class Postgres(Command):
    COMMAND = 'pg'
    reaper_login = None

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

        state, args = self.apply_state(args, state)

        if state.in_repl:
            if not args:
                log2('Please use SQL statement. e.g. pg \l')

                return 'command-missing'
            else:
                self.run_sql(state, args)
        else:
            if not args:
                log2('* Command or SQL statements is missing.')
                Command.display_help()

                return 'command-missing'
            else:
                # head with the Chain of Responsibility pattern
                cmds = Command.chain(Postgres.cmd_list())
                if not cmds.run(cmd, state) :
                    if not args:
                        log2('* Command or SQL statements is missing.')
                        Command.display_help()

                        return 'command-missing'
                    else:
                        self.run_sql(state, args)

        return state

    def cmd_list():
        return [PostgresLs(), PostgresPreview()]

    def run_sql(self, state: ReplState, args: list[str]):
        if not state.pg_path:
            if state.in_repl:
                log2('Enter "use <pg-name>" first.')
            else:
                log2('* pg-name is missing.')

            return state

        PostgresSession(state.namespace, state.pg_path).run_sql(' '.join(args))

    def completion(self, state: ReplState):
        leaf = {}
        if PostgresSession(state.namespace, state.pg_path).db:
            leaf = {
                '\h': None,
                '\d': None,
                '\dt': None,
                '\du': None,
                'delete': {'from': None},
                'insert': {'into': None},
                'select': None,
                'update': None,
            }
        elif state.pg_path:
            leaf = {
                '\h': None,
                '\l': None,
            }

        if state.pg_path:
            return super().completion(state, leaf) | leaf
        else:
            return {}

    def help(self, _: ReplState):
        return f'[{Postgres.COMMAND}] <sql-statements>\t run psql with queries'

class PostgresCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Sub-Commands:')

        log(lines_to_tabular([c.help(ReplState()).replace(f'{Postgres.COMMAND} ', '  ', 1) for c in Postgres.cmd_list()], separator='\t'))
        log()
        ClusterCommandHelper.cluster_help()
        log('PG-Name:  Kubernetes secret for Postgres credentials')
        log('          e.g. stgawsscpsr-c3-c3-k8spg-cs-001')
        log('Database: Postgres database name within a host')
        log('          e.g. stgawsscpsr_c3_c3')