from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.commands.nodetool.utils_nodetools import NodeTools

class Status(Check):
    def name(self):
        return 'status'

    def check(self, ctx: CheckContext) -> CheckResult:
        issues: list[Issue] = []

        try:
            status, result = NodeTools.status(ctx)
            # ctx_fg = ctx.copy(background=False, text_color=Color.gray)
            # result = CassandraNodes.exec(ctx.pod, ctx.namespace, f"nodetool -u {ctx.user} -pw {ctx.pw} status", ctx=ctx_fg)
            # status = parse_nodetool_status(result.stdout)
            pod_details = {
                'name': ctx.pod,
                'namespace': ctx.namespace,
                'statefulset': ctx.statefulset,
                'status': status
            }
            if result.stderr:
                pod_details['stderr'] = result.stderr

            for pod in pod_details['status']:
                if pod['status'] != 'UN':
                    issues.append(Issue(
                        statefulset=ctx.statefulset,
                        namespace=ctx.namespace,
                        pod=ctx.pod,
                        category='status',
                        desc=f"node: {ctx.host_id} reported DOWN"
                    ))

            return CheckResult(self.name(), pod_details, issues)
        except Exception as e:
            pod_details = {
                'err': str(e)
            }

            return CheckResult(self.name(), pod_details, issues)

    def help(self):
        return f'{Status().name()}: check if a node is down with nodetool status'

# def parse_nodetool_status(stdout: str):
#     nodes: list[dict] = []
#     for line in stdout.splitlines():
#         groups = re.match(r"(\S*)\s+(\S*)\s+(.*B)\s+(\S*)\s+(\S*)\s+(\S*)\s+(\S*)", line)
#         if groups:
#             nodes.append({
#                 'status': groups[1],
#                 'address': groups[2],
#                 'load': groups[3],
#                 'tokens': groups[4],
#                 'owns': groups[5],
#                 'host_id': groups[6],
#                 'rack': groups[7]
#             })

#     return nodes