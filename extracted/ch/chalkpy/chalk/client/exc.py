from __future__ import annotations

from typing import List, Optional

from typing_extensions import Self

import chalk
from chalk.client.models import ChalkError

CHALK_TRACE_ID_KEY = "trace"
_CHALK_TRACE_ID_KEY = CHALK_TRACE_ID_KEY  # for backcompat
_CHALK_TRACE_ID_MESSAGE = "Trace ID:"
_CHALK_TRACE_ID_MISSING = "<trace ID missing>"


class ChalkBaseException(Exception):
    """The base type for Chalk exceptions.

    This exception makes error handling easier, as you can
    look only for this exception class.
    """

    errors: List[ChalkError]
    """The errors from executing a Chalk operation.

    These errors contain more detailed information about
    why the exception occurred.
    """

    def __init__(
        self, errors: Optional[List[ChalkError]] = None, trace_id: Optional[str] = None, detail: Optional[str] = None
    ):
        if errors is None:
            errors = []

        self.errors = errors
        self.trace_id = trace_id
        self.detail = detail

        super().__init__(self.full_message)

    @property
    def message(self) -> str:
        """A message describing the specific type of exception raised."""
        return f"Failed to execute Chalk operation (chalkpy=={chalk.__version__})"

    @property
    def full_message(self) -> str:
        """A message that describes the specific type of exception raised
        and contains the readable representation of each error in the
        errors attribute.

        Also includes the trace ID if one is available.
        """
        msg = self.message

        if self.errors:
            for e in self.errors[:10]:
                if e.display_primary_key:
                    msg += "\n\nPkey associated with error:\n\t"
                    if e.display_primary_key_fqn:
                        msg += f"{e.display_primary_key_fqn}: "
                    msg += f"{e.display_primary_key}"
                msg += f"\n\n{e.message}"
                if e.exception:
                    msg += f"\n{e.exception.stacktrace}"
                    msg += f"\n{e.exception.message}"

        if self.detail:
            msg += f"\n\nAdditional details: \n\t{self.detail}"

        if self.trace_id and _CHALK_TRACE_ID_MESSAGE not in msg:
            msg += f"\n\n{_CHALK_TRACE_ID_MESSAGE}: \n\t{self.trace_id}"

        return msg


class ChalkCustomException(ChalkBaseException):
    def __init__(
        self,
        message: str,
        errors: Optional[List[ChalkError]] = None,
        trace_id: Optional[str] = None,
        detail: Optional[str] = None,
    ):
        self._message = message
        super().__init__(errors=errors, trace_id=trace_id, detail=detail)

    @property
    def message(self) -> str:
        return self._message

    @classmethod
    def from_base(cls, base_exc: ChalkBaseException, message: str) -> Self:
        return cls(
            message=message,
            errors=base_exc.errors,
            trace_id=base_exc.trace_id,
            detail=base_exc.detail,
        )


class ChalkAuthException(ChalkBaseException):
    """Raised when constructing a `ChalkClient` without valid credentials.

    When this exception is raised, no explicit `client_id` and `client_secret`
    were provided, there was no `~/.chalk.yml` file with applicable credentials,
    and the environment variables `CHALK_CLIENT_ID` and `CHALK_CLIENT_SECRET`
    were not set.

    You may need to run `chalk login` from your command line, or check that your
    working directory is set to the root of your project.
    """

    @property
    def message(self):
        return (
            "Explicit `client_id` and `client_secret` are not provided, "
            "there is no `~/.chalk.yml` file with applicable credentials, "
            "and the environment variables `CHALK_CLIENT_ID` and "
            "`CHALK_CLIENT_SECRET` are not set. "
            "You may need to run `chalk login` from your command line, "
            "or check that your working directory is set to the root of "
            "your project."
        )


__all__ = [
    "ChalkBaseException",
    "ChalkCustomException",
    "ChalkAuthException",
]
