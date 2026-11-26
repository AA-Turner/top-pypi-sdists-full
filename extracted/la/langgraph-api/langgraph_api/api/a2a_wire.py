from datetime import UTC, datetime
from typing import Any


def normalize_parts(parts: Any, *, v1: bool = False) -> list[Any]:
    """Adapt v1 content members to the existing internal Part representation."""
    if not isinstance(parts, list):
        raise ValueError("Message parts must be an array")
    normalized = []
    for part in parts:
        if not isinstance(part, dict):
            if v1:
                raise ValueError("Each message part must be an object")
            normalized.append(part)
            continue
        if not v1 and "url" not in part and "raw" not in part:
            normalized.append(part)
            continue
        members = [key for key in ("text", "data", "url", "raw", "file") if key in part]
        if len(members) != 1:
            raise ValueError(
                "Each message part must contain exactly one content member"
            )
        member = members[0]
        if member in ("url", "raw"):
            if not isinstance(part[member], str):
                raise ValueError(f"Part '{member}' must be a string")
            part = {
                **{
                    key: value
                    for key, value in part.items()
                    if key not in ("url", "raw", "mediaType", "filename")
                },
                "file": {
                    "uri" if member == "url" else "bytes": part[member],
                    **({"mimeType": part["mediaType"]} if "mediaType" in part else {}),
                    **({"name": part["filename"]} if "filename" in part else {}),
                },
            }
        normalized.append(part)
    return normalized


def to_v1_response(body: Any) -> Any:
    """Serialize typed A2A JSON-RPC results without rewriting opaque payloads."""
    if not isinstance(body, dict) or not isinstance(body.get("result"), dict):
        return body
    return {**body, "result": _result(body["result"])}


def _result(result: dict[str, Any]) -> dict[str, Any]:
    kind = result.get("kind")
    if kind == "task":
        return _task(result)
    if kind == "message":
        return {"message": _message(result)}
    if kind == "status-update":
        return {"statusUpdate": _status_update(result)}
    if kind == "artifact-update":
        return {"artifactUpdate": _artifact_update(result)}
    out = dict(result)
    for key, serializer in (
        ("task", _task),
        ("message", _message),
        ("statusUpdate", _status_update),
        ("artifactUpdate", _artifact_update),
    ):
        if isinstance(result.get(key), dict):
            out[key] = serializer(result[key])
    if isinstance(result.get("tasks"), list):
        out["tasks"] = [_task(task) for task in result["tasks"]]
    return out


def _without_kind(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != "kind"}


def _task(task: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(task)
    if isinstance(task.get("status"), dict):
        out["status"] = _status(task["status"])
    if isinstance(task.get("history"), list):
        out["history"] = [_message(message) for message in task["history"]]
    if isinstance(task.get("artifacts"), list):
        out["artifacts"] = [_artifact(artifact) for artifact in task["artifacts"]]
    return out


def _status(status: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(status)
    if isinstance(status.get("message"), dict):
        out["message"] = _message(status["message"])
    timestamp = status.get("timestamp")
    if isinstance(timestamp, str | datetime):
        parsed = (
            datetime.fromisoformat(timestamp)
            if isinstance(timestamp, str)
            else timestamp
        )
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        out["timestamp"] = (
            parsed.astimezone(UTC)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )
    return out


def _message(message: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(message)
    if isinstance(message.get("parts"), list):
        out["parts"] = [_part(part) for part in message["parts"]]
    return out


def _artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(artifact)
    if isinstance(artifact.get("parts"), list):
        out["parts"] = [_part(part) for part in artifact["parts"]]
    return out


def _part(part: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(part)
    file = part.get("file")
    if isinstance(file, dict):
        out.pop("file")
        names = {
            "uri": "url",
            "bytes": "raw",
            "name": "filename",
            "mimeType": "mediaType",
        }
        out.update((names.get(key, key), value) for key, value in file.items())
    return out


def _status_update(event: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(event)
    out.pop("final", None)
    if isinstance(event.get("status"), dict):
        out["status"] = _status(event["status"])
    return out


def _artifact_update(event: dict[str, Any]) -> dict[str, Any]:
    out = _without_kind(event)
    if isinstance(event.get("artifact"), dict):
        out["artifact"] = _artifact(event["artifact"])
    return out
