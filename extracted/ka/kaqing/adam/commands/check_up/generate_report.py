import click
import json

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_log import kaqing_log_file, log2
from adam.utils_cassandra.cassandra_status import CassandraStatus

class GenerateReport(Command):
    COMMAND = 'generate report'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(GenerateReport, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return GenerateReport.COMMAND

    def required(self):
        return ReplState.NON_L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                results = run_checks(state.sts,
                                     state.namespace,
                                     state.pod,
                                     status=CassandraStatus.snapshot(state, ctx=ctx),
                                     ctx=ctx)
                output = CheckResult.report(results)

                if state.in_repl:
                    with kaqing_log_file() as json_file:
                        json.dump(output, json_file, indent=2)
                        log2(f'Report stored in {json_file.name}.')
                else:
                    click.echo(json.dumps(output, indent=2))

                return output

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'generate report')