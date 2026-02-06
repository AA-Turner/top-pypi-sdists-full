from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.config import Config
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods

class DownloadFile(Command):
    COMMAND = 'download file'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DownloadFile, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DownloadFile.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='file'):
                to_file = PodFiles.download_file(Devices.of(state).pod(state),
                                             Devices.of(state).default_container(state),
                                             state.namespace,
                                             args[0],
                                             args[1] if len(args) > 1 else None)
                log2(f'Downloaded to {to_file}.')

                return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {f: None for f in Devices.of(state).files(state)}, pods=Devices.of(state).pods(state, '-'), auto='jit')

    def help(self, state: ReplState):
        return super().help(state, 'download file from pod', args='<from-file> [to-file]')