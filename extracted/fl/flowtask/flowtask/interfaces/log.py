from abc import ABC
from enum import Enum
import traceback
from navconfig.logging import logging
from ..utils import cPrint
from ..exceptions import ComponentError

### TODO: Adding functions for Raising Errors.
class SkipErrors(Enum):
    SKIP = "skip"
    LOG = "log_only"
    ENFORCE = None

    def __str__(self):
        return {
            SkipErrors.SKIP: "skip",
            SkipErrors.LOG: "Log Errors",
            SkipErrors.ENFORCE: "Enforce",
        }[self]

class LogSupport(ABC):
    """LogSupport.

    Adding Logging support to every FlowTask Component.
    """

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__)
        self.skipError: SkipErrors = SkipErrors.ENFORCE
        # logging object
        self._logger = logging.getLogger(
            f"FlowTask.Component.{self._name}"
        )
        # Debugging
        self._debug: bool = kwargs.get('debug', False)
        if self._debug:
            self._logger.setLevel(logging.DEBUG)
        super().__init__(*args, **kwargs)

    def log(self, message) -> None:
        self._logger.info(message)
        if self._debug is True:
            cPrint(message, level="INFO")

    def debug(self, message):
        self._logger.debug(message)
        if self._debug is True:
            cPrint(message, level="DEBUG")

    def warning(self, message):
        self._logger.warning(message)
        if self._debug is True:
            cPrint(message, level="WARN")

    def exception(self, message):
        self._logger.exception(message, stack_info=True)
        if self._debug is True:
            cPrint(message, level="CRITICAL")

    def echo(self, message: str, level: str = "INFO") -> None:
        cPrint(message, level=level)

    def error(
        self,
        message: str,
        exc: BaseException,
        status: int = 400,
        stacktrace: bool = False,
    ):
        payload = None
        if stacktrace is True:
            payload = traceback.format_exc()
        raise ComponentError(
            f"{message}, error={exc}", status=status, stacktrace=payload
        ) from exc
