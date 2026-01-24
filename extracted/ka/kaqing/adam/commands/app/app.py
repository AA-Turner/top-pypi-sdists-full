from adam.commands import app, extract_options
from adam.commands.command import Command
from adam.repl_state import ReplState, RequiredState

class App(Command):
    COMMAND = 'app'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(App, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return App.COMMAND

    def required(self):
        return RequiredState.APP_APP

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--force') as (args, forced):
                with app(state) as http:
                    http.post(args, forced=forced)

                return state

    def completion(self, _: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, "post app action  use 'show app actions' for registered actions  --force refresh session", command='<AppType>.<AppAction>', args='<args> [--force]')