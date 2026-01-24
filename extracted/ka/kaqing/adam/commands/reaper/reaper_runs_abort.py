from adam.commands.command import Command
from adam.commands.reaper.utils_reaper import reaper
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class ReaperRunsAbort(Command):
    COMMAND = 'reaper abort runs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperRunsAbort, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperRunsAbort.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with reaper(state) as http:
                # PAUSED, RUNNING, ABORTED
                aborted = 0

                while True == True:
                    response = http.get('repair_run?state=RUNNING', params={
                        'cluster_name': 'all',
                        'limit': Config().get('reaper.abort-runs-batch', 10)
                    })
                    if not response:
                        break

                    runs = response.json()
                    if not runs:
                        break

                    for run in runs:
                        run_id = run['id']
                        # PUT /repair_run/{id}/state/{state}
                        http.put(f'repair_run/{run_id}/state/ABORTED')
                        aborted += 1

                if aborted:
                    log2(f'Aborted {aborted} runs in total.')
                else:
                    log2('No running repair runs found.')

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'abort all running reaper runs')