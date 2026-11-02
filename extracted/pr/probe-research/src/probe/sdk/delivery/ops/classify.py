"""classify a failed op -- transient, permanent, auth or idempotent -- including the dead-letter matchers that ask the server."""

from __future__ import annotations
import os
import re
from typing import Callable
from ... import errors
from ....foundation.safe_warn import safe_warn as _diagnostics
from ...secret_gate import CredentialBlocked

# Transient-when-status statuses beyond the typed transport/server errors.
_TRANSIENT_STATUSES = {408, 429}

#: Statuses meaning "not ever", not "not now". 501 only: RFC 9110 says the server does
#: not SUPPORT the method (cacheable by default). Named explicitly because every other
#: 5xx is a transient hiccup worth retrying.
_PERMANENT_STATUSES = {501}

#: How long one op may keep failing transiently, from its first failure on the wall clock,
#: before the drain treats it as permanent (plan 0.6), so one poison op cannot park its run's
#: writes forever. A count let the poll rate decide; a day outlasts any outage worth waiting out.
TRANSIENT_BUDGET_SECONDS = 24 * 60 * 60.0


def _transient_budget_seconds() -> float:
    """Read at failure time (rare) so a test or operator can change it without a reload;
    a malformed value warns and keeps the default."""
    raw = os.environ.get("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC")
    if raw:
        try:
            return max(0.0, float(raw))
        except ValueError:
            # Read inside a drain: a plain warnings.warn raises under -W error.
            _diagnostics.warn(
                f"ignoring malformed PROBE_OUTBOX_TRANSIENT_BUDGET_SEC={raw!r}; "
                "expected seconds as a float",
                stacklevel=2,
            )
    return TRANSIENT_BUDGET_SECONDS


def _failing_for_seconds(op: dict, now: float) -> float:
    """Seconds since this op FIRST failed transiently. Stamps ``first_failed_at`` (epoch
    seconds) on the op the first time, so the clock survives rewrites, worker restarts
    and reboots."""
    first = op.get("first_failed_at")
    if not isinstance(first, (int, float)) or isinstance(first, bool):
        op["first_failed_at"] = now
        return 0.0
    return max(0.0, now - float(first))


def classify(exc: Exception) -> str:
    """``transient`` | ``permanent`` | ``auth`` | ``idempotent`` for one failure.

    Phase-agnostic core; the phase-AWARE cases (404 after a ``have`` dedup, the
    superseded-confirm race) are handled where the phase is known -- inside
    ``Client.upload_fingerprinted`` -- and never reach this classifier.
    Anything that is not a typed client error counts as transient: our own bug
    must park the queue, not destroy data.
    """
    if isinstance(exc, CredentialBlocked):
        return "permanent"
    if isinstance(exc, errors.UnroutableEndpointError):
        # Checked BEFORE AuthError (its parent). "auth" means a login would fix it, so
        # the drainer parks the queue; an op pinned to an endpoint no credential here can
        # satisfy is not that, and parking stops every op behind it, including those for
        # the logged-in endpoint. Dead-letter it: visible in `probe outbox status`,
        # retryable with `probe outbox retry` if the endpoint becomes reachable.
        return "permanent"
    if isinstance(exc, errors.WorkspaceLockedError):
        # Checked BEFORE ScopeError (its parent), same shape. "auth" parks the queue and is
        # right when the CREDENTIAL is wrong; this 403 says one DESTINATION is closed to
        # this person while every other queued op is deliverable. Parking would stall the
        # whole backlog behind one file bound for a workspace they are not on.
        return "permanent"
    if isinstance(exc, errors.UploadRefused):
        # A presigned upload's own capability was refused (#2073): no credential was sent,
        # so a login cannot fix it and parking stopped every write of the run. This upload
        # fails (recorded as failed); the rest goes on.
        return "permanent"
    if isinstance(exc, (errors.AuthError, errors.ScopeError)):
        return "auth"
    if isinstance(exc, errors.WorkspaceLimitError):
        # Checked BEFORE ValidationError (its parent). This computer's workspace limit was
        # refused (e.g. it names a deleted workspace): the same for every op, fixed by
        # `probe workspace limit`, not by the op. Kept queued and retried, exempt from the
        # transient budget in `drain`; dead-lettering would fail every queued write.
        return "transient"
    if isinstance(exc, errors.ConflictError):
        return "idempotent" if exc.existing_id else "permanent"
    if isinstance(exc, errors.ValidationError):
        # Includes locally raised journal errors (missing staged bytes, unknown op kind)
        # with no HTTP status: retrying never satisfies them, and 'transient' would park
        # the drainer forever (perf review).
        return "permanent"
    if isinstance(exc, (errors.TransportError, errors.ServerError)):
        # A ServerError still carries the status; one 5xx means "never" (see
        # `_PERMANENT_STATUSES`). Checked before the blanket transient answer.
        if getattr(exc, "status", None) in _PERMANENT_STATUSES:
            return "permanent"
        return "transient"
    if isinstance(exc, errors.RosError):
        if exc.status in _TRANSIENT_STATUSES:
            return "transient"
        if exc.status in _PERMANENT_STATUSES:
            return "permanent"
        if exc.status is not None and 400 <= exc.status < 500:
            return "permanent"
        return "transient"
    return "transient"


def _run_exists_now() -> Callable[[dict], bool | None]:
    """`Journal.drop_unrecoverable`'s question, asked of the server now with each write's
    own credential (`_settings_for_op`), once per credential and run: True, False on the
    server's "run not found", None otherwise."""
    from urllib.parse import quote

    Client = delivery_client()

    answers: dict[tuple, bool | None] = {}

    def run_exists(op: dict) -> bool | None:
        context = op.get("context") if isinstance(op.get("context"), dict) else {}
        stamp = context.get("principal") if isinstance(context.get("principal"), dict) else {}
        if not stamp.get("fingerprint"):
            # Queued before writes named their credential (#2035): only today's login is
            # at hand and another team's login reads every run as absent. Cannot tell.
            return None
        key = (context.get("name"), context.get("base_url"), stamp.get("fingerprint"), str(op.get("run_ref")))
        if key in answers:
            return answers[key]
        answer: bool | None = None
        try:
            client = Client(settings=_settings_for_op(context or None), async_writes=False)
        except Exception:  # noqa: BLE001 -- no credential here: cannot tell
            answers[key] = None
            return None
        try:
            client.transport.request("GET", f"/v1/runs/{quote(str(op.get('run_ref')), safe='')}")
            answer = True
        except errors.NotFoundError as exc:
            answer = False if errors.names_no_such_run(exc) else None
        except Exception:  # noqa: BLE001 -- refused, away, in the trash: cannot tell
            answer = None
        finally:
            client.close()
        answers[key] = answer
        return answer

    return run_exists


#: The server's 409 for an edge whose exact (source, relation, target) exists
#: (`app/lineage/service.py`). Its OTHER 409 here, "run already has a genealogy parent",
#: names a DIFFERENT edge: a real conflict.
_EDGE_EXISTS = "lineage edge already exists"


def edge_already_exists(exc: Exception) -> bool:
    """Is this the server's "lineage edge already exists" 409 (the exact edge is there),
    not its other 409 on `POST /v1/edges` (a second genealogy parent, a DIFFERENT edge)?
    One rule for the outbox (`_edge_already_there`) and `probe edge add`."""
    if not isinstance(exc, errors.ConflictError):
        return False
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    return str(detail.get("message") or exc).startswith(_EDGE_EXISTS)


def _edge_already_there(op: dict, exc: Exception) -> bool:
    """A queued ``POST /v1/edges`` the server answered "lineage edge already exists": the
    edge is recorded, so the write is done. Unlike the 409-with-existing_id rule, true on
    a FIRST attempt too (the conflict key is the whole edge). What the op carried beyond
    that (``reason``, ``meta``, ``provenance``) is NOT applied to the old edge; the
    delivery logs it (a dead letter would hold the outbox for a human over an annotation)."""
    if op.get("correlation"):
        return False
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("path") != "/v1/edges":
        return False
    return edge_already_exists(exc)


def _resolve_queued_run_ref(
    client, ref: str | None, cache: dict[str, str]
) -> tuple[str, str] | None:
    """``(petname, uuid)`` for a run ref a 422 just rejected, or None to re-raise it. Enqueue never
    reads the run (async queues with no network), and every replayed route but one wants a uuid.
    Only after a 422, so the happy path pays nothing; cached per drain, never longer."""
    if not ref or _is_uuid(ref):
        return None
    if ref not in cache:
        try:
            cache[ref] = str(client.get_run(ref)["id"])
        except Exception:  # noqa: BLE001 -- the original 422 is the better error
            return None
    return (ref, cache[ref]) if cache[ref] != ref else None


_URL_QUERY = re.compile(r"\?\S+")


def _redact(text: str) -> str:
    """Strip query strings from URLs in error text. A presigned PUT URL's query IS a
    signed, bearer-equivalent write capability; transport errors embed the full URL, and
    last_error is persisted to op files, status.json, doctor output and the drainer log
    (security review)."""
    # scanning disabled: return scrub_text(_URL_QUERY.sub("?<redacted>", text))
    return _URL_QUERY.sub("?<redacted>", text)
from probe.sdk.delivery.ops.ops import _is_uuid, delivery_client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _settings_for_op  # noqa: E402 -- pieces need each other; the front door loads this one first
