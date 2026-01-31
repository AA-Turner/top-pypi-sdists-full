from kubernetes import client
from typing import List

from adam.checks.check_utils import run_checks
from adam.columns.columns import Columns, collect_checks
from adam.utils_context import Context
from adam.utils_issues import IssuesUtils
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState
from adam.utils import SORT, duration, kaqing_log_file, log2
from adam.utils_tabulize import tabulize

def show_pods(pods: List[client.V1Pod], ns: str, show_namespace = True, show_host_id = True, ctx: Context = Context.NULL):
    if len(pods) == 0:
        log2('No pods found.')
        return

    host_ids_by_pod = {}
    if show_host_id:
        names = [pod.metadata.name for pod in pods]

        msg = 'd`Retrieving|Retrived {size} host ids'
        with Pods.parallelize(names, msg=msg, action = 'get-host-id') as exec:
            host_pods = exec.map(lambda pod: (CassandraNodes.get_host_id(pod, ns), pod))
            host_ids_by_pod = {pod: id for id, pod in host_pods}

    def line(pod: client.V1Pod):
        pod_cnt = len(pod.status.container_statuses)
        ready = 0
        if pod.status.container_statuses:
            for container_status in pod.status.container_statuses:
                if container_status.ready:
                    ready += 1

        status = pod.status.phase
        if pod.metadata.deletion_timestamp:
            status = 'Terminating'

        pod_name = pod.metadata.name
        line = ""
        if show_host_id:
            if pod_name in host_ids_by_pod:
                line = line + f"{host_ids_by_pod[pod_name]} "
            else:
                line = line + f"{CassandraNodes.get_host_id(pod_name, ns)} "
        line += pod_name
        if show_namespace:
            line += f"@{ns}"
        return line + f" {ready}/{pod_cnt} {status}"

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

def show_table(state: ReplState, pods: list[str], cols: str, header: str, ctx: Context = Context.NULL):
    columns = Columns.create_columns(cols)

    results = run_checks(cluster=state.sts, pod=state.pod, namespace=state.namespace, checks=collect_checks(columns), ctx=ctx)

    tabulize(pods,
             lambda p: ','.join([c.pod_value(results, p) for c in columns]),
             header=header,
             separator=',',
             log_file=ctx.log_file,
             sorted=SORT,
             ctx=ctx.copy(show_out=True))
    IssuesUtils.show(results, state.in_repl, ctx=ctx)

def write_to_kaqing_log_file(r: str, i: str = None):
    with kaqing_log_file() as f:
        f.write(r)
        if i:
            f.write('\n')
            f.write(i)

        return f.name