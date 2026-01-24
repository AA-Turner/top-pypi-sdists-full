import os
import signal

from adam.app_session import AppSession
from adam.apps import Apps
from adam.commands import extract_options
from adam.config import Config
from adam.sso.idp import Idp
from adam.sso.idp_login import IdpLogin
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log, log2, log_exc

class Login(Command):
    COMMAND = 'login'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Login, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Login.COMMAND

    def required(self):
        return ReplState.NON_L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        def custom_handler(signum, frame):
            AppSession.ctrl_c_entered = True

        signal.signal(signal.SIGINT, custom_handler)

        with self.validate(args, state) as (args, state):
            with extract_options(args, 'd') as (args, debug):
                if debug:
                    Config().set('debug', True)

                username: str = os.getenv('USERNAME')
                if len(args) > 0:
                    username = args[0]

                login: IdpLogin = None
                with log_exc(True):
                    if not(host := Apps.app_host('c3', 'c3', state.namespace)):
                        log2('Cannot locate ingress for app.')
                        return state

                    if not (login := Idp.login(host, username=username, use_token_from_env=False)):
                        log2('Invalid username/password. Please try again.')

                log(f'IDP_TOKEN={login.ser() if login else ""}')

                return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'SSO login')