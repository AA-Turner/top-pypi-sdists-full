from adam.commands import extract_trailing_options
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra
from adam.repl_state import ReplState, RequiredState
from adam.utils_context import Context

class ShowCassandraRepairs(Command):
    COMMAND = 'show cassandra repairs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowCassandraRepairs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowCassandraRepairs.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, background):
                with cassandra(state) as pods:
                    return pods.nodetool('repair_admin list', Context.new(cmd, background=background))

    def completion(self, state: ReplState):
        return super().completion(state, {'&': None})

    def help(self, state: ReplState):
        return super().help(state, 'show Cassandra repairs', args='[&]')