"""ride neighbouring metric ops in one POST and split the batch when it fails."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Callable
from .... import errors
# At module load, not in the drain: a module first imported while a script exits clears
# its pending KeyboardInterrupt (tests/test_ctrlc_exit_code.py).
from ....values import unstorable


# -- coalesced delivery (plan 1.2) ---------------------------------------------

#: One merged POST carries at most this many points and bytes (the server takes 50,000
#: points; a smaller request fails and retries cheaper and keeps one server transaction short).
MERGE_MAX_POINTS = 5_000
MERGE_MAX_BYTES = 2 * 1024 * 1024


def _merge_key(op: dict) -> str | None:
    """What a metric op must share with its neighbours to ride in one POST (everything but its
    points), or None when it never merges.

    Only a logged metrics POST to a run named by its id whose EVERY point has a step or a
    client wall clock: an unstepped point without a timestamp takes the server's transaction
    time, so two merged into one transaction would collapse under the wall-clock dedupe index.
    Ops queued before 1.4 (no wall clock) drain one by one, as they always did.
    """
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("correlation"):
        return None
    match = _METRICS_ROUTE.fullmatch(op.get("path") or "")
    if match is None or not _is_uuid(match.group(1)):
        return None
    body = op.get("body")
    points = body.get("points") if isinstance(body, dict) else None
    if not isinstance(points, list) or not points:
        return None
    for point in points:
        if not isinstance(point, dict):
            return None
        if point.get("step_index") is None and not point.get("wall_clock"):
            return None
    rest = {key: value for key, value in body.items() if key != "points"}
    try:
        return json.dumps(
            [
                op.get("run_ref"),
                op.get("context"),
                op.get("attribution"),
                op.get("path"),
                op.get("blocking", True),
                bool(op.get("best_effort")),
                rest,
            ],
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return None


def _coalesce(
    lane: list[tuple[Path, dict]],
    start: int,
    held_back: str | None,
    *,
    still_queued: Callable[[Path, dict], bool] | None = None,
) -> list:
    """The ops from ``lane[start]`` on that ride in one POST, or [] when fewer than two would:
    consecutive, same `_merge_key`, not held back behind a waiting upload, within the point
    and byte caps. ``still_queued(path, op)`` (a pass that let go of the drain lock, #3618)
    leaves out an op another drain sent meanwhile and re-reads a changed one."""
    if start >= len(lane):
        return []
    head_key = _merge_key(lane[start][1])
    if head_key is None or _attempts(lane[start][1]) > 0:
        # An op that already failed goes alone: were it the poison in a batch, merging it
        # again would pin its failure on the head every pass (review of #2053).
        return []
    batch: list[tuple[Path, dict]] = []
    points = size = 0
    for path, op in lane[start:]:
        if batch and (held_back is not None and path.name > held_back):
            break
        if batch and still_queued is not None and not still_queued(path, op):
            continue
        if _merge_key(op) != head_key or (batch and _attempts(op) > 0):
            break
        count = len(op["body"]["points"])
        weight = len(json.dumps(op["body"]["points"]))
        if batch and (points + count > MERGE_MAX_POINTS or size + weight > MERGE_MAX_BYTES):
            break
        batch.append((path, op))
        points += count
        size += weight
    return batch if len(batch) > 1 else []


def _count_producers(items: list[tuple[Path, dict]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for _, op in items:
        producer_id = op.get("producer_id")
        if producer_id:
            counts[producer_id] = counts.get(producer_id, 0) + 1
    return counts


#: Statuses a merged POST can get because of ONE of its ops: the batch is split in halves
#: until that op is found (review of #2053: a 500, e.g. a step past int64 or a key past the
#: index row size, was pinned on the head and every op before the poison was dead-lettered
#: in turn, 24 h each).
_SPLIT_STATUSES = frozenset({413, 422, 500})


def _merged_failure(exc: Exception) -> str:
    """What a failed merged POST means for its batch: ``"split"`` (one op may be the cause),
    ``"whole"`` (true of every op: the merge key gives the batch one run, epoch and context --
    a fenced epoch, a deleted run, a locked workspace), or ``"stop"`` (the server is busy or
    away: the head's failure, as it would be alone)."""
    if isinstance(exc, errors.DeadlineExceeded):
        return "stop"
    verdict = classify(exc)
    status = getattr(exc, "status", None)
    if verdict == "permanent":
        return "split" if status in _SPLIT_STATUSES or status is None else "whole"
    if verdict == "transient" and status in _SPLIT_STATUSES:
        return "split"
    # 503/429/408/502/504, a connect failure, auth, and an answer lost after sending:
    # splitting that made every half wait out a read timeout (hung server, 2 runs x 64 ops:
    # 14 requests, 28.7 s holding the lock). It stops at the head, which counts toward the
    # pass's lost-answer limit and goes alone next pass (it has an attempt now), so a batch
    # simply too big to answer in time still gets through (review of #2053).
    return "stop"


def _deliver_batch(journal, client, batch, run_ids) -> tuple[list, list, int]:
    """Send ``batch`` (see `_coalesce`) as one POST. Returns (ops that landed; ops that did
    not, each with its error; how many landed inside a multi-op POST), in queue order.

    A merged POST refused for a reason one op could cause (`_merged_failure`: 413, 422, a
    500) is split in halves down to single ops, which go through `_execute` as an unmerged op
    would; an op refused on its own for good is reported and the rest carry on (as behind a
    dead letter). A refusal true of the whole batch (409 fence, 404, a locked workspace)
    reports every op at once, with no further requests. Anything else (503, 429, a connect
    timeout, an auth block, the caller's deadline) stops the batch at its head, as it would
    the op alone; the ops after it are not attempted."""
    landed: list = []
    failed: list = []
    merged = [0]

    def attempt(items) -> bool:
        """False once the batch must stop."""
        if len(items) == 1:
            path, op = items[0]
            try:
                _execute(journal, client, path, op, run_ids)
            except Exception as exc:  # noqa: BLE001 -- settled by the caller
                failed.append((items[0], exc))
                return classify(exc) in ("permanent", "idempotent")
            landed.append(items[0])
            return True
        try:
            _send_merged(client, items)
        except Exception as exc:  # noqa: BLE001 -- classified here, settled by the caller
            how = _merged_failure(exc)
            if how == "split":
                middle = len(items) // 2
                return attempt(items[:middle]) and attempt(items[middle:])
            if how == "whole":
                failed.extend((item, exc) for item in items)
                return True
            failed.append((items[0], exc))
            return False
        landed.extend(items)
        merged[0] += len(items)
        return True

    attempt(list(batch))
    return landed, failed, merged[0]


def _send_merged(client, items) -> None:
    """One POST carrying every point of ``items``, in queue order. Each op is prepared (NUL
    check, scrub) exactly as `_execute` would prepare it alone."""
    points: list = []
    for _, op in items:
        for value in op.values():
            unstorable.has_nul(value)
        unstorable.validate_nuls(op.get("body"), path=op.get("path", ""), method="POST")
        # scanning disabled: op.update(scrub_op(op))
        points.extend(op["body"]["points"])
    head = items[0][1]
    body = {**head["body"], "points": points}
    client.transport.request("POST", head["path"], json_body=body)
from probe.sdk.delivery.ops.classify import classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _execute  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _attempts, _is_uuid  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.upload_windows import _METRICS_ROUTE  # noqa: E402 -- pieces need each other; the front door loads this one first
