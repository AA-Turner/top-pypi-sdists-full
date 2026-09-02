# Copyright (C) 2018-present Jesus Lara
#
"""FlowTask Exceptions."""


class TaskException(Exception):
    """DataIntegrator Base class for other exceptions."""

    def __init__(self, message: str = None, status: int = 0, **kwargs):
        if isinstance(message, BaseException):
            message = message.message
        super().__init__(message)
        self.stacktrace = None
        if 'stacktrace' in kwargs:
            self.stacktrace = kwargs['stacktrace']
        self.args = kwargs
        self.message = message
        self.status = status

    def __str__(self):
        return f"{self.message}"

    def __repr__(self):
        return f"<{__name__}>: {self.message}"


class FlowTaskError(TaskException):
    """FlowTask Configuration Error."""

    def __init__(self, message: str = None, status: int = 500):
        super().__init__(message or "Configuration Error", status)


class ParserError(TaskException):
    """Simple Task Error."""

    def __init__(self, message: str = None, status: int = 400):
        super().__init__(message or "Task Parse Error", status)


class TaskError(TaskException):
    """Simple Task Error."""

    def __init__(self, message: str = None, status: int = 400):
        super().__init__(message or "Bad request", status)


class NotFound(TaskException):
    """File or Data Not Found."""

    def __init__(self, message: str = None, status: int = 404):
        super().__init__(message or "Not found", status)


class NotSupported(TaskException):
    """Not Supported functionality."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "Not Supported", status)


class TaskNotFound(TaskException):
    """Task was not Found in system."""

    def __init__(self, message: str = None, status: int = 404):
        super().__init__(message or "Task Not found", status)


class TaskParseError(TaskException):
    """Bad Syntax on Task."""

    def __init__(self, message: str = None, status: int = 503):
        super().__init__(message or "Error on Parsing Task", status)


class Unauthorized(TaskException):
    """Task not Authorized."""

    def __init__(self, message: str = None, status: int = 401):
        super().__init__(message or "Unauthorized", status)


class AccessRestricted(TaskException):
    """Access is Restricted."""

    def __init__(self, message: str = None, status: int = 403):
        super().__init__(message or "Unauthorized", status)


class TaskDefinition(TaskException):
    """Error on Task Definition."""

    def __init__(self, message: str = None, status: int = 501):
        super().__init__(message or "Internal Error on Task", status)


class TaskFailed(TaskException):
    """Task failed."""

    def __init__(self, message: str = None, status: int = 500):
        super().__init__(message or "Task Failed", status)


class ComponentError(TaskException):
    """Error on Component Task."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "Component Error", status)


class FileError(TaskException):
    """File Error."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "File Error", status)


class DataError(TaskException):
    """Data Error."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "Data Error", status)


class TimeOutError(TaskException):
    """Timeout Error."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "Timeout Error", status)


class FileNotFound(TaskException):
    """File Doesnt Exists."""

    def __init__(self, message: str = None, status: int = 404):
        super().__init__(message or "File Not found", status)


class EmptyFile(TaskException):
    """File is Empty."""

    def __init__(self, message: str = None, status: int = 404):
        super().__init__(message or "Empty File", status)


class DataNotFound(TaskException):
    """No Data Was found."""

    def __init__(self, message: str = None, status: int = 204):
        super().__init__(message or "Data Not found", status)


class InvalidArgument(Exception):
    """Invalid Argument for Task."""

    def __init__(self, message: str = None):
        super().__init__(message)


class ConfigError(Exception):
    """Invalid Argument for Task."""

    def __init__(self, message: str = None):
        super().__init__(message)


class ActionError(TaskException):
    """Error on Action Task."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "Action Error", status)

    def __str__(self):
        return f"<{__name__}>: {self.message}"


class EventError(TaskException):
    """Error on Event Task."""

    def __init__(self, message: str = None, status: int = 406):
        super().__init__(message or "Event Error", status)

    def __str__(self):
        return f"<{__name__}>: {self.message}"
