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
    #: True when the server answered with its TRASH notice (410 `in_trash`): the
    #: thing asked for exists and is in the trash. The transport sets it; the
    #: detail itself is the notice sentence by then, so this is how a caller
    #: tells "in the trash" from any other 410 (`client_too_old` included).
    in_trash: bool = False
    #: The workspace uuid the API limited this request to when it answered 404 (its
    #: `X-Probe-Workspace-Limit-Applied` echo): the thing may exist outside it. The
    #: transport sets it and says so in the message.
    workspace_limit_applied: str | None = None

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


#: The run resolver's 404 detail (`app/runs/service.py` `_NOT_FOUND`): the run a
#: write named does not exist for the credential that sent it. A run token's
#: refusal, a swept multipart upload, R2 and an absent route also answer 404,
#: with other details, and their writes are lost for reasons of ours.
#: tests/unit/test_delivery_alert_config.py pins it to the server's.
RUN_NOT_FOUND_DETAIL = "run not found"


def names_no_such_run(exc: BaseException) -> bool:
    """The server said the run does not exist -- not a workspace limit hiding
    it, not any other 404."""
    return (
        isinstance(exc, NotFoundError)
        and exc.detail == RUN_NOT_FOUND_DETAIL
        and not exc.workspace_limit_applied
    )


class ConflictError(RosError):
    """409 - natural-key conflict, or a delete blocked because a published
    experiment version pins something in the subtree. The detail is an object;
    the useful fields are surfaced as attributes."""

    def __init__(self, message: str, *, detail: Any = None):
        super().__init__(message, status=409, detail=detail)
        self.existing_id: str | None = None
        self.suggestion: str | None = None
        self.deleted: bool = False
        #: The slug's holder, on a create the slug namespace refused:
        #: ``{id, parent_project_id, kind, workspace_id}``. Slugs are one
        #: tenant-wide namespace for projects and experiments, so a create-or-get
        #: adopts the holder only when it is the thing it meant to create.
        self.existing: dict | None = None
        if isinstance(detail, dict):
            self.existing_id = detail.get("existing_id")
            self.suggestion = detail.get("suggestion")
            self.deleted = bool(detail.get("deleted", False))
            existing = detail.get("existing")
            self.existing = existing if isinstance(existing, dict) else None


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


#: What a person types to get past a `client_too_old` refusal. The server's
#: sentence names it (`app/client_version`); a refusal that does not -- an older
#: server's, or a proxy's rewrite -- gets it appended, because "too old" without
#: the command is a dead end on a training box nobody is watching.
UPGRADE_COMMAND = "pip install -U probe-research"


def upgrade_message(message: str, min_version: str | None) -> str:
    """The refusal's sentence, ending in how to upgrade (added only when missing)."""
    if "pip install" in message:
        return message
    target = f"probe-research {min_version} or later" if min_version else "a newer probe-research"
    return f"{message.rstrip()} Upgrade to {target}: `{UPGRADE_COMMAND}`."


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


class DocumentNotWritten(RosError):
    """An experiment was created or edited, and the document written after it was not.

    The experiment API takes no `document` yet, so a create (or an edit) with one
    is two writes: the first landed, the second failed. Raised so the caller
    knows the experiment EXISTS -- retrying the create would only meet its own
    slug -- and how to finish: the message names the command. ``experiment`` is
    the row the first write answered; ``__cause__`` is the failure."""

    def __init__(self, message: str, *, experiment: dict, status: int | None = None):
        super().__init__(message, status=status)
        self.experiment = experiment


class ValidationError(RosError):
    """422 - request validation (missing question, caps, malformed cursor, ...)."""


#: The server marks "this team has several workspaces and the create named
#: none" with this in a 422's `detail.code` (2026-10-14, per-computer workspaces).
WORKSPACE_REQUIRED = "workspace_required"


class WorkspaceRequired(ValidationError):
    """422 - a new project needs a workspace and this computer has none set.

    Raised before anything is created: a team with several workspaces never has
    one guessed for it (the old guess, its oldest, filed every member's work
    under its first member). Fix: `probe workspace use <slug>` (this computer),
    `PROBE_WORKSPACE`, or `workspace=` / `--workspace` for one call.
    """


#: The server marks a refused workspace limit (`X-Probe-Workspace-Limit`) with these
#: in `detail.code`: a value that is not a uuid (400) or a uuid naming no workspace
#: the caller can see (422). `probe.sdk.workspace_limit` raises them locally too.
INVALID_WORKSPACE_LIMIT = "invalid_workspace_limit"
WORKSPACE_LIMIT_UNKNOWN = "workspace_limit_unknown"
#: What every such refusal ends with: the limit is this computer's setting, so the
#: fix is a command on it, never a credential.
WORKSPACE_LIMIT_FIX = (
    "Run `probe workspace limit --team` or pick another (`probe workspace limit <workspace>`)."
)


class WorkspaceLimitError(ValidationError):
    """This computer's workspace limit was refused: no request it makes can succeed
    until the limit is changed. Not the credential and not the data -- the outbox
    keeps the write queued (`journal.classify`: transient) until it is fixed."""


class InvalidWorkspaceLimit(WorkspaceLimitError):
    """400 `invalid_workspace_limit`: the limit (or its team-items choice) is malformed."""


class WorkspaceLimitUnknown(WorkspaceLimitError):
    """422 `workspace_limit_unknown`: the limit names a workspace that no longer exists
    or that the caller cannot see."""


def _limit_message(detail: Any) -> str:
    message = _detail_message(detail)
    return message if "probe workspace limit" in message else f"{message.rstrip()} {WORKSPACE_LIMIT_FIX}"


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
    if status == 422 and isinstance(detail, dict) and detail.get("code") == WORKSPACE_REQUIRED:
        return WorkspaceRequired(_detail_message(detail), status=422, detail=detail)
    if isinstance(detail, dict) and detail.get("code") == WORKSPACE_LIMIT_UNKNOWN:
        return WorkspaceLimitUnknown(_limit_message(detail), status=status, detail=detail)
    if isinstance(detail, dict) and detail.get("code") == INVALID_WORKSPACE_LIMIT:
        return InvalidWorkspaceLimit(_limit_message(detail), status=status, detail=detail)
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

