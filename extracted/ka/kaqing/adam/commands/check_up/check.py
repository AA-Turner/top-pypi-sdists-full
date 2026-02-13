import click

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import all_checks, checks_from_csv, run_checks
from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.check_up.issues import Issues
from adam.repl_state import ReplState
from adam.utils_log import log
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_tabulize import tabulize
from adam.commands.check_up.utils_issues import IssuesUtils

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

    def required(self):
        return ReplState.NON_L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with validate_args(args,
                                    state,
                                    name='check name',
                                    msg=lambda: tabulize([check.help() for check in all_checks()], separator=':')) as arg:
                    checks = checks_from_csv(args[0])
                    if not checks:
                        return 'invalid check name'

                    results = run_checks(state.sts,
                                         state.namespace,
                                         state.pod,
                                         checks=checks,
                                         status=CassandraStatus.snapshot(state, ctx=ctx),
                                         ctx=ctx)

                    issues = CheckResult.collect_issues(results)
                    IssuesUtils.show_issues(issues, in_repl=state.in_repl, ctx=ctx)

                    return issues if issues else 'no issues found'

    def completion(self, _: ReplState):
        return {Check.COMMAND: {check.name(): None for check in all_checks()}}

    def help(self, state: ReplState):
        return super().help(state, 'run a single check', args='<check-name>')

class CheckCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Check-names:')

        for check in all_checks():
            log(f'  {check.name()}')
        log()

        ClusterOrPodCommandHelper.cluter_or_pod_help()