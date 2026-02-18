from adam.commands import extract_options
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra_keyspaces
from adam.config import Config
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.utils_log import log_exc
from adam.utils_cassandra.pod_service import cassandra

class ShowGcGrace(Command):
    COMMAND = 'show gc-grace'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowGcGrace, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def required(self):
        return RequiredState.CLUSTER

    def command(self):
        return ShowGcGrace.COMMAND

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with extract_options(args, '--reaper') as (args, include_reaper):
                        excludes = [e.strip(' \r\n') for e in Config().get(
                            'cql.alter-tables.excludes',
                            'system_auth,system_traces,reaper_db,system_distributed,system_views,system,system_schema,system_virtual_schema').split(',')]
                        keyspaces = [ks for ks in cassandra_keyspaces(state, on_any=True) if ks not in excludes]
                        if not include_reaper and 'reaper_db' in keyspaces:
                            keyspaces.remove('reaper_db')

                        cql = "SELECT table_name, gc_grace_seconds FROM system_schema.tables WHERE keyspace_name in ('" + "','".join(keyspaces) + "')"
                        with log_exc(True):
                            with cassandra(state) as pods:
                                pods.cql(cql, on_any=True, ctx=ctx)

                        return state

    def completion(self, state: ReplState) -> dict[str, any]:
        return super().completion(state)

    def help(self, state: ReplState) -> str:
        return super().help(state, 'show gc grace in seconds  --reaper include reaper', args='[--reaper]')