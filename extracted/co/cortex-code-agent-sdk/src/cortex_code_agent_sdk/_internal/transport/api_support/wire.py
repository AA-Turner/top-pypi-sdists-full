"""Wire response parsing for direct Agent API transport."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

from .types import _PendingToolUse, _StreamResponse, _ToolResultData, _ToolUseData
from .utils import _add_usage, _as_record, _empty_usage, _parse_json_object


def _parse_response_body(
    body: str,
    include_partial_messages: bool,
    on_metadata: Callable[[dict[str, str]], None] | None = None,
) -> _StreamResponse:
    current_event_type = ""
    text = ""
    thinking = ""
    content: list[dict[str, Any]] = []
    tool_uses: list[_ToolUseData] = []
    tool_results: list[_ToolResultData] = []
    tool_input_buffers: dict[str, str] = {}
    pending_tool_uses: dict[str, _PendingToolUse] = {}
    metadata: list[dict[str, str]] = []
    partial_events: list[dict[str, Any]] = []
    usage = _empty_usage()

    for raw_line in body.splitlines():
        parsed = _parse_sse_line(raw_line.strip(), current_event_type)
        if parsed["skip"]:
            continue
        if parsed["is_event_line"]:
            current_event_type = str(parsed.get("event_type") or "")
            continue
        event_type = parsed.get("event_type")
        data_content = parsed.get("data_content")
        if not event_type or event_type == "done" or data_content is None:
            continue

        event = _process_data_event(
            str(event_type),
            str(data_content),
            tool_input_buffers,
            pending_tool_uses,
        )
        if event.get("text"):
            text_delta = str(event["text"])
            text += text_delta
            if include_partial_messages:
                partial_events.append(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "text_delta", "text": text_delta},
                    }
                )
        if event.get("thinking"):
            thinking += str(event["thinking"])
        if isinstance(event.get("tool_use"), _ToolUseData) and not any(
            tool_use.id == event["tool_use"].id for tool_use in tool_uses
        ):
            tool_uses.append(event["tool_use"])
        if isinstance(event.get("tool_result"), _ToolResultData):
            existing = next(
                (
                    index
                    for index, tool_result in enumerate(tool_results)
                    if tool_result.tool_use_id == event["tool_result"].tool_use_id
                ),
                None,
            )
            if existing is None:
                tool_results.append(event["tool_result"])
            else:
                tool_results[existing] = event["tool_result"]
        if isinstance(event.get("usage"), dict):
            _add_usage(usage, event["usage"])
        if isinstance(event.get("metadata"), dict):
            metadata.append(event["metadata"])
            if on_metadata:
                on_metadata(event["metadata"])

    if thinking:
        content.append({"type": "thinking", "thinking": thinking})
    if text:
        content.append({"type": "text", "text": text})
    for tool_use in tool_uses:
        content.append(
            {
                "type": "tool_use",
                "id": tool_use.id,
                "name": tool_use.name,
                "input": tool_use.input,
            }
        )
    return _StreamResponse(
        text=text,
        thinking=thinking,
        content=content,
        tool_uses=tool_uses,
        tool_results=tool_results,
        usage=usage,
        metadata=metadata,
        raw_body=body,
        partial_events=partial_events,
    )


def _process_data_event(
    event_type: str,
    data_content: str,
    tool_input_buffers: dict[str, str],
    pending_tool_uses: dict[str, _PendingToolUse],
) -> dict[str, Any]:
    if event_type == "metadata":
        return _metadata_from_wire(data_content)
    if event_type == "error":
        raise RuntimeError(_format_stream_error(data_content))

    try:
        data = json.loads(data_content)
    except json.JSONDecodeError:
        return {}

    if event_type == "response.text.delta":
        return {"text": data.get("text") or data.get("delta", {}).get("text") or ""}
    if event_type == "response.thinking.delta":
        return {"thinking": data.get("text") or data.get("thinking") or ""}
    if (
        event_type == "response.tool_use"
        and data.get("name")
        and (data.get("tool_use_id") or data.get("id"))
    ):
        return {"tool_use": _tool_use_from_wire(data)}
    if event_type in {"response.tool_result", "tool_result"}:
        tool_result = _tool_result_from_wire(data)
        return {"tool_result": tool_result} if tool_result else {}
    if event_type == "response.done":
        return {"usage": _usage_from_wire(data.get("usage", data))}

    if event_type in {"message.delta", "content_block_delta"}:
        delta = data.get("delta", {})
        if isinstance(delta.get("text"), str):
            return {"text": delta["text"]}
        if delta.get("type") == "text_delta" and isinstance(delta.get("text"), str):
            return {"text": delta["text"]}
        if delta.get("type") == "thinking_delta" and isinstance(
            delta.get("thinking"), str
        ):
            return {"thinking": delta["thinking"]}
        if delta.get("type") == "input_json_delta" and isinstance(
            delta.get("partial_json"), str
        ):
            index = str(data.get("index", "0"))
            tool_input_buffers[index] = (
                tool_input_buffers.get(index, "") + delta["partial_json"]
            )
            return {}
        content = delta.get("content")
        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    return {"text": block["text"]}
                if block.get("type") == "thinking" and isinstance(
                    block.get("thinking"), str
                ):
                    return {"thinking": block["thinking"]}
                if block.get("type") == "input_json_delta" and isinstance(
                    block.get("partial_json"), str
                ):
                    index = str(data.get("index", "0"))
                    tool_input_buffers[index] = (
                        tool_input_buffers.get(index, "") + block["partial_json"]
                    )
                    return {}
                if block.get("type") == "tool_use":
                    return {"tool_use": _tool_use_from_wire(block)}
                if block.get("type") == "tool_result":
                    tool_result = _tool_result_from_wire(block)
                    return {"tool_result": tool_result} if tool_result else {}

    if event_type == "content_block_start":
        block = data.get("content_block")
        if (
            isinstance(block, dict)
            and block.get("type") == "tool_use"
            and block.get("id")
            and block.get("name")
        ):
            index = str(data.get("index", "0"))
            tool_input_buffers[index] = ""
            pending_tool_uses[index] = _PendingToolUse(
                id=str(block["id"]),
                type=block.get("tool_type")
                if isinstance(block.get("tool_type"), str)
                else None,
                name=str(block["name"]),
                input=_as_record(block.get("input")),
                client_side_execute=block.get("client_side_execute"),
                permission=_parse_permission(block.get("permission")),
            )
        return {}

    if event_type == "content_block_stop":
        index = str(data.get("index", "0"))
        pending = pending_tool_uses.pop(index, None)
        if pending is None:
            return {}
        input_json = tool_input_buffers.pop(index, "")
        return {
            "tool_use": _ToolUseData(
                id=pending.id,
                type=pending.type,
                name=pending.name,
                input=pending.input
                if pending.input
                else _parse_json_object(input_json),
                client_side_execute=pending.client_side_execute,
                permission=pending.permission,
            )
        }

    if event_type == "message.stop":
        message = data.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), list):
            for block in message["content"]:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    return {"tool_use": _tool_use_from_wire(block)}
                if block.get("type") == "tool_result":
                    tool_result = _tool_result_from_wire(block)
                    return {"tool_result": tool_result} if tool_result else {}

    if event_type == "response":
        if isinstance(data.get("content"), list):
            for block in data["content"]:
                if not isinstance(block, dict):
                    continue
                if isinstance(block.get("tool_use"), dict) and block["tool_use"].get(
                    "name"
                ):
                    return {"tool_use": _tool_use_from_wire(block["tool_use"])}
                if block.get("type") == "tool_use":
                    return {"tool_use": _tool_use_from_wire(block)}
                if block.get("type") == "tool_result" or block.get("tool_result"):
                    tool_result = _tool_result_from_wire(
                        block.get("tool_result") or block
                    )
                    return {"tool_result": tool_result} if tool_result else {}
        metadata = data.get("metadata")
        if isinstance(metadata, dict) and metadata.get("usage"):
            return {"usage": _usage_from_wire(metadata["usage"])}

    return {}


def _format_stream_error(data_content: str) -> str:
    try:
        data = json.loads(data_content)
    except json.JSONDecodeError:
        return f"Agent run stream error: {data_content}"
    if not isinstance(data, dict):
        return f"Agent run stream error: {data_content}"
    code = data.get("code")
    message = data.get("message", data_content)
    if isinstance(code, str):
        return f"Agent run stream error {code}: {message}"
    return f"Agent run stream error: {message}"


def _parse_sse_line(line: str, current_event_type: str) -> dict[str, Any]:
    if not line:
        return {
            "event_type": None,
            "data_content": None,
            "skip": True,
            "is_event_line": False,
        }
    if line.startswith("{"):
        try:
            ndjson = json.loads(line)
            result = ndjson.get("result", {}) if isinstance(ndjson, dict) else {}
            if isinstance(result.get("sse"), dict):
                return {
                    "event_type": result["sse"].get("event"),
                    "data_content": result["sse"].get("data"),
                    "skip": False,
                    "is_event_line": False,
                }
            if result.get("errorResponse") is not None:
                return {
                    "event_type": "error",
                    "data_content": json.dumps(result["errorResponse"]),
                    "skip": False,
                    "is_event_line": False,
                }
            if (
                result.get("debugResponse") is not None
                or result.get("aggregatedResponse") is not None
                or result.get("aggregatedStreamingResponse") is not None
            ):
                return {
                    "event_type": None,
                    "data_content": None,
                    "skip": True,
                    "is_event_line": False,
                }
        except json.JSONDecodeError:
            pass
    if line.startswith("event:"):
        return {
            "event_type": line[6:].strip(),
            "data_content": None,
            "skip": False,
            "is_event_line": True,
        }
    if line.startswith("data:"):
        data = line[5:].strip()
        if data == "[DONE]":
            return {
                "event_type": "done",
                "data_content": None,
                "skip": False,
                "is_event_line": False,
            }
        return {
            "event_type": current_event_type or None,
            "data_content": data,
            "skip": False,
            "is_event_line": False,
        }
    return {
        "event_type": None,
        "data_content": None,
        "skip": True,
        "is_event_line": False,
    }


def _metadata_from_wire(data_content: str) -> dict[str, Any]:
    metadata: dict[str, Any] | None
    try:
        parsed = json.loads(data_content)
        metadata = parsed.get("metadata") if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        metadata = None
    role = (
        metadata.get("role")
        if isinstance(metadata, dict) and isinstance(metadata.get("role"), str)
        else _extract_json_scalar_string(data_content, "role")
    )
    message_id = _extract_json_scalar_string(data_content, "message_id")
    if (
        not message_id
        and isinstance(metadata, dict)
        and metadata.get("message_id") is not None
    ):
        message_id = str(metadata["message_id"])
    if role in {"user", "assistant", "cortex_control"} and message_id:
        return {"metadata": {"role": role, "message_id": message_id}}
    return {}


def _tool_use_from_wire(data: dict[str, Any]) -> _ToolUseData:
    return _ToolUseData(
        id=str(data.get("tool_use_id") or data.get("id")),
        type=(
            data.get("type")
            if isinstance(data.get("type"), str)
            else data.get("tool_type")
            if isinstance(data.get("tool_type"), str)
            else None
        ),
        name=str(data.get("name")),
        input=_as_record(data.get("input")),
        client_side_execute=data.get("client_side_execute"),
        permission=_parse_permission(data.get("permission")),
    )


def _tool_result_from_wire(data: dict[str, Any]) -> _ToolResultData | None:
    tool_use_id = data.get("tool_use_id") or data.get("id")
    if tool_use_id is None:
        return None
    return _ToolResultData(
        tool_use_id=str(tool_use_id),
        name=str(data.get("name") or "unknown"),
        content=_tool_result_content_to_text(
            data.get("content", data.get("text", data.get("result", "")))
        ),
        is_error=data.get("is_error") is True
        or str(data.get("status", "")).lower() == "error",
    )


def _tool_result_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if isinstance(block.get("text"), str):
                    parts.append(block["text"])
                elif block.get("json") is not None:
                    parts.append(
                        block["json"]
                        if isinstance(block["json"], str)
                        else json.dumps(block["json"])
                    )
                else:
                    parts.append(json.dumps(block))
            else:
                parts.append(block if isinstance(block, str) else json.dumps(block))
        return "\n".join(parts)
    if content is None:
        return ""
    return json.dumps(content)


def _usage_from_wire(raw: Any) -> dict[str, int]:
    if not isinstance(raw, dict):
        return _empty_usage()

    def int_or_zero(value: Any) -> int:
        return int(value) if value is not None else 0

    tokens_consumed = raw.get("tokens_consumed")
    if isinstance(tokens_consumed, list):
        usage = _empty_usage()
        for consumed in tokens_consumed:
            if not isinstance(consumed, dict):
                continue
            input_tokens = consumed.get("input_tokens", {})
            output_tokens = consumed.get("output_tokens", {})
            if isinstance(input_tokens, dict):
                total = int_or_zero(input_tokens.get("total"))
                cache_read = int_or_zero(input_tokens.get("cache_read"))
                cache_write = int_or_zero(input_tokens.get("cache_write"))
                uncached = input_tokens.get("uncached")
                usage["input_tokens"] += (
                    int_or_zero(uncached)
                    if uncached is not None
                    else max(total - cache_read - cache_write, 0)
                )
                usage["cache_read_input_tokens"] += cache_read
                usage["cache_write_input_tokens"] += cache_write
            if isinstance(output_tokens, dict):
                usage["output_tokens"] += int_or_zero(output_tokens.get("total"))
        return usage
    cache_read_val = raw.get("cache_read_input_tokens")
    if cache_read_val is None:
        cache_read_val = raw.get("cache_read_tokens")
    cache_read = int_or_zero(cache_read_val)
    cache_write_val = raw.get("cache_write_input_tokens")
    if cache_write_val is None:
        cache_write_val = raw.get("cache_write_tokens")
    cache_write = int_or_zero(cache_write_val)
    total_or_input = int_or_zero(raw.get("input_tokens"))
    uncached = raw.get("uncached_tokens")
    return {
        "input_tokens": (
            int_or_zero(uncached)
            if uncached is not None
            else max(total_or_input - cache_read - cache_write, 0)
        ),
        "output_tokens": int_or_zero(raw.get("output_tokens")),
        "cache_read_input_tokens": cache_read,
        "cache_write_input_tokens": cache_write,
    }


def _parse_thread_creation_response(body: str) -> tuple[str | None, str | None]:
    thread_id = _extract_json_id(body, "thread_id")
    artifact_message_id = _extract_json_id(body, "artifact_reference_message_id")
    if thread_id or artifact_message_id:
        return thread_id, artifact_message_id
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None, None
    if not isinstance(data, dict):
        return None, None
    return (
        str(data["thread_id"]) if data.get("thread_id") is not None else None,
        str(data["artifact_reference_message_id"])
        if data.get("artifact_reference_message_id") is not None
        else None,
    )


def _parse_latest_thread_message_id(body: str) -> str | None:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    raw_messages = data.get("messages")
    if not isinstance(raw_messages, list):
        thread = data.get("thread")
        raw_messages = thread.get("messages") if isinstance(thread, dict) else []
    if not isinstance(raw_messages, list):
        return None
    for raw_message in raw_messages:
        if not isinstance(raw_message, dict):
            continue
        if raw_message.get("role") != "assistant":
            continue
        message_id = _parse_message_id(raw_message)
        if message_id is None or _parse_created_on(raw_message) is None:
            return None
        return message_id
    return None


def _parse_message_id(message: dict[str, Any]) -> str | None:
    raw_id = message.get("message_id") or message.get("messageId") or message.get("id")
    if isinstance(raw_id, str) and raw_id:
        return raw_id
    if isinstance(raw_id, int | float):
        return str(int(raw_id))
    return None


def _parse_created_on(message: dict[str, Any]) -> float | None:
    raw_created_on = message.get("created_on") or message.get("createdOn")
    if isinstance(raw_created_on, int | float):
        return float(raw_created_on)
    if isinstance(raw_created_on, str) and raw_created_on:
        try:
            return float(raw_created_on)
        except ValueError:
            return None
    return None


def _parse_artifact_creation_response(body: str) -> str | None:
    artifact_id = _extract_json_scalar_string(body, "id")
    if artifact_id:
        return artifact_id
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    artifact = data.get("artifact")
    if isinstance(artifact, dict) and artifact.get("id") is not None:
        return str(artifact["id"])
    return str(data["id"]) if data.get("id") is not None else None


def _parse_agent_run_start_response(body: str) -> tuple[str | None, str | None]:
    run_id = _extract_json_scalar_string(body, "run_id")
    user_message_id = _extract_json_scalar_string(body, "user_message_id")
    if run_id or user_message_id:
        return run_id, user_message_id
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None, None
    if not isinstance(data, dict):
        return None, None
    metadata_raw = data.get("metadata")
    metadata = metadata_raw if isinstance(metadata_raw, dict) else data
    return (
        str(metadata["run_id"]) if metadata.get("run_id") is not None else None,
        str(metadata["user_message_id"])
        if metadata.get("user_message_id") is not None
        else None,
    )


def _parse_agent_run_cancel_response(body: str) -> str | None:
    assistant_message_id = _extract_json_scalar_string(body, "assistant_message_id")
    if assistant_message_id:
        return assistant_message_id
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    metadata_raw = data.get("metadata")
    metadata = metadata_raw if isinstance(metadata_raw, dict) else data
    return (
        str(metadata["assistant_message_id"])
        if metadata.get("assistant_message_id") is not None
        else None
    )


def _extract_json_id(body: str, key: str) -> str | None:
    value = _extract_json_scalar_string(body, key)
    return value if value and re.match(r"^[0-9]+$", value) else None


def _extract_json_scalar_string(body: str, key: str) -> str | None:
    escaped_key = re.escape(key)
    match = re.search(rf'"{escaped_key}"\s*:\s*(?:"([^"]+)"|([0-9]+))', body)
    if not match:
        return None
    return match.group(1) or match.group(2)


def _parse_permission(raw: Any) -> dict[str, list[str]] | None:
    if not isinstance(raw, dict):
        return None
    options = raw.get("options")
    if not isinstance(options, list):
        return None
    values = [option for option in options if isinstance(option, str) and option]
    return {"options": values} if values else None
