from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.repl_session import ReplSession
from adam.utils import log, tabulize, log2

class IssuesUtils:
    def show(check_results: list[CheckResult], in_repl = False, to: int = 2) -> str:
        return IssuesUtils.show_issues(CheckResult.collect_issues(check_results), in_repl=in_repl, to=to)

    def show_issues(issues: list[Issue], in_repl = False, to: int = 2):
        lines = []

        def show_line(s: str = ''):
            if to == 1:
                log(s)
            elif to == 2:
                log2(s)
            else:
                lines.append(s)

        if not issues:
            show_line('No issues found.')
        else:
            suggested = 0
            show_line(f'* {len(issues)} issues found.')
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
            r = tabulize(lines, separator='||', to=to)
            if to == 0:
                show_line(r)
            if suggested:
                show_line()
                show_line(f'* {suggested} suggested commands are added to history. Press <Up> arrow to access them.')

        return '\n'.join(lines)