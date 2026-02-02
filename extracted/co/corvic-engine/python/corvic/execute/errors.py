"""Python sandboxed function errors."""

from corvic.result import Error


class SignaledError(Error):
    """Error raised when sandboxed method execution was interrupted by a signal."""


class ExceptionError(Error):
    """Error raised when sandboxed method execution was interrupted by an exception."""

    def __init__(self, exc: Exception):
        self._exc = exc
        super().__init__("exception raised during sandboxed method execution")

    @property
    def exception(self) -> Exception:
        return self._exc
