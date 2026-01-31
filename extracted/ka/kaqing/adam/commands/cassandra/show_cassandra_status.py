import sys

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.checks.compactionstats import CompactionStats
from adam.checks.gossip import Gossip
from adam.columns.columns import Columns
from adam.commands import extract_options, extract_trailing_options
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra
from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.utils_context import Context
from adam.utils_issues import IssuesUtils
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import SORT, Color, offload, log_exc
from adam.utils_tabulize import tabulize

class ShowCassandraStatus(Command):
    COMMAND = 'show cassandra status'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowCassandraStatus, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowCassandraStatus.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, background):
                with extract_options(args, ['-s', '--show']) as (args, verbose):
                    ctx = Context.new(cmd, background=background, show_out=verbose, text_color=Color.gray, show_verbose=verbose)
                    if background:
                        with offload(name='display-table') as exec:
                            exec.submit(lambda: self.show_status(state, ctx=ctx))
                    else:
                        self.show_status(state, ctx=ctx)

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, {'-s': {'&': None}, '&': None})

    def help(self, state: ReplState):
        return super().help(state, 'show merged nodetool status  -s show processing details', args='[-s]')

    def show_status(self, state: ReplState, ctx: Context = Context.NULL):
        if state.namespace and state.pod:
            self.show_single_pod(state, ctx=ctx)
        elif state.namespace and state.sts:
            self.merge(state, Config().get('nodetool.samples', sys.maxsize), ctx=ctx)

    def show_single_pod(self, state: ReplState, ctx: Context = Context.NULL):
        with log_exc(True):
            with cassandra(state) as pods:
                result = pods.nodetool('status', ctx=ctx)
                status = NodeTools.parse_nodetool_status(result.stdout)
                check_results = run_checks(cluster=state.sts, namespace=state.namespace, checks=[CompactionStats(), Gossip()], ctx=ctx)
                self.show_table(status, check_results, ctx=ctx)

    def merge(self, state: ReplState, samples: int, ctx: Context = Context.NULL):
        statuses: list[list[dict]] = []

        pod_names = StatefulSets.pod_names(state.sts, state.namespace)
        for pod_name in pod_names:
            pod_name = pod_name.split('(')[0]

            with log_exc(True):
                with cassandra(state, pod=pod_name) as pods:
                    result = pods.nodetool('status', ctx=ctx.copy(background=False, show_out=False))
                    status = NodeTools.parse_nodetool_status(result.stdout)
                    if status:
                        statuses.append(status)
                    if samples <= len(statuses) and len(pod_names) != len(statuses):
                        break

        combined_status = self.merge_status(statuses)
        ctx.log2(f'Showing merged status from {len(statuses)}/{len(pod_names)} nodes...', text_color=Color.gray)
        check_results = run_checks(cluster=state.sts, namespace=state.namespace, checks=[CompactionStats(), Gossip()], ctx=ctx)
        self.show_table(combined_status, check_results, ctx=ctx)

        return combined_status

    def merge_status(self, statuses: list[list[dict]]):
        combined = statuses[0]

        status_by_host = {}
        for status in statuses[0]:
            status_by_host[status['host_id']] = status
        for status in statuses[1:]:
            for s in status:
                if s['host_id'] in status_by_host:
                    c = status_by_host[s['host_id']]
                    if c['status'] == 'UN' and s['status'] == 'DN':
                        c['status'] = 'DN*'
                else:
                    combined.append(s)

        return combined

    def show_table(self, status: list[dict[str, any]], check_results: list[CheckResult], ctx: Context = Context.NULL):
        cols = Config().get('status.columns', 'status,address,load,tokens,owns,host_id,gossip,compactions')
        header = Config().get('status.header', '--,Address,Load,Tokens,Owns,Host ID,GOSSIP,COMPACTIONS')
        columns = Columns.create_columns(cols)

        tabulize(status, lambda s: ','.join([c.host_value(check_results, s) for c in columns]), header=header, separator=',', sorted=SORT, log_file=ctx.log_file)
        IssuesUtils.show(check_results, ctx=ctx)