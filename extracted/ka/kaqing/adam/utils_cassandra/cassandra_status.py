from kubernetes import client
import sys
import threading

from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.utils_cassandra.node_restart_schedules import NodeRestartSchedules
from adam.utils_cassandra.pod_service import cassandra
from adam.utils_context import NULL
from adam.repl_state import ReplState
from adam.utils_k8s.pods import Pods, strip_pod_name
from adam.utils_k8s.k8s_context import K8sContext
from adam.utils_k8s.statefulsets import StatefulSets

class CassandraStatus:
    STATUS = 'status'
    IP_ADDRESS = 'address'
    HOST_ID = 'host_id'

    lock = threading.Lock()

    pods_by_ip: dict[str, str] = {}
    ips_by_pod: dict[str, str] = {}
    host_ids_by_pod: dict[str, str] = {}
    pod_names_by_host_id: dict[str, str] = {}

    def snapshot_from_pod(state: ReplState, k8s: K8sContext = K8sContext.NULL, ctx = NULL):
        return CassandraStatus.snapshot(state, samples=1, k8s=k8s, target_pod=state.pod, ctx=ctx)

    def snapshot(state: ReplState, samples: int = 0, k8s: K8sContext = K8sContext.NULL, target_pod: str = None, ctx = NULL):
        if not samples:
            samples = Config().get('nodetool.samples', sys.maxsize)

        with cassandra(state.with_no_pod(), pod=target_pod) as pods:
            statuses: list[list[dict]] = []
            rs = pods.nodetool('status', status=True, samples=samples, k8s=k8s, ctx=ctx.copy(background=False, show_out=False))
            if not isinstance(rs, list):
                rs = [rs]

            for r in rs:
                status = NodeTools.parse_nodetool_status(r.stdout)
                if status:
                    statuses.append(status)

            status = CassandraStatus._merge_status(statuses)

            host_ids_by_ip = {}
            for node in status:
                host_ids_by_ip[node['address']] = node['host_id']

            pods = k8s.pods(state.sts, state.namespace)
            for v1pod in pods:
                ip = Pods.pod_ip(v1pod)
                pod_name = Pods.pod_name(v1pod)

                with CassandraStatus.lock:
                    CassandraStatus.pods_by_ip[ip] = pod_name
                    CassandraStatus.ips_by_pod[pod_name] = ip
                    if ip in host_ids_by_ip:
                        host_id = host_ids_by_ip[ip]
                        CassandraStatus.host_ids_by_pod[pod_name] = host_id
                        CassandraStatus.pod_names_by_host_id[host_id] = pod_name

            status_by_pod_name = {Pods.pod_name(v1pod): Pods.pod_status(v1pod) for v1pod in pods}
            ready_by_pod_name = {Pods.pod_name(v1pod): Pods.pod_ready(v1pod) for v1pod in pods}
            restarts = NodeRestartSchedules.restarts(namespace=state.namespace, ctx=ctx)
            in_restarts = 0
            for node in status:
                if node['address'] in CassandraStatus.pods_by_ip and (pod := CassandraStatus.pods_by_ip[node['address']]):
                    node['pod'] = strip_pod_name(pod)
                    node['pod_status'] = status_by_pod_name[pod]
                    if pod in restarts:
                        node['pod_status'] = node['pod_status'] + '*'
                        in_restarts += 1
                    node['pod_ready'] = ready_by_pod_name[pod]

            return CassandraStatus(state.namespace, pods, status, samples=len(statuses), in_restarts=in_restarts)

    def _merge_status(statuses: list[list[dict]]) -> list[dict]:
        if not statuses:
            return []

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

    def get_pod(self, state: ReplState, pod_name: str):
        pod = None
        for p in StatefulSets.pods(state.sts, state.namespace):
            if p.metadata.name == pod_name:
                pod = p
                break

        return pod

    def __init__(self, namespace: str, pods: list[client.V1Pod] = None, status: list[dict] = None, samples: int = 1, in_restarts = 0):
        # [
        #  {'status': 'UN', 'address': '172.18.13.6', 'load': '8.11 MiB', 'tokens': '16', 'owns': '?', 'host_id': 'e84aafe5-94e6-4d98-aa0e-ac28eaffe5fe', 'rack': 'default'},
        #  {'status': 'UN', 'address': '172.18.16.55', 'load': '8.42 MiB', 'tokens': '16', 'owns': '?', 'host_id': '50262572-e99e-48b8-bb2e-6f397a40ea04', 'rack': 'default'},
        #  {'status': 'UN', 'address': '172.18.6.61', 'load': '8.45 MiB', 'tokens': '16', 'owns': '?', 'host_id': '87625c74-b1f3-4694-b4e7-e6b9dec4bcb5', 'rack': 'default'}
        # ]
        self.namespace = namespace
        self.pods = pods
        self.status = status
        self.samples = samples
        self.in_restarts = in_restarts

    def cluster_size(self):
        return len(self.pods)

    def pod_names(self):
        return [pod.metadata.name for pod in self.pods]

    def ip_from_pod_name(self, pod_name: str, default: str = None) -> str:
        with CassandraStatus.lock:
            if pod_name not in CassandraStatus.ips_by_pod:
                if default:
                    return default

                raise AddressTranslationError(f'Cannot locate ip from pod: {pod_name}.', self)

            return CassandraStatus.ips_by_pod[pod_name]

    def pod_name_from_ip(self, ip: str, default: str = None) -> str:
        with CassandraStatus.lock:
            if ip not in CassandraStatus.pods_by_ip:
                if default:
                    return default

                raise AddressTranslationError(f'Cannot locate pod name from ip: {ip}.', self)

            return CassandraStatus.pods_by_ip[ip]

    def host_id_from_pod_name(self, pod_name: str, default: str = None) -> str:
        with CassandraStatus.lock:
            if pod_name not in CassandraStatus.host_ids_by_pod:
                if default:
                    return default

                raise AddressTranslationError(f'Cannot locate host id from pod: {pod_name}.', self)

            return CassandraStatus.host_ids_by_pod[pod_name]

    def pod_name_from_host_id(self, host_id: str, default: str = None) -> str:
        with CassandraStatus.lock:
            if host_id not in CassandraStatus.pod_names_by_host_id:
                if default:
                    return default

                raise AddressTranslationError(f'Cannot locate pod from host_id: {host_id}.', self)

            return CassandraStatus.pod_names_by_host_id[host_id]

    def status_by_host_id(self):
        return {s['host_id']: s for s in self.status}

    def status_by_ip(self):
        return {s['address']: s for s in self.status}

    def status_by_pod_name(self):
        dict = {}

        for s in self.status:
            if s['address'] in CassandraStatus.pods_by_ip:
                dict[CassandraStatus.pods_by_ip[s['address']]] = s

        return dict

class AddressTranslationError(Exception):
    def __init__(self, message, status: CassandraStatus = None):
        super().__init__(message)
        self.status = status