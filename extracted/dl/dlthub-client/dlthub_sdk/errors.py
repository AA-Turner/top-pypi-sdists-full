"""Public exception tree.

Every failure talking to the platform raises a `DlthubError`, so one `except`
catches them. Invalid arguments raise `ValueError` before any request is sent,
and `with` on an async client raises `TypeError`.
"""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from typing import Mapping

# Other libraries
from packaging.version import InvalidVersion, Version

# Current package
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk.version import PKG_NAME, __version__

#: Response header carrying the lowest client version the platform supports.
MIN_CLIENT_VERSION_HEADER = "x-dlthub-min-client-version"


@dataclass(frozen=True)
class FieldError:
    """One reason the platform rejected a request, as it reported it."""

    key: str | None
    """The field at fault, when the platform named one."""
    message: str
    """What is wrong with it."""


@dataclass(frozen=True)
class ClientUpdate:
    """The platform requires a newer ``dlthub-client`` than the one installed."""

    installed: str
    """The version running here."""
    minimum: str
    """The lowest version the platform supports."""

    @classmethod
    def from_headers(cls, headers: Mapping[str, str]) -> ClientUpdate | None:
        """Read the platform's minimum client version off one response.

        Args:
            headers: The response headers, looked up case-insensitively.

        Returns:
            The update, or ``None`` when the installed version is not below the
            advertised minimum, or the response advertised none.
        """
        wanted = next(
            (v for k, v in headers.items() if k.lower() == MIN_CLIENT_VERSION_HEADER),
            None,
        )
        if wanted is None:
            return None
        try:
            if Version(__version__) >= Version(wanted):
                return None
        except InvalidVersion:
            return None
        return cls(installed=__version__, minimum=wanted)

    def __str__(self) -> str:
        return (
            f"Note: {PKG_NAME} {self.installed} is below the platform's supported "
            f"minimum ({self.minimum}) and may be the cause of this error. Upgrade "
            f"it (`uv sync --upgrade-package {PKG_NAME}` or `pip install --upgrade "
            f"{PKG_NAME}`) and restart or redeploy to the dlthub platform."
        )


class DlthubError(Exception):
    """Base for every error raised by the SDK.

    Args:
        message: Human-readable description.
        code: Stable platform error code, when the response carried one. Branch
            on this; ``message`` is prose and may change between releases.
        status: HTTP status the platform returned, when known.
        fields: Per-field reasons, when the platform reported any.
        client_update: Set when the failing response advertised a minimum
            client version above the installed one, a likely cause of the
            failure.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status: int | None = None,
        fields: tuple[FieldError, ...] = (),
        client_update: ClientUpdate | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.fields = fields
        self.client_update = client_update

    def __str__(self) -> str:
        if self.code:
            head = f"{self.message} [{self.code}]"
        elif self.status is not None:
            head = f"{self.message} (HTTP {self.status})"
        else:
            head = self.message
        if self.client_update:
            head = f"{head} {self.client_update}"
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


class DataplaneTokenRejected(NotAuthenticated):
    """The data plane rejected the short-lived token the platform issued for it.

    Your own credential was accepted (it obtained that token), so renewing or
    replacing it will not help. For regular calls the SDK has already fetched a
    fresh token and retried once; uploads are not retried.
    """


class NotAuthorized(DlthubError):
    """The caller is authenticated but lacks the access the call needs.

    `message` says what was missing.
    """


class NotFound(DlthubError):
    """The addressed resource does not exist.

    Args:
        kind: What was looked for.
        ref: The id or name that was not found, or ``None`` when the call
            addressed no particular one.
        code: Stable platform error code, when the response carried one.
        status: HTTP status the platform returned, when known.
        fields: Per-field reasons, when the platform reported any.
        client_update: As for :class:`DlthubError`.
    """

    def __init__(
        self,
        kind: EntityKind,
        ref: str | None = None,
        *,
        code: str | None = None,
        status: int | None = None,
        fields: tuple[FieldError, ...] = (),
        client_update: ClientUpdate | None = None,
    ) -> None:
        super().__init__(
            f"{kind} {ref!r} not found" if ref is not None else f"no {kind} found",
            code=code,
            status=status,
            fields=fields,
            client_update=client_update,
        )
        self.kind = kind
        self.ref = ref


class Conflict(DlthubError):
    """The current state does not allow the call, e.g. the workspace is archived.

    `code` names the reason when the platform gave one (`workspace_archived`,
    `upstream_not_fresh`, ...) and `message` describes it. The set of reasons grows
    with the platform, so branch on `code` rather than on this class alone.
    """


class ApiError(DlthubError):
    """The platform rejected the request or returned an unusable response."""


class BadRequest(ApiError):
    """The request itself was rejected. Retrying it unchanged will fail again.

    `message` says why, `code` names the reason when the platform gave one, and
    `fields` carries the per-field reasons when the platform named any. Also
    raised before sending when an argument cannot form a request, e.g. an id
    that is not a uuid; `status` is then `None`.
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
    """An upload or log stream exceeded its time limit.

    Other requests have no client-side timeout.
    """


class ConnectionFailed(TransportError, ConnectionError):
    """The platform could not be reached."""


class WaitTimeout(DlthubError, TimeoutError):
    """What was awaited had not settled before the deadline. Nothing failed."""


class ScopeMissing(DlthubError, ValueError):
    """The call needs an organization or workspace that was not given.

    For example, `runtime.workspaces.list()` without `organization_id` at
    connect time or as an argument.
    """


class UnboundEntity(DlthubError, AttributeError):
    """The object was constructed directly, so it cannot call the platform.

    Only objects returned by the SDK can. Also an `AttributeError`, so `hasattr`
    keeps working.
    """
