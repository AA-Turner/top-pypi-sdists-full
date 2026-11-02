"""Many uploads of one run in two requests plus their PUTs: the drain's parallel window presigns,
PUTs and confirms up to 100 files; anything not clean goes back to the per-op path (DESIGN.md)."""

from __future__ import annotations

import hashlib
import os
import threading
import time
from collections.abc import Callable, Iterable
from concurrent.futures import Executor, as_completed
from contextvars import copy_context
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from ... import errors
from ...secret_gate import checked_upload

#: Files per request: the server's `UPLOAD_MANY_MAX`.
MANY_MAX = 100
#: Largest file these doors carry: bigger ones are bytes-bound, and each file in
#: flight holds a frozen copy on disk.
ITEM_MAX_BYTES = 8 * 1024 * 1024

#: How long a server without the doors is not asked again: an older server costs
#: one extra request per 10 min; a stray 404 (proxy mid-deploy) does not stick.
MISSING_TTL_SECONDS = 600.0

#: (Base URL, credential) -> when this process found the doors closed to it.
_missing: dict[str, float] = {}
#: (Base URL, credential) whose direct links this process could not use.
_no_direct: set[str] = set()
_missing_lock = threading.Lock()
#: httpx connect/DNS/TLS failures, matched by name: the outbox never imports httpx.
_CONNECT_FAILURES = frozenset({"ConnectError", "ConnectTimeout"})


@dataclass(frozen=True)
class Item:
    """One file: path, the fingerprint it must still match, and its presign body (an ``UploadRequest``)."""

    path: str
    digest: str
    size: int
    content_type: str | None
    body: dict


def _server(client: Any) -> str | None:
    """Server AND credential a door verdict is about (another credential may differ)."""
    settings = getattr(client, "settings", None)
    base = getattr(settings, "base_url", None)
    if not base:
        return None
    token = getattr(settings, "token", None) or getattr(settings, "ingest_token", None) or ""
    return f"{base} {hashlib.sha256(str(token).encode()).hexdigest()[:16]}"


def available(client: Any) -> bool:
    """Whether to try the doors on ``client``'s server (never if it names none)."""
    server = _server(client)
    if server is None:
        return False
    with _missing_lock:
        found = _missing.get(server)
        return found is None or time.monotonic() - found > MISSING_TTL_SECONDS


def enabled() -> bool:
    """Whether a run's window uses these doors (on unless `PROBE_UPLOAD_MANY=0`).

    Prod 2026-10-29, 60 x 5 KB on one run: 3.67 files/s through the doors (8 per
    request, 4 in flight) vs 3.3 per file, with about a sixth of the requests."""
    return os.environ.get("PROBE_UPLOAD_MANY") != "0"


def forget_direct(client: Any) -> None:
    """This process stops asking ``client``'s server for direct links."""
    with _missing_lock:
        _no_direct.add(str(_server(client)))


def direct_wanted(client: Any) -> bool:
    """Whether to ask ``client``'s server for direct-to-storage links."""
    server = _server(client)
    with _missing_lock:
        return server is not None and server not in _no_direct


def _direct_unreachable(client: Any, url: str, exc: BaseException) -> bool:
    """A PUT to a non-API host that could not connect or was refused: direct links fail from here."""
    api_host = urlsplit(str(getattr(client.settings, "base_url", ""))).netloc
    if urlsplit(url).netloc in ("", api_host):
        return False
    if isinstance(exc, errors.UploadRefused):
        return True
    return isinstance(exc, errors.TransportError) and type(exc.__cause__).__name__ in _CONNECT_FAILURES


def _door_missing(exc: BaseException) -> bool:
    """Whether the doors are not for this client: a 405, or a 404 that is not the run
    resolver's (older server, credential not allowed). A missing run is the op's failure."""
    status = getattr(exc, "status", None)
    return status == 405 or (status == 404 and not errors.names_no_such_run(exc))


def _each(pool: Executor, fn: Callable[[int], Any], indices: Iterable[int]) -> dict[int, Any]:
    """index -> ``fn(i)`` on ``pool`` for calls that returned (a raise leaves its index out)."""
    futures = {pool.submit(copy_context().run, fn, i): i for i in indices}
    results: dict[int, Any] = {}
    for future in as_completed(futures):
        try:
            results[futures[future]] = future.result()
        except Exception:  # noqa: BLE001 -- the per-op path meets it again and decides
            pass
    return results


def send(client: Any, run_id: str, items: list[Item], pool: Executor) -> dict[int, dict] | None:
    """Presign, PUT and confirm ``items`` on run ``run_id`` (checks and PUTs on ``pool``).
    Returns index -> confirmed artifact (as `Client.upload_fingerprinted`) for each
    clean file, or None when the server has no such doors (nothing was sent)."""

    def check(i: int) -> bool:
        # As `freeze_upload`: bytes still match their fingerprint (and the strict policy, if on).
        with checked_upload(items[i].path, digest=items[i].digest, size=items[i].size):
            return True

    live = sorted(_each(pool, check, range(len(items))))
    if not live:
        return {}
    try:
        answers = client.presign_run_uploads(
            run_id, [items[i].body for i in live], direct=direct_wanted(client)
        )
    except Exception as exc:  # noqa: BLE001 -- any refusal is the per-op path's to classify
        if _door_missing(exc):
            with _missing_lock:
                _missing[str(_server(client))] = time.monotonic()
            return None
        return {}
    if not isinstance(answers, list) or len(answers) != len(live):
        return {}
    minted = {
        i: answer
        for i, answer in zip(live, answers)
        if isinstance(answer, dict) and answer.get("status") == 201 and answer.get("artifact_id")
    }

    def put(i: int) -> bool:
        item, answer = items[i], minted[i]
        with checked_upload(item.path, digest=item.digest, size=item.size) as frozen:
            try:
                client.transport.put_file(
                    answer["upload_url"],
                    frozen,
                    content_type=item.content_type or "application/octet-stream",
                    headers=answer.get("upload_headers") or answer.get("headers"),
                )
            except Exception as exc:
                if _direct_unreachable(client, answer["upload_url"], exc):
                    forget_direct(client)
                raise  # the per-op path sends this file again, through the relay
        return True

    sent = _each(pool, put, [i for i, answer in minted.items() if not answer.get("have")])
    landed = [i for i, answer in minted.items() if answer.get("have") or sent.get(i)]
    if not landed:
        return {}
    try:
        confirmed = client.confirm_uploads([str(minted[i]["artifact_id"]) for i in landed])
    except Exception:  # noqa: BLE001 -- the per-op path confirms them alone
        return {}
    by_id = {
        str(answer.get("artifact_id")): answer for answer in confirmed if isinstance(answer, dict)
    }
    out: dict[int, dict] = {}
    for i in landed:
        answer = by_id.get(str(minted[i]["artifact_id"]))
        if answer and answer.get("status") == 200 and isinstance(answer.get("artifact"), dict):
            out[i] = answer["artifact"]
    return out
