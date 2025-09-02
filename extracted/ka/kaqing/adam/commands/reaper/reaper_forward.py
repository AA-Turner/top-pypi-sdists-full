import threading
import time

from adam.commands.command import Command
from .reaper_session import ReaperSession
from adam.config import Config
from adam.repl_session import ReplSession
from adam.repl_state import ReplState, RequiredState
from adam.utils import lines_to_tabular, log2

class ReaperForward(Command):
    COMMAND = 'reaper forward'
    reaper_login = None

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

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not(reaper := ReaperSession.create(state)):
            return state

        spec = reaper.reaper_spec(state)
        if state.in_repl:
            if ReaperSession.is_forwarding:
                log2("Another port-forward is already running.")

                return "already-running"

            # make it a daemon to exit with a Ctrl-D
            thread = threading.Thread(target=self.loop, args=(state, reaper), daemon=True)
            thread.start()

            while not ReaperSession.is_forwarding:
                time.sleep(1)

            d = {
                'reaper-ui': spec["web-uri"],
                'reaper-username': spec["username"],
                'reaper-password': spec["password"]
            }
            log2()
            log2(lines_to_tabular([f'{k},{v}' for k, v in d.items()], separator=','))

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

    def loop(self, state: ReplState, reaper: ReaperSession):
        def body(uri: str, _: dict[str, str]):
            ReaperSession.is_forwarding = True
            try:
                while not ReaperSession.stopping.is_set():
                    time.sleep(1)
            finally:
                ReaperSession.stopping.clear()
                ReaperSession.is_forwarding = False

        return reaper.port_forwarded(state, 'webui', body)

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperForward.COMMAND}\t port-forward to reaper'