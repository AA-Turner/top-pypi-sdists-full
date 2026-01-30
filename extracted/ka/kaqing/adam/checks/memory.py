from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.utils import Color
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils_k8s.pods import Pods

class Memory(Check):
    def name(self):
        return 'memory'

    def check(self, ctx: CheckContext) -> CheckResult:
        issues: list[Issue] = []
        details = {
            'name': ctx.pod,
            'namespace': ctx.namespace,
            'statefulset': ctx.statefulset,
            'used': 'NA',
            'request': 'NA',
            'limit': 'NA'
        }

        try:
            metrics = CustomResources.get_metrics(ctx.namespace, ctx.pod, container_name='cassandra')
            details['used'] = metrics['usage']['memory']

            container = Pods.get_container(ctx.namespace, ctx.pod, container_name='cassandra')
            if container.resources.requests and "memory" in container.resources.requests:
                details['request'] = container.resources.requests["memory"]
            if container.resources.limits and "memory" in container.resources.limits:
                details['limit'] = container.resources.limits["memory"]

            if issue := self.find_error(ctx, 'Not marking nodes down due to local pause',
                                        'local pause due to memory pressure'):
                issues.append(issue)
            if issue := self.find_error(ctx, 'java.lang.OutOfMemoryError: Direct buffer memory',
                                        'direct buffer OOM'):
                issues.append(issue)
            if issue := self.find_error(ctx, 'query aborted (see tombstone_failure_threshold)',
                                        'too many tombstones'):
                issues.append(issue)
        except Exception as e:
            issues.append(self.issue_from_err(sts_name=ctx.statefulset, ns=ctx.namespace, pod_name=ctx.pod, exception=e))

        return CheckResult(self.name(), details, issues)

    def find_error(self, ctx: CheckContext, pattern: str, issue_desc: str):
        ctx_fg = ctx.copy(backgrounded=False, text_color=Color.gray)
        escaped = pattern.replace('"', '\"')
        result = CassandraNodes.exec(ctx.pod, ctx.namespace, f'tac /c3/cassandra/logs/system.log | grep "{escaped}" | head -1', ctx=ctx_fg)
        if result.stdout.find(pattern) > 0:
            return Issue(
                statefulset=ctx.statefulset,
                namespace=ctx.namespace,
                pod=ctx.pod,
                category=self.name(),
                desc=f"node: {ctx.host_id} reported {issue_desc}",
                details=result.stdout.strip(' \r\n'),
                # qing admin restart -n gkeops845 -p cs-d0767a536f-cs-d0767a536f-default-sts-0
                suggestion=f"qing restart {ctx.pod}@{ctx.namespace}"
            )

        return None

    def help(self):
        return f'{Memory().name()}: check current container memory usage and scan system log for an error'