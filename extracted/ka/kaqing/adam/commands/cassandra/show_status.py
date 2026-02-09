import sys

from adam.checks.check_result import CheckResult
from adam.columns.columns import Columns
from adam.commands import extract_options, extract_trailing_options
from adam.commands.command import Command
from adam.commands.devices.devices import device
from adam.config import Config
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_concurrent import offload
from adam.utils_context import Context
from adam.repl_state import ReplState, RequiredState
from adam.utils_color import Color
from adam.utils_k8s.k8s_context import K8sContext
from adam.utils_tabulize import tabulize

class ShowStatus(Command):
    COMMAND = 'show status'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowStatus, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowStatus.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def aliases(self):
        return ['ss']

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, background):
                with offload(background) as submit:
                    submit(lambda: self.show_status(state, ctx=self.context().copy(background=background)))

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {'&': None}, pods=device(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'show merged nodetool status  & background', args='[&]')

    def show_status(self, state: ReplState, ctx: Context = Context.NULL):
        if state.pod:
            status: CassandraStatus = CassandraStatus.snapshot_from_pod(state, k8s=K8sContext.preload_pods(state.sts, state.namespace), ctx=ctx)
            self.show_table(status.status, [], ctx=ctx)
        elif state.sts:
            self.merge(state, Config().get('nodetool.samples', sys.maxsize), ctx=ctx)

    def merge(self, state: ReplState, samples: int, ctx: Context = Context.NULL):
        status: CassandraStatus = CassandraStatus.snapshot(state, samples=samples, k8s=K8sContext.preload_pods(state.sts, state.namespace), ctx=ctx)
        ctx.log2(f'Showing merged status from {status.samples}/{status.cluster_size()} nodes...', text_color=Color.gray)
        # remove compaction stats and gossip for faster return
        # check_results = run_checks(cluster=state.sts, namespace=state.namespace, checks=[CompactionStats(), Gossip()], ctx=ctx.copy(background=False, show_out=False))
        self.show_table(status.status, [], ctx=ctx)

        if status.in_restarts:
            ctx.log2()
            ctx.log2('  * Node restart is pending or in progress. Use :?? to check restart schedules.')

        return status.status

    def show_table(self, status: list[dict[str, any]], check_results: list[CheckResult], ctx: Context = Context.NULL):
        cols = Config().get('status.columns', 'status,pod,ready,pod_status,load,tokens,owns,host_id')
        header = Config().get('status.header', '--,Pod,Ready,Status,Load,Tokens,Owns,Host ID')
        # remove compaction stats and gossip for faster return
        # cols = Config().get('status.columns', 'status,address,load,tokens,owns,host_id,gossip,compactions')
        # header = Config().get('status.header', '--,Address,Load,Tokens,Owns,Host ID,GOSSIP,COMPACTIONS')
        columns = Columns.create_columns(cols)

        tabulize(sorted(status, key=lambda l: l['pod'] if 'pod' in l else '-'),
                 lambda s: ','.join([c.host_value(check_results, s) for c in columns]),
                 header=header,
                 separator=',',
                 ctx=ctx)

        # remove compaction stats and gossip for faster return
        # IssuesUtils.show(check_results, ctx=ctx)