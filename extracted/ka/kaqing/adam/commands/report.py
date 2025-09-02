import click
import json

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log2

class Report(Command):
    COMMAND = 'report'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Report, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Report.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        output: dict[str, any] = {}
        state, args = self.apply_state(args, state)
        if state.in_repl:
            args, show = Command.extract_options(args, ['-s', '--show'])

            args, redirect = Command.extract_options(args, ['>'])
            if not redirect or not args:
                log2('Please specify file name: e.g. report > /tmp/report.log')
                return 'no-report-destination'

            results = run_checks(state.sts, state.namespace, state.pod, show_output=show)
            output = CheckResult.report(results)
            with open(args[0], "w") as json_file:
                json.dump(output, json_file, indent=2)
                log2(f'Report stored in {args[0]}.')
        else:
            args, show = Command.extract_options(args, ['-s', '--show'])

            results = run_checks(state.sts, state.namespace, state.pod, show_output=show)
            output = CheckResult.report(results)
            click.echo(json.dumps(output, indent=2))

        return output

    def completion(self, _: ReplState):
        return {Report.COMMAND: {">": None}}

    def help(self, _: ReplState):
        return f"{Report.COMMAND} > <file-name>\t generate report"