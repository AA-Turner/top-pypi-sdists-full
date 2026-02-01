import re

from adam.utils import Color
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_exec_result import PodExecResult

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