import sys
from kubernetes import client

from adam.commands.cql.utils_cql import cassandra
from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.utils import Color, log_timing
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.utils_context import Context
from adam.repl_state import ReplState
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils_tabulize import tabulize

class CassandraStatus:
    # remembers last ip to pod mappings
    pods_by_ip = {}

    def merged_nodetool_status(state: ReplState, samples: int = 0, ctx: Context = Context.NULL) -> tuple[dict, int, int]:
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

        host_ids_by_pod, pods_by_host_id = CassandraStatus.pods_host_mappings(state, ctx)
        #   status = NodeTools.merged_nodetool_status(state, samples=Config().get('nodetool.samples', sys.maxsize), ctx=ctx.copy(show_out=False))
        status, samples, nodes = CassandraStatus.merged_nodetool_status(state)
        status_by_ip = {s['address']: s for s in status}
        status_by_host_id = {s['host_id']: s for s in status}

        if pod not in host_ids_by_pod:
            return NodeRestartability(pod, host_ids_by_pod=host_ids_by_pod, err=f'Cannot locate host id from pod: {pod}.')

        host_id = host_ids_by_pod[pod]

        if host_id not in status_by_host_id or 'address' not in status_by_host_id[host_id]:
            return NodeRestartability(pod, host_ids_by_pod=host_ids_by_pod, err=f'Cannot locate IP address from host_id: {pod} -> {host_id}.')

        ip = status_by_host_id[host_id]['address']

        # find pod that's up
        pod_to_run_on: str = None
        for p, host_id in host_ids_by_pod.items():
            if host_id in status_by_host_id:
               status = status_by_host_id[host_id]
               if 'status' in status and status['status'] == 'UN':
                  pod_to_run_on = p
                  break

        if not pod_to_run_on:
            return NodeRestartability(pod, host_ids_by_pod=host_ids_by_pod, err=f'Cannot locate any pod that works at the moment.')

        ctx.log(f'Chose {pod_to_run_on} for running nodetool ring.')

        with cassandra(state, pod=pod_to_run_on) as pods:
            with log_timing('nodetool ring'):
               r = pods.nodetool('ring', ctx=ctx.copy(show_out=False))

            if isinstance(r, list):
               r = r[0]

            tokens, my_tokens = CassandraStatus.replica_ips(ip, r.stdout)
            for k in tokens.keys():
               p = '-'
               if k in status_by_ip:
                  if 'host_id' in status_by_ip[k]:
                     host_id = status_by_ip[k]['host_id']
                     if host_id in pods_by_host_id:
                           p = pods_by_host_id[host_id]

               CassandraStatus.pods_by_ip[k] = p

            if ctx.show_verbose:
               ctx.log2(f'{ip} has {len(my_tokens)} primary token ranges.', verbose=True)
               ctx.log2(verbose=True)
               tabulize(sorted(tokens.keys()),
                        lambda k: f'{status_by_ip[k]["status"]}\t{k}\t{CassandraStatus.pods_by_ip[k]}\t{len(tokens[k])}',
                        header='--\tAddress\tPOD\t# Tokens Shared',
                        separator='\t',
                        ctx=ctx.copy(show_out=True, text_color=Color.gray))

            downs = {}
            has_multiple_copies = {}
            for k, status in status_by_ip.items():
               if k in CassandraStatus.pods_by_ip:
                  p = (CassandraStatus.pods_by_ip[k], state.namespace)

                  in_restart = 'no'
                  if p in in_restartings:
                     in_restart = 'yes'

                  if status["status"] != 'UN' or in_restart == 'yes':
                     token_list = ['Unknown']
                     if k in tokens:
                         token_list = tokens[k]
                     downs[k] = {'status': status['status'], 'pod': p[0], 'namespace': p[1], 'tokens': token_list, 'in_restart': in_restart}
               else:
                  return NodeRestartability(pod, host_ids_by_pod=host_ids_by_pod, err=f'Cannot locate pod from ip: {k}.')

               if k == ip:
                  has_multiple_copies = tokens[k]

            return NodeRestartability(pod, downs, has_multiple_copies, host_ids_by_pod=host_ids_by_pod)

    def pods_host_mappings(state: ReplState, ctx: Context = Context.NULL):
        with log_timing('pods_host_mappings'):
            pod_names = StatefulSets.pod_names(state.sts, state.namespace)
            msg = 'd`Retrieving|Retrived {size} host ids'
            with Pods.parallelize(pod_names, msg=msg, action = 'get-host-id') as exec:
               host_pods = exec.map(lambda pod: (CassandraNodes.get_host_id(pod, state.namespace, ctx), pod))
               pods_by_host_id = {id: pod for id, pod in host_pods}
               host_ids_by_pod = {pod: id for id, pod in host_pods}

               return host_ids_by_pod, pods_by_host_id

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

    def nodetool_status(state: ReplState, pod: str, ctx: Context = Context.NULL) -> str:
        host_ids_by_pod, _ = CassandraStatus.pods_host_mappings(state, ctx)
        if pod not in host_ids_by_pod:
            return 'Uknown'

        host_id = host_ids_by_pod[pod]

        status = CassandraStatus.merged_nodetool_status(state, samples=Config().get('nodetool.samples', sys.maxsize), ctx=ctx.copy(show_out=False))
        status_by_host_id = {s['host_id']: s for s in status}

        if host_id not in status_by_host_id:
            return 'Unknown'

        return status_by_host_id[host_id]['status']