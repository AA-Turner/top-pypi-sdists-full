"""pick the credential an op is delivered with: the one that queued it, its stamp and fingerprints, or none here."""

from __future__ import annotations
import hashlib
import os
import time
from probe.foundation.compat.compat import StrEnum
from typing import Any
from .... import errors
from ....session_marker import WIZARD_HINT
from probe.sdk.delivery.status_fields import StatusField


def _settings_for(context: dict | None):
    from ....settings.settings import DEFAULT_BASE_URL, Settings, load_context, resolve

    name = (context or {}).get("name")
    pinned = (context or {}).get("base_url")
    settings = resolve(context=name)
    stored = load_context(name)
    if pinned and pinned.rstrip("/") != settings.base_url.rstrip("/"):
        # Ambient resolution (env vars outrank the context file) produced a credential for a
        # DIFFERENT endpoint than this op was enqueued for. Never mix: a token issued for
        # endpoint A must not be sent to pinned host B (security review). Use only the named
        # context's stored record for the pinned endpoint; auth-block when none matches.
        stored_base = (stored.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
        if stored_base == pinned.rstrip("/") and (
            stored.get("token") or stored.get("ingest_token")
        ):
            from ....settings.workspace_limit import resolve_limit

            return Settings(
                base_url=pinned.rstrip("/"),
                token=stored.get("token"),
                ingest_token=stored.get("ingest_token"),
                hmac_secret=stored.get("hmac_secret"),
                # The pinned context's own limit: its writes are its requests.
                workspace_limit=resolve_limit(stored),
            )
        if stored and stored_base != pinned.rstrip("/"):
            # A context record EXISTS and names a different endpoint: no login for this
            # context can produce a credential for the pinned one (refusing to mix them is the
            # point), so this op is undeliverable from this machine and must not park the queue.
            raise errors.UnroutableEndpointError(
                f"pinned endpoint {pinned} is not what context "
                f"{name or '<default>'} names ({stored_base}), and no stored "
                "credential matches it -- this op cannot be delivered from here"
            )
        # No record, or a record for THIS endpoint carrying no credential: the researcher is
        # logged out, signing in again recovers it, and their queued work must be parked and
        # kept, not dead-lettered. A self-hosted user mid-logout is otherwise
        # indistinguishable from a dead ephemeral test port.
        raise errors.AuthError(
            f"no stored credential for pinned endpoint {pinned} "
            f"(context {name or '<default>'}); {WIZARD_HINT}"
        )
    if pinned:
        settings.base_url = pinned.rstrip("/")
    # Same endpoint, but the pinned context STORES its own credential: the stored token
    # outranks any ambient PROBE_TOKEN for a drain. Tenants can share one API URL, and a
    # detached worker inheriting another account's env must not replay this context's ops
    # under the wrong principal (codex). Env credentials still serve contexts storing none.
    if stored.get("token"):
        settings.token = stored.get("token")
    if stored.get("ingest_token"):
        settings.ingest_token = stored.get("ingest_token")
    return settings


class CredentialSource(StrEnum):
    """Where the credential that queued an op came from (#2035)."""

    #: ``PROBE_TOKEN`` / ``PROBE_INGEST_TOKEN`` in the writer's environment.
    ENV = "env"
    #: The writer's context's stored login.
    CONFIG = "config"
    #: Anything else: a token passed in code, or another context's login.
    CODE = "code"


def credential_fingerprint(token: str | None, ingest_token: str | None) -> str | None:
    """A short one-way name for the credential that queued an op, so the op can say WHICH
    credential without carrying it: 64 bits of a SHA-256 over a long random token (enough to
    tell two apart, useless for recovering it).

    The bearer token when there is one, else the ingest token, never the pair. A
    ``PROBE_TOKEN`` job's settings pick up the stored login's ingest token, so a pair
    fingerprint changed whenever that login re-logged in and the job's queued writes matched no
    drainer (#2041 review)."""
    secret = token or ingest_token
    if not secret:
        return None
    digest = hashlib.sha256(b"probe.outbox.credential/2\0")
    digest.update(("token\0" if token else "ingest\0").encode())
    digest.update(secret.encode("utf-8", "backslashreplace"))
    return digest.hexdigest()[:16]


def stamp_identity(stamp: dict | None) -> tuple[str, str] | None:
    """(customer_id, user_id) the stamp says queued the op, when recorded."""
    if isinstance(stamp, dict) and stamp.get("customer_id") and stamp.get("user_id"):
        return str(stamp["customer_id"]), str(stamp["user_id"])
    return None


#: `_identity_of` answers per token fingerprint: (answer or exception, when). An exporter
#: passes every fraction of a second; the account behind a token does not change that fast
#: (#2041 re-review: 43 `/v1/me` in 8 s).
_IDENTITY_CACHE: dict[tuple[str, str], tuple[Any, float]] = {}
_IDENTITY_TTL_SECONDS = 300.0
_IDENTITY_ERROR_TTL_SECONDS = 60.0


def _identity_of(settings, transport=None) -> tuple[str, str] | None:
    """(customer_id, user_id) ``settings.token`` belongs to, per `GET /v1/me`: one attempt,
    5 s, cached per endpoint and token for 5 minutes (a failure for one). ``transport`` is
    one already carrying that token (a drainer client's own), else one is built from
    ``settings``. Raises what the request raised."""
    from ...transport.transport import Transport

    key = (str(settings.base_url or "").rstrip("/"), credential_fingerprint(settings.token, None) or "")
    cached = _IDENTITY_CACHE.get(key)
    if cached is not None:
        answer, at = cached
        ttl = _IDENTITY_ERROR_TTL_SECONDS if isinstance(answer, BaseException) else _IDENTITY_TTL_SECONDS
        if time.monotonic() - at < ttl:
            if isinstance(answer, BaseException):
                raise answer
            return answer
    owned = transport is None
    if owned:
        transport = Transport(settings, max_retries=0)
    try:
        response = transport.request("GET", "/v1/me", idempotent=True, timeout=5.0)
        who = response.json() if response.content else {}
    except Exception as exc:
        _IDENTITY_CACHE[key] = (exc, time.monotonic())
        raise
    finally:
        if owned:
            transport.close()
    answer = (
        (str(who["customer_id"]), str(who["user_id"]))
        if who.get("customer_id") and who.get("user_id")
        else None
    )
    _IDENTITY_CACHE[key] = (answer, time.monotonic())
    return answer


def op_credential(op: dict) -> tuple[str | None, bool]:
    """(fingerprint, is_ingest) of the credential ``op`` must be delivered with. An `/ingest`
    request is authenticated with the ingest token, everything else with the personal token
    (`Transport._auth_headers`), so a write names whichever its route uses (#2041 re-review):
    matching the personal token for an ingest write let a drainer send it with ITS OWN ingest
    token."""
    stamp = (op.get("context") or {}).get("principal") if isinstance(op, dict) else None
    if not isinstance(stamp, dict):
        return None, False
    ingest = op.get("kind") == "http" and routes.is_ingest(op.get("path"))
    key = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
    return (str(key) if key else None), ingest


def _login_base_of(context: dict | None, base_url: str | None) -> str | None:
    """``base_url`` when it is the server ``context``'s stored login is for, else None: what
    `record_account`'s ``login_of`` may name."""
    from ....settings.settings import DEFAULT_BASE_URL, load_context

    try:
        stored = load_context((context or {}).get("name"))
    except Exception:  # noqa: BLE001
        return None
    base = (stored.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
    return base if base == str(base_url or "").rstrip("/") else None


def _stored_login_fingerprint(context: dict | None) -> str | None:
    """The fingerprint of the login stored for ``context``'s context, or None."""
    from ....settings.settings import load_context

    try:
        return credential_fingerprint(load_context((context or {}).get("name")).get("token"), None)
    except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
        return None


def _route_fingerprint(settings, ingest: bool) -> str | None:
    """The fingerprint of the key ``settings`` would send on that route."""
    if ingest:
        return credential_fingerprint(None, settings.ingest_token)
    return credential_fingerprint(settings.token, settings.ingest_token)


def _settings_for_op(
    context: dict | None, *, ingest: bool = False, account: tuple[str, str] | None = None
):
    """The credential to deliver an op with: the one that queued it (matched by fingerprint, per
    route), or none (`CredentialNotHere`, #2035). A stored login's write may follow a re-login only
    when `GET /v1/me` names the same account; an adopted credential uses the account recorded at
    adoption; never an environment token for someone else's write. DESIGN.md has every case."""
    stamp = (context or {}).get("principal")
    if not isinstance(stamp, dict) or not stamp.get("fingerprint"):
        return _settings_for(context)
    wanted = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
    if not wanted:
        raise CredentialNotHere(
            "queued for the ingest route by a client that had no ingest token; nothing may "
            "send it with another one"
        )
    from ....settings.settings import load_context, resolve

    name = (context or {}).get("name")
    pinned = ((context or {}).get("base_url") or "").rstrip("/")
    adopted = None if ingest else adopted_account(stamp.get("fingerprint"))
    try:
        ambient = resolve(context=name) if adopted is None else None
    except Exception:  # noqa: BLE001 -- an unreadable config is just no candidate
        ambient = None
    if (
        ambient is not None
        and (not pinned or ambient.base_url.rstrip("/") == pinned)
        and _route_fingerprint(ambient, ingest) == wanted
    ):
        if pinned:
            ambient.base_url = pinned
        return ambient
    try:
        stored = _settings_for(context)
        failure = None
    except Exception as exc:  # noqa: BLE001 -- raised below only where it applies
        stored, failure = None, exc
    if stored is not None and _route_fingerprint(stored, ingest) == wanted:
        return stored
    if (stamp.get("source") != CredentialSource.CONFIG and adopted is None) or ingest:
        raise CredentialNotHere(
            f"queued with a credential from {stamp.get('source') or 'elsewhere'} "
            f"(fingerprint {wanted}) that this process does not hold; it is delivered by the "
            "process that queued it, or by `probe outbox drain` run with the same credential"
        )
    record = load_context(name)
    if adopted is not None:
        from ....settings.settings import DEFAULT_BASE_URL

        stored_base = (record.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
        if pinned and pinned != stored_base:
            # Adopted for the login stored here, which is another server's: it waits (held,
            # never dead-lettered), and that login's token is never sent to the pinned server.
            raise CredentialNotHere(
                f"adopted, but queued for {pinned} and the login stored for context "
                f"{name or '<default>'} is {stored_base}'s; it waits",
                permanent=True,
            )
    if failure is not None:
        raise failure
    if not (record.get("token") or record.get("ingest_token")):
        # Logged out since: park until a sign-in, as an unstamped op would, but never hand
        # this op to an environment token instead.
        raise errors.AuthError(
            f"no stored credential for context {name or '<default>'} ({WIZARD_HINT})"
        )
    # The stored login outranks the environment field by field in `_settings_for`; a field the
    # login does not store must not be filled from someone else's environment either.
    stored.token = record.get("token")
    stored.ingest_token = record.get("ingest_token")
    from ....settings.settings import DEFAULT_BASE_URL as _DEFAULT_BASE

    record_base = (record.get("base_url") or _DEFAULT_BASE).rstrip("/")
    env_base = (os.environ.get("PROBE_BASE_URL") or "").rstrip("/")
    if stored.base_url.rstrip("/") != record_base and (
        adopted is not None or stored.base_url.rstrip("/") != env_base
    ):
        # The config changed between the reads: this token is never sent to a server its own
        # record does not name. The next pass reads it again.
        raise CredentialNotHere(
            f"the login of context {name or '<default>'} changed while this write was routed; "
            "it waits"
        )
    queued_as = stamp_identity(stamp) or account or recorded_account(stamp.get("fingerprint"))
    if adopted is not None:
        if queued_as not in (None, adopted):
            # One token is one account: an op recording another account was not queued by the
            # credential the user vouched for.
            raise CredentialNotHere(
                f"adopted for another account than the one its write records "
                f"(fingerprint {wanted}); it waits",
                permanent=True,
            )
        queued_as = adopted
    if queued_as is None:
        raise CredentialNotHere(
            f"queued under an earlier login of context {name or '<default>'} whose account "
            "was never recorded, so the login stored now cannot be matched to it",
            permanent=True,
        )
    try:
        now_as = _identity_of(stored)
    except errors.AuthError:
        raise  # the new login is refused too: set aside with the rest of its writes
    except Exception as exc:  # noqa: BLE001 -- cannot confirm: wait, never guess
        raise CredentialNotHere(
            f"could not confirm the account of context {name or '<default>'}'s login "
            f"({type(exc).__name__}); the write waits"
        ) from exc
    if now_as != queued_as:
        raise CredentialNotHere(
            f"queued under another account than the one logged in to context "
            f"{name or '<default>'} now; it waits for that account's login",
            permanent=True,
        )
    return stored


#: How long a refused credential's writes are set aside before one retry; the same bound as
#: the worker's box-wide auth block (outbox_worker).
CREDENTIAL_RETRY_COOLDOWN_SECONDS = 300.0


def _stamp_fingerprint(op: dict | None) -> str | None:
    """The fingerprint of the key ``op`` is delivered with (see `op_credential`)."""
    return op_credential(op or {})[0]


def _cooling_refusals(journal: "Journal") -> dict[str, str]:
    """Refused credentials still inside their cooldown, from status.json."""
    from datetime import datetime, timezone

    status = Journal.read_status(journal.dir, include_receipts=False, keep_idle_refusals=True) or {}
    recorded = status.get(StatusField.REFUSED_FINGERPRINTS)
    cooling: dict[str, str] = {}
    if not isinstance(recorded, dict):
        return cooling
    now = datetime.now(timezone.utc)
    for refused, since in recorded.items():
        try:
            at = datetime.fromisoformat(str(since))
        except ValueError:
            continue
        if at.tzinfo is None:
            at = at.replace(tzinfo=timezone.utc)
        if (now - at).total_seconds() < CREDENTIAL_RETRY_COOLDOWN_SECONDS:
            cooling[str(refused)] = str(since)
    return cooling
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk import routes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.accounts import recorded_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import adopted_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import CredentialNotHere  # noqa: E402 -- pieces need each other; the front door loads this one first
