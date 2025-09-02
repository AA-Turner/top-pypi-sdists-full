from adam.commands.command import Command
from adam.k8s_utils.cassandra_clusters import CassandraClusters
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.repl_state import ReplState, RequiredState

class ShowRepairs(Command):
    COMMAND = 'show cassandra repairs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowRepairs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowRepairs.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, _ = state.apply_args(args)
        if not self.validate_state(state):
            return state

        user, pw = state.user_pass()
        command = f"nodetool -u {user} -pw {pw} repair_admin list"

        if state.pod:
            return CassandraNodes.exec(state.pod, state.namespace, command)
        else:
            return CassandraClusters.exec(state.sts, state.namespace, command, action='nodetool')

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ShowRepairs.COMMAND}\t show Cassandra repairs'