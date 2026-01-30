from adam.commands.command import Command
from adam.commands.devices.device import Device
from adam.repl_state import ReplState
from adam.utils import tabulize
from adam.utils_athena import Athena
from adam.utils_context import Context

class DeviceAuditLog(Command, Device):
    COMMAND = f'{ReplState.L}:'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DeviceAuditLog, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DeviceAuditLog.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        state.device = ReplState.L

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'move to Audit Log Operations device')

    def ls(self, cmd: str, _: ReplState):
        tabulize(Athena.table_names(), header='NAME', separator=',')

    def pwd(self, _: ReplState):
        return '\t'.join([f'{ReplState.L}:>', '/'])

    def try_fallback_action(self, chain: Command, state: ReplState, cmd: str):
        return True, chain.run(f'audit {cmd}', state)

    def show_tables(self, _: ReplState):
        tabulize(Athena.table_names(), separator=',')

    def show_table_preview(self, _: ReplState, table: str, rows: int, ctx: Context = Context.NULL):
        Athena.run_query(f'select * from {table} limit {rows}', ctx=ctx)