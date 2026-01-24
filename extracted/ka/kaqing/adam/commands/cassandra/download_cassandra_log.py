from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.config import Config
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils import log2
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.repl_state import ReplState, RequiredState
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods

class DownloadCassandraLog(Command):
    COMMAND = 'download cassandra log'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DownloadCassandraLog, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DownloadCassandraLog.COMMAND

    def required(self):
        return RequiredState.POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            path = Config().get('logs.path', '/c3/cassandra/logs/system.log')
            r: PodExecResult = CassandraNodes.exec(state.pod, state.namespace, f'cat {path}', backgrounded=True, history=False)

            to_file = PodFiles.download_file(state.pod, 'cassandra', state.namespace, path)
            log2(f'Downloaded to {to_file}.')

            return r

    def completion(self, state: ReplState):
        return super().completion(state, pods=Devices.of(state).pods(state, '-'), auto='jit')

    def help(self, state: ReplState):
        return super().help(state, 'download cassandra system log')