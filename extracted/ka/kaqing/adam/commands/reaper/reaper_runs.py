from adam.commands.command import Command
from adam.commands.reaper.utils_reaper import reaper, Reapers
from adam.config import Config
from adam.repl_state import ReplState, RequiredState

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
            ctx = self.context()
            with reaper(state) as http:
                response = http.get('repair_run?state=RUNNING', params={
                    'cluster_name': 'all',
                    'limit': Config().get('reaper.show-runs-batch', 10)
                })

                if not Reapers.tabulize_runs(state, response, ctx=ctx):
                    ctx.log2('No running runs found.')
                    ctx.log2()

                response = http.get('repair_run?state=PAUSED,ABORTED,DONE', params={
                    'cluster_name': 'all',
                    'limit': Config().get('reaper.show-runs-batch', 10)
                })

                if not Reapers.tabulize_runs(state, response, ctx=ctx):
                    ctx.log2('No runs found.')

            return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'show reaper runs')