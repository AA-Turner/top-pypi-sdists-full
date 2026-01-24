from functools import partial
import threading
import time

from adam.commands.command import Command
from adam.commands.reaper.reaper_forward_session import ReaperForwardSession
from adam.commands.reaper.utils_reaper import Reapers, port_forwarding
from adam.config import Config
from adam.repl_session import ReplSession
from adam.repl_state import ReplState, RequiredState
from adam.utils import tabulize, log2

class ReaperForward(Command):
    COMMAND = 'reaper forward'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperForward, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperForward.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            if not Reapers.pod_name(state):
                return state

            spec = Reapers.reaper_spec(state)
            if state.in_repl:
                if ReaperForwardSession.is_forwarding:
                    log2("Another port-forward is already running.")

                    return "already-running"

                # make it a daemon to exit with a Ctrl-D
                thread = threading.Thread(target=self.loop, args=(state,), daemon=True)
                thread.start()

                while not ReaperForwardSession.is_forwarding:
                    time.sleep(1)

                d = {
                    'reaper-ui': spec["web-uri"],
                    'reaper-username': spec["username"],
                    'reaper-password': spec["password"]
                }
                log2()
                tabulize(d.items(), lambda a: f'{a[0]},{a[1]}', separator=',')

                for k, v in d.items():
                    ReplSession().prompt_session.history.append_string(f'cp {k}')
                log2()
                log2(f'Use <Up> arrow key to copy the values to clipboard.')
            else:
                try:
                    log2(f'Click: {spec["web-uri"]}')
                    log2(f'username: {spec["username"]}')
                    log2(f'password: {spec["password"]}')
                    log2()
                    log2(f"Press Ctrl+C to break.")

                    time.sleep(Config().get('reaper.port-forward.timeout', 3600 * 24))
                except KeyboardInterrupt:
                    pass

            return state

    def loop(self, state: ReplState):
        with port_forwarding(state, Reapers.local_port(), partial(Reapers.svc_or_pod, state), Reapers.target_port()):
            ReaperForwardSession.is_forwarding = True
            try:
                while not ReaperForwardSession.stopping.is_set():
                    time.sleep(1)
            finally:
                ReaperForwardSession.stopping.clear()
                ReaperForwardSession.is_forwarding = False

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'port-forward to reaper')