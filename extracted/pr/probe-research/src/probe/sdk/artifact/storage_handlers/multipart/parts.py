"""Move the bytes: PUT parts from the staged copy in parallel; sha256 the copy on a background thread."""

from __future__ import annotations
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from .... import errors
from ...hashing import fingerprint
from probe.sdk.artifact.storage_handlers.multipart.doors import _grant
from probe.sdk.artifact.storage_handlers.multipart.staging import _check_staged
#: Part PUTs in flight at once, per upload.
PARALLEL_PARTS = 4
#: Consecutive slices with refused part URLs and nothing sent before the upload is permanently refused.
_MAX_REFUSED_SLICES = 3
#: Part URLs asked for per request (the server's own cap).
_PART_URL_BATCH = 100


_HASHING: dict[str, dict] = {}
_HASHING_LOCK = threading.Lock()


def _hash_staged(state: dict) -> tuple[str, int]:
    """sha256 of the staged copy, checked unchanged before and after the read."""
    _check_staged(state)
    digest, size = fingerprint(state["staged_path"])
    _check_staged(state)
    return digest, size


def _hash_in_background(op_id: str, state: dict) -> tuple[str, int] | None:
    """The staged copy's (sha256, size), hashed on a daemon thread so the drain pass
    does not wait ~30 s per 10 GB. None while running (come back later); a process
    dying mid-hash restarts it next visit. Raises what the hash raised."""
    with _HASHING_LOCK:
        job = _HASHING.get(op_id)
        if job is None:
            job = {"done": threading.Event(), "result": None, "error": None}
            _HASHING[op_id] = job

            def run(job=job, state=dict(state)) -> None:
                try:
                    job["result"] = _hash_staged(state)
                except BaseException as exc:  # noqa: BLE001 -- handed to the caller
                    job["error"] = exc
                finally:
                    job["done"].set()

            threading.Thread(target=run, name="probe-multipart-hash", daemon=True).start()
            return None
        if not job["done"].is_set():
            return None
        del _HASHING[op_id]
    if job["error"] is not None:
        raise job["error"]
    return job["result"]


def _send_parts(
    client: Any,
    upload: dict,
    state: dict,
    numbers: list[int],
    deadline: float,
    save: Callable[[], None],
) -> None:
    """PUT these parts from the staged copy, `PARALLEL_PARTS` at a time, starting none after ``deadline``.

    A store failure is TRANSIENT (it blinked; part URLs expire after an hour and
    the next slice asks again): never an auth block. Exception: a store that keeps
    refusing the signed URLs (`UploadRefused`, #2075): `_MAX_REFUSED_SLICES`
    slices in a row that sent nothing make it permanent and the drain records the
    reference row instead of retrying for the 7 days of staging."""
    part_size = int(state["part_size"])
    path = state["staged_path"]
    for start in range(0, len(numbers), _PART_URL_BATCH):
        if time.monotonic() >= deadline:
            return
        grant = _grant(
            client,
            upload,
            state["upload_id"],
            {"part_numbers": numbers[start : start + _PART_URL_BATCH]},
        ) or {}

        def put(part: dict) -> bool:
            if time.monotonic() >= deadline:
                return False
            number = int(part["part_number"])
            client.transport.put_part(
                part["url"],
                path,
                offset=(number - 1) * part_size,
                length=int(part["size"]),
            )
            return True

        with ThreadPoolExecutor(max_workers=PARALLEL_PARTS, thread_name_prefix="probe-part") as pool:
            outcomes = [pool.submit(put, part) for part in grant.get("parts") or ()]
            failures = [f.exception() for f in outcomes if f.exception() is not None]
            sent = sum(1 for f in outcomes if f.exception() is None and f.result())
        if sent and state.get("refused_slices"):
            state["refused_slices"] = 0
            save()
        if not failures:
            continue
        deadline_hit = next((e for e in failures if isinstance(e, errors.DeadlineExceeded)), None)
        if deadline_hit is not None:
            raise deadline_hit
        refused = [e for e in failures if isinstance(e, errors.UploadRefused)]
        if refused and not sent:
            state["refused_slices"] = int(state.get("refused_slices") or 0) + 1
            save()
            if state["refused_slices"] >= _MAX_REFUSED_SLICES:
                raise refused[0]
        first = refused[0] if refused else failures[0]
        # Object storage, not the API: not an auth block nor "server unreachable" for other lanes.
        raise errors.ServerError(
            f"object storage refused a part ({getattr(first, 'status', None)}): {first}", status=503
        ) from None
