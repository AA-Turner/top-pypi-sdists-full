import requests

from adam.commands.command import Command
from .reaper_session import ReaperSession
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import convert_seconds, epoch, lines_to_tabular, log, log2

class ReaperRuns(Command):
    COMMAND = 'reaper show runs'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperRuns, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperRuns.COMMAND

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

        self.show_runs(state, reaper)

        return state

    def show_runs(self, state: ReplState, reaper: ReaperSession):
        def body(uri: str, headers: dict[str, str]):
            return requests.get(uri, headers=headers, params={
                'cluster_name': 'all',
                'limit': Config().get('reaper.show-runs-batch', 10)
            })

        def line(run):
            state = run['state']
            start_time = run['start_time']
            end_time = run['end_time']
            duration = '-'
            if state == 'DONE' and end_time:
                hours, minutes, seconds = convert_seconds(epoch(end_time) - epoch(start_time))
                if hours:
                    duration = f"{hours:2d}h {minutes:2d}m {seconds:2d}s"
                elif minutes:
                    duration = f"{minutes:2d}m {seconds:2d}s"
                else:
                    duration = f"{seconds:2d}s"

            return f"{start_time},{duration},{state},{run['cluster_name']},{run['keyspace_name']},{len(run['column_families'])},{run['segments_repaired']}/{run['total_segments']}"

        # PAUSED, RUNNING, ABORTED
        response = reaper.port_forwarded(state, 'repair_run?state=RUNNING', body, method='GET')
        if not response:
            return

        header = 'Start,Duration,State,Cluster,Keyspace,Tables,Repaired'

        runs = response.json()
        if runs:
            log(lines_to_tabular(sorted([line(run) for run in runs], reverse=True), header, separator=","))
        else:
            log2('No running runs found.')
            log2()

        response = reaper.port_forwarded(state, 'repair_run?state=PAUSED,ABORTED,DONE', body, method='GET')
        if not response:
            return

        runs = response.json()
        if runs:
            log(lines_to_tabular(sorted([line(run) for run in runs], reverse=True), header, separator=","))
        else:
            log2('No runs found.')

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperRuns.COMMAND}\t show reaper runs'