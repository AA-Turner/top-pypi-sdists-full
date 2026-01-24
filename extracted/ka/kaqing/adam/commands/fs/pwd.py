from adam.app_session import AppSession
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState
from adam.utils import tabulize, log, log_exc

class Pwd(Command):
    COMMAND = 'pwd'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Pwd, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Pwd.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (_, state):
            host = "unknown"
            with log_exc():
                app_session: AppSession = AppSession.create('c3', 'c3')
                host = app_session.host

            tabulize([device.pwd(state) for device in Devices.all()] + [
                f'',
                f'HOST\t{host}',
                f'NAMESPACE\t{state.namespace if state.namespace else "/"}',
            ], header='DEVICE\tLOCATION', separator='\t')
            log()

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'print current working directories')