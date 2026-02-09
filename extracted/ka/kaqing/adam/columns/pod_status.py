from adam.checks.check_result import CheckResult
from adam.columns.column import Column

class PodStatus(Column):
    def name(self):
        return 'pod_status'

    def checks(self):
        return []

    def pod_value(self, _: list[CheckResult], pod_status: str):
        return pod_status