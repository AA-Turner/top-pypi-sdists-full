import sys

from adam.commands.cql.utils_cql import cassandra
from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.utils_context import Context
from adam.repl_state import ReplState
from adam.utils_k8s.statefulsets import StatefulSets

class CassandraStatus:
    def merged_nodetool_status(state: ReplState, samples: int = 0, ctx: Context = Context.NULL) -> tuple[list[dict], int, int]:
        if not samples:
            samples = Config().get('nodetool.samples', sys.maxsize)

        statuses: list[list[dict]] = []

        with cassandra(state.with_no_pod()) as pods:
            rs = pods.nodetool('status', status=True, samples=samples, ctx=ctx.copy(background=False, show_out=False))
            for r in rs:
                status = NodeTools.parse_nodetool_status(r.stdout)
                if status:
                    statuses.append(status)

        combined_status = CassandraStatus._merge_status(statuses)

        return combined_status, len(statuses), len(pods.pod_names())

    def _merge_status(statuses: list[list[dict]]):
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