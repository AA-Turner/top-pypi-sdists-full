from concurrent.futures import ThreadPoolExecutor
import time
from kubernetes import client
from typing import List

from adam.checks.check_utils import run_checks
from adam.columns.columns import Columns, collect_checks
from adam.commands.issues import Issues
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState
from adam.utils import convert_seconds, duration, lines_to_tabular, log, log2

def show_pods(pods: List[client.V1Pod], ns: str, show_namespace = True, show_host_id = True):
    if len(pods) == 0:
        log2('No pods found.')
        return

    host_ids_by_pod = {}
    if show_host_id:
        names = [pod.metadata.name for pod in pods]

        def get_host_id_with_pod(pod, ns):
            return (CassandraNodes.get_host_id(pod, ns), pod)

        def body(executor: ThreadPoolExecutor, pod, ns, show_out):
            if executor:
                return executor.submit(get_host_id_with_pod, pod, ns)

            id = CassandraNodes.get_host_id(pod, ns)

            return (id, pod)

        host_ids_by_pod = {pod: id for id, pod in Pods.on_pods(names, ns, body, action='get-host-id', show_out=False)}

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

    pod_names = [line(pod) for pod in pods]

    log(lines_to_tabular(pod_names, 'HOST_ID POD_NAME READY POD_STATUS' if show_host_id else 'POD_NAME READY POD_STATUS'))

def show_rollout(sts: str, ns: str):
    restarted, rollingout = StatefulSets.restarted_at(sts, ns)
    if restarted:
        d = duration(restarted)
        if rollingout:
            log2(f'* Cluster is being rolled out for {d}...')
        else:
            log2(f'Cluster has completed rollout {d} ago.')

def show_table(state: ReplState, pods: list[str], cols: str, header: str, show_output=False):
    columns = Columns.create_columns(cols)

    results = run_checks(cluster=state.sts, pod=state.pod, namespace=state.namespace, checks=collect_checks(columns), show_output=show_output)

    def line(pod_name: str):
        cells = [c.pod_value(results, pod_name) for c in columns]
        return ','.join(cells)

    lines = [line(pod) for pod in pods]
    lines.sort()

    log(lines_to_tabular(lines, header, separator=','))

    Issues.show(results, state.in_repl)