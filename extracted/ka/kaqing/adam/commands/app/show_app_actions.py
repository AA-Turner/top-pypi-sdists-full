from adam.app_session import AppSession
from adam.apps import Apps
from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import tabulize, log

class ShowAppActions(Command):
    COMMAND = 'show app actions'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowAppActions, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowAppActions.COMMAND

    def required(self):
        return ReplState.A

    def run(self, cmd: str, state: ReplState):
        if not (args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            actions = []
            for typ in Apps().app_types():
                actions.extend(typ.actions)

            lines = tabulize(actions, lambda a: str(a), header='ACTION,ARGS,DESCRIPTION', separator=',')
            log()

            app_session: AppSession = AppSession.create(state.app_env or 'c3', state.app_app or 'c3')
            endpoint = Config().get('app.console-endpoint', 'https://{host}/{env}/{app}/static/console/index.html')
            endpoint = endpoint.replace('{host}', app_session.host).replace('{env}', app_session.env).replace('{app}', state.app_app or 'c3')
            tabulize([f'CONSOLE:,{endpoint}'], separator=',')

            return lines

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show registered app actions')