"""Failures of a sandbox operation, always raised and never returned as an exit code."""


class SandboxError(Exception):
    """A sandbox operation produced no result, so there is no exit code to read or score.

    A process that runs and fails is not an error: its exit code is the result.
    """

    def __init__(
        self, message: str, status: int | None = None, code: str | None = None, detail: str | None = None
    ) -> None:
        """Retain the HTTP status, protocol code and detail when the sandbox host answered."""
        super().__init__(message)
        self.status = status
        self.code = code
        self.detail = detail
