from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.checks.issue import Issue
from adam.commands.command import Command
from adam.repl_session import ReplSession
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log, log2

class Issues(Command):
    COMMAND = 'issues'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Issues, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Issues.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        args, show = Command.extract_options(args, ['-s', '--show'])

        results = run_checks(state.sts, state.namespace, state.pod, show_output=show)

        issues = CheckResult.collect_issues(results)
        Issues.show_issues(issues, in_repl=state.in_repl)

        return issues if issues else 'issues'

    def show(check_results: list[CheckResult], in_repl = False):
        Issues.show_issues(CheckResult.collect_issues(check_results), in_repl=in_repl)

    def show_issues(issues: list[Issue], in_repl = False):
        if not issues:
            log2('No issues found.')
        else:
            suggested = 0
            log2(f'* {len(issues)} issues found.')
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
            log(lines_to_tabular(lines, separator='||'))
            if suggested:
                log2()
                log2(f'* {suggested} suggested commands are added to history. Press <Up> arrow to access them.')

    def completion(self, _: ReplState):
        return {Issues.COMMAND: None}

    def help(self, _: ReplState):
        return f'{Issues.COMMAND}\t find all issues'