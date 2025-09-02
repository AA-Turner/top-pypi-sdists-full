import time
import traceback

from adam.apps import Apps
from adam.config import Config
from adam.sso.idp import Idp
from adam.sso.idp_login import IdpLogin
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import duration, lines_to_tabular, log, log2

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

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)

        login: IdpLogin = None
        try:
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
                log(lines_to_tabular(lines, separator='\t'))
        except Exception as e:
            log2(e)
            if Config().is_debug():
                log2(traceback.format_exc())

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{ShowLogin.COMMAND}\t show login details'