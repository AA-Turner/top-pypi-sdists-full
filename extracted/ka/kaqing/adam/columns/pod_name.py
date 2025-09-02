from adam.checks.check_result import CheckResult
from adam.columns.column import Column

class PodName(Column):
    def name(self):
        return 'pod'

    def checks(self):
        return []

    def pod_value(self, _: list[CheckResult], pod_name: str):
        return pod_name