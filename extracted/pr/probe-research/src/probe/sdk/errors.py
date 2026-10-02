"""SDK exceptions mapped from the Probe Research error contract.

The API returns a FastAPI envelope ``{"detail": <string | object>}``. 409 carries
an object ``{message, existing_id, suggestion?, deleted?}``; everything else is a
string or a validation error list. See ``CONTRACT.md`` (Error contract).
"""

from __future__ import annotations

from typing import Any


class RosError(Exception):
    """Base for every client error."""

    #: Seconds the server asked us to wait before trying again (its
    #: ``Retry-After`` header), or None when it named none. A class default so
    #: every subclass -- including the ones built with their own signatures --
    #: carries it; the transport sets it on the instance it raises.
    retry_after: float | None = None

    def __init__(self, message: str, *, status: int | None = None, detail: Any = None):
        super().__init__(message)
        self.status = status
        self.detail = detail


class TransportError(RosError):
    """Network failure, timeout, or unreachable host (no HTTP status).

    ``unreachable`` is True when the request never reached the server (a
    connect failure or timeout), as opposed to a response that was lost."""

    unreachable: bool = False


class DeadlineExceeded(TransportError):
    """A caller's deadline ran out before this request could be (fully) sent.

    Raised by the transport inside a :func:`probe.sdk.transport.deadline_scope`
    -- today only `Run.finish()`'s close budget. It says nothing about the
    SERVER: the request was never attempted, or was cut short by our own clock.
    So the outbox drain stops its pass on it WITHOUT charging the op an
    attempt, and the op keeps its place and its failure history for the
    detached worker. A TransportError subclass so every existing
    ``except TransportError`` still reads it as "not delivered, try later".

    ``sent`` is True when the request had fully left and only the RESPONSE was
    cut short: the server may have applied it, so the drain records the
    attempt (a replayed create whose 409 carries ``existing_id`` is then read
    as its own earlier delivery, not a conflict).
    """

    def __init__(self, message: str, *, sent: bool = False):
        super().__init__(message)
        self.sent = sent


class OfflineRunNotCreated(RosError):
    """An op of an OFFLINE run (plan 2.12) reached the drain before its run
    exists on the server: the run's create op has not been delivered (it is
    still queued, or was refused and sits in ``failed/``). Not the op's fault,
    so the drain stops the pass without charging it an attempt; ``probe sync``
    names the fix."""


class AuthError(RosError):
    """401 - missing / invalid / revoked / expired credential, or membership gone."""


class UnroutableEndpointError(AuthError):
    """A queued op is pinned to an endpoint no credential here can satisfy.

    NOT "log in and this works": the op was recorded against an endpoint the
    named context does not name -- a local test server on an ephemeral port,
    another tenant's context that was since removed -- so no login for the
    CURRENT context can ever produce a credential for it, and refusing to send
    this context's token to that host is the point (a token issued for
    endpoint A must not reach pinned host B).

    An AuthError subclass so every `except AuthError` still catches it, and a
    distinct type so `classify` can call it permanent rather than parking the
    whole queue behind an op that will never move.
    """


class ScopeError(RosError):
    """403 - valid credential but insufficient scope/role."""


#: The server marks a workspace-write refusal with this in `detail.code`. A bare
#: 403 cannot be told apart from "this token lacks the write scope", and the two
#: need OPPOSITE handling -- see WorkspaceLockedError.
WORKSPACE_WRITE_DENIED = "workspace_write_denied"

#: The server marks a refused generation press with this in a 409's
#: `detail.code`: the team's page generation is switched off (research-os 0245),
#: so NOTHING was queued. A definite answer, unlike a lost acknowledgement.
GENERATION_PAUSED = "generation_paused"


class WorkspaceLockedError(ScopeError):
    """403 - the credential is fine; this WORKSPACE restricts who may edit it.

    THE DISTINCTION IS THE WHOLE POINT, and it is about the outbox rather than
    about the message. Every other 403 means the credential is wrong, so the
    drainer parks the queue and keeps the data -- re-sending with the same token
    would only fail again. This one means one DESTINATION is closed to this
    person: the credential is good, every other queued op is unaffected, and
    parking on it would stall a researcher's entire upload backlog behind one
    file bound for a workspace they are not on.

    So `classify` calls it permanent (dead-letter this op, keep draining) the
    same way `UnroutableEndpointError` is, and for the same reason: an op that
    can never move must not stop the ones that can. `probe outbox status` shows
    it; `probe outbox retry` re-queues it once access is granted.

    A ScopeError subclass so every `except ScopeError` still catches it.
    """

    @property
    def workspace_name(self) -> str | None:
        return (self.detail or {}).get("workspace_name") if isinstance(self.detail, dict) else None


class UploadRefused(RosError):
    """401/403 from a presigned upload URL: the upload's own signed capability
    was refused, never this machine's credential.

    A presigned PUT carries no Authorization header -- the URL, or its
    capability header, is the authorization -- so its refusal says nothing
    about the login: the capability expired, or it was minted by a server
    other than the one that answered. The second is #2073: a self-host install
    whose `public_base_url` still named Probe's hosted API handed out upload
    URLs there, and reading each refusal as a refused credential paused every
    write of the run. The outbox classifies this permanent: THIS upload fails
    and is recorded as failed; the queue goes on.

    Deliberately NOT an AuthError or ScopeError subclass: every
    `except AuthError` means "the credential is wrong", and this is not that.
    """


class NotFoundError(RosError):
    """404 - absent, other-tenant, or already deleted."""


class ConflictError(RosError):
    """409 - natural-key conflict, or a delete blocked because a published
    experiment version pins something in the subtree. The detail is an object;
    the useful fields are surfaced as attributes."""

    def __init__(self, message: str, *, detail: Any = None):
        super().__init__(message, status=409, detail=detail)
        self.existing_id: str | None = None
        self.suggestion: str | None = None
        self.deleted: bool = False
        if isinstance(detail, dict):
            self.existing_id = detail.get("existing_id")
            self.suggestion = detail.get("suggestion")
            self.deleted = bool(detail.get("deleted", False))


class LimitReachedError(RosError):
    """402 - the create was refused by a plan cap.

    A REFUSAL, not a failure: the request was valid, the credential was fine, and
    the same call will succeed once the tenant is on a paid plan or frees budget
    by deleting something. Retrying unchanged never helps, which is why this is
    its own class rather than a generic 4xx -- a caller with a retry loop needs to
    be able to tell it apart from the transient statuses without matching on a
    message.

    The detail object is contract surface (``CONTRACT.md``); the useful fields
    are surfaced as attributes, as with ``ConflictError``.
    """

    def __init__(self, message: str, *, detail: Any = None):
        super().__init__(message, status=402, detail=detail)
        self.limit: str | None = None
        self.current: int | None = None
        self.maximum: int | None = None
        self.plan: str | None = None
        #: Absent when the deployment configures no booking URL (self-host).
        self.booking_url: str | None = None
        if isinstance(detail, dict):
            self.limit = detail.get("limit")
            self.current = detail.get("current")
            self.maximum = detail.get("maximum")
            self.plan = detail.get("plan")
            self.booking_url = detail.get("booking_url")


#: The server marks a refusal that a newer client would not have received with
#: this in the body's top-level `code` (a retired route's 410), beside
#: `min_version`. Keyed on the CODE and never the status: the trash answers 410
#: too, and "upgrade" is the wrong thing to tell someone whose run is in it.
CLIENT_TOO_OLD = "client_too_old"


class ClientTooOldError(RosError):
    """The server retired what this client asked for; a newer release speaks it.

    Raised as-is where the caller is waiting (``probe.init()``, a CLI command).
    In the outbox it is permanent: the op dead-letters instead of retrying,
    because resending the same request from the same client can never succeed.
    ``min_version`` is the release that fixes it, when the server named one.
    """

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        detail: Any = None,
        min_version: str | None = None,
    ):
        super().__init__(message, status=status, detail=detail)
        self.min_version = min_version


class ValidationError(RosError):
    """422 - request validation (missing question, caps, malformed cursor, ...)."""


class ServerError(RosError):
    """5xx - the API or a database is down / behind schema."""


class CapabilityUnavailable(RosError):
    """A client surface exists but the deployed backend lacks the capability."""

    def __init__(self, capability: str, message: str | None = None):
        self.capability = capability
        super().__init__(message or f"Probe Research capability is unavailable: {capability}")


_BY_STATUS: dict[int, type[RosError]] = {
    401: AuthError,
    403: ScopeError,
    404: NotFoundError,
    402: LimitReachedError,
    409: ConflictError,
    422: ValidationError,
}

#: Statuses whose class promotes fields off an object detail and therefore takes
#: ``(message, *, detail)`` instead of the base ``(message, *, status, detail)``.
_OBJECT_DETAIL_STATUSES = frozenset({402, 409})


def _detail_message(detail: Any) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, dict):
        return str(detail.get("message") or detail)
    return str(detail)


def error_for(status: int, detail: Any) -> RosError:
    """Build the right exception for an HTTP status + parsed ``detail``."""
    # BEFORE the status table: a workspace-write refusal is a 403 whose meaning
    # is per-DESTINATION, not per-credential, and only `detail.code` separates
    # the two. Branching on the code rather than the status is what stops one
    # closed workspace from parking a whole outbox.
    if (
        status == 403
        and isinstance(detail, dict)
        and detail.get("code") == WORKSPACE_WRITE_DENIED
    ):
        return WorkspaceLockedError(_detail_message(detail), status=403, detail=detail)
    if status in _OBJECT_DETAIL_STATUSES:
        cls = _BY_STATUS[status]
        return cls(_detail_message(detail), detail=detail)  # type: ignore[call-arg]
    cls = _BY_STATUS.get(status)
    if cls is None:
        cls = ServerError if status >= 500 else RosError
    return cls(_detail_message(detail), status=status, detail=detail)


class UnfilteredListing(RosError):
    """A ``?slug=`` lookup came back unfiltered, so a MISS proves nothing.

    FastAPI silently DROPS a query parameter a route does not declare, so an
    engine predating the filter answers an unfiltered first page. ``_exactly``
    degrades that to "absent", which is right for get-or-create and wrong for
    anything deciding whether a UUID-shaped ref is an id: there, "not a slug" is
    the premise the whole decision rests on.

    Detected by row count -- the one signal that survives the drop, since an
    exact match on a UNIQUE column returns 0 or 1.
    """

