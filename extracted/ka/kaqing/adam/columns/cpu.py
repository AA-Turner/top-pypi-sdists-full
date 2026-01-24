from kubernetes.utils.quantity import parse_quantity

from adam.checks.check_result import CheckResult
from adam.checks.cpu import Cpu as CpuCheck
from adam.columns.column import Column

class Cpu(Column):
    def name(self):
        return 'cpu'

    def checks(self):
        return [CpuCheck()]

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        r = self.result_by_pod(check_results, pod_name)
        cpu = r.details[CpuCheck().name()]
        busy = 100.0 - float(cpu['idle'])

        return f'{round(busy)}%/{parse_quantity(cpu["limit"]) * 100}%'