from adam.commands.command import Command
from adam.commands.devices.devices import device
from adam.directories import Directories
from adam.utils_concurrent import parallelize
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import strip_pod_name
from adam.utils_tabulize import tabulize

class FindFiles(Command):
    COMMAND = 'find file'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(FindFiles, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return FindFiles.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                if state.pod:
                    pod_names = [state.pod]
                else:
                    pod_names = device(state).pod_names(state)

                def find_files(pod: str):
                    files = PodFiles.find_files(pod, 'cassandra', state.namespace, f'{Directories.export_csv_dir()}/*', remote=True, ctx=ctx.copy(show_out=False))
                    files.extend(PodFiles.find_files(pod, 'cassandra', state.namespace, f'{Directories.remote_q_dir()}/*', remote=True, ctx=ctx.copy(show_out=False)))

                    return pod, files

                with parallelize(pod_names) as exec:
                    logs = []

                    for pod, ls in exec.map(find_files):
                        for i, l in enumerate(ls):
                            logs.append(f'{"" if i else strip_pod_name(pod)}\t{l}')

                    tabulize(logs, separator='\t', ctx=ctx)

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, pods=device(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'find qing-related files from pods')