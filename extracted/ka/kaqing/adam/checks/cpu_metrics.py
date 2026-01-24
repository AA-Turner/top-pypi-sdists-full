from kubernetes.utils import parse_quantity

from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.config import Config
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils_k8s.pods import Pods

class CpuMetrics(Check):
    def name(self):
        return 'cpu-metrics'

    def check(self, ctx: CheckContext) -> CheckResult:
        issues: list[Issue] = []

        details = {
            'name': ctx.pod,
            'namespace': ctx.namespace,
            'statefulset': ctx.statefulset,
            'cpu': 'Unknown',
            'limit': 'NA'
        }

        try:
            container = Pods.get_container(ctx.namespace, ctx.pod, container_name='cassandra')
            if container.resources.limits and "cpu" in container.resources.limits:
                details['limit'] = container.resources.limits["cpu"]

            metrics = CustomResources.get_metrics(ctx.namespace, ctx.pod, container_name='cassandra')
            usage = 'Unknown'
            if metrics:
                usage = details['cpu'] = metrics["usage"]["cpu"]

            cpu_threshold = Config().get('checks.cpu-threshold', 0.0)
            if  cpu_threshold != 0.0 and usage != "Unknown" and parse_quantity(usage) > cpu_threshold:
                issues.append(Issue(
                    statefulset=ctx.statefulset,
                    namespace=ctx.namespace,
                    pod=ctx.pod,
                    category='cpu',
                    desc=f'CPU is too busy: {usage}',
                    suggestion=f"qing restart {ctx.pod}@{ctx.namespace}"
                ))
        except Exception as e:
            issues.append(self.issue_from_err(sts_name=ctx.statefulset, ns=ctx.namespace, pod_name=ctx.pod, exception=e))

        return CheckResult(self.name(), details, issues)

    def help(self):
        return f'{CpuMetrics().name()}: check cpu busy percentage with metrics'