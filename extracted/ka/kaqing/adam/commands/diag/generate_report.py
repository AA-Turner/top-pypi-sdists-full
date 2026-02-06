import click
import json

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.commands import extract_options
from adam.commands.command import Command
from adam.commands.commands_utils import kaqing_log_file
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_context import Context

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
            with extract_options(args, ['-s', '--show']) as (args, show_out):
                results = run_checks(state.sts, state.namespace, state.pod, ctx=Context(show_verbose=show_out))
                output = CheckResult.report(results)

                if state.in_repl:
                    with kaqing_log_file() as json_file:
                        json.dump(output, json_file, indent=2)
                        log2(f'Report stored in {json_file.name}.')
                else:
                    click.echo(json.dumps(output, indent=2))

                return output

    def completion(self, state: ReplState):
        return super().completion(state, {'-s': None})

    def help(self, state: ReplState):
        return super().help(state, 'generate report  -s show processing details', args='[-s]')