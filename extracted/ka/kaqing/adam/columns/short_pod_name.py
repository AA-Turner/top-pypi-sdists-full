from adam.checks.check_result import CheckResult
from adam.columns.column import Column
from adam.utils_k8s.pods import strip_pod_name

class ShortPodName(Column):
    def name(self):
        return 'short-pod'

    def checks(self):
        return []

    def pod_value(self, _: list[CheckResult], pod_name: str):
        pod_name = strip_pod_name(pod_name)
        return pod_name