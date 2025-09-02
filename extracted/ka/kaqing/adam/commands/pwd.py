from adam.app_session import AppSession
from adam.commands.command import Command
from adam.commands.postgres.postgres_session import PostgresSession
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log

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

        state, _ = self.apply_state(args, state)

        def device_line(state: ReplState, device: str):
            words = []

            if device == ReplState.P:
                pg = PostgresSession(state.namespace, state.pg_path)

                if pg.host:
                    words.append(f'host/{pg.host}')
                if pg.db:
                    words.append(f'database/{pg.db}')
            elif device == ReplState.A:
                if state.app_env:
                    words.append(f'env/{state.app_env}')
                if state.app_app:
                    words.append(f'app/{state.app_app}')
            else:
                if state.sts:
                    words.append(f'sts/{state.sts}')
                if state.pod:
                    words.append(f'pod/{state.pod}')

            return '\t'.join([f'{device}:>'] + (words if words else ['/']))

        host = "unknown"
        try:
            app_session: AppSession = AppSession.create('c3', 'c3')
            host = app_session.host
        except:
            pass

        log(lines_to_tabular([
            device_line(state, ReplState.A),
            device_line(state, ReplState.C),
            device_line(state, ReplState.P),
            f'',
            f'HOST\t{host}',
            f'NAMESPACE\t{state.namespace if state.namespace else "/"}',
        ], 'DEVICE\tLOCATION', separator='\t'))
        log()

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{Pwd.COMMAND}\t print current working directories'