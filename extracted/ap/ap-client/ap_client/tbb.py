from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Sequence

from . import waiter

TBB_TEMPLATE = "trajbigbang-pipeline"
TBB_API_VERSION = "trajbigbang.agenthub/v1"
TBB_ENGINE = "pipeline"
TBB_RUN_TAG = "tbb-pipeline:run"
TBB_VALIDATE_TAG = "tbb-pipeline:validate-config"
TBB_MAX_REQUEST_BYTES = 64 * 1024
_COMMAND_TAGS = {"run": TBB_RUN_TAG, "validate-config": TBB_VALIDATE_TAG}


class TBBProtocolError(ValueError):
    pass


def _new_uuid() -> str:
    return str(uuid.uuid4())


def read_pipeline_config(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise TBBProtocolError(f"cannot read UTF-8 config {path}: {exc}") from exc
    if not content.strip():
        raise TBBProtocolError(f"config {path} must not be empty")
    return content


def build_tbb_params(
    config_text: str,
    command: str,
    runtime_timeout_sec: int | None = None,
) -> dict[str, Any]:
    if command not in _COMMAND_TAGS:
        raise TBBProtocolError(f"unsupported TBB command: {command}")
    request = {
        "apiVersion": TBB_API_VERSION,
        "requestId": f"req-{_new_uuid()}",
        "workspaceKey": f"workspace-{_new_uuid()}",
        "engine": TBB_ENGINE,
        "command": command,
        "config": config_text,
        "argv": [],
    }
    encoded = json.dumps(request, ensure_ascii=False, separators=(",", ":"))
    if len(encoded.encode("utf-8")) > TBB_MAX_REQUEST_BYTES:
        raise TBBProtocolError("serialized TBB request_json exceeds 64 KiB")
    params: dict[str, Any] = {"request_json": encoded}
    if runtime_timeout_sec is not None:
        params["runtime_timeout_sec"] = runtime_timeout_sec
    return params


def merge_tbb_tags(command: str, user_tags: Sequence[str] | None) -> list[str]:
    try:
        reserved = _COMMAND_TAGS[command]
    except KeyError as exc:
        raise TBBProtocolError(f"unsupported TBB command: {command}") from exc
    merged = [reserved]
    seen = {reserved}
    for raw in user_tags or ():
        value = str(raw).strip()
        if not value:
            continue
        if value.startswith("tbb-pipeline:"):
            raise TBBProtocolError("tbb-pipeline:* is reserved by ap job tbb")
        if value in seen:
            continue
        merged.append(value)
        seen.add(value)
    return merged


def parse_job_request(job: dict[str, Any], expected_command: str) -> dict[str, Any]:
    if job.get("template") != TBB_TEMPLATE:
        raise TBBProtocolError(f"job is not template {TBB_TEMPLATE}")
    try:
        expected_tag = _COMMAND_TAGS[expected_command]
    except KeyError as exc:
        raise TBBProtocolError(f"unsupported TBB command: {expected_command}") from exc
    if expected_tag not in (job.get("tags") or []):
        raise TBBProtocolError(f"job is missing reserved tag {expected_tag}")

    params = job.get("params") or {}
    raw = params.get("request_json") if isinstance(params, dict) else None
    if not isinstance(raw, (str, dict)):
        raise TBBProtocolError("job params do not contain request_json")
    try:
        request = json.loads(raw) if isinstance(raw, str) else dict(raw)
    except json.JSONDecodeError as exc:
        raise TBBProtocolError("job request_json is invalid JSON") from exc
    if not isinstance(request, dict):
        raise TBBProtocolError("job request_json must be a JSON object")

    for field, expected in {
        "apiVersion": TBB_API_VERSION,
        "engine": TBB_ENGINE,
        "command": expected_command,
    }.items():
        if request.get(field) != expected:
            raise TBBProtocolError(f"job request_json has unexpected {field}")
    return request


def _validate_tbb_metrics_identity(metrics: dict[str, Any], expected_command: str) -> None:
    expected_fields = {"engine": TBB_ENGINE, "command": expected_command}
    for field, expected in expected_fields.items():
        if field in metrics and metrics[field] != expected:
            raise TBBProtocolError(f"TBB metrics has unexpected {field}")

    if "result" not in metrics:
        return
    result = metrics["result"]
    if not isinstance(result, dict):
        raise TBBProtocolError("TBB metrics result must be an object")
    for field, expected in expected_fields.items():
        if field in result and result[field] != expected:
            raise TBBProtocolError(f"TBB metrics result has unexpected {field}")


def extract_tbb_metrics(response: dict[str, Any], expected_command: str) -> dict[str, Any] | None:
    metric_items = response.get("metrics")
    if not isinstance(metric_items, list):
        raise TBBProtocolError("job metrics must be a list")
    for metric in metric_items:
        if not isinstance(metric, dict):
            raise TBBProtocolError("job metric must be an object")
        if metric.get("type") != "eval":
            continue
        data = metric.get("data")
        if not isinstance(data, dict):
            raise TBBProtocolError("eval metric data must be an object")
        _validate_tbb_metrics_identity(data, expected_command)
        return data
    return None


def pipeline_result_availability(job_status: str, metrics: dict[str, Any] | None) -> str:
    if metrics is not None:
        return "available"
    if job_status in waiter.TERMINAL_JOB_STATUSES:
        return "unavailable"
    return "pending"


def build_status_payload(job: dict[str, Any], metrics: dict[str, Any] | None) -> dict[str, Any]:
    job_status = job.get("status")
    return {
        "job_id": job.get("job_id"),
        "job_status": job_status,
        "pipeline_result": pipeline_result_availability(job_status, metrics),
        "metrics": metrics,
    }


def tbb_result_succeeded(metrics: dict[str, Any], expected_command: str) -> bool:
    _validate_tbb_metrics_identity(metrics, expected_command)
    result = metrics.get("result")
    if not isinstance(result, dict):
        return False
    native_exit_code = metrics.get("native_exit_code")
    return (
        metrics.get("passed") is True
        and isinstance(native_exit_code, int)
        and not isinstance(native_exit_code, bool)
        and native_exit_code == 0
        and result.get("status") == "completed"
    )


def build_status_row(job: dict[str, Any], metrics: dict[str, Any] | None) -> dict[str, Any]:
    job_status = job.get("status")
    result = metrics.get("result") if metrics is not None else None
    summary = result.get("summary") if isinstance(result, dict) else None
    pipeline_status = (
        result.get("status")
        if isinstance(result, dict) and isinstance(result.get("status"), str)
        else pipeline_result_availability(job_status, metrics)
    )
    return {
        "job_id": job.get("job_id"),
        "job_status": job_status,
        "pipeline_status": pipeline_status,
        "duration_sec": metrics.get("duration_sec") if metrics else None,
        "task_total": summary.get("task_total") if isinstance(summary, dict) else None,
        "failure_count": summary.get("failure_count") if isinstance(summary, dict) else None,
    }
