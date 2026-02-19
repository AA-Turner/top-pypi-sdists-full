from adam.commands.command import Command
from adam.config import Config
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.presentation.table_renderer import renderer

class ShowStorage(Command):
    COMMAND = 'show storage'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowStorage, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowStorage.COMMAND

    def aliases(self):
        return ['st']

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args, show_out=False) as (args, ctx):
                cols = Config().get('storage.columns', 'short-pod,volume_root,volume_cassandra,snapshots,data,compactions')
                header = Config().get('storage.header', 'POD_NAME,VOLUME /,VOLUME CASS,SNAPSHOTS,DATA,COMPACTIONS')

                with renderer(state) as pods:
                    pods.display_table(cols, header, ctx=ctx)

                return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show storage overview')