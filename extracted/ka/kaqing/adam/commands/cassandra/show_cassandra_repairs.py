from adam.commands.command import Command
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.utils_cassandra.pod_service import cassandra

class ShowCassandraRepairs(Command):
    COMMAND = 'show repairs'

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

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with cassandra(state) as pods:
                    return pods.nodetool('repair_admin list', ctx)

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show Cassandra repairs')