from adam.commands import extract_options, extract_sequence, extract_trailing_options
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import Color
from adam.utils_context import Context

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

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with extract_options(args, ['-s', '--show']) as (args, verbose):
                    with extract_sequence(args, ['with', 'recipe', '=', 'mpstat']) as (_, recipe_qing):
                        cols = Config().get('processes.columns', 'pod,cpu-metrics,mem')
                        header = Config().get('processes.header', 'POD_NAME,M_CPU(USAGE/LIMIT),MEM/LIMIT')
                        if recipe_qing:
                            cols = Config().get('processes-mpstat.columns', 'pod,cpu,mem')
                            header = Config().get('processes-mpstat.header', 'POD_NAME,Q_CPU/TOTAL,MEM/LIMIT')

                        with cassandra(state) as pods:
                            pods.display_table(cols, header, ctx=Context.new(cmd, backgrounded=backgrounded, show_verbose=verbose))

                        return state

    def completion(self, state: ReplState):
        recipes = ['metrics', 'mpstat']
        return super().completion(state, {'with': {'recipe': {'=': {r: {'-s': {'&': None}, '&': None} for r in recipes}}}, '-s': {'&': None}, '&': None})

    def help(self, state: ReplState):
        return super().help(state, 'show process overview  -s show processing details', args='[with recipe=metrics|mpstat] [-s]')