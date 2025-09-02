from adam.checks.check_result import CheckResult
from adam.checks.status import Status
from adam.columns.column import Column
from adam.columns.host_id import HostId
from adam.columns.node_utils import merge_gossip

class Gossip(Column):
    def name(self):
        return 'gossip'

    def checks(self):
        return [Status()]

    def host_value(self, check_results: list[CheckResult], status: dict[str, any]):
        if not hasattr(self, 'hosts_with_gossip_issue'):
            self.hosts_with_gossip_issue = merge_gossip(check_results)

        host = status[HostId().name()]

        return 'DOWN' if host in self.hosts_with_gossip_issue else 'UP'