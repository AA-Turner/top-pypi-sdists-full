"""AccountRecords: the machine-wide record of which account each credential fingerprint belongs to."""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Callable
from .....foundation.durable import homedir
from .....foundation.durable.durable import (
    file_lock,
    now_iso,
    write_text_atomic)


#: How many token -> account records `record_account` keeps (newest win); as many as the
#: adoptions they vouch for (`_ADOPTIONS_KEPT`).
_ACCOUNTS_KEPT = 4096


def _accounts_path() -> Path:
    """Which account each credential fingerprint belongs to, machine-wide:
    `<state>/probe/credential-accounts.json`. Outside the outbox on purpose: outboxes are per
    rank and per `PROBE_OUTBOX_DIR`, while an account learned anywhere vouches everywhere.
    Ids only (team and user), never a token."""
    base = os.environ.get("XDG_STATE_HOME")
    root = Path(base) if base else homedir.home() / ".local" / "state"
    return root / "probe" / "credential-accounts.json"


def _update_records(
    path: Path, change: Callable[[dict], bool], *, kept: int, wait: bool = True
) -> bool:
    """Read-modify-write one of the small machine-wide records beside
    `credential-accounts.json`, under its lock, atomically, 0600. ``change`` edits the dict in
    place and answers whether anything changed; past ``kept`` entries the oldest (by ``at``)
    go. ``wait=False`` skips the write when another process holds the lock (evidence, not a
    delivery step: every rank of a distributed job must not queue behind one lock); returns
    False only then. Raises what the file system raised."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = path.with_suffix(".lock")
    if wait:
        guard = file_lock(lock)
    else:
        guard = _try_lock(lock)
    with guard as held:
        if held is False:
            return False
        try:
            records = json.loads(path.read_text())
        except (OSError, ValueError):
            records = {}
        if not isinstance(records, dict):
            records = {}
        if not change(records):
            return True
        if len(records) > kept:
            newest = sorted(records.items(), key=lambda kv: str((kv[1] or {}).get("at")))
            records = dict(newest[-kept:])
        write_text_atomic(path, json.dumps(records, indent=2) + "\n", mode=0o600)
    _RECORDS_CACHE.pop(str(path), None)
    return True


#: `_read_records` answers per path: (mtime_ns, size, records). A kick reads the adoptions
#: record on every write of a training loop; one stat is cheap, a parse per write is not.
_RECORDS_CACHE: dict[str, tuple[int, int, dict]] = {}


def _read_records(path: Path) -> dict:
    try:
        stat = path.stat()
    except OSError:
        return {}
    cached = _RECORDS_CACHE.get(str(path))
    if cached is not None and cached[0] == stat.st_mtime_ns and cached[1] == stat.st_size:
        return cached[2]
    try:
        records = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    records = records if isinstance(records, dict) else {}
    _RECORDS_CACHE[str(path)] = (stat.st_mtime_ns, stat.st_size, records)
    return records


def record_account(
    fingerprint: str | None,
    account: tuple[str, str] | None,
    *,
    scopes: "list[str] | None" = None,
    login_of: str | None = None,
) -> None:
    """Remember that the credential named ``fingerprint`` is ``account``, and the ``scopes``
    `/v1/me` named for it when known.

    Written by the wizard's sign-in, a job's heartbeat lookup and a drain that just delivered
    with a stored login (#2041 round 3): a write queued under a login whose account nobody
    recorded can then still follow a same-account re-login instead of waiting forever. The
    scopes keep a narrower token's writes from going out with a login that may do more
    (`adoption_account`). ``login_of`` (a server URL) says the token was this machine's stored
    login for that server, so a job that copied it into `PROBE_TOKEN` is still taken for the
    login once a re-login replaced it, in any process (`was_login`). Never raises: evidence,
    not a step in delivery."""
    if not fingerprint or not account or not all(account):
        return
    entry: dict = {"customer_id": str(account[0]), "user_id": str(account[1]), "at": now_iso()}

    def change(records: dict) -> bool:
        before = records.get(fingerprint) or {}
        if scopes is not None:
            entry["scopes"] = sorted(str(s) for s in scopes)
        elif isinstance(before, dict) and isinstance(before.get("scopes"), list):
            entry["scopes"] = before["scopes"]  # a lookup without them keeps them
        if login_of:
            entry["login_of"] = str(login_of).rstrip("/")
        elif isinstance(before, dict) and before.get("login_of"):
            entry["login_of"] = before["login_of"]
        if {k: v for k, v in before.items() if k != "at"} == {
            k: v for k, v in entry.items() if k != "at"
        }:
            return False
        records[fingerprint] = entry
        return True

    try:
        _update_records(_accounts_path(), change, kept=_ACCOUNTS_KEPT)
    except Exception:  # noqa: BLE001 -- see docstring
        return


def recorded_account(fingerprint: str | None) -> tuple[str, str] | None:
    """The account `record_account` remembered for ``fingerprint``, or None."""
    if not fingerprint:
        return None
    entry = _read_records(_accounts_path()).get(fingerprint) or {}
    if isinstance(entry, dict) and entry.get("customer_id") and entry.get("user_id"):
        return str(entry["customer_id"]), str(entry["user_id"])
    return None


def was_login(fingerprint: str | None, base_url: str | None, account=None) -> bool:
    """Whether ``fingerprint`` was recorded as this machine's stored login for ``base_url``
    (`record_account`'s ``login_of``) and, with ``account``, as that account's: another
    context's login on the same server, or a previous login of another person, is not the
    login stored now."""
    entry = _read_records(_accounts_path()).get(fingerprint or "") or {}
    login_of = entry.get("login_of") if isinstance(entry, dict) else None
    if not login_of or str(login_of) != str(base_url or "").rstrip("/"):
        return False
    return account is None or recorded_account(fingerprint) == tuple(account)


def recorded_scopes(fingerprint: str | None) -> "frozenset[str] | None":
    """The scopes `record_account` remembered for ``fingerprint``, or None when none were (an
    older release's record, or the wizard's)."""
    entry = _read_records(_accounts_path()).get(fingerprint or "") or {}
    scopes = entry.get("scopes") if isinstance(entry, dict) else None
    return frozenset(str(s) for s in scopes) if isinstance(scopes, list) else None
from probe.sdk.delivery.journal.item_locks import _try_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
