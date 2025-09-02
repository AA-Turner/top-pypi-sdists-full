import requests

from adam.commands.command import Command
from .reaper_session import ReaperSession
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class ReaperRunsAbort(Command):
    COMMAND = 'reaper abort runs'
    reaper_login = None

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

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not(reaper := ReaperSession.create(state)):
            return state

        self.stop_runs(state, reaper)

        return state

    def stop_runs(self, state: ReplState, reaper: ReaperSession):
        def body_list(uri: str, headers: dict[str, str]):
            return requests.get(uri, headers=headers, params={
                'cluster_name': 'all',
                'limit': Config().get('reaper.abort-runs-batch', 10)
            })

        def body_abort(uri: str, headers: dict[str, str]):
            return requests.put(uri, headers=headers)

        # PAUSED, RUNNING, ABORTED
        aborted = 0
        while True == True:
            response = reaper.port_forwarded(state, 'repair_run?state=RUNNING', body_list, method='GET')
            if not response:
                break

            runs = response.json()
            if not runs:
                break

            for run in runs:
                run_id = run['id']
                # PUT /repair_run/{id}/state/{state}
                reaper.port_forwarded(state, f'repair_run/{run_id}/state/ABORTED', body_abort, method='PUT')
                log2(f'Aborted {len(runs)} runs.')
                aborted += 1

        if aborted:
            log2(f'Aborted {aborted} runs in total.')
        else:
            log2('No running repair runs found.')

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperRunsAbort.COMMAND}\t abort all running reaper runs'