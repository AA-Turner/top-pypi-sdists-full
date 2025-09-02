from abc import abstractmethod

from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue

class Check:
    """Abstract base class for checks"""
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def check(self, context: CheckContext) -> CheckResult:
        pass

    @abstractmethod
    def help(self):
        pass

    def issue_from_err(self, sts_name: str, ns: str, pod_name: str, exception: Exception):
        return Issue(
            statefulset=sts_name,
            namespace=ns,
            pod=pod_name,
            category='kaqing',
            desc=f"{exception}"
        )