import click

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import all_checks, checks_from_csv, run_checks
from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.issues import Issues
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log

class Check(Issues):
    COMMAND = 'check'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Check, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Check.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        args, show = Command.extract_options(args, ['-s', '--show'])

        if not args:
            if state.in_repl:
                log(lines_to_tabular([check.help() for check in all_checks()], separator=':'))
            else:
                log('* Check name is missing.')
                Command.display_help()
            return 'arg missing'

        checks = checks_from_csv(args[0])
        if not checks:
            return 'invalid check name'

        results = run_checks(state.sts, state.namespace, state.pod, checks=checks, show_output=show)

        issues = CheckResult.collect_issues(results)
        Issues.show_issues(issues, in_repl=state.in_repl)

        return issues if issues else 'no issues found'

    def completion(self, _: ReplState):
        return {Check.COMMAND: {check.name(): None for check in all_checks()}}

    def help(self, _: ReplState):
        return f'{Check.COMMAND} <check-name>\t run a single check'

class CheckCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Check-names:')

        for check in all_checks():
            log(f'  {check.name()}')
        log()

        ClusterOrPodCommandHelper.cluter_or_pod_help()