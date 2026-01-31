import re

from adam.repl_state import ReplState
from adam.utils import Color, log_exc, log_timing
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s.statefulsets import StatefulSets

class NodeTools:
    def status(ctx: Context = Context.NULL) -> tuple[dict, PodExecResult]:
        ctx_fg = ctx.copy(background=False, text_color=Color.gray)
        result = CassandraNodes.exec(ctx.pod, ctx.namespace, f"nodetool -u {ctx.user} -pw {ctx.pw} status", ctx=ctx_fg)
        return NodeTools.parse_nodetool_status(result.stdout), result

    def parse_nodetool_status(stdout: str) -> list[dict]:
        nodes: list[dict] = []

        for line in stdout.splitlines():
            groups = re.match(r"(\S*)\s+(\S*)\s+(.*B)\s+(\S*)\s+(\S*)\s+(\S*)\s+(\S*)", line)
            if groups:
                nodes.append({
                    'status': groups[1],
                    'address': groups[2],
                    'load': groups[3],
                    'tokens': groups[4],
                    'owns': groups[5],
                    'host_id': groups[6],
                    'rack': groups[7]
                })

        return nodes

    def parse_nodetool_ring(stdout: str) -> list[dict]:
        # Datacenter: cs-a7b13e29bd
        # ==========
        # Address           Rack        Status State   Load            Owns                Token
        #                                                                                 9092166997895998344
        # 172.18.7.7        default     Up     Normal  8.32 MiB        ?                   -9051871175443108837
        nodes: list[dict] = []

        s = 0
        for line in stdout.splitlines():
            if s == 0:
                if line.startswith('Address'):
                    s = 1
            elif s == 1:
                nodes.append({'address': None, 'token': line.strip(' ')})
                s = 2
            elif s == 2:
                groups = re.match(r"(\S*)\s+(\S*)\s+(\S*)\s+(\S*)\s+(.*B)\s+(\S*)\s+(\S*)", line)
                if groups:
                    nodes.append({
                        'address': groups[1],
                        'rack': groups[2],
                        'status': groups[3],
                        'state': groups[4],
                        'load': groups[5],
                        'owns': groups[6],
                        'token': groups[7]
                    })

        return nodes

    def merged_nodetool_status(state: ReplState, samples: int = 3, ctx: Context = Context.NULL):
        with log_timing('merged_nodetool_status'):
            statuses: list[list[dict]] = []

            pod_names = StatefulSets.pod_names(state.sts, state.namespace)
            for pod_name in pod_names:
                pod_name = pod_name.split('(')[0]

                with log_exc(True):
                    ctx_fg = ctx.copy(background=False, text_color=Color.gray)
                    user, pw = state.user_pass()
                    result = CassandraNodes.exec(pod_name, state.namespace, f"nodetool -u {user} -pw {pw} status", ctx=ctx_fg)
                    status = NodeTools.parse_nodetool_status(result.stdout)
                    if status:
                        statuses.append(status)
                    if samples <= len(statuses) and len(pod_names) != len(statuses):
                        break

            return NodeTools._merge_status(statuses)

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