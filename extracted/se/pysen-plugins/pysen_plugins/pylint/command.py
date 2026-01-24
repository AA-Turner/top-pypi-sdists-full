import pathlib

from pysen import Source, process_utils
from pysen.error_lines import parse_error_lines
from pysen.lint_command import LintCommandBase
from pysen.path import change_dir
from pysen.reporter import Reporter
from pysen.source import PythonFileFilter


class PylintCommand(LintCommandBase):
    def __init__(
        self, base_dir: pathlib.Path, source: Source, settings_path: pathlib.Path
    ) -> None:
        super().__init__(base_dir, source)
        self._source = source
        self._base_dir = base_dir

    @property
    def name(self) -> str:
        return "pylint"

    @property
    def has_side_effects(self) -> bool:
        return False

    def __call__(self, reporter: Reporter) -> int:
        sources = self._source.resolve_files(
            self._base_dir, PythonFileFilter, reporter=reporter
        )
        cmd = [
            "pylint",
            "--msg-template='{abspath}:{line}:{column}: {msg}'",
            "--score=n",
        ]
        cmd.extend(map(str, sources))
        with change_dir(self.base_dir):
            ret, stdout, _ = process_utils.run(cmd, reporter)

        # NOTE(ryo): We cannot control the output of pylint to show only
        # parseable lines, so we optimistically use "/" to determine whether
        # the line contains a parseable error.
        #
        # Example output:
        # ************* Module source
        # /examples/pylint/source.py:1:0: Missing module docstring
        # ************* Module hoge
        # /examples/pylint/hoge.py:1:0: Similar lines in 2 files
        # ==foo:0
        # ==bar:0
        # Class MyClass:
        #     def __init__(self):
        #         self._a = 1
        stdout = "\n".join(line for line in stdout.splitlines() if line.startswith("/"))
        diagnostics = parse_error_lines(stdout, logger=reporter.logger)
        reporter.report_diagnostics(list(diagnostics))

        return ret
