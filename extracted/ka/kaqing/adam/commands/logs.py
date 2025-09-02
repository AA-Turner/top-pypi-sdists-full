from adam.commands.command import Command
from adam.config import Config
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.repl_state import ReplState, RequiredState

class Logs(Command):
    COMMAND = 'logs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Logs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Logs.COMMAND

    def required(self):
        return RequiredState.POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        path = Config().get('logs.path', '/c3/cassandra/logs/system.log')
        return CassandraNodes.exec(state.pod, state.namespace, f'cat {path}')

    def completion(self, _: ReplState):
        return {}

    def help(self, _: ReplState):
        return f'{Logs.COMMAND}\t show cassandra system log'