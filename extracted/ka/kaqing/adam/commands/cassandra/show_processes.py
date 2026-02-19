from adam.commands import extract_sequence
from adam.commands.command import Command
from adam.config import Config
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.presentation.table_renderer import renderer

class ShowProcesses(Command):
    COMMAND = 'show processes'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowProcesses, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowProcesses.COMMAND

    def aliases(self):
        return ['sp']

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args, show_out=False) as (args, ctx):
                with extract_sequence(args, ['with', 'recipe', '=', 'mpstat']) as (_, recipe_qing):
                    cols = Config().get('processes.columns', 'short-pod,cpu-metrics,mem')
                    header = Config().get('processes.header', 'POD_NAME,M_CPU(USAGE/LIMIT),MEM/LIMIT')
                    if recipe_qing:
                        cols = Config().get('processes-mpstat.columns', 'short-pod,cpu,mem')
                        header = Config().get('processes-mpstat.header', 'POD_NAME,Q_CPU/TOTAL,MEM/LIMIT')

                    with renderer(state) as pods:
                        pods.display_table(cols, header, find_issues=False, ctx=ctx)

                    return state

    def completion(self, state: ReplState):
        recipes = ['metrics', 'mpstat']
        return super().completion(state, {'with': {'recipe': {'=': {r: None for r in recipes}}}})

    def help(self, state: ReplState):
        return super().help(state, 'show process overview', args='[with recipe=metrics|mpstat]')