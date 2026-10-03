"""Execute the existing portable JavaScript evaluator ABI in a bounded QuickJS sandbox."""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import rfc8785
from pydantic import Field

from .agents import invoke
from .client import EvalClient
from .datasets import read_eval_manifest
from .definitions import define_dataset
from .models import Model, Output, parse_verdict

from .trace_tools import TRACE_PROJECTION_SHA256


class PortableEvalLimits(Model):
    memory_bytes: int = Field(default=32 * 1024 * 1024, gt=0)
    stack_bytes: int = Field(default=64 * 1024, gt=0)
    timeout_ms: float | None = Field(default=None, gt=0)
    max_input_bytes: int = Field(default=4 * 1024 * 1024, gt=0)
    max_output_bytes: int = Field(default=4 * 1024 * 1024, gt=0)
    judge_timeout_ms: float = Field(default=30000, gt=0)
    judge_concurrency: int = Field(default=4, gt=0)


class PortableEvaluator(Model):
    kind: str = "portable"
    artifact: dict[str, Any]
    expected_sha256: str | None = None
    judge: Callable[..., Any] | None = Field(default=None, exclude=True)
    limits: PortableEvalLimits = Field(default_factory=PortableEvalLimits)
    slug: str
    name: str
    output: Output
    scope: str = "batch"


class PortableJudgeRequest(Model):
    trace: dict[str, Any]
    trace_pair: dict[str, Any] | None = None
    rubric: str


def _quickjs() -> Any:
    try:
        import quickjs

        return quickjs
    except ImportError as error:
        raise ImportError(
            'Portable evaluator execution needs pip install "raindrop-ai[portable]"'
        ) from error


def verify_portable_eval_artifact(
    artifact: dict[str, Any], *, expected_sha256: str | None = None
) -> dict[str, Any]:
    expected = {
        "format",
        "formatVersion",
        "runtimeAbi",
        "evaluator",
        "traceProjectionVersion",
        "traceProjectionSha256",
        "source",
        "sha256",
    }
    if (
        set(artifact) != expected
        or artifact["format"] != "raindrop.eval-program"
        or isinstance(artifact["formatVersion"], bool)
        or artifact["formatVersion"] != 1
        or artifact["runtimeAbi"] != "raindrop-eval-v2"
    ):
        raise ValueError("Invalid portable evaluator artifact")
    if (
        isinstance(artifact["traceProjectionVersion"], bool)
        or artifact["traceProjectionVersion"] != 1
        or artifact["traceProjectionSha256"] != TRACE_PROJECTION_SHA256
    ):
        raise ValueError("Portable evaluator targets a different trace projection")
    identity = artifact["evaluator"]
    from uuid import UUID

    UUID(identity["id"])
    if (
        set(identity)
        != {"id", "slug", "programVersion", "executionMode", "outputType", "scope"}
        or identity["scope"] != "batch"
        or identity["outputType"] not in ("boolean", "score", "number")
        or identity["executionMode"] not in ("judge", "deterministic")
    ):
        raise ValueError("Invalid portable evaluator identity")
    if (
        not isinstance(identity["programVersion"], int)
        or isinstance(identity["programVersion"], bool)
        or identity["programVersion"] < 1
        or not identity["slug"]
        or not isinstance(artifact["source"], str)
        or not artifact["source"]
    ):
        raise ValueError("Invalid portable evaluator version or source")
    digest = hashlib.sha256(
        rfc8785.dumps(
            {key: value for key, value in artifact.items() if key != "sha256"}
        )
    ).hexdigest()
    if digest != artifact["sha256"] or (
        expected_sha256 is not None and digest != expected_sha256
    ):
        raise ValueError("Portable artifact does not match its content pin")
    return artifact


def import_portable_evaluator(
    artifact: dict[str, Any],
    *,
    expected_sha256: str | None = None,
    name: str | None = None,
    judge: Callable[..., Any] | None = None,
    limits: PortableEvalLimits | dict[str, Any] | None = None,
) -> PortableEvaluator:
    verified = verify_portable_eval_artifact(artifact, expected_sha256=expected_sha256)
    return PortableEvaluator(
        artifact=verified,
        expected_sha256=expected_sha256,
        name=name or verified["evaluator"]["slug"],
        judge=judge,
        limits=limits or PortableEvalLimits(),
        slug=verified["evaluator"]["slug"],
        output=verified["evaluator"]["outputType"],
    )


async def evaluate_portable_evaluator(
    evaluator: PortableEvaluator,
    *,
    traces: list[dict[str, Any]],
    seed: str,
    rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    artifact = verify_portable_eval_artifact(
        evaluator.artifact, expected_sha256=evaluator.expected_sha256
    )
    cases = [
        {**{k: v for k, v in row.items() if k != "rowId"}, "caseId": row["rowId"]}
        for row in (rows or [])
    ]
    if cases and (
        len(cases) != len(traces)
        or any(
            row["candidate"]["trace"]["event"]["id"] != trace["event"]["id"]
            for row, trace in zip(cases, traces)
        )
    ):
        raise ValueError("Portable rows must match traces exactly, in slice order")
    by_id = {trace["event"]["id"]: trace for trace in traces}
    if len(by_id) != len(traces):
        raise ValueError("Portable trace ids must be unique")
    row_by_id = {row["candidate"]["trace"]["event"]["id"]: row for row in (rows or [])}
    limits = evaluator.limits
    payload = json.dumps(
        {"traces": traces, "cases": cases, "seed": seed},
        ensure_ascii=False,
        allow_nan=False,
    )
    if len(payload.encode()) > limits.max_input_bytes:
        raise ValueError("Portable input exceeds max_input_bytes")
    timeout_ms = limits.timeout_ms or (
        60000 if artifact["evaluator"]["executionMode"] == "judge" else 1000
    )
    deadline = time.monotonic() + timeout_ms / 1000
    vm = _quickjs().Context()
    vm.set_memory_limit(limits.memory_bytes)
    vm.set_max_stack_size(limits.stack_bytes)
    vm.set_time_limit(timeout_ms / 1000)
    vm.eval(
        "var __hostQueue = []; var __hostWaiters = {}; var __done = false; var __output; var __error; globalThis.__raindrop_eval_judge = function(raw) { return new Promise(function(resolve) { var request = JSON.parse(raw); __hostQueue.push(request); __hostWaiters[request.requestId] = resolve; }); };"
    )
    vm.eval(artifact["source"])
    vm.eval(
        "__raindrop_eval_run("
        + json.dumps(payload)
        + ").then(function(value) { __output = value; __done = true; }, function(error) { __error = String(error); __done = true; });"
    )

    async def judge(request: dict[str, Any]) -> dict[str, Any]:
        request_id = request.get("requestId", "unknown")
        try:
            if (
                request.get("type") != "judge_request"
                or request["traceId"] not in by_id
                or evaluator.judge is None
            ):
                raise ValueError("Judge unavailable")
            verdict = await asyncio.wait_for(
                invoke(
                    evaluator.judge,
                    PortableJudgeRequest(
                        trace=by_id[request["traceId"]],
                        trace_pair=row_by_id.get(request["traceId"]),
                        rubric=request["rubric"][:40000],
                    ),
                ),
                timeout=min(
                    limits.judge_timeout_ms / 1000,
                    max(0.001, deadline - time.monotonic()),
                ),
            )
            return {
                "type": "judge_response",
                "requestId": request_id,
                "status": "completed",
                "result": parse_verdict(evaluator.output, verdict),
            }
        except Exception:
            return {
                "type": "judge_response",
                "requestId": request_id,
                "status": "unavailable",
                "message": "Judge unavailable",
            }

    def respond(response: dict[str, Any]) -> None:
        vm.eval(
            "__hostWaiters["
            + json.dumps(response["requestId"])
            + "]("
            + json.dumps(json.dumps(response))
            + ");"
        )

    pending: set[asyncio.Task[dict[str, Any]]] = set()
    try:
        while not vm.eval("__done"):
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Portable evaluator exceeded {timeout_ms}ms")
            vm.set_time_limit(max(0.001, deadline - time.monotonic()))
            # Drain JS microtasks before waiting for host I/O: separate promise
            # continuations can each enqueue a judge request in the same turn.
            while vm.execute_pending_job():
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"Portable evaluator exceeded {timeout_ms}ms")
            requests = json.loads(vm.eval("JSON.stringify(__hostQueue.splice(0))"))
            for request in requests:
                if len(pending) < limits.judge_concurrency:
                    pending.add(asyncio.create_task(judge(request)))
                else:
                    respond(
                        {
                            "type": "judge_response",
                            "requestId": request["requestId"],
                            "status": "unavailable",
                            "message": "Judge unavailable",
                        }
                    )
            if pending:
                completed, pending = await asyncio.wait(
                    pending, return_when=asyncio.FIRST_COMPLETED
                )
                for task in completed:
                    respond(task.result())
            else:
                await asyncio.sleep(0)
    finally:
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
    if vm.eval("__error !== undefined"):
        raise RuntimeError("Portable evaluator failed: " + vm.eval("__error"))
    raw = vm.eval("__output")
    if not isinstance(raw, str) or len(raw.encode()) > limits.max_output_bytes:
        raise ValueError("Portable output exceeds max_output_bytes or is invalid")
    envelope = json.loads(raw)
    if envelope.get("type") != "result":
        raise ValueError("Invalid portable result envelope")
    result = envelope["result"]
    stats = result["stats"]
    for key in ("traceCount", "hydratedCount", "judgeCalls", "skippedRows"):
        if (
            isinstance(stats[key], bool)
            or not isinstance(stats[key], (int, float))
            or stats[key] < 0
            or int(stats[key]) != stats[key]
        ):
            raise ValueError("Invalid portable result statistics")
    duration = stats["durationMs"]
    if (
        isinstance(duration, bool)
        or not isinstance(duration, (int, float))
        or not math.isfinite(duration)
        or duration < 0
        or stats["skippedReason"] not in (None, "no trace")
    ):
        raise ValueError("Invalid portable result statistics")
    if not isinstance(result["failures"], list) or any(
        not isinstance(message, str) for message in result["failures"]
    ):
        raise ValueError("Invalid portable failures")
    if result["stats"]["traceCount"] != len(traces):
        raise ValueError("Inconsistent portable trace count")
    returned = set()
    for outcome in result["outcomes"]:
        trace_id = outcome["traceId"]
        if trace_id not in by_id or trace_id in returned:
            raise ValueError(
                "Portable evaluator returned duplicate or foreign trace ids"
            )
        returned.add(trace_id)
        if outcome["state"] == "graded":
            parse_verdict(
                evaluator.output,
                {
                    k: outcome[k]
                    for k in ("pass", "score", "value", "note")
                    if k in outcome
                },
            )
        elif outcome["state"] == "errored":
            if not isinstance(outcome.get("message"), str):
                raise ValueError("Invalid portable error outcome")
        elif outcome["state"] == "ungraded":
            if outcome.get("reason") not in (
                "not sampled",
                "trace unavailable",
                "content unreadable",
            ):
                raise ValueError("Invalid portable ungraded outcome")
        else:
            raise ValueError("Invalid portable outcome state")
    if returned != set(by_id):
        raise ValueError("Portable evaluator omitted a trace")
    return result


async def pull_eval(
    client: EvalClient,
    *,
    dataset: str,
    evaluators: list[str],
    snapshot_path: str,
    judges: dict[str, Callable[..., Any]] | None = None,
    query_url: str | None = None,
) -> dict[str, Any]:
    if not evaluators or len(set(evaluators)) != len(evaluators):
        raise ValueError("Pulled evaluators must be nonempty and unique")
    manifest = await read_eval_manifest(client, dataset, query_url=query_url)
    from urllib.parse import quote

    pulled = []
    for slug in evaluators:
        data = (
            await client.request(
                "GET", f"/v1/evals/{quote(slug, safe='')}", query_url=query_url
            )
        )["data"]
        artifact = verify_portable_eval_artifact(data["artifact"])
        if data["slug"] != slug or artifact["evaluator"]["slug"] != slug:
            raise ValueError("Pulled artifact identity mismatch")
        pulled.append(
            {
                "slug": slug,
                "name": data["name"],
                "artifact": artifact,
                "expectedSha256": artifact["sha256"],
            }
        )
    snapshot = {
        "schemaVersion": 1,
        "pulledAt": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "reference": dataset,
            "datasetId": manifest["datasetId"],
            "fingerprint": manifest["fingerprint"],
            "rows": manifest["cases"],
        },
        "evaluators": pulled,
    }
    path = Path(snapshot_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(
        mode="w", dir=path.parent, encoding="utf-8", delete=False
    ) as temp:
        json.dump(snapshot, temp, ensure_ascii=False)
        temp.flush()
        import os

        os.fsync(temp.fileno())
        temporary = Path(temp.name)
    try:
        loaded = load_eval_snapshot(str(temporary), judges=judges)
        temporary.replace(path)
        loaded["snapshotPath"] = snapshot_path
        return loaded
    finally:
        temporary.unlink(missing_ok=True)


def load_eval_snapshot(
    snapshot_path: str, *, judges: dict[str, Callable[..., Any]] | None = None
) -> dict[str, Any]:
    snapshot = json.loads(Path(snapshot_path).read_text())
    if snapshot["schemaVersion"] != 1:
        raise ValueError("Unknown eval snapshot version")
    data = snapshot["dataset"]

    def stringify(value: Any) -> str:
        # Snapshot pins use JSON.stringify, including insertion order and JS numbers.
        if isinstance(value, dict):
            indices = sorted(
                (
                    key
                    for key in value
                    if key.isascii()
                    and key.isdecimal()
                    and str(int(key)) == key
                    and int(key) < 2**32 - 1
                ),
                key=int,
            )
            keys = indices + [key for key in value if key not in indices]
            return (
                "{"
                + ",".join(stringify(key) + ":" + stringify(value[key]) for key in keys)
                + "}"
            )
        if isinstance(value, list):
            return "[" + ",".join(stringify(item) for item in value) + "]"
        if isinstance(value, str):
            encoded = json.dumps(value, ensure_ascii=False)
            return "".join(
                f"\\u{ord(char):04x}" if 0xD800 <= ord(char) <= 0xDFFF else char
                for char in encoded
            )
        if isinstance(value, int) and not isinstance(value, bool):
            value = float(value)
        return rfc8785.dumps(value).decode()

    canonical_rows = [
        {
            **{key: row[key] for key in ("id", "name", "input", "output")},
            "properties": dict(
                sorted(
                    row["properties"].items(),
                    key=lambda item: item[0].encode("utf-16-be", "surrogatepass"),
                )
            ),
        }
        for row in data["rows"]
    ]
    canonical_rows.sort(key=lambda row: row["id"].encode("utf-16-be", "surrogatepass"))
    canonical = stringify({"dataset_id": data["datasetId"], "rows": canonical_rows})
    fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
    if fingerprint != data["fingerprint"]:
        raise ValueError("Eval snapshot dataset fingerprint is invalid")
    dataset = define_dataset(
        id=data["datasetId"],
        name=data["reference"],
        version=data["fingerprint"],
        rows=data["rows"],
        remote={
            "reference": data["reference"],
            "datasetId": data["datasetId"],
            "fingerprint": data["fingerprint"],
        },
    )
    evaluators = []
    for entry in snapshot["evaluators"]:
        evaluator = import_portable_evaluator(
            entry["artifact"],
            expected_sha256=entry["expectedSha256"],
            name=entry["name"],
            judge=(judges or {}).get(entry["slug"]),
        )
        if evaluator.slug != entry["slug"]:
            raise ValueError("Eval snapshot evaluator has mismatched identity")
        evaluators.append(evaluator)
    return {"dataset": dataset, "evaluators": evaluators, "snapshotPath": snapshot_path}
