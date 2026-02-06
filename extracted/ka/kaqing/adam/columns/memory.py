from kubernetes.utils import parse_quantity

from adam.checks.check_result import CheckResult
from adam.checks.memory import Memory as MemoryCheck
from adam.columns.column import Column
from adam.utils import log_exc

class Memory(Column):
    def name(self):
        return 'mem'

    def checks(self):
        return [MemoryCheck()]

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        r = self.result_by_pod(check_results, pod_name)
        mem = r.details[MemoryCheck().name()]

        return f"{Memory.to_g(mem['used'])}/{Memory.to_g(mem['limit'])}"

    def to_g(v: str):
        with log_exc():
            return f'{round(parse_quantity(v) / 1024 / 1024 / 1024, 2)}G'