from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra
from adam.repl_state import ReplState, RequiredState
from adam.utils_context import Context

class ShowCassandraVersion(Command):
    COMMAND = 'show cassandra version'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowCassandraVersion, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowCassandraVersion.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (_, state):
            with cassandra(state) as pods:
                return pods.cql('show version', on_any=True, ctx=Context.new(show_out=True))

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show Cassandra version')