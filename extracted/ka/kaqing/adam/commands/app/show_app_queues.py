from adam.commands import app, extract_options
from adam.commands.command import Command
from adam.repl_state import ReplState, RequiredState

class ShowAppQueues(Command):
    COMMAND = 'show app queues'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowAppQueues, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowAppQueues.COMMAND

    def required(self):
        return RequiredState.APP_APP

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (_, state):
            with extract_options(args, '--force') as (args, forced):
                with app(state) as http:
                    http.post(['InvalidationQueue.countAll'], forced=forced, ctx=self.context())

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {'--force': None})

    def help(self, state: ReplState):
        return super().help(state, 'show invalidation queue counts  --force refresh session', args='[--force]')