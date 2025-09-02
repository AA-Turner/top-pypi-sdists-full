from adam.checks.check_result import CheckResult
from adam.checks.compactionstats import CompactionStats
from adam.columns.column import Column
from adam.columns.host_id import HostId
from adam.columns.node_utils import merge_compactions

class Compactions(Column):
    def name(self):
        return 'compactions'

    def checks(self):
        return [CompactionStats()]

    def pod_value(self, check_results: list[CheckResult], pod_name: str):
        r = self.result_by_pod(check_results, pod_name)
        cd = r.details[CompactionStats().name()]

        return cd['compactions']

    def host_value(self, check_results: list[CheckResult], status: dict[str, any]):
        if not hasattr(self, 'compactions_by_host'):
            self.compactions_by_host = merge_compactions(check_results)

        host = status[HostId().name()]
        return self.compactions_by_host[host] if host in self.compactions_by_host else 'NA'