from adam.checks.check_result import CheckResult
from adam.checks.disk import Disk
from adam.columns.column import Column

class RootVolume(Column):
    def name(self):
        return 'volume_root'

    def checks(self):
        return [Disk()]

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        self.init_check_results(check_results)

        r = self.r_by_pod[pod_name]
        dd = r.details[Disk().name()]
        root = dd['devices']['/']
        fr = f"{root['per']}({root['used']}/{root['total']})"

        return fr