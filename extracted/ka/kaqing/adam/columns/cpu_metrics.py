from kubernetes.utils.quantity import parse_quantity

from adam.checks.check_result import CheckResult
from adam.checks.cpu_metrics import CpuMetrics as CpuCheck
from adam.columns.column import Column

class CpuMetrics(Column):
    def name(self):
        return 'cpu-metrics'

    def checks(self):
        return [CpuCheck()]

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        r = self.result_by_pod(check_results, pod_name)
        cpu = r.details[CpuCheck().name()]

        cpu_decimal = parse_quantity(cpu['cpu'])
        cpu_limit = parse_quantity(cpu['limit'])
        business = cpu_decimal * 100 / cpu_limit

        return f"{business:.2f}%({cpu_decimal}/{cpu_limit})"