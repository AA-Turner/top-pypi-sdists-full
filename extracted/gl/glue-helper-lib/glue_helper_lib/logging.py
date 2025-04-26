import logging
import typing
import enum
import sys


class LogLevel(enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger(logging.Logger):
    """Logger for AWS glue that puts the logs into the 'output'
    cloudwatch logs of a Glue job.

    Args:
        name: name of the logger
        level: minimum log level of log statements that are logged
        formatter: Format for the log messages: defaults to
            <time - name - [level] - message>
    """

    def __init__(
        self,
        name: str,
        level: LogLevel,
        formatter: typing.Optional[logging.Formatter] = None,
    ) -> None:
        super().__init__(name, level.value)
        self._configure(formatter)

    def _configure(self, formatter: typing.Optional[logging.Formatter]):
        handler = logging.StreamHandler(sys.stdout)
        if not formatter:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
            )
        handler.setFormatter(formatter)
        self.addHandler(handler)
