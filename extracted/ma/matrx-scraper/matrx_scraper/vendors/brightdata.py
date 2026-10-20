"""Bright Data Web Scraper API — the ONE client for structured site records.

Bright Data sells per-site "datasets" (Google Maps place, Trustpilot reviews,
Indeed jobs, ...): send inputs (a URL, or a keyword for a discover mode), get
structured JSON records back. Billed per RECORD delivered.

Wire contract (live-verified 2026-10-11):

* ``POST /datasets/v3/scrape?dataset_id=<id>&format=json&include_errors=true``
  with a JSON array body ``[{"url": ...}]``. Small jobs answer 200 with the
  records inline; larger ones answer 202 ``{"snapshot_id": ...}``.
* 202 → poll ``GET /datasets/v3/progress/{id}`` until ``status=ready`` (or
  ``failed``) → ``GET /datasets/v3/snapshot/{id}?format=json``.
* Discover modes add ``&type=discover_new&discover_by=<keyword|...>`` and accept
  ``&limit_per_input=N``.
* An invalid input answers 400 ``validation_error`` naming the required fields
  (free) — the catalog's ``required_fields`` were read off exactly that.

Money discipline — FAIL CLOSED. Every request that can bill is preceded by the
registered guards (a guard refuses by raising) and followed by the registered
observers (the host turns a ``BrightDataBillableCall`` into a ledger row). With
NO observer registered the client refuses to send at all
(``BrightDataRecorderMissing``): spend no ledger sees is the defect this exists
to stop. The package never reads the API key from the environment; the host
constructs the client and injects it (``configure_ext(brightdata_client=...)``).

Web Unlocker (``POST /request {zone, url, format:"raw"}``) is a different product billed per
successful REQUEST. Its zone is ``matrx_unlocker`` (created 2026-10-12). ``unlock(url)`` below goes
through the SAME fail-closed observer/guard: the billable call carries ``operation="unlock"`` and
``units = 1 request``; the guards are asked with ``"unlock:<zone>"``.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field, replace
from typing import Any, Literal

import httpx
from matrx_utils import vcprint

from matrx_scraper.utils.proxy import redact_url_secrets

BRIGHTDATA_API_ROOT = "https://api.brightdata.com"

#: Sync-scrape wait before Bright Data hands back a snapshot id, plus polling.
DEFAULT_TIMEOUT_S = 180.0
POLL_INTERVAL_S = 3.0

#: HARD bounds on one call, enforced here so every caller inherits them: inputs per call, and
#: the TOTAL records the call may bill (``limit * len(inputs)``). Bright Data bills per returned
#: record; ``limit`` alone is per input, so an unbounded inputs list was an unbounded bill.
#: These are the STANDALONE defaults. A host injects its own numbers (its limit knobs) with
#: ``configure_ext(site_data_limits=<async () -> BrightDataLimits>)``; the guards stay fail-closed
#: either way, only the numbers move. Read the live ones with ``await current_limits()``.
MAX_INPUTS_PER_CALL = 10
MAX_TOTAL_RECORDS = 100

#: ``configure_ext`` key for the host's limits callable.
EXT_LIMITS = "site_data_limits"


@dataclass(frozen=True, slots=True)
class BrightDataLimits:
    """The per-call ceilings in force. ``*_setting`` names where the number came from (the
    host's knob, or ``"package default"``) so a refusal can say which setting to change."""

    max_inputs: int = MAX_INPUTS_PER_CALL
    max_total_records: int = MAX_TOTAL_RECORDS
    max_inputs_setting: str = "package default"
    max_total_records_setting: str = "package default"
    #: Set ONLY when the host's setting could not be read and the built-in numbers are standing in:
    #: the plain sentence a caller shows next to the result (a stand-in announces itself).
    notice: str | None = None


DEFAULT_LIMITS = BrightDataLimits()


def _fallback_limits() -> BrightDataLimits:
    """The built-in numbers standing in for a setting that could not be read, saying so."""
    return replace(
        DEFAULT_LIMITS,
        notice=(f"Using the built-in limit of {DEFAULT_LIMITS.max_total_records} records because your "
                "organization's setting could not be read."),
    )


async def current_limits() -> BrightDataLimits:
    """The ceilings for THIS call: the host's injected callable, else the package defaults.

    A host callable that raises or answers nonsense is a defect, so it is said loudly and the
    package defaults hold (fail closed: the defaults are the small numbers)."""
    from matrx_scraper._ext import get_ext, has_ext

    if not has_ext(EXT_LIMITS):
        return DEFAULT_LIMITS
    hook = get_ext(EXT_LIMITS)
    if hook is None:
        return DEFAULT_LIMITS
    try:
        got = await hook()
    except Exception as exc:  # noqa: BLE001 - a broken hook must not lift the ceiling
        vcprint(f"[brightdata] limits hook raised {type(exc).__name__}: {exc}; package defaults hold",
                color="red", log_level=logging.ERROR)
        return _fallback_limits()
    if (not isinstance(got, BrightDataLimits) or got.max_inputs < 1 or got.max_total_records < 1):
        vcprint(f"[brightdata] limits hook answered {got!r}; package defaults hold", color="red",
                log_level=logging.ERROR)
        return _fallback_limits()
    return got


class BrightDataError(RuntimeError):
    """A Bright Data request failed. ``status_code`` is the HTTP status (0 = transport)."""

    def __init__(self, message: str, *, status_code: int = 0, body: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class BrightDataInputError(BrightDataError):
    """Bright Data refused the inputs (400 validation_error). ``field_errors`` names the fields."""

    def __init__(self, message: str, *, field_errors: list[Any], body: Any = None) -> None:
        super().__init__(message, status_code=400, body=body)
        self.field_errors = field_errors


class BrightDataTimeout(BrightDataError):
    """The job did not finish inside the bound. ``snapshot_id`` can still be collected later."""

    def __init__(self, message: str, *, snapshot_id: str) -> None:
        super().__init__(message)
        self.snapshot_id = snapshot_id


class BrightDataUncappedRequest(ValueError):
    """A request was about to leave with no record cap. Bright Data bills every record it
    returns and some datasets fan out unbounded (one Trustpilot URL returned 230 records), so
    an uncapped request is refused BEFORE it is sent."""


class BrightDataCapExceeded(BrightDataUncappedRequest):
    """The request's TOTAL possible record bill (``limit * len(inputs)``) or its input count is
    over the hard bound. Raised BEFORE anything is sent. ``limits`` = the ceilings in force."""

    def __init__(self, message: str, *, limits: BrightDataLimits | None = None) -> None:
        super().__init__(message)
        self.limits = limits


class BrightDataRecorderMissing(RuntimeError):
    """A billable request was about to leave a process where nothing records its cost.
    Raised BEFORE the request is sent."""


@dataclass(frozen=True, slots=True)
class BrightDataBillableCall:
    """One completed job Bright Data will bill. ``records_billed`` = good records delivered."""

    dataset_id: str
    records_billed: int
    snapshot_id: str | None
    mode: str
    discover_by: str | None = None
    inputs: int = 1
    #: True when ``records_billed`` is the cap booked conservatively (a job that timed out and
    #: whose delivery is unknown), not a count of records received.
    estimated: bool = False
    detail: str = ""
    #: ``record`` (Web Scraper API, units = records) or ``unlock`` (Web Unlocker, units = requests).
    operation: str = "record"


BrightDataCallObserver = Callable[[BrightDataBillableCall], None]
#: Pre-call guards, awaited with ``(dataset_id)`` before any request leaves. Refuse by raising.
BrightDataCallGuard = Callable[[str], Awaitable[None]]

_call_observers: list[BrightDataCallObserver] = []
_call_guards: list[BrightDataCallGuard] = []


def register_brightdata_call_observer(observer: BrightDataCallObserver) -> None:
    """Install a host cost observer. Idempotent — a double registration would double-bill."""
    if observer not in _call_observers:
        _call_observers.append(observer)


def clear_brightdata_call_observers() -> None:
    _call_observers.clear()


def register_brightdata_call_guard(guard: BrightDataCallGuard) -> None:
    if guard not in _call_guards:
        _call_guards.append(guard)


def clear_brightdata_call_guards() -> None:
    _call_guards.clear()


#: Awaited after each observed call so the ledger row is durable before ``scrape`` returns —
#: a short-lived process (a script) can otherwise exit with the detached write unfinished,
#: which lost a real 3-record row on 2026-10-11. A server registers the same drain.
_flushers: list[Callable[[], Awaitable[object]]] = []


def register_brightdata_call_flusher(flusher: Callable[[], Awaitable[object]]) -> None:
    if flusher not in _flushers:
        _flushers.append(flusher)


def clear_brightdata_call_flushers() -> None:
    _flushers.clear()


async def _flush() -> None:
    for flusher in list(_flushers):
        try:
            await flusher()
        except Exception as exc:  # noqa: BLE001 - the records are already paid for
            vcprint(f"[brightdata] call flusher {flusher!r} raised {type(exc).__name__}: {exc}", color="red")


def _notify_billable(call: BrightDataBillableCall) -> None:
    for observer in list(_call_observers):
        try:
            observer(call)
        except Exception as exc:  # noqa: BLE001 - never lose paid records to bookkeeping
            vcprint(
                f"[brightdata] call observer {observer!r} raised {type(exc).__name__}: {exc}",
                color="red",
            )


@dataclass
class BrightDataResult:
    records: list[dict[str, Any]]
    snapshot_id: str | None
    mode: Literal["sync", "snapshot"]
    records_billed: int
    errors: list[dict[str, Any]] = field(default_factory=list)
    elapsed_s: float = 0.0


def _is_error_record(rec: Any) -> bool:
    """``include_errors=true`` mixes per-input failures into the record list."""
    if not isinstance(rec, dict):
        return True
    if rec.get("error") or rec.get("error_code"):
        return True
    return False


def _split(rows: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if isinstance(rows, dict):
        rows = [rows]
    if not isinstance(rows, list):
        return [], [{"error": f"unexpected payload type {type(rows).__name__}"}]
    good, bad = [], []
    for rec in rows:
        if _is_error_record(rec):
            bad.append(rec if isinstance(rec, dict) else {"error": repr(rec)[:300]})
        else:
            good.append(rec)
    return good, bad


UNLOCKER_ZONE = "matrx_unlocker"
#: Hard ceiling on one unlocked page body we keep, so a huge page can never balloon memory.
UNLOCK_MAX_BYTES = 5_000_000
UNLOCK_TIMEOUT_S = 60.0


@dataclass
class UnlockResult:
    """One Web Unlocker request. ``status`` = the TARGET page's HTTP status as relayed; ``html``
    the body; ``billed`` whether this request was booked as a billable unlock."""

    url: str
    status: int
    html: str
    elapsed_s: float
    billed: bool
    error_code: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error_code is None and 200 <= self.status < 300 and bool(self.html)


class BrightDataClient:
    """Async client for the Web Scraper API and Web Unlocker. Construct with the key; the host injects it."""

    def __init__(
        self,
        api_key: str,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        api_root: str = BRIGHTDATA_API_ROOT,
        poll_interval_s: float = POLL_INTERVAL_S,
        unlocker_zone: str = UNLOCKER_ZONE,
    ) -> None:
        if not api_key:
            raise ValueError("BrightDataClient needs an api_key")
        self._unlocker_zone = unlocker_zone
        self._api_key = api_key
        self._transport = transport
        self._root = api_root.rstrip("/")
        self._poll_interval_s = poll_interval_s

    def __repr__(self) -> str:  # never leak the key into a log line
        return f"BrightDataClient(root={self._root!r})"

    def _client(self, timeout_s: float) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            transport=self._transport,
            timeout=httpx.Timeout(timeout_s, connect=15.0),
            headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
        )

    async def scrape(
        self,
        dataset_id: str,
        inputs: list[dict[str, Any]],
        *,
        limit: int,
        discover_by: str | None = None,
        timeout_s: float = DEFAULT_TIMEOUT_S,
    ) -> BrightDataResult:
        """Run one job: sync answer when Bright Data has it inline, else poll the snapshot.

        Raises ``BrightDataRecorderMissing`` (nothing sent) when no cost observer is
        registered, ``BrightDataUncappedRequest`` (nothing sent) when ``limit`` is not a
        positive record cap, ``BrightDataInputError`` on a 400 naming fields, ``BrightDataTimeout``
        (carrying the snapshot id) past ``timeout_s``, ``BrightDataError`` otherwise.
        """
        params = await self._admit(dataset_id, inputs, limit=limit, discover_by=discover_by)

        started = time.monotonic()
        deadline = started + timeout_s
        async with self._client(timeout_s) as client:
            try:
                resp = await client.post(f"{self._root}/datasets/v3/scrape", params=params, json=inputs)
            except httpx.TimeoutException as exc:
                raise BrightDataError(f"The data source did not answer within {timeout_s:.0f}s") from exc
            except httpx.HTTPError as exc:
                raise BrightDataError("The data source could not be reached") from exc

            if resp.status_code == 200:
                good, bad = _split(_json(resp))
                billed = len(good)  # Bright Data bills every record it returned
                good = good[: limit * len(inputs)]
                result = BrightDataResult(
                    records=good, snapshot_id=None, mode="sync", records_billed=billed,
                    errors=bad, elapsed_s=time.monotonic() - started,
                )
            elif resp.status_code == 202:
                body = _json(resp)
                snapshot_id = str((body or {}).get("snapshot_id") or "")
                if not snapshot_id:
                    raise BrightDataError("The data source accepted the request but gave no job to follow", status_code=202, body=body)
                try:
                    rows = await self._await_snapshot(client, snapshot_id, deadline=deadline)
                except BrightDataTimeout as exc:
                    # Delivery is unknown and the job may have billed before the cancel landed:
                    # book the cap (the upper bound), announced as estimated; never free.
                    _notify_billable(
                        BrightDataBillableCall(
                            dataset_id=dataset_id, records_billed=limit * len(inputs),
                            snapshot_id=snapshot_id, mode="snapshot", discover_by=discover_by,
                            inputs=len(inputs), estimated=True,
                            detail=f"estimated: timed out after {timeout_s:.0f}s, booked at the cap "
                                   f"of {limit * len(inputs)} records; {exc}",
                        )
                    )
                    await _flush()
                    raise
                good, bad = _split(rows)
                billed = len(good)
                good = good[: limit * len(inputs)]
                result = BrightDataResult(
                    records=good, snapshot_id=snapshot_id, mode="snapshot", records_billed=billed,
                    errors=bad, elapsed_s=time.monotonic() - started,
                )
            else:
                _raise_for(resp)
                raise AssertionError("unreachable")  # pragma: no cover

        if result.records_billed:
            _notify_billable(
                BrightDataBillableCall(
                    dataset_id=dataset_id, records_billed=result.records_billed,
                    snapshot_id=result.snapshot_id, mode=result.mode,
                    discover_by=discover_by, inputs=len(inputs),
                )
            )
            await _flush()
        return result

    async def unlock(self, url: str, *, timeout_s: float = UNLOCK_TIMEOUT_S) -> UnlockResult:
        """``POST /request {zone, url, format:"raw"}`` — fetch ONE page through the unlocker.

        Fail closed exactly like ``scrape``: ``BrightDataRecorderMissing`` (nothing sent) when no
        cost observer is registered, and every registered guard is awaited first (a spend refusal
        raises). A request the unlocker served (HTTP 200 with no ``x-brd-err-code``) is booked
        ONCE as ``operation="unlock"``, units = 1, and flushed before this returns. A failed
        request (error code / non-200) is not booked.
        """
        if not _call_observers:
            raise BrightDataRecorderMissing(
                "Refusing a billable request: no cost observer is registered in this "
                "process. The host must register a call observer first."
            )
        if not isinstance(url, str) or not url.strip().lower().startswith(("http://", "https://")):
            raise ValueError("unlock needs an http(s) URL")
        for guard in list(_call_guards):
            await guard(f"unlock:{self._unlocker_zone}")
        started = time.monotonic()
        async with self._client(timeout_s) as client:
            try:
                resp = await client.post(
                    f"{self._root}/request",
                    json={"zone": self._unlocker_zone, "url": url.strip(), "format": "raw"},
                )
            except httpx.TimeoutException as exc:
                raise BrightDataError(f"The page did not answer within {timeout_s:.0f}s") from exc
            except httpx.HTTPError as exc:
                raise BrightDataError("The page could not be reached") from exc
        elapsed = time.monotonic() - started
        err_code = resp.headers.get("x-brd-err-code") or None
        err_msg = resp.headers.get("x-brd-err-msg") or None
        body = resp.content[:UNLOCK_MAX_BYTES].decode(resp.encoding or "utf-8", errors="replace")
        served = resp.status_code == 200 and err_code is None
        if not served:
            vcprint(f"[brightdata] unlock HTTP {resp.status_code} code={err_code} msg={_scrub(err_msg)[:200]}",
                    color="yellow", log_level=logging.WARNING)
            return UnlockResult(
                url=url, status=resp.status_code, html="", elapsed_s=elapsed, billed=False,
                error_code=err_code or f"http_{resp.status_code}",
                error=_scrub(err_msg or body[:200]) or None,
            )
        _notify_billable(
            BrightDataBillableCall(
                dataset_id=self._unlocker_zone, records_billed=1, snapshot_id=None, mode="unlock",
                inputs=1, operation="unlock", detail=f"unlock {url[:200]}",
            )
        )
        await _flush()
        return UnlockResult(url=url, status=200, html=body, elapsed_s=elapsed, billed=True)

    async def _admit(
        self, dataset_id: str, inputs: list[dict[str, Any]], *, limit: int, discover_by: str | None
    ) -> dict[str, Any]:
        """Every refusal that must happen BEFORE a billable request leaves, then its params."""
        if not _call_observers:
            raise BrightDataRecorderMissing(
                "Refusing a billable request: no cost observer is registered in this "
                "process. The host must register a call observer first."
            )
        if not inputs:
            raise ValueError("inputs must be a non-empty list")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise BrightDataUncappedRequest(
                f"Refusing an uncapped request (limit={limit!r}): every request must "
                "carry a positive per-input record cap."
            )
        limits = await current_limits()
        if len(inputs) > limits.max_inputs or limit * len(inputs) > limits.max_total_records:
            raise BrightDataCapExceeded(
                f"Refusing a request that could bill {limit * len(inputs)} records from "
                f"{len(inputs)} inputs: at most {limits.max_inputs} inputs and {limits.max_total_records} "
                "total records (limit x inputs) per call.",
                limits=limits,
            )
        for guard in list(_call_guards):
            await guard(dataset_id)

        params: dict[str, Any] = {"dataset_id": dataset_id, "format": "json", "include_errors": "true"}
        if discover_by:
            params["type"] = "discover_new"
            params["discover_by"] = discover_by
        # The cap rides BOTH query params: limit_per_input (discover modes) and
        # limit_multiple_results (URL collections that return many records per URL).
        # Billing happens server-side, so the cap on the REQUEST is what saves money;
        # the result is also truncated on receipt.
        params["limit_per_input"] = limit
        params["limit_multiple_results"] = limit
        return params

    # ── Trigger mode: durable jobs ────────────────────────────────────────
    # ``scrape`` waits in-process and cancels on timeout. A host that persists the snapshot id
    # (a durable job) uses these three instead: nothing is canceled, a restarted process asks
    # ``progress`` again and ``collect``s when ready. Billing is booked once, at ``collect``.

    async def trigger(
        self,
        dataset_id: str,
        inputs: list[dict[str, Any]],
        *,
        limit: int,
        discover_by: str | None = None,
    ) -> str:
        """``POST /datasets/v3/trigger`` → the snapshot id. Same refusals as ``scrape``."""
        params = await self._admit(dataset_id, inputs, limit=limit, discover_by=discover_by)
        params.pop("format", None)
        async with self._client(60.0) as client:
            try:
                resp = await client.post(f"{self._root}/datasets/v3/trigger", params=params, json=inputs)
            except httpx.HTTPError as exc:
                raise BrightDataError("The data source could not be reached") from exc
        if resp.status_code != 200:
            _raise_for(resp)
        snapshot_id = str((_json(resp) or {}).get("snapshot_id") or "")
        if not snapshot_id:
            raise BrightDataError("The data source accepted the request but gave no job to follow", body=_json(resp))
        return snapshot_id

    async def progress(self, snapshot_id: str) -> dict[str, Any]:
        """``GET /datasets/v3/progress/{id}`` — ``status`` is running | ready | failed (+ counts)."""
        async with self._client(30.0) as client:
            try:
                prog = await client.get(f"{self._root}/datasets/v3/progress/{snapshot_id}")
            except httpx.HTTPError as exc:
                raise BrightDataError("The data source could not be reached") from exc
        if prog.status_code != 200:
            _raise_for(prog)
        body = _json(prog) or {}
        return body if isinstance(body, dict) else {"status": str(body)}

    async def collect(
        self,
        snapshot_id: str,
        *,
        dataset_id: str,
        limit_total: int,
        inputs: int = 1,
        discover_by: str | None = None,
        bill: bool = True,
    ) -> BrightDataResult:
        """Download a READY snapshot. ``bill=False`` when the host already booked this snapshot
        (a resumed job re-downloading after a crash) — a snapshot is billed exactly once."""
        started = time.monotonic()
        async with self._client(300.0) as client:
            try:
                snap = await client.get(f"{self._root}/datasets/v3/snapshot/{snapshot_id}", params={"format": "json"})
            except httpx.HTTPError as exc:
                raise BrightDataError("The data source could not be reached") from exc
        if snap.status_code == 202:
            raise BrightDataError("The data source has not finished preparing these records yet", status_code=202)
        if snap.status_code != 200:
            _raise_for(snap)
        good, bad = _split(_json(snap))
        billed = len(good)
        result = BrightDataResult(
            records=good[:limit_total], snapshot_id=snapshot_id, mode="snapshot", records_billed=billed,
            errors=bad, elapsed_s=time.monotonic() - started,
        )
        if bill and billed:
            _notify_billable(
                BrightDataBillableCall(
                    dataset_id=dataset_id, records_billed=billed, snapshot_id=snapshot_id,
                    mode="snapshot", discover_by=discover_by, inputs=inputs,
                )
            )
            await _flush()
        return result

    async def _await_snapshot(self, client: httpx.AsyncClient, snapshot_id: str, *, deadline: float) -> Any:
        while True:
            if time.monotonic() >= deadline:
                # A job left running still delivers — and bills — records nobody collects or
                # records. Cancel it (best effort) so a timeout never becomes unledgered spend.
                cancelled = False
                try:
                    c = await client.post(f"{self._root}/datasets/v3/snapshot/{snapshot_id}/cancel")
                    cancelled = c.status_code == 200
                except httpx.HTTPError:
                    cancelled = False
                raise BrightDataTimeout(
                    "The data source was still collecting when the wait ran out"
                    + ("; it was canceled." if cancelled else "; canceling it FAILED — it may still bill."),
                    snapshot_id=snapshot_id,
                )
            prog = await client.get(f"{self._root}/datasets/v3/progress/{snapshot_id}")
            if prog.status_code != 200:
                _raise_for(prog)
            status = str((_json(prog) or {}).get("status") or "").lower()
            if status == "ready":
                break
            if status == "failed":
                raise BrightDataError("The data source could not collect these records", body=_json(prog))
            await asyncio.sleep(self._poll_interval_s)
        snap = await client.get(f"{self._root}/datasets/v3/snapshot/{snapshot_id}", params={"format": "json"})
        if snap.status_code != 200:
            _raise_for(snap)
        return _json(snap)


def _json(resp: httpx.Response) -> Any:
    try:
        return resp.json()
    except ValueError:
        # format=json occasionally returns NDJSON for snapshots.
        import json

        rows = [json.loads(line) for line in resp.text.splitlines() if line.strip()]
        return rows


_VENDOR_WORDS = re.compile(r"bright\s*-?data|brightdata|\bgd_[a-z0-9]+", re.IGNORECASE)


def _scrub(text: Any) -> str:
    """Words from the data source that may reach a person or an agent: the vendor's name and
    dataset ids never do (Arman: we never say it is from the vendor). Detail lives in server logs."""
    return _VENDOR_WORDS.sub("the data source", str(text if text is not None else "")).strip()


scrub_vendor_text = _scrub


def _raise_for(resp: httpx.Response) -> None:
    try:
        body: Any = resp.json()
    except ValueError:
        body = resp.text[:500]
    vcprint(f"[brightdata] HTTP {resp.status_code} from {redact_url_secrets(str(resp.request.url.path))}: {str(body)[:500]}",
            color="red", log_level=logging.WARNING)
    if resp.status_code == 400 and isinstance(body, dict) and body.get("code") == "validation_error":
        errors = list(body.get("errors") or [])
        names = ", ".join(f"{e[0]}: {e[1]}" for e in errors if isinstance(e, list) and len(e) >= 2)
        raise BrightDataInputError(f"The data source refused these inputs: {_scrub(names or body.get('error'))}",
                                   field_errors=errors, body=body)
    raise BrightDataError(f"The data source answered with an error (HTTP {resp.status_code})", status_code=resp.status_code, body=body)


__all__ = [
    "BRIGHTDATA_API_ROOT",
    "BrightDataBillableCall",
    "BrightDataCallGuard",
    "BrightDataCallObserver",
    "BrightDataCapExceeded",
    "BrightDataClient",
    "BrightDataError",
    "BrightDataInputError",
    "BrightDataLimits",
    "DEFAULT_LIMITS",
    "EXT_LIMITS",
    "current_limits",
    "scrub_vendor_text",
    "BrightDataRecorderMissing",
    "BrightDataResult",
    "BrightDataTimeout",
    "BrightDataUncappedRequest",
    "UNLOCKER_ZONE",
    "UnlockResult",
    "MAX_INPUTS_PER_CALL",
    "MAX_TOTAL_RECORDS",
    "clear_brightdata_call_flushers",
    "clear_brightdata_call_guards",
    "clear_brightdata_call_observers",
    "register_brightdata_call_flusher",
    "register_brightdata_call_guard",
    "register_brightdata_call_observer",
]
