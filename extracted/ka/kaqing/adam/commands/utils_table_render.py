from kubernetes import client
from typing import List

from adam.checks.check_utils import run_checks
from adam.columns.columns import Columns, collect_checks
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_context import Context
from adam.commands.check_up.utils_issues import IssuesUtils
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState
from adam.utils import SORT, duration
from adam.utils_log import log2
from adam.utils_tabulize import tabulize

def show_pods_simple(state: ReplState, pods: List[client.V1Pod], ctx: Context = Context.NULL):
    if len(pods) == 0:
        log2('No pods found.')
        return

    def line(pod: client.V1Pod):
        status = Pods.pod_status(pod)
        pod_name = Pods.pod_name(pod)

        line = ""
        line += pod_name
        return line + f" {Pods.pod_ready(pod)} {status}"

    tabulize(pods,
             line,
             header='POD_NAME READY POD_STATUS',
             ctx=ctx.copy(show_out=True))

def show_pods(state: ReplState, pods: List[client.V1Pod], ns: str, show_namespace = True, show_host_id = True, ctx: Context = Context.NULL):
    if len(pods) == 0:
        log2('No pods found.')
        return

    cs: CassandraStatus = None
    if show_host_id:
        cs = CassandraStatus.snapshot(state, ctx=ctx)

    def line(pod: client.V1Pod):
        status = Pods.pod_status(pod)
        pod_name = Pods.pod_name(pod)

        line = ""
        if show_host_id:
            line = line + cs.host_id_from_pod_name(pod_name, '-') + ' '
        line += pod_name
        if show_namespace:
            line += f"@{ns}"
        return line + f" {Pods.pod_ready(pod)} {status}"

    tabulize(pods,
             line,
             header='HOST_ID POD_NAME READY POD_STATUS' if show_host_id else 'POD_NAME READY POD_STATUS',
             ctx=ctx.copy(show_out=True))

def show_rollout(sts: str, ns: str, ctx: Context = Context.NULL):
    restarted, rollingout = StatefulSets.restarted_at(sts, ns)
    if restarted:
        d = duration(restarted)
        if rollingout:
            ctx.log2(f'* Cluster is being rolled out for {d}...')
        else:
            ctx.log2(f'Cluster has completed rollout {d} ago.')

def show_table(state: ReplState, pods: list[str], cols: str, header: str, find_issues = True, ctx: Context = Context.NULL):
    columns = Columns.create_columns(cols)

    status: CassandraStatus = CassandraStatus.snapshot(state, ctx=ctx)

    results = run_checks(cluster=state.sts,
                         pod=state.pod,
                         namespace=state.namespace,
                         checks=collect_checks(columns),
                         find_issues=find_issues,
                         status=status,
                         ctx=ctx)

    tabulize(pods,
             lambda p: ','.join([c.pod_value(results, p) for c in columns]),
             header=header,
             separator=',',
             sorted=SORT,
             ctx=ctx.copy(show_out=True))
    if find_issues:
        IssuesUtils.show(results, state.in_repl, ctx=ctx)