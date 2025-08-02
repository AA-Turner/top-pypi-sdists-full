from logging import Logger

from qwak.inner.build_logic.build_loggers.trigger_build_logger import TriggerBuildLogger
from qwak.inner.build_logic.interface.build_phase import BuildPhase
from yaspin.core import Yaspin


class CliTriggerBuildLogger(TriggerBuildLogger):
    def __init__(self, logger: Logger, prefix: str, build_phase: BuildPhase, verbose: int = 0,
                 json_logs: bool = False) -> None:
        super().__init__(logger, prefix, build_phase, verbose, json_logs)
        self.spinner = None

    def set_spinner(self, spinner: Yaspin):
        self.spinner = spinner

    def spinner_text(self, line: str) -> None:
        if self.spinner:
            self.spinner.text = f"{self.prefix}{line}"
