"""Public exception tree.

Everything raised out of the SDK derives from :class:`DlthubError`, so one
``except`` catches the lot. No exception from an underlying HTTP library ever
reaches a caller.
"""

from __future__ import annotations

# Python internals
from dataclasses import dataclass

# Current package
from dlthub_sdk._glue.enums import EntityKind


@dataclass(frozen=True)
class FieldError:
    """One reason the platform rejected a request, as it reported it.

    Attributes:
        key: The field at fault, when the platform named one.
        message: What is wrong with it.
    """

    key: str | None
    message: str


class DlthubError(Exception):
    """Base for every error raised by the SDK.

    Args:
        message: Human-readable description.
        code: Stable platform error code, when the response carried one. Branch
            on this; ``message`` is prose and may change between releases.
        status: HTTP status the platform returned, when known.
        fields: Per-field reasons, when the platform reported any.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status: int | None = None,
        fields: tuple[FieldError, ...] = (),
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.fields = fields

    def __str__(self) -> str:
        if self.code:
            head = f"{self.message} [{self.code}]"
        elif self.status is not None:
            head = f"{self.message} (HTTP {self.status})"
        else:
            head = self.message
        return head + "".join(
            f"\n  {f.key}: {f.message}" if f.key else f"\n  {f.message}"
            for f in self.fields
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(message={self.message!r}, "
            f"code={self.code!r}, status={self.status!r})"
        )


class NotAuthenticated(DlthubError):
    """The credential is missing, malformed, or rejected."""


class NotAuthorized(DlthubError):
    """The caller is authenticated but lacks access to the resource."""


class NotFound(DlthubError):
    """The addressed resource does not exist.

    Args:
        kind: What was looked for.
        ref: The id or name that was not found, or ``None`` when the call
            addressed no particular one.
        code: Stable platform error code, when the response carried one.
        status: HTTP status the platform returned, when known.
        fields: Per-field reasons, when the platform reported any.
    """

    def __init__(
        self,
        kind: EntityKind,
        ref: str | None = None,
        *,
        code: str | None = None,
        status: int | None = None,
        fields: tuple[FieldError, ...] = (),
    ) -> None:
        super().__init__(
            f"{kind} {ref!r} not found" if ref is not None else f"no {kind} found",
            code=code,
            status=status,
            fields=fields,
        )
        self.kind = kind
        self.ref = ref


class Conflict(DlthubError):
    """The resource is not in a state that allows the operation."""


class ApiError(DlthubError):
    """The platform rejected the request or returned an unusable response."""


class BadRequest(ApiError):
    """The request itself was rejected. Retrying it unchanged will fail again.

    ``fields`` carries the per-field reasons when the platform named any.
    """


class ServerError(ApiError):
    """The platform failed to handle the request. Retrying may succeed."""


class InvalidResponse(ApiError):
    """A response did not parse, or broke an invariant the SDK depends on."""


class TransportError(DlthubError):
    """The request never produced a response.

    Nothing was applied platform-side only if the request never arrived, which
    this error cannot distinguish — treat a mutation as of unknown outcome.
    """


class TransportTimeout(TransportError, TimeoutError):
    """The request took longer than the transport allows."""


class ConnectionFailed(TransportError, ConnectionError):
    """The platform could not be reached."""


class WaitTimeout(DlthubError, TimeoutError):
    """What was awaited had not settled before the deadline. Nothing failed."""


class ScopeMissing(DlthubError, ValueError):
    """An operation needed a scope the context does not carry."""


class UnboundEntity(DlthubError, AttributeError):
    """An entity was constructed directly and carries no context.

    An ``AttributeError`` too, so ``hasattr`` keeps working.
    """
