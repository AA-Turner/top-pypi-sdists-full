import logging
from logging import Logger

from qwak.inner.build_logic.interface.build_logger_interface import BuildLogger
from qwak.inner.build_logic.interface.build_phase import BuildPhase
from yaspin.core import Yaspin


PREFIX_FORMAT = "{prefix} - "
EXCEPTION_FORMAT = """Message: {line}
Exception: {e}
"""


class TriggerBuildLogger(BuildLogger):
    def __init__(
        self, logger: Logger, prefix: str, build_phase: BuildPhase, verbose: int = 0, json_logs: bool = False,
    ) -> None:
        self.logger = logging.LoggerAdapter(
            logger,
            {
                "phase": build_phase.description,
                "phase_id": build_phase.phase_id,
            },
        )
        self.prefix = PREFIX_FORMAT.format(prefix=prefix) if prefix else ""
        self.spinner = None
        self.verbose = verbose
        self.json_logs = json_logs

    def set_spinner(self, spinner: Yaspin):
        self.spinner = spinner

    def exception(self, line: str, e: BaseException) -> None:
        self.logger.error(
            EXCEPTION_FORMAT.format(line=line, e=e),
            exc_info=False,
        )

    def error(self, line: str) -> None:
        self.logger.error(f"{self.prefix}{line}")

    def warning(self, line: str) -> None:
        self.logger.warning(f"{self.prefix}{line}")

    def info(self, line: str) -> None:
        self.logger.info(f"{self.prefix}{line}")

    def debug(self, line: str) -> None:
        self.logger.debug(f"{self.prefix}{line}")

    def spinner_text(self, line: str) -> None:
        if self.spinner:
            self.spinner.text = f"{self.prefix}{line}"
