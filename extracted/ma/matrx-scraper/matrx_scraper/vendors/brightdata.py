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

Web Unlocker (``POST /request {zone, url, format:"raw"}``) is a different
Bright Data product; it needs a zone, and none exists on our account. It is
deliberately not implemented here.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Literal

import httpx
from matrx_utils import vcprint

BRIGHTDATA_API_ROOT = "https://api.brightdata.com"

#: Sync-scrape wait before Bright Data hands back a snapshot id, plus polling.
DEFAULT_TIMEOUT_S = 180.0
POLL_INTERVAL_S = 3.0

#: HARD bounds on one call, enforced here so every caller inherits them: inputs per call, and
#: the TOTAL records the call may bill (``limit * len(inputs)``). Bright Data bills per returned
#: record; ``limit`` alone is per input, so an unbounded inputs list was an unbounded bill.
MAX_INPUTS_PER_CALL = 10
MAX_TOTAL_RECORDS = 100


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
    over the hard bound. Raised BEFORE anything is sent."""


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


class BrightDataClient:
    """Async client for the Web Scraper API. Construct with the key; the host injects it."""

    def __init__(
        self,
        api_key: str,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        api_root: str = BRIGHTDATA_API_ROOT,
        poll_interval_s: float = POLL_INTERVAL_S,
    ) -> None:
        if not api_key:
            raise ValueError("BrightDataClient needs an api_key")
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
        if not _call_observers:
            raise BrightDataRecorderMissing(
                "Refusing a billable Bright Data request: no cost observer is registered in this "
                "process. The host must call register_brightdata_call_observer(...) first."
            )
        if not inputs:
            raise ValueError("inputs must be a non-empty list")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise BrightDataUncappedRequest(
                f"Refusing an uncapped Bright Data request (limit={limit!r}): every request must "
                "carry a positive per-input record cap."
            )
        if len(inputs) > MAX_INPUTS_PER_CALL or limit * len(inputs) > MAX_TOTAL_RECORDS:
            raise BrightDataCapExceeded(
                f"Refusing a Bright Data request that could bill {limit * len(inputs)} records from "
                f"{len(inputs)} inputs: at most {MAX_INPUTS_PER_CALL} inputs and {MAX_TOTAL_RECORDS} "
                "total records (limit x inputs) per call."
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

        started = time.monotonic()
        deadline = started + timeout_s
        async with self._client(timeout_s) as client:
            try:
                resp = await client.post(f"{self._root}/datasets/v3/scrape", params=params, json=inputs)
            except httpx.TimeoutException as exc:
                raise BrightDataError(f"Bright Data did not answer within {timeout_s:.0f}s") from exc
            except httpx.HTTPError as exc:
                raise BrightDataError(f"Bright Data transport error: {type(exc).__name__}: {exc}") from exc

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
                    raise BrightDataError("Bright Data answered 202 without a snapshot_id", status_code=202, body=body)
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
                    f"Bright Data job {snapshot_id} was still running when the wait ran out"
                    + ("; it was cancelled." if cancelled else "; cancelling it FAILED — it may still bill."),
                    snapshot_id=snapshot_id,
                )
            prog = await client.get(f"{self._root}/datasets/v3/progress/{snapshot_id}")
            if prog.status_code != 200:
                _raise_for(prog)
            status = str((_json(prog) or {}).get("status") or "").lower()
            if status == "ready":
                break
            if status == "failed":
                raise BrightDataError(f"Bright Data job {snapshot_id} failed", body=_json(prog))
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


def _raise_for(resp: httpx.Response) -> None:
    try:
        body: Any = resp.json()
    except ValueError:
        body = resp.text[:500]
    if resp.status_code == 400 and isinstance(body, dict) and body.get("code") == "validation_error":
        errors = list(body.get("errors") or [])
        names = ", ".join(f"{e[0]}: {e[1]}" for e in errors if isinstance(e, list) and len(e) >= 2)
        raise BrightDataInputError(f"Bright Data refused the inputs — {names or body.get('error')}",
                                   field_errors=errors, body=body)
    msg = body.get("error") if isinstance(body, dict) else body
    raise BrightDataError(f"Bright Data answered {resp.status_code}: {msg}", status_code=resp.status_code, body=body)


__all__ = [
    "BRIGHTDATA_API_ROOT",
    "BrightDataBillableCall",
    "BrightDataCallGuard",
    "BrightDataCallObserver",
    "BrightDataCapExceeded",
    "BrightDataClient",
    "BrightDataError",
    "BrightDataInputError",
    "BrightDataRecorderMissing",
    "BrightDataResult",
    "BrightDataTimeout",
    "BrightDataUncappedRequest",
    "MAX_INPUTS_PER_CALL",
    "MAX_TOTAL_RECORDS",
    "clear_brightdata_call_flushers",
    "clear_brightdata_call_guards",
    "clear_brightdata_call_observers",
    "register_brightdata_call_flusher",
    "register_brightdata_call_guard",
    "register_brightdata_call_observer",
]
