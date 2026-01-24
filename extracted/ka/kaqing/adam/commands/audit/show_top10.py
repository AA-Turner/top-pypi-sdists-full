from adam.commands.audit.utils_show_top10 import run_configured_query
from adam.commands.command import Command
from adam.repl_state import ReplState

class ShowTop10(Command):
    COMMAND = 'show top'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowTop10, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowTop10.COMMAND

    def required(self):
        return ReplState.L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            run_configured_query('audit.queries.top10', args)

            return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'show top <limit> audit lines  <limit> default to 10', args='[limit]')