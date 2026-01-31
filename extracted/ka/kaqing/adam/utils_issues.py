from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.repl_session import ReplSession
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

class IssuesUtils:
    def show(check_results: list[CheckResult], in_repl = False, err = False, ctx: Context = Context.NULL) -> str:
        return IssuesUtils.show_issues(CheckResult.collect_issues(check_results), in_repl=in_repl, err = err, ctx=ctx)

    def show_issues(issues: list[Issue], in_repl = False, err = False, ctx: Context = Context.NULL):
        lines = []

        if not issues:
            ctx._log('No issues found.', err = err)
        else:
            suggested = 0
            ctx._log(f'* {len(issues)} issues found.', err = err)
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
            tabulize(lines,
                     separator='||',
                     err=err,
                     ctx=ctx)
            if suggested:
                ctx._log(err = err)
                ctx._log(f'* {suggested} suggested commands are added to history. Press <Up> arrow to access them.', err = err)

        return '\n'.join(lines)