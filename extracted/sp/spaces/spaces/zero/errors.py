"""
"""

from typing import TypedDict

from typing_extensions import NotRequired


class ZeroGPUError(TypedDict):
    title: str
    message: str
    traceback: NotRequired[str]


class ZeroGPUException(Exception):
    _title = "ZeroGPU error"

    def __init__(self, message: str):
        super().__init__(message)
        self.detail = ZeroGPUError(title=self._title, message=message)


class ZeroGPUClientError(ZeroGPUException):
    _title = "ZeroGPU client error"


class ZeroGPUQuotaExceeded(ZeroGPUClientError):
    _title = "ZeroGPU quota exceeded"


class ZeroGPUPendingCreditsExceeded(ZeroGPUClientError):
    _title = "ZeroGPU pending credits exceeded"


class ZeroGPUIllegalDuration(ZeroGPUClientError):
    _title = "ZeroGPU illegal duration"


class ZeroGPUQueueTimeout(ZeroGPUClientError):
    _title = "ZeroGPU queue timeout"


class ZeroGPUWorkerError(ZeroGPUException):
    _title = "ZeroGPU worker error"


class ZeroGPUTaskException(ZeroGPUWorkerError):
    def __init__(self, message: str, exception: Exception, traceback: str):
        super().__init__(message)
        self.exception = exception
        self.detail['traceback'] = traceback

    def __reduce__(self):
        assert 'traceback' in self.detail
        return type(self), (self.args[0], self.exception, self.detail['traceback']), self.__dict__


class ZeroGPUTaskAborted(ZeroGPUWorkerError):
    pass
