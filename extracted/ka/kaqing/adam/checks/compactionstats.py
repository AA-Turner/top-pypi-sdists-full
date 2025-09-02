import re

from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.config import Config
from adam.k8s_utils.cassandra_nodes import CassandraNodes

class CompactionStats(Check):
    def name(self):
        return 'compactionstats'

    def check(self, ctx: CheckContext) -> CheckResult:
        issues: list[Issue] = []

        try:
            result = CassandraNodes.exec(ctx.pod, ctx.namespace, f"nodetool -u {ctx.user} -pw {ctx.pw} compactionstats", show_out=ctx.show_output)
            compactions = parse_nodetool_compactionstats(result.stdout)
            pod_details = {
                'name': ctx.pod,
                'namespace': ctx.namespace,
                'statefulset': ctx.statefulset,
                'host_id': ctx.host_id,
                'compactions': compactions
            }
            if result.stderr: pod_details['stderr'] = result.stderr

            desc: str = None
            if pod_details['compactions'] == 'Unknown':
                desc = f"node: {ctx.host_id} cannot get compaction stats"
            else:
                c = int(pod_details['compactions'])
                threshold = Config().get('checks.compactions-threshold', 250)
                if c >= threshold:
                    desc = f"node: {ctx.host_id} reports high pending compactions: {c}"
            if desc:
                issues.append(Issue(
                    statefulset=ctx.statefulset,
                    namespace=ctx.namespace,
                    pod=ctx.pod,
                    category="compaction",
                    desc=desc
                ))

            return CheckResult(self.name(), pod_details, issues)
        except Exception as e:
            pod_details = {
                'err': str(e)
            }

            return CheckResult(self.name(), pod_details, issues)

    def help(self):
        return f'{CompactionStats().name()}: check pending compactions with nodetool compactionstats'

def parse_nodetool_compactionstats(stdout: str):
    # pending tasks: 0
    for line in stdout.splitlines():
        groups = re.match(r"pending tasks: (\d+)$", line)
        if groups:
            return str(groups[1])

    return "Unknown"