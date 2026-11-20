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
    print_exception = False

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


class ZeroGPUSerializationError(ZeroGPUWorkerError):
    """
    Pickling errors happen on the sending side and unpickling ones on the receiving side
    Arguments, send and throw values go to the worker. Yield and return values and exceptions come from it
    Worker side ones have their traceback printed by the worker. Main process ones rely on `print_exception`
    """
    _title = "ZeroGPU serialization error"
    _action: str

    def __init__(self, task: str, traceback: str):
        super().__init__(f"Error while {self._action} `{task}` task")
        self.task = task
        self.traceback = traceback
        self.detail['traceback'] = traceback

    def __reduce__(self):
        return type(self), (self.task, self.traceback)


class ZeroGPUArgsPicklingError(ZeroGPUSerializationError):
    _action = "pickling arguments for"
    print_exception = True


class ZeroGPUArgsUnpicklingError(ZeroGPUSerializationError):
    _action = "unpickling arguments for"


class ZeroGPUSendValuePicklingError(ZeroGPUSerializationError):
    _action = "pickling send value for"
    print_exception = True


class ZeroGPUThrowValuePicklingError(ZeroGPUSerializationError):
    _action = "pickling throw value for"
    print_exception = True


class ZeroGPUYieldValuePicklingError(ZeroGPUSerializationError):
    _action = "pickling yield value from"


class ZeroGPUReturnValuePicklingError(ZeroGPUSerializationError):
    _action = "pickling return value from"


class ZeroGPUExceptionPicklingError(ZeroGPUSerializationError):
    _action = "pickling exception from"


class ZeroGPUInputUnpicklingError(ZeroGPUSerializationError):
    _action = "unpickling value for"


class ZeroGPUOutputUnpicklingError(ZeroGPUSerializationError):
    _action = "unpickling value from"
    print_exception = True
