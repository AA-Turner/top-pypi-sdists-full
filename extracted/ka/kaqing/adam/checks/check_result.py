from adam.checks.issue import Issue

class CheckResult:
    def __init__(self, name: str, details: any = None, issues: list[Issue] = None):
        self.name = name
        self.details = details
        self.issues = issues

    def collect_details(results: list['CheckResult']):
        return [r.details for r in results]

    def collect_issues(results: list['CheckResult']) -> list[Issue]:
        return sum([r.issues for r in results], [])

    def report(results: list['CheckResult']):
        return {
            'checks': CheckResult.collect_details(results),
            'issues': [issue.to_dict() for issue in CheckResult.collect_issues(results)]
        }