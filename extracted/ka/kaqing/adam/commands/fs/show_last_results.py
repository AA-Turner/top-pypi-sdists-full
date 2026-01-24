from adam.commands.fs.utils_fs import show_last_results, show_last_local_results
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log_to_pods

class ShowLastResults(Command):
    COMMAND = 'show last results'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowLastResults, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowLastResults.COMMAND

    def aliases(self):
        return [':?']

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        if log_to_pods():
            show_last_results(state)
        else:
            show_last_local_results(state)

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show results of last command')