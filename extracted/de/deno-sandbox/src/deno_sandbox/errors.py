from typing import TypedDict


class AuthenticationError(Exception):
    """Raised when there is an authentication error."""

    pass


class MissingApiToken(Exception):
    """Raised when an API token is missing."""

    pass


class UnknownRpcMethod(Exception):
    """Raised when an unknown RPC method is called."""

    pass


class ProcessAlreadyExited(Exception):
    """Raised when trying to interact with a process that has already exited."""

    pass


class HTTPStatusError(Exception):
    """Raised when an HTTP request returns a non-success status code."""

    def __init__(
        self,
        status_code: int,
        message: str,
        code: str = "UNKNOWN_ERROR",
        trace_id: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.code = code
        self.trace_id = trace_id

        detail = f"status: {status_code}, code: {code}"
        if trace_id:
            detail += f", traceId: {trace_id}"
        super().__init__(f"{message} ({detail})")


class ZodErrorRaw(TypedDict):
    expected: str
    code: str
    path: list[str]
    message: str


class RpcValidationError(ValueError):
    """Raised when there is a validation error in RPC parameters."""

    def __init__(self, errors: list[ZodErrorRaw]) -> None:
        self.errors = errors

        msg = "Invalid Parameters:\n"
        for err in errors:
            msg += f"- Path: {'.'.join(err['path'])}, Expected: {err['expected']}\n"

        super().__init__(msg)
