import code
from functools import partial

from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra_table_names, run_cql
from adam.repl_state import ReplState, RequiredState
from adam.utils import tabulize
from adam.utils_context import Context
from adam.utils_k8s.statefulsets import StatefulSets

class Code(Command):
    COMMAND = 'python'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Code, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Code.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            sts = state.sts
            pod = state.pod
            pods = StatefulSets.pod_names(state.sts, state.namespace)
            tables = cassandra_table_names(state)
            cql = partial(run_cql, state, Context.new(show_out=True))

            my_local = globals() | locals()
            # my_local = globals() | {'StatefulSets': StatefulSets} | locals()
            lines = [
                'sts: StatefulSet name',
                'pod: Pod name',
                'pods: Pod names in the current StatefulSet',
                'tables: Cassandra tables names in the current StatefulSet',
                "cql('select...'): run cql statement"
            ]

            code.interact(local=my_local, banner=tabulize(lines, header='Variables', separator=':'))

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'run interactive Python shell')