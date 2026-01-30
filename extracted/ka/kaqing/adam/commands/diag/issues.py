from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.commands import extract_options
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_context import Context
from adam.utils_issues import IssuesUtils

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

    def required(self):
        return ReplState.NON_L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, ['-s', '--show']) as (args, show_out):
                results = run_checks(state.sts, state.namespace, state.pod, ctx=Context(show_verbose=show_out))

                issues = CheckResult.collect_issues(results)
                IssuesUtils.show_issues(issues, in_repl=state.in_repl)

                return issues if issues else 'issues'

    def completion(self, state: ReplState):
        return super().completion(state, {'-s': None})

    def help(self, state: ReplState, desc: str = None, args: str = None):
        args1 = args if args else '[-s]'
        return super().help(state, 'find all issues  -s show processing details', args=args1)