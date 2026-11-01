"""hand a dead credential's queued writes to the stored login: refusal kinds, adoption rules, rescue_stranded."""

from __future__ import annotations
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum
from pathlib import Path
from .... import errors
from .....foundation.durable.durable import now_iso


#: How many adopted credentials `adopt_credential` keeps (newest win). Each is a dead
#: credential with stranded writes: thousands is no machine's.
_ADOPTIONS_KEPT = 4096


def rescue_lock_path() -> Path:
    """One rescue at a time per user on this machine, whatever outbox it starts from
    (`outbox_worker.rescue`, `probe doctor`): the outboxes one rescue covers overlap."""
    return _accounts_path().with_name("credential-rescue.lock")


def _adoptions_path() -> Path:
    """Credentials whose queued writes the user handed to their stored login
    (`probe outbox adopt`): `<state>/probe/credential-adoptions.json`, beside the accounts
    record for the same reason (machine-wide, ids only). Never cleared by a sign-in or
    `outbox retry`: a rescue a later login undid would strand the writes again."""
    return _accounts_path().with_name("credential-adoptions.json")


class AdoptedBy(StrEnum):
    """Who adopted a credential's writes (`adopt_credential`)."""

    #: `probe outbox adopt`.
    USER = "user"
    #: `rescue_stranded`, run by itself from the CLI's every-command check.
    RESCUE = "rescue"


def adopt_credential(
    fingerprint: str, account: tuple[str, str], *, by: AdoptedBy = AdoptedBy.USER
) -> None:
    """Record that ``fingerprint``'s queued writes go out with the stored login of their
    context from now on, while that login is ``account`` (`_settings_for_op`). The caller has
    checked that it is (`adoption_account`). Raises what the file system raised: unlike
    `record_account`, this IS the step asked for."""
    entry = {
        "customer_id": str(account[0]),
        "user_id": str(account[1]),
        "by": str(by),
        "at": now_iso(),
    }

    def change(records: dict) -> bool:
        records[fingerprint] = entry
        return True

    _update_records(_adoptions_path(), change, kept=_ADOPTIONS_KEPT)


def adopted_account(fingerprint: str | None) -> tuple[str, str] | None:
    """The account ``fingerprint``'s writes were adopted for, or None."""
    if not fingerprint:
        return None
    entry = _read_records(_adoptions_path()).get(fingerprint) or {}
    if isinstance(entry, dict) and entry.get("customer_id") and entry.get("user_id"):
        return str(entry["customer_id"]), str(entry["user_id"])
    return None


class Refusal(StrEnum):
    """What a queued write's last refusal says about its credential
    (`op_refusal`)."""

    #: Probe refused the credential itself: a 401, or a 403 saying the key was
    #: revoked or expired or its team is gone (`key_refusal.credential_refused`).
    CREDENTIAL = "credential"
    #: A 403 for a missing scope or role: the credential works, but may not do
    #: this. Its writes must never go out with a credential that may.
    SCOPE = "scope"


def op_shows_dead_credential(op: dict) -> bool:
    """Whether ``op``'s last refusal (`last_error`) was of the credential itself (the token is
    dead), whatever else the op records: a write refused for scope before its token was
    revoked is still evidence of the revocation, just never sent by another credential."""
    from ....settings.key_refusal import credential_refused

    text = str(op.get("last_error") or "") if isinstance(op, dict) else ""
    kind, _, message = text.partition(": ")
    return kind == "AuthError" or (kind == "ScopeError" and credential_refused(403, message))


def op_refusal(op: dict) -> "Refusal | None":
    """The kind of refusal recorded on ``op`` by the drain that last tried it with its own
    credential (`last_error`, ``"<Error>: <message>"``), or None. On the op file itself, so
    a sign-in (`clear_auth_block`) does not erase it."""
    from ....settings.key_refusal import credential_refused

    if isinstance(op, dict) and op.get("refused_for_scope"):
        return Refusal.SCOPE
    text = str(op.get("last_error") or "") if isinstance(op, dict) else ""
    kind, _, message = text.partition(": ")
    if kind == "AuthError":
        return Refusal.CREDENTIAL
    if kind == "ScopeError":
        if credential_refused(403, message):
            return Refusal.CREDENTIAL
        # Refused while going out with an adopting login: not this write's own credential's
        # verdict.
        return None if op.get("refused_via_adoption") else Refusal.SCOPE
    return None


class NotAdoptable(StrEnum):
    """Why a credential's writes cannot go out with the stored login."""

    #: No write of it, and no record on this machine, says whose it was.
    UNKNOWN_ACCOUNT = "unknown_account"
    #: A context its writes name stores no login.
    NO_LOGIN = "no_login"
    #: Its writes are for another server than the login stored for them.
    OTHER_SERVER = "other_server"
    #: `/v1/me` with that login did not answer.
    UNCONFIRMED = "unconfirmed"
    #: That login is another team or user.
    OTHER_ACCOUNT = "other_account"
    #: The credential may not do what its writes ask (a scope refusal, or recorded scopes
    #: without `write`): the login could, and must not do it in its place. (A DELETE never
    #: goes this way: `adopted_route_refuses`.)
    SCOPE = "scope"


def adoption_account(
    fingerprint: str, ops: list[dict]
) -> tuple[tuple[str, str] | None, NotAdoptable | None, str | None]:
    """Whether ``fingerprint``'s queued ``ops`` may go out with the stored login of every
    context they name: (account, None, None) when each login is for the server the ops are
    pinned to and is, per `GET /v1/me`, the same team and user the credential was (a write's
    stamp, else `recorded_account`), and nothing says the credential lacked the scopes its
    writes need; else (None, why, the context). The one check behind `probe outbox adopt` and
    `rescue_stranded`."""
    from ....settings.settings import DEFAULT_BASE_URL, Settings, load_context

    account = None
    contexts: dict = {}
    for op in ops:
        context = op.get("context") or {}
        contexts.setdefault(context.get("name"), set()).add(
            str(context.get("base_url") or "").rstrip("/")
        )
        account = account or stamp_identity(context.get("principal"))
        if op_refusal(op) == Refusal.SCOPE:
            return None, NotAdoptable.SCOPE, context.get("name")
    scopes = recorded_scopes(fingerprint)
    if scopes is not None and "write" not in scopes:
        return None, NotAdoptable.SCOPE, None
    account = account or recorded_account(fingerprint)
    if account is None:
        return None, NotAdoptable.UNKNOWN_ACCOUNT, None
    for name in sorted(contexts, key=lambda c: c or ""):
        try:
            stored = load_context(name)
        except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
            stored = {}
        if not stored.get("token"):
            return None, NotAdoptable.NO_LOGIN, name
        base = (stored.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
        if contexts[name] - {"", base}:
            return None, NotAdoptable.OTHER_SERVER, name
        try:
            now_as = _identity_of(Settings(base_url=base, token=stored["token"]))
        except Exception:  # noqa: BLE001 -- cannot confirm: never guess
            return None, NotAdoptable.UNCONFIRMED, name
        if now_as != account:
            return None, NotAdoptable.OTHER_ACCOUNT, name
    return account, None, None


@dataclass
class RescueReport:
    """What `rescue_stranded` did: credentials adopted now (fingerprint ->
    writes), and writes of credentials adopted earlier still queued."""

    rescued: dict = field(default_factory=dict)
    adopted_waiting: int = 0
    #: Fingerprint -> `NotAdoptable`: dead, but not this login's to send.
    refused: dict = field(default_factory=dict)
    #: The queue folders holding rescued or adopted writes: the ones to drain.
    queues: set = field(default_factory=set)
    #: Dead credentials left for later: a holder may still run, or the login's account could
    #: not be confirmed. A rescue with these is not idle.
    deferred: int = 0
    #: The one endpoint every rescued write names, or None (two, or none).
    base_url: str | None = None


def rescue_stranded(root: "Journal", *, here: "set[str] | frozenset[str]") -> RescueReport:
    """Hand to the stored login the writes of every env or in-code credential that is dead and
    was the logged-in account's own (`adopt_credential`, `AdoptedBy.RESCUE`), so they go out
    without anyone running a command.

    Dead: Probe refused the credential itself on one of its writes (`op_shows_dead_credential`,
    on the op file no sign-in clears; a scope refusal never counts) and no process recorded
    holding it may still run (`credential_holders`): a job alive with it is restarted, not
    overridden. Its own: `adoption_account` over EVERY write it queued (one refused for scope
    keeps them all), same team and user per `GET /v1/me`, same server, scopes that allow its
    writes. ``here`` (credentials this process holds, the stored login) are never adopted.
    `/ingest` writes, DELETEs and writes refused for scope are never sent this way and not
    counted. Never sends anything itself; never raises for one credential."""
    report = RescueReport()
    by_fp: dict[str, list[dict]] = {}
    where: dict[str, set] = {}
    for queue in root.namespaces():
        for _path, op in queued_ops(queue):
            stamp = (op.get("context") or {}).get("principal")
            if not isinstance(stamp, dict) or not stamp.get("fingerprint"):
                continue
            if stamp.get("source") not in (CredentialSource.ENV, CredentialSource.CODE):
                continue
            if op_credential(op)[1]:
                continue  # an /ingest write: only its own ingest token sends it
            fp = str(stamp["fingerprint"])
            by_fp.setdefault(fp, []).append(op)
            where.setdefault(fp, set()).add(queue.dir)
    endpoints: set = set()
    for fp, ops in sorted(by_fp.items()):
        if fp in here:
            continue
        # What the adopted route would send: never a DELETE or a write refused for scope
        # (`adopted_route_refuses`). The adoption check still sees every write: one refused
        # for scope keeps the whole credential's.
        sendable = [op for op in ops if adopted_route_refuses(op) is None]
        if adopted_account(fp) is not None:
            report.adopted_waiting += len(sendable)
            if sendable:
                report.queues |= where[fp]
            continue
        if not sendable:
            continue
        if not any(op_shows_dead_credential(op) for op in ops):
            continue
        if any(_holder_may_live(h) for h in credential_holders(fp)):
            report.deferred += 1
            continue  # restart it with a valid token; its writes are its own
        try:
            account, why, _context = adoption_account(fp, ops)
            if account is None:
                if why in (NotAdoptable.UNCONFIRMED, NotAdoptable.NO_LOGIN):
                    report.deferred += 1
                report.refused[fp] = why
                continue
            adopt_credential(fp, account, by=AdoptedBy.RESCUE)
        except Exception as exc:  # noqa: BLE001 -- one credential never stops the rest
            log.warning("outbox: could not rescue credential %s: %s", fp, type(exc).__name__)
            continue
        report.rescued[fp] = len(sendable)
        report.queues |= where[fp]
        endpoints.update(str((op.get("context") or {}).get("base_url") or "") for op in ops)
    if len(endpoints) == 1 and "" not in endpoints:
        report.base_url = endpoints.pop()
    return report


def held_credentials(ops, *, here: "set[str] | frozenset[str]") -> list[dict]:
    """Which env or in-code credentials the queued ``ops`` wait for that nothing in ``here``
    (this shell's credentials, the stored login) holds: one entry per credential, most writes
    first, with its writes' count and source, the account behind it when known (a stamp, else
    `recorded_account`), the kind of its last refusal (`op_refusal`) and whether it was
    adopted (its writes then go out with the login; one still here says why it cannot).
    Unstamped ops and stored-login ops are left out: a re-login sends those."""
    found: dict[str, dict] = {}
    for op in ops:
        stamp = (op.get("context") or {}).get("principal") if isinstance(op, dict) else None
        if not isinstance(stamp, dict) or not stamp.get("fingerprint"):
            continue
        if stamp.get("source") not in (CredentialSource.ENV, CredentialSource.CODE):
            continue
        fp = str(stamp["fingerprint"])
        if fp in here:
            continue
        entry = found.setdefault(
            fp, {"fingerprint": fp, "source": stamp.get("source"), "writes": 0, "refusal": None}
        )
        entry["writes"] += 1
        if "account" not in entry and stamp_identity(stamp) is not None:
            entry["account"] = stamp_identity(stamp)
        refusal = op_refusal(op)
        if refusal == Refusal.SCOPE or (refusal and entry["refusal"] is None):
            entry["refusal"] = refusal
    out = []
    for fp, entry in found.items():
        entry["adopted"] = adopted_account(fp) is not None
        entry.setdefault("account", recorded_account(fp))
        out.append(entry)
    return sorted(out, key=lambda e: (-e["writes"], e["fingerprint"]))


class AdoptedRouteRefused(errors.ValidationError):
    """A write of an adopted credential that its adopting login may not send
    (`adopted_route_refuses`). Dead-lettered with this reason -- visible in
    `probe outbox status`, retryable -- rather than held: a held write stalls
    every later write of its run, the close included, for good."""


def adopted_route_refuses(op: dict) -> str | None:
    """Why ``op`` may not go out with the login its credential was adopted by, or None.
    Checked per write when SENT, not once at adoption: an adoption covers what that
    credential queues later too. Never a DELETE (a login may delete what the credential may
    not: a companion key's permanent deletes, a token without `delete`); never a write the
    credential was refused for scope; never one its recorded scopes do not allow."""
    method = str(op.get("method") or "").upper() if isinstance(op, dict) else ""
    if method == "DELETE":
        return "a DELETE goes out only with the credential that queued it"
    if op_refusal(op) == Refusal.SCOPE:
        return "Probe refused it for scope: no other credential may send it"
    fp = op_credential(op)[0]
    scopes = recorded_scopes(fp)
    writes = method not in ("GET", "HEAD") if method else op.get("kind") != "http"
    if scopes is not None and writes and "write" not in scopes:
        return "the credential that queued it may not write"
    return None
from probe.sdk.delivery.journal.journal import Journal, log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import queued_ops  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.accounts import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _accounts_path,
    _read_records,
    _update_records,
    recorded_account,
    recorded_scopes,
)
from probe.sdk.delivery.outbox.drain.credentials import CredentialSource, _identity_of, op_credential, stamp_identity  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.holders import _holder_may_live, credential_holders  # noqa: E402 -- pieces need each other; the front door loads this one first
