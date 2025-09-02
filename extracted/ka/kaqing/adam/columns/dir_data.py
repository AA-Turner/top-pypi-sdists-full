from adam.checks.check_result import CheckResult
from adam.checks.disk import Disk
from adam.columns.column import Column

class DataDir(Column):
    def name(self):
        return 'data'

    def checks(self):
        return [Disk()]

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        r = self.result_by_pod(check_results, pod_name)
        dd = r.details[Disk().name()]

        return dd['data']['size']
        # self.init_check_results(check_results)

        # v = self.r_by_pod[pod_name]
        # print(v)