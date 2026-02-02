from copy import copy
import ipaddress
import sys
import threading
import traceback
from kubernetes import client

from adam.commands.cql.utils_cql import cassandra
from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.utils import Color, log_timing
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.utils_context import Context
from adam.repl_state import ReplState
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_tabulize import tabulize

class CassandraStatus:
    def merged_nodetool_status(state: ReplState, samples: int = 0, ctx: Context = Context.NULL) -> tuple[list[dict], int, int]:
        if not samples:
            samples = Config().get('nodetool.samples', sys.maxsize)

        statuses: list[list[dict]] = []

        with cassandra(state) as pods:
            pod_names = pods.pod_names()
            cluster_size = len(pod_names)

            # 1. If 3 samples are requested out of 96 nodes, first 32 pods are examined concurrently.
            # 2. If at least 3 samples are acquired, the method returns with the first 3 samples.
            # 3. If not all 3 samples are acquired, the next 32 pods are examined concurrently, and so on.
            # 4. After all 96 nodes are examined, if the number of samples is less than 3, the samples are returned.
            s = min(len(pod_names), max(samples * 3, int(len(pod_names) / 3)))

            pns = pod_names[:s]
            pod_names = pod_names[s:]

            while samples and pns:
                rs = pods.nodetool('status', status=True, pods=pns, ctx=ctx.copy(background=False, show_out=False))
                for r in rs:
                    status = NodeTools.parse_nodetool_status(r.stdout)
                    if status:
                        statuses.append(status)
                        samples -= 1
                        if not samples:
                            break

                if s < len(pod_names):
                    pns = pod_names[:s]
                    pod_names = pod_names[s:]
                else:
                    pns = pod_names
                    pod_names = []

        # following block is for serialized naive pod runnings

        # pod_names = StatefulSets.pod_names(state.sts, state.namespace)
        # for pod_name in pod_names:
        #     pod_name = pod_name.split('(')[0]

        #     with log_exc(True):
        #         with cassandra(state, pod=pod_name) as pods:
        #             result = pods.nodetool('status', ctx=ctx.copy(background=False, show_out=False))
        #             status = NodeTools.parse_nodetool_status(result.stdout)
        #             if status:
        #                 statuses.append(status)
        #             if samples <= len(statuses) and len(pod_names) != len(statuses):
        #                 break

        combined_status = CassandraStatus._merge_status(statuses)

        return combined_status, len(statuses), cluster_size

    def _merge_status(statuses: list[list[dict]]):
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

    def restartable(state: ReplState, pod: str, in_restartings: list, ctx: Context = Context.NULL):
        if (pod, state.namespace) in in_restartings:
            return NodeRestartability(pod, err=f'{pod} is already in restart.')

        nat: CassandraNAT = CassandraNAT.build(state, ctx=ctx)

        ip: str = None
        try:
            ip = nat.local_ip_from_pod_name(pod)
        except NATError as e:
            return NodeRestartability(pod, host_ids_by_pod=nat._host_ids_by_pod, err=str(e))

        # find pod that's up
        pod_to_run_on: str = None
        for p, host_id in nat._host_ids_by_pod.items():
            if host_id in nat.status_by_host_id(state):
               status = nat.status_by_host_id(state)[host_id]
               if 'status' in status and status['status'] == 'UN':
                  pod_to_run_on = p
                  break

        if not pod_to_run_on:
            return NodeRestartability(pod, host_ids_by_pod=nat._host_ids_by_pod, err=f'[DOWN] Cannot locate any pod that works at the moment.')

        ctx.log(f'Chose {pod_to_run_on} for running nodetool ring.')

        with cassandra(state, pod=pod_to_run_on) as pods:
            with log_timing('nodetool ring'):
               r = pods.nodetool('ring', ctx=ctx.copy(show_out=False))

            if isinstance(r, list):
               r = r[0]

            tokens, my_tokens = CassandraStatus.replica_ips(ip, r.stdout)

            if ctx.show_verbose:
               ctx.log2(f'{ip} has {len(my_tokens)} primary token ranges.', verbose=True)
               ctx.log2(verbose=True)
               tabulize(sorted(tokens.keys()),
                        lambda k: f'{nat.status_by_ip(state)[k]["status"]}\t{k}\t{nat.pod_name_from_local_ip[k]}\t{len(tokens[k])}',
                        header='--\tAddress\tPOD\t# Tokens Shared',
                        separator='\t',
                        ctx=ctx.copy(show_out=True, text_color=Color.gray))

            downs = {}
            has_multiple_copies = {}
            try:
                for k, status in nat.status_by_ip(state).items():
                    if p := (nat.pod_name_from_local_ip(k), state.namespace):
                        in_restart = 'yes' if p in in_restartings else 'no'

                        if status["status"] != 'UN' or in_restart == 'yes':
                            token_list = ['Unknown']
                            if k in tokens:
                                token_list = tokens[k]
                            downs[k] = {'status': status['status'], 'pod': p[0], 'namespace': p[1], 'tokens': token_list, 'in_restart': in_restart}

                    if k == ip:
                        has_multiple_copies = tokens[k]
            except NATError as e:
                return NodeRestartability(pod, host_ids_by_pod=nat._host_ids_by_pod, err=str(e))

            return NodeRestartability(pod, downs, has_multiple_copies, host_ids_by_pod=nat._host_ids_by_pod)

    def replica_ips(ip: str, ring_out: str):
         ring = NodeTools.parse_nodetool_ring(ring_out)

         tokens : dict[str, set] = {}

         def line(ip: str):
            if ip not in tokens:
               tokens[ip] = set()

            return tokens[ip]

         my_tokens = set()
         token = None
         s = 0
         for n in ring:
            if s == 0:
               if n['address'] == ip:
                  token = n['token']
                  my_tokens.add(token)
                  # line(ip).add(n['token'])

                  s = 1
            elif s == 1:
               line(n['address']).add(token)

               s = 2
            elif s == 2:
               line(n['address']).add(token)

               s = 0

         return tokens, my_tokens

    def pod_status(pod: client.V1Pod):
        s = 'Unknown'

        try:
            s = pod.status.phase
            if pod.metadata.deletion_timestamp:
                  s = 'Terminating'
        except:
            pass

        return s

    # TODO remove this; used only by a test
    def nodetool_status(state: ReplState, pod: str, ctx: Context = Context.NULL) -> str:
        if pod not in CassandraNAT.host_ids_by_pod:
            return 'Uknown'

        host_id = CassandraNAT.host_ids_by_pod[pod]

        status = CassandraStatus.merged_nodetool_status(state, samples=Config().get('nodetool.samples', sys.maxsize), ctx=ctx.copy(show_out=False))
        status_by_host_id = {s['host_id']: s for s in status}

        if host_id not in status_by_host_id:
            return 'Unknown'

        return status_by_host_id[host_id]['status']

class CassandraNAT:
    # additive; remembers last ip to pod mappings
    pods_by_ip: dict[str, str] = {}
    ips_by_pod: dict[str, str] = {}
    host_ids_by_pod: dict[str, str] = {}

    lock = threading.Lock()

    def build(state: ReplState, ctx: Context = Context.NULL):
        host_ids_by_ip = {}

        try:
            with cassandra(state) as pods:
                cql = 'select broadcast_address, host_id from system.local; select peer, host_id from system.peers'
                result: PodExecResult = pods.cql(cql, ctx=ctx.copy(show_out=ctx.debug), no_color=True, on_any=True)
                result = result[0]

                for line in result.stdout.splitlines():
                    if line:
                        #    172.18.6.43 | 87625c74-b1f3-4694-b4e7-e6b9dec4bcb5
                        tokens = [t.strip(' \r\n\t') for t in line.strip(' ').split('|')]
                        if len(tokens) == 2 and CassandraNAT.is_valid_ip(tokens[0]):
                            host_ids_by_ip[tokens[0]] = tokens[1]

                for pod, ip in pods.pod_name_n_ips():
                    with CassandraNAT.lock:
                        CassandraNAT.pods_by_ip[ip] = pod
                        CassandraNAT.ips_by_pod[pod] = ip
                        if ip in host_ids_by_ip:
                            CassandraNAT.host_ids_by_pod[pod] = host_ids_by_ip[ip]

        except Exception as e:
            traceback.print_exc()
            pass
            # return str(e)

        return CassandraNAT(copy(CassandraNAT.host_ids_by_pod))

    def __init__(self):
        pass

    def __init__(self, host_ids_by_pod: dict):
        self._host_ids_by_pod = host_ids_by_pod
        self._status: list[dict] = None

    def local_ip_from_pod_name(self, pod_name: str) -> str:
        with CassandraNAT.lock:
            if pod_name not in CassandraNAT.ips_by_pod:
                raise NATError(f'Cannot locate local ip from pod: {pod_name}.', self)

            return CassandraNAT.ips_by_pod[pod_name]

    def pod_name_from_local_ip(self, local_ip: str) -> str:
        with CassandraNAT.lock:
            if local_ip not in CassandraNAT.pods_by_ip:
                raise NATError(f'Cannot locate pod name from local ip: {local_ip}.', self)

            return CassandraNAT.pods_by_ip[local_ip]

    def status_by_host_id(self, state: ReplState):
        if not self._status:
            self._status, samples, nodes = CassandraStatus.merged_nodetool_status(state)

        return {s['host_id']: s for s in self._status}

    def status_by_ip(self, state: ReplState):
        if not self._status:
            self._status, samples, nodes = CassandraStatus.merged_nodetool_status(state)

        return {s['address']: s for s in self._status}

    def is_valid_ip(ip_string):
        try:
            ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False

class NATError(Exception):
    def __init__(self, message, nat: CassandraNAT = None):
        super().__init__(message)
        self.nat = nat
