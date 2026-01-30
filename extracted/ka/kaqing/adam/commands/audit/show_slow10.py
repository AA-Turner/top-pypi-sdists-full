from adam.commands import extract_trailing_options
from adam.commands.audit.utils_show_top10 import run_configured_query
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_context import Context

class ShowSlow10(Command):
    COMMAND = 'show slow'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowSlow10, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowSlow10.COMMAND

    def required(self):
        return ReplState.L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                run_configured_query('audit.queries.slow10', args, ctx=Context.new(cmd, show_out=True, backgrounded=backgrounded))

                return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'show slow <limit> audit lines  <limit> default to 10', args='[limit]')