from adam.commands.command import Command
from adam.commands.reaper.utils_reaper import reaper, Reapers
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import convert_seconds, epoch, log2

class ReaperRuns(Command):
    COMMAND = 'reaper show runs'

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

        with self.validate(args, state) as (args, state):
            header = 'ID,START,DURATION,STATE,CLUSTER,KEYSPACE,TABLES,REPAIRED'

            def line(run):
                id = run['id']
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

                return f"{id},{start_time},{duration},{state},{run['cluster_name']},{run['keyspace_name']},{len(run['column_families'])},{run['segments_repaired']}/{run['total_segments']}"

            with reaper(state) as http:
                response = http.get('repair_run?state=RUNNING', params={
                    'cluster_name': 'all',
                    'limit': Config().get('reaper.show-runs-batch', 10)
                })

                if not Reapers.tabulize_runs(state, response):
                # runs = response.json()
                # if runs:
                #     tabulize(sorted([line(run) for run in runs], reverse=True), header=header, separator=",")
                # else:
                    log2('No running runs found.')
                    log2()

                response = http.get('repair_run?state=PAUSED,ABORTED,DONE', params={
                    'cluster_name': 'all',
                    'limit': Config().get('reaper.show-runs-batch', 10)
                })

                if not Reapers.tabulize_runs(state, response):
                # runs = response.json()
                # if runs:
                #     tabulize(sorted([line(run) for run in runs], reverse=True), header=header, separator=",")
                # else:
                    log2('No runs found.')

            return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'show reaper runs')