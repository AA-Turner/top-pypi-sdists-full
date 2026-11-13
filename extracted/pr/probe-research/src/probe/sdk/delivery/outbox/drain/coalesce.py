"""Ride a run's neighbouring telemetry ops in few POSTs: its metric ops in one `/metrics` POST, its
step records in one `/steps/batch` POST (one pass, plan T4) and its sample ops in one
`/samples/batch` POST; split a batch when it fails."""

from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Callable
from .... import errors
# At module load, not in the drain: a module first imported while a script exits clears
# its pending KeyboardInterrupt (tests/test_ctrlc_exit_code.py).
from ....values import unstorable
from .... import routes
from ....routes import WriteOp


# -- coalesced delivery (plan 1.2) ---------------------------------------------

#: One merged POST carries at most this many points and bytes (the server takes 50,000
#: points; a smaller request fails and retries cheaper and keeps one server transaction short).
MERGE_MAX_POINTS = 5_000
MERGE_MAX_BYTES = 2 * 1024 * 1024
#: Step records per `POST /v1/runs/{id}/steps/batch`: the server's cap (`StepBatch`).
STEPS_MAX = 1_000
#: Items (samples, seals, ...) and bytes per `POST /v1/runs/{id}/samples/batch` (RL plan §4).
SAMPLES_MAX = 1_000
SAMPLES_MAX_BYTES = 4 * 1024 * 1024


def _delivery_headers(op: dict) -> list:
    """What one request carries once for every op in it (`_delivery_scope`): the queuing agent
    session, its 5-minute effort bucket and the write origin. Ops differing here go apart
    (review of #3785, I13), as an upload window's do."""
    return [op.get("agent_session"), _queued_bucket(op), op.get("write_origin")]


def _merge_key(op: dict) -> str | None:
    """What a metric op must share with its neighbours to ride in one POST (everything but its
    points, and its `_delivery_headers`), or None when it never merges.

    Only a logged metrics POST to a run named by its id whose EVERY point has a step or a
    client wall clock: an unstepped point without a timestamp takes the server's transaction
    time, so two merged into one transaction would collapse under the wall-clock dedupe index.
    Ops queued before 1.4 (no wall clock) drain one by one, as they always did.
    """
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("correlation"):
        return None
    route = routes.classify("POST", op.get("path"))
    if route.op is not WriteOp.METRICS or not route.exact or not _is_uuid(route.run):
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
                _delivery_headers(op),
            ],
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return None


#: The server feature that serves `POST /v1/runs/{id}/steps/batch`.
STEPS_BATCH_FEATURE = "steps_batch"


def _step_key(op: dict) -> str | None:
    """What a step op must share with its neighbours to ride in one `/steps/batch` POST (its
    run, context, writer session and epoch, and its `_delivery_headers`), or None when it
    never merges."""
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("correlation"):
        return None
    route = routes.classify("POST", op.get("path"))
    if route.op is not WriteOp.STEPS or not route.exact or not _is_uuid(route.run):
        return None
    body = op.get("body")
    step = body.get("step_index") if isinstance(body, dict) else None
    if not isinstance(step, int) or isinstance(step, bool):
        return None
    try:
        return json.dumps(
            [
                op.get("run_ref"),
                op.get("context"),
                op.get("attribution"),
                op.get("path"),
                op.get("blocking", True),
                bool(op.get("best_effort")),
                body.get("session_id"),
                body.get("write_epoch"),
                _delivery_headers(op),
            ],
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return None


#: The sample routes whose ops merge with their own route's neighbours (the key holds the path, so a
#: `/samples/points` op never rides in a `/samples/batch` POST: an older server would drop its lists unread).
_SAMPLE_ROUTES = frozenset({WriteOp.SAMPLES, WriteOp.SAMPLE_POINTS})


def _get_samples_key(op: dict) -> str | None:
    """What a sample op must share with its neighbours to ride in one `/samples/batch` (or
    `/samples/points`) POST: its run, context, path, writer and every non-list body field (epoch,
    producer), and its `_delivery_headers`. None when it never merges."""
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("correlation"):
        return None
    route = routes.classify("POST", op.get("path"))
    if route.op not in _SAMPLE_ROUTES or not route.exact or not _is_uuid(route.run):
        return None
    body = op.get("body")
    if not isinstance(body, dict):
        return None
    rest = {key: value for key, value in body.items() if not isinstance(value, list)}
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
                _delivery_headers(op),
            ],
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return None


def count_sample_items(body: dict) -> int:
    """Items one samples body carries: every entry of every list field."""
    return sum(len(value) for value in body.values() if isinstance(value, list))


def _collect_sample_batch(
    lane: list[tuple[Path, dict]],
    start: int,
    held_back: str | None,
    *,
    still_queued: Callable[[Path, dict], bool] | None = None,
) -> list:
    """Sample ops sharing the head's `_get_samples_key`, from ``lane[start]``, up to the caps. Metric
    and step ops between them stay queued for their own batch (each kind keeps its order); any
    other op ends the walk. [] unless two or more."""
    if start >= len(lane):
        return []
    head = lane[start][1]
    key = _get_samples_key(head)
    if key is None or _attempts(head) > 0:
        return []
    batch: list = []
    count = size = 0
    stepped: set[tuple[str, object]] = set()
    for path, op in lane[start:]:
        if batch:
            if held_back is not None and path.name > held_back:
                break
            if still_queued is not None and not still_queued(path, op):
                continue
            if _merge_key(op) is not None or _step_key(op) is not None:
                continue
            if _attempts(op) > 0 or _get_samples_key(op) != key:
                break
        items = count_sample_items(op["body"])
        weight = len(json.dumps(op["body"]))
        if batch and (count + items > SAMPLES_MAX or size + weight > SAMPLES_MAX_BYTES):
            break
        # A batch names a step once per seal and once per commit (`SampleBatchIn`).
        steps = _get_sealed_steps(op["body"])
        if steps & stepped:
            break
        batch.append((path, op))
        stepped |= steps
        count += items
        size += weight
    return batch if len(batch) >= 2 else []


def _get_sealed_steps(body: dict) -> set[tuple[str, object]]:
    """The (list, step) pairs a samples body's seals and commits name."""
    return {
        (name, item.get("step"))
        for name in ("seals", "commits")
        for item in body.get(name) or ()
        if isinstance(item, dict)
    }


def _partition(
    lane: list[tuple[Path, dict]],
    start: int,
    held_back: str | None,
    *,
    still_queued: Callable[[Path, dict], bool] | None = None,
) -> tuple[list, list]:
    """ONE walk of a run's lane from ``lane[start]`` (plan T4): metric ops sharing the first
    metric op's `_merge_key` go in the first list, step ops sharing the first step's
    `_step_key` in the second, interleaved as `Run.log` writes them. It stops at the first
    other op, a second key, an op that already failed (a retry goes alone), an op held back
    behind a waiting upload, or a cap. ([], []) unless one list holds two or more: the head
    then goes alone, as before."""
    if start >= len(lane):
        return [], []
    head = lane[start][1]
    if _attempts(head) > 0 or (_merge_key(head) is None and _step_key(head) is None):
        return [], []
    metrics: list = []
    steps: list = []
    metric_key = step_key = None
    points = size = step_size = 0
    for path, op in lane[start:]:
        if metrics or steps:
            if held_back is not None and path.name > held_back:
                break
            if still_queued is not None and not still_queued(path, op):
                continue
            if _attempts(op) > 0 or op.get("context") != head.get("context"):
                break
        key = _merge_key(op)
        if key is not None:
            if metric_key is not None and key != metric_key:
                break
            count = len(op["body"]["points"])
            weight = len(json.dumps(op["body"]["points"]))
            if metrics and (points + count > MERGE_MAX_POINTS or size + weight > MERGE_MAX_BYTES):
                break
            metric_key = key
            metrics.append((path, op))
            points += count
            size += weight
            continue
        key = _step_key(op)
        if key is None or (step_key is not None and key != step_key):
            break
        weight = len(json.dumps(op["body"]))
        if steps and (len(steps) >= STEPS_MAX or step_size + weight > MERGE_MAX_BYTES):
            break
        step_key = key
        steps.append((path, op))
        step_size += weight
    if len(metrics) < 2 and len(steps) < 2:
        return [], []
    return metrics, steps


#: Per base URL: (whether the server serves `steps_batch`, when that was learned). A drain
#: builds its clients per pass, so their own feature cache would ask on every pass.
_STEPS_BATCH_KNOWN: dict[str, tuple[bool, float]] = {}
_STEPS_BATCH_TTL_SECONDS = 600.0


def steps_batch_supported(client) -> bool:
    """Whether ``client``'s server takes `POST /steps/batch` (`GET /v1/server/features`).
    An unanswered question is "no", this time only: its steps go one POST each, as before."""
    cached = getattr(client, "_server_features_cache", None)
    if isinstance(cached, frozenset):
        return STEPS_BATCH_FEATURE in cached
    base = str(getattr(getattr(client, "settings", None), "base_url", "") or "")
    known = _STEPS_BATCH_KNOWN.get(base)
    if known is not None and time.monotonic() - known[1] < _STEPS_BATCH_TTL_SECONDS:
        return known[0]
    ask = getattr(client, "supports_feature", None)
    if ask is None:
        return False
    try:
        answer = bool(ask(STEPS_BATCH_FEATURE))
    except Exception:  # noqa: BLE001 -- unknown is "no", and not remembered
        return False
    if base:
        _STEPS_BATCH_KNOWN[base] = (answer, time.monotonic())
    return answer


def _forget_steps_batch(client) -> None:
    """The server answered the batch route with "no such route" (rolled back): steps go one
    by one until the next look."""
    base = str(getattr(getattr(client, "settings", None), "base_url", "") or "")
    if base:
        _STEPS_BATCH_KNOWN[base] = (False, time.monotonic())
    cached = getattr(client, "_server_features_cache", None)
    if isinstance(cached, frozenset):
        client._server_features_cache = cached - {STEPS_BATCH_FEATURE}


class _BatchRouteAbsent(Exception):
    """`POST /steps/batch` met FastAPI's own 404: an older server. Its ops go one by one."""


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


#: Ops a batch sends one at a time (an older server's step records, a split's halves) before it
#: stops and leaves the rest queued: the pass's next op lets a waiting `finish()` take the drain
#: lock first (review of #3785, I9: 1,000 POSTs in a row held it for minutes).
ALONE_MAX = 32


def _deliver_items(journal, client, batch, run_ids, send) -> tuple[list, list, int, bool]:
    """Send ``batch`` as one POST through ``send(client, items)`` (`_send_merged`,
    `_send_steps`), or each op alone when ``send`` is None, each under its own
    `_delivery_scope`, at most `ALONE_MAX` of them. Returns (ops that landed; ops that did not,
    each with its error; how many landed inside a multi-op POST; whether it stopped before the
    end), in queue order.

    A merged POST refused for a reason one op could cause (`_merged_failure`: 413, 422, a
    500) is split in halves down to single ops, which go through `_execute` as an unmerged op
    would; an op refused on its own for good is reported and the rest carry on (as behind a
    dead letter). A refusal true of the whole batch (409 fence, 404, a locked workspace)
    reports every op at once, with no further requests. Anything else (503, 429, a connect
    timeout, an auth block, the caller's deadline) stops the batch at its head, as it would
    the op alone; the ops after it are not attempted. A batch route the server does not have
    (`_BatchRouteAbsent`) sends its ops one by one."""
    landed: list = []
    failed: list = []
    merged = [0]
    alone = [0]

    def attempt(items) -> bool:
        """False once the batch must stop."""
        if len(items) == 1 or send is None:
            for item in items:
                if alone[0] >= ALONE_MAX:
                    return False  # the rest stays queued, in order, for the pass's next ops
                alone[0] += 1
                path, op = item
                try:
                    with _delivery_scope(op):
                        _execute(journal, client, path, op, run_ids)
                except Exception as exc:  # noqa: BLE001 -- settled by the caller
                    failed.append((item, exc))
                    if classify(exc) not in ("permanent", "idempotent"):
                        return False
                    continue
                landed.append(item)
            return True
        try:
            send(client, items)
        except _BatchRouteAbsent:
            return attempt_alone(items)
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

    def attempt_alone(items) -> bool:
        nonlocal send
        send = None
        return attempt(items)

    finished = attempt(list(batch))
    return landed, failed, merged[0], not finished


def _send_steps(client, items) -> None:
    """One `POST /v1/runs/{id}/steps/batch` carrying every step record of ``items`` in queue
    order (the server keeps the last of a repeated step, as one-by-one POSTs did). The writer
    fence (`session_id`, `write_epoch`, shared by `_step_key`) rides once, at the top."""
    steps: list = []
    for _, op in items:
        for value in op.values():
            unstorable.has_nul(value)
        unstorable.validate_nuls(op.get("body"), path=op.get("path", ""), method="POST")
        steps.append({k: v for k, v in op["body"].items() if k not in ("session_id", "write_epoch")})
    head = items[0][1]
    body: dict = {"steps": steps}
    for fence in ("session_id", "write_epoch"):
        if fence in head["body"]:
            body[fence] = head["body"][fence]
    try:
        client.transport.request(
            "POST",
            routes.batch_path(WriteOp.STEPS, head["path"]),
            json_body=body,
            **build_async_ack_kwargs(client),
        )
    except errors.NotFoundError as exc:
        if getattr(exc, "detail", None) == "Not Found":  # FastAPI's: no such route
            _forget_steps_batch(client)
            raise _BatchRouteAbsent from exc
        raise


def merge_sample_bodies(bodies: list[dict]) -> dict:
    """One samples body from many sharing a `_get_samples_key`: each list field concatenated in
    queue order, the rest (epoch, producer) taken from the first."""
    merged: dict = {}
    for body in bodies:
        for key, value in body.items():
            if isinstance(value, list):
                merged.setdefault(key, []).extend(value)
            else:
                merged.setdefault(key, value)
    return merged


def _send_samples(client, items) -> None:
    """One `POST /v1/runs/{id}/samples/batch` (or `/samples/points`) carrying every item of ``items``,
    in queue order."""
    for _, op in items:
        for value in op.values():
            unstorable.has_nul(value)
        unstorable.validate_nuls(op.get("body"), path=op.get("path", ""), method="POST")
    head = items[0][1]
    body = gate_samples_body(client, "POST", head["path"], merge_sample_bodies([op["body"] for _, op in items]))
    client.transport.request("POST", head["path"], json_body=body, **build_async_ack_kwargs(client))


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
    client.transport.request("POST", head["path"], json_body=body, **build_async_ack_kwargs(client))
from probe.sdk.delivery.ops.classify import classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ingest_queue import build_async_ack_kwargs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _execute  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _delivery_scope  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import gate_samples_body  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _attempts, _is_uuid, _queued_bucket  # noqa: E402 -- pieces need each other; the front door loads this one first
