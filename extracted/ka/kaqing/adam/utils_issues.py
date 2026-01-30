from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.repl_session import ReplSession
from adam.utils import _log, log, tabulize, log2

class IssuesUtils:
    def show(check_results: list[CheckResult], in_repl = False, log_file: str = None, err = False) -> str:
        return IssuesUtils.show_issues(CheckResult.collect_issues(check_results), in_repl=in_repl, log_file = log_file, err = err)

    def show_issues(issues: list[Issue], in_repl = False, log_file: str = None, err = False):
        lines = []

        if not issues:
            _log('No issues found.', file = log_file, err = err)
        else:
            suggested = 0
            _log(f'* {len(issues)} issues found.', file = log_file, err = err)
            lines = []
            for i, issue in enumerate(issues, start=1):
                lines.append(f"{i}||{issue.category}||{issue.desc}")
                lines.append(f"||statefulset||{issue.statefulset}@{issue.namespace}")
                lines.append(f"||pod||{issue.pod}@{issue.namespace}")
                if issue.details:
                    lines.append(f"||details||{issue.details}")

                if issue.suggestion:
                    lines.append(f'||suggestion||{issue.suggestion}')
                    if in_repl:
                        ReplSession().prompt_session.history.append_string(issue.suggestion)
                        suggested += 1
            tabulize(lines, separator='||', log_file=log_file, err=err)
            if suggested:
                _log(file = log_file, err = err)
                _log(f'* {suggested} suggested commands are added to history. Press <Up> arrow to access them.', file = log_file, err = err)

        return '\n'.join(lines)