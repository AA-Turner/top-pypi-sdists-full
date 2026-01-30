import os

from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra_table_names
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_k8s.statefulsets import StatefulSets

class Shell(Command):
    COMMAND = ':sh'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Shell, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Shell.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, _):
            with validate_args(args, state, at_least=0) as args_str:
                # sts = state.sts
                # pod = state.pod
                # pods = StatefulSets.pod_names(state.sts, state.namespace)
                # tables = cassandra_table_names(state)
                # cql = partial(run_cql, state, Context.new(show_out=True))
                if args_str:
                    os.system(args_str)
                    log2()
                else:
                    if state.sts:
                        os.environ['NS'] = state.namespace
                        os.environ['STS'] = state.sts
                        os.environ['PODS'] = ' '.join(StatefulSets.pod_names(state.sts, state.namespace))
                        if state.pod:
                            os.environ['POD'] = state.pod
                        if state.device == ReplState.C:
                            os.environ['TABLES'] = ' '.join(cassandra_table_names(state))

                    os.system('QING_DROPPED=true bash')

                    # function cql() { kubectl exec $POD -n $NAMESPACE -- cqlsh -u cs-a7b13e29bd-superuser -p lDed6uXQAQP72kHOYuML -e "$@"; }
                    # for table in $TABLES; do cql "select count(*) from $table"; done

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'drop down to shell')