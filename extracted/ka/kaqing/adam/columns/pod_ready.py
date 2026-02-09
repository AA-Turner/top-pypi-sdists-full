from adam.checks.check_result import CheckResult
from adam.columns.column import Column

class PodReady(Column):
    def name(self):
        return 'pod_ready'

    def checks(self):
        return []

    def pod_value(self, _: list[CheckResult], pod_ready: str):
        return pod_ready