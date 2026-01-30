from abc import abstractmethod

from adam.commands.command import Command
from adam.config import Config
from adam.utils_context import Context
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_state import BashSession, ReplState
from adam.utils import log2
from adam.utils_k8s.pods import Pods

class Device:
    def pods(self, state: ReplState, me: str = None) -> tuple[list[str], str]:
        return self.pod_names(state), me if me else self.pod(state)

    def default_pod(self, state: ReplState) -> tuple[list[str], str]:
        if me := self.pod(state):
            return me

        if pods := self.pod_names(state):
            return pods[0]

        return None

    def pod(self, state: ReplState) -> str:
        return None

    def pod_names(self, state: ReplState) -> list[str]:
        return []

    def default_container(self, state: ReplState) -> str:
        return None

    @abstractmethod
    def ls(self, cmd: str, state: ReplState):
        pass

    def ls_completion(self, cmd: str, state: ReplState, default: dict = {}):
        return default

    def cd(self, dir: str, state: ReplState):
        pass

    def cd_completion(self, cmd: str, state: ReplState, default: dict = {}):
        return default

    def direct_dirs(self, cmd: str, state: ReplState, default: dict = {}) -> list[str]:
        return []

    @abstractmethod
    def pwd(self, state: ReplState):
        pass

    def try_fallback_action(self, chain: Command, state: ReplState, cmd: str):
        return False, None

    def enter(self, state: ReplState):
        pass

    def preview(self, table: str, state: ReplState):
        if not table:
            if state.in_repl:
                log2('Table is required.')
                log2()
                log2('Tables:')
                self.show_tables(state)
            else:
                log2('* Table is missing.')
                self.show_tables(state)

                Command.display_help()

            return 'command-missing'

        rows = Config().get('preview.rows', 10)
        self.show_table_preview(state, table, rows)

        return state

    @abstractmethod
    def show_tables(self, state: ReplState):
        pass

    @abstractmethod
    def show_table_preview(self, state: ReplState, table: str, rows: int, ctx: Context = Context.NULL):
        pass

    def bash(self, s0: ReplState, s1: ReplState, args: list[str], ctx: Context = Context.NULL):
        if s1.in_repl:
            if self.bash_target_changed(s0, s1):
                r = self._exec_with_dir(s1, args, ctx=ctx)
            else:
                r = self._exec_with_dir(s0, args, ctx=ctx)

            if not r:
                s1.exit_bash()

                return 'inconsistent pwd'

            return r
        else:
            self.exec_no_dir(' '.join(args), s1)

            return s1

    def _exec_with_dir(self, state: ReplState, args: list[str], ctx: Context = Context.NULL) -> list[PodExecResult]:
        session_just_created = False
        if not args:
            session_just_created = True
            session = BashSession(state.device)
            state.enter_bash(session)

        if state.bash_session:
            if args != ['pwd']:
                if args:
                    args.append('&&')
                args.extend(['pwd', '>', f'/tmp/.qing-{state.bash_session.session_id}'])

            if not session_just_created:
                if pwd := state.bash_session.pwd(state):
                    args = ['cd', pwd, '&&'] + args

        return self.exec_with_dir(' '.join(args), session_just_created, state, ctx=ctx)

    @abstractmethod
    def bash_target_changed(self, s0: ReplState, s1: ReplState):
        pass

    @abstractmethod
    def exec_no_dir(self, command: str, state: ReplState, ctx: Context = Context.NULL):
        pass

    @abstractmethod
    def exec_with_dir(self, command: str, session_just_created: bool, state: ReplState, ctx: Context = Context.NULL):
        pass

    def bash_completion(self, cmd: str, state: ReplState, default: dict = {}):
        return default

    def files(self, state: ReplState):
        r: PodExecResult = Pods.exec(self.default_pod(state), self.default_container(state), state.namespace, f'find -maxdepth 1 -type f', shell='bash', ctx=Context.NULL)

        log_files = []
        for line in r.stdout.split('\n'):
            line = line.strip(' \r')
            if line:
                if line.startswith('./'):
                    line = line[2:]
                log_files.append(line)

        return log_files