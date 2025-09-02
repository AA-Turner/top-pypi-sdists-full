from abc import abstractmethod

from adam.checks.check_result import CheckResult

class Column:
    @abstractmethod
    def name(self):
        pass

    def checks(self):
        return []

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        return None

    def host_value(self, check_results: list[CheckResult], status: dict[str, any]):
        return status[self.name()]

    def result_by_pod(self, check_results: list[CheckResult], pod_name: str):
        self.init_check_results(check_results)

        return self.r_by_pod[pod_name]

    def init_check_results(self, check_results: list[CheckResult]):
        if hasattr(self, 'r_by_pod'):
            return

        self.r_by_pod: dict[str, CheckResult] = {}
        for r in check_results:
            for v in r.details.values():
                if v['name']:
                    key = v['name']
                    self.r_by_pod[key] = r
                    break