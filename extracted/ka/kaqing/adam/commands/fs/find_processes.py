from adam.commands import extract_options, validate_args
from adam.commands.command import Command
from adam.commands.fs.utils_fs import ProcessInfo, find_pids_for_cluster
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class FindProcesses(Command):
    COMMAND = 'find processes'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(FindProcesses, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return FindProcesses.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '-kill') as (args, kill):
                with validate_args(args, state, name='words to look for', separator=' ') as keywords:
                    processes, pids = self._find_processes(state, keywords, kill=kill)

                    if kill:
                        log2(f'{len(pids)} processes were terminated with keywords: {",".join(keywords)}.')
                        processes, pids = self._find_processes(state, keywords, kill=kill)

                    ProcessInfo.tabulize(processes)
                    log2()
                    if pids:
                        log2(f'PIDS with {",".join(keywords)}: {",".join(pids)}')
                    else:
                        log2(f'No processes were found with keywords: {",".join(keywords)}.')

                    return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'find processes with words  --kill kill matching processes', args='word... [-kill]')

    def _find_processes(self, state: ReplState, keywords: list[str], kill=False):
        processes = find_pids_for_cluster(state, keywords, kill=kill)

        pids = []
        for p in processes:
            pids.append(f'{p.pid}@{p.pod}')

        return processes, pids