from adam.commands import extract_options, extract_trailing_options
from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils_cassandra.table_renderer import renderer
from adam.utils_context import Context

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

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def aliases(self):
        return ['st']

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, background):
                cols = Config().get('storage.columns', 'pod,volume_root,volume_cassandra,snapshots,data,compactions')
                header = Config().get('storage.header', 'POD_NAME,VOLUME /,VOLUME CASS,SNAPSHOTS,DATA,COMPACTIONS')
                with renderer(state) as pods:
                    pods.display_table(cols, header, ctx=Context.new(cmd, background=background))

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {'&': None})

    def help(self, state: ReplState):
        return super().help(state, 'show storage overview  & background', args='[&]')