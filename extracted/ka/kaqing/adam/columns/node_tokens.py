from adam.checks.check_result import CheckResult
from adam.checks.status import Status
from adam.columns.column import Column

class NodeTokens(Column):
    def name(self):
        return 'tokens'

    def checks(self):
        return [Status()]

    def host_value(self, _: list[CheckResult], status: dict[str, any]):
        return status[self.name()]