import time

from adam.apps import Apps
from adam.sso.idp import Idp
from adam.sso.idp_login import IdpLogin
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import duration, tabulize, log2, log_exc

class ShowLogin(Command):
    COMMAND = 'show login'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowLogin, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowLogin.COMMAND

    def required(self):
        return ReplState.NON_L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            login: IdpLogin = None
            with log_exc(True):
                if not(host := Apps.app_host('c3', 'c3', state.namespace)):
                    log2('Cannot locate ingress for app.')
                    return state

                login = Idp.login(host, use_token_from_env=True)
                if login and login.id_token_obj:
                    it = login.id_token_obj
                    lines = [
                        f'email\t{it.email}',
                        f'user\t{it.username}',
                        f'IDP expires in\t{duration(time.time(), it.exp)}',
                        f'IDP Groups\t{",".join(it.groups)}'
                    ]
                    tabulize(lines, separator='\t')

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show SSO login details')