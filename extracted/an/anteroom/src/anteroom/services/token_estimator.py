"""Provider-shaped token estimation for usage fallback.

When a provider does not return streaming usage data, this module estimates
the major request components Anteroom sent: messages, system prompts, tool
schemas, tool calls/results, structured content, and response text. Native
provider usage remains authoritative whenever it is present.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestTokenBreakdown:
    """Per-component token breakdown for a full LLM request."""

    message_tokens: int
    system_prompt_tokens: int
    tool_schema_tokens: int
    total: int


@dataclass(frozen=True)
class RequestFixedOverhead:
    """Cached fixed request overhead for repeated full-request estimates."""

    system_prompt_tokens: int
    tool_schema_tokens: int
    has_system_prompt: bool | None = None


_encoding: Any = None

_MESSAGE_OVERHEAD = 4
_SYSTEM_PROMPT_OVERHEAD = 4
_TOOL_SCHEMA_OVERHEAD = 8
_TOOL_CALL_OVERHEAD = 8
_TOOL_RESULT_OVERHEAD = 6
_STRUCTURED_PART_OVERHEAD = 2

_IMAGE_BASE_TOKENS = 85
_IMAGE_PAYLOAD_TOKEN_CAP = 1024
_DOCUMENT_BASE_TOKENS = 300
_DOCUMENT_PAYLOAD_TOKEN_CAP = 4096

_LOCAL_METADATA_KEYS = {
    "metadata",
    "annotations",
    "usage",
    "usage_estimated",
    "position",
    "created_at",
    "updated_at",
}

_TEXT_LIKE_KEYS = {
    "text",
    "content",
    "title",
    "name",
    "filename",
    "file_name",
    "tool_use_id",
    "tool_call_id",
    "id",
}

_JSON_LIKE_KEYS = {
    "input",
    "arguments",
    "parameters",
    "schema",
    "input_schema",
}

_MEDIA_LIKE_KEYS = {
    "image_url",
    "url",
    "source",
    "data",
    "base64",
    "file_data",
}


def _get_encoding() -> Any:
    """Get the cl100k_base encoding, cached after first call."""
    global _encoding
    if _encoding is None:
        try:
            import tiktoken

            _encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            _encoding = False
    return _encoding


def _count_encoded_text(text: str) -> int:
    """Count text tokens with tiktoken, falling back to a char estimate."""
    if not text:
        return 0
    enc = _get_encoding()
    if enc:
        return len(enc.encode(text, allowed_special="all"))
    return max(1, (len(text) + 3) // 4)


def _stable_json(value: Any) -> str:
    """Serialize request-shaped data deterministically and compactly."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _count_dense_json_tokens(value: Any) -> int:
    """Count JSON with a guard against undercounting punctuation-heavy payloads."""
    serialized = value if isinstance(value, str) else _stable_json(value)
    if not serialized:
        return 0
    return max(_count_encoded_text(serialized), max(1, (len(serialized) + 2) // 3))


def _largest_string_size(value: Any) -> int:
    """Return the length of the largest string embedded in a media-like payload."""
    if isinstance(value, str):
        return len(value)
    if isinstance(value, dict):
        return max((_largest_string_size(v) for v in value.values()), default=0)
    if isinstance(value, list):
        return max((_largest_string_size(v) for v in value), default=0)
    return 0


def _bounded_payload_tokens(size: int, *, base: int, cap: int, chars_per_token: int) -> int:
    """Estimate opaque binary/base64 payloads without counting every byte."""
    if size <= 0:
        return base
    return base + min(cap, max(1, (size + chars_per_token - 1) // chars_per_token))


def _count_media_part_tokens(part: dict[str, Any], *, document: bool = False) -> int:
    """Conservatively estimate image/document parts without serializing payloads."""
    size = 0
    label_tokens = 0
    for key, value in part.items():
        if key in _LOCAL_METADATA_KEYS or key == "type":
            continue
        if key in {"text", "content"} and isinstance(value, str) and not _looks_like_data_payload(value):
            label_tokens += _count_encoded_text(value)
            continue
        if key in {"title", "name", "filename", "file_name", "mime_type", "media_type"} and isinstance(value, str):
            label_tokens += _count_encoded_text(value)
            continue
        if key in _MEDIA_LIKE_KEYS or _looks_like_media_key(key):
            size = max(size, _largest_string_size(value))

    if document:
        opaque_tokens = _bounded_payload_tokens(
            size,
            base=_DOCUMENT_BASE_TOKENS,
            cap=_DOCUMENT_PAYLOAD_TOKEN_CAP,
            chars_per_token=1000,
        )
    else:
        opaque_tokens = _bounded_payload_tokens(
            size,
            base=_IMAGE_BASE_TOKENS,
            cap=_IMAGE_PAYLOAD_TOKEN_CAP,
            chars_per_token=1500,
        )
    return opaque_tokens + label_tokens


def _looks_like_data_payload(value: str) -> bool:
    """Detect data URLs or very large base64-ish strings."""
    if value.startswith("data:"):
        return True
    if len(value) < 512:
        return False
    alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r")
    sample = value[:1024]
    return all(ch in alphabet for ch in sample)


def _looks_like_media_key(key: str) -> bool:
    lowered = key.lower()
    return any(marker in lowered for marker in ("image", "document", "pdf", "base64", "bytes", "blob"))


def _scrub_large_payloads(value: Any) -> Any:
    """Replace large opaque strings before JSON fallback counting."""
    if isinstance(value, str):
        if _looks_like_data_payload(value):
            return f"<opaque payload chars={len(value)}>"
        return value
    if isinstance(value, dict):
        scrubbed: dict[str, Any] = {}
        for key, item in value.items():
            if key in _LOCAL_METADATA_KEYS:
                continue
            if key in _MEDIA_LIKE_KEYS or _looks_like_media_key(key):
                scrubbed[key] = f"<opaque payload chars={_largest_string_size(item)}>"
            else:
                scrubbed[key] = _scrub_large_payloads(item)
        return scrubbed
    if isinstance(value, list):
        return [_scrub_large_payloads(item) for item in value]
    return value


def _count_tool_use_block(part: dict[str, Any]) -> int:
    total = _TOOL_CALL_OVERHEAD
    for key in ("id", "name"):
        value = part.get(key)
        if isinstance(value, str):
            total += _count_encoded_text(value)
    if "input" in part:
        total += _count_dense_json_tokens(part["input"])
    return total


def _count_tool_result_block(part: dict[str, Any]) -> int:
    total = _TOOL_RESULT_OVERHEAD
    tool_id = part.get("tool_use_id") or part.get("tool_call_id")
    if isinstance(tool_id, str):
        total += _count_encoded_text(tool_id)
    return total + _count_content_tokens(part.get("content", ""))


def _count_structured_part_tokens(part: Any) -> int:
    if isinstance(part, str):
        return _count_encoded_text(part)
    if not isinstance(part, dict):
        return _count_encoded_text(str(part)) if part is not None else 0

    part_type = str(part.get("type", "")).lower()
    if part_type in {"text", "input_text", "output_text"}:
        text = part.get("text", part.get("content", ""))
        return _count_encoded_text(text) if isinstance(text, str) else _count_content_tokens(text)
    if part_type in {"tool_use", "server_tool_use"}:
        return _count_tool_use_block(part)
    if part_type in {"tool_result", "function_result"}:
        return _count_tool_result_block(part)
    if part_type in {"image", "image_url", "input_image"}:
        return _count_media_part_tokens(part)
    if part_type in {"document", "file", "input_file"}:
        return _count_media_part_tokens(part, document=True)

    total = 0
    saw_known_field = False
    for key, value in part.items():
        if key in _LOCAL_METADATA_KEYS or key == "type":
            continue
        if key in _TEXT_LIKE_KEYS:
            saw_known_field = True
            total += _count_content_tokens(value)
        elif key in _JSON_LIKE_KEYS:
            saw_known_field = True
            total += _count_dense_json_tokens(value)
        elif key in _MEDIA_LIKE_KEYS or _looks_like_media_key(key):
            saw_known_field = True
            total += _count_media_part_tokens({key: value})

    if saw_known_field:
        return total + _STRUCTURED_PART_OVERHEAD
    return _count_dense_json_tokens(_scrub_large_payloads(part))


def _count_content_tokens(content: Any) -> int:
    if content is None:
        return 0
    if isinstance(content, str):
        if _looks_like_data_payload(content):
            return _bounded_payload_tokens(
                len(content),
                base=_DOCUMENT_BASE_TOKENS,
                cap=_DOCUMENT_PAYLOAD_TOKEN_CAP,
                chars_per_token=1000,
            )
        return _count_encoded_text(content)
    if isinstance(content, list):
        return sum(_count_structured_part_tokens(part) for part in content)
    if isinstance(content, dict):
        return _count_structured_part_tokens(content)
    return _count_encoded_text(str(content))


def _count_tool_call_tokens(tool_call: dict[str, Any]) -> int:
    total = _TOOL_CALL_OVERHEAD
    if isinstance(tool_call.get("id"), str):
        total += _count_encoded_text(tool_call["id"])
    if isinstance(tool_call.get("type"), str):
        total += _count_encoded_text(tool_call["type"])
    func = tool_call.get("function", {})
    if isinstance(func, dict):
        name = func.get("name", "")
        args = func.get("arguments", "")
        if isinstance(name, str):
            total += _count_encoded_text(name)
        total += _count_dense_json_tokens(args)
    else:
        total += _count_dense_json_tokens(func)
    return total


def _combined_system_prompt(system_prompt: str, extra_system_prompt: str) -> str:
    if extra_system_prompt and system_prompt:
        return extra_system_prompt + "\n\n" + system_prompt
    return extra_system_prompt or system_prompt


def count_tool_schema_tokens(tool_schemas: list[dict[str, Any]] | None) -> int:
    """Estimate provider tool/function schema overhead."""
    if not tool_schemas:
        return 0
    total = 0
    for tool in tool_schemas:
        total += _TOOL_SCHEMA_OVERHEAD + _count_dense_json_tokens(_scrub_large_payloads(tool))
    return total


def count_message_tokens(messages: list[dict[str, Any]]) -> int:
    """Count tokens in a list of provider-shaped chat messages.

    Includes ~4 tokens per-message overhead for role/separators (OpenAI chat format).
    Falls back to len(text)//4 if tiktoken is unavailable.
    """
    total = 0
    for msg in messages:
        total += _MESSAGE_OVERHEAD
        if isinstance(msg.get("name"), str):
            total += _count_encoded_text(msg["name"])
        total += _count_content_tokens(msg.get("content", ""))
        if msg.get("role") == "tool" and isinstance(msg.get("tool_call_id"), str):
            total += _TOOL_RESULT_OVERHEAD + _count_encoded_text(msg["tool_call_id"])
        for tc in msg.get("tool_calls", []):
            if isinstance(tc, dict):
                total += _count_tool_call_tokens(tc)
    return total


def count_text_tokens(text: str) -> int:
    """Count tokens in a plain text string."""
    return _count_encoded_text(text)


def estimate_usage(
    messages: list[dict[str, Any]],
    response_content: str,
    model: str,
    *,
    system_prompt: str = "",
    extra_system_prompt: str = "",
    tool_schemas: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Estimate token usage from request components and response content.

    Returns a usage dict compatible with the ``usage`` event protocol,
    with ``estimated: True`` so handlers can flag it in metadata.
    The ``model`` field is the real model name (not prefixed) so cost
    reporting works unchanged.
    """
    prompt_tokens = estimate_request_tokens(
        messages=messages,
        system_prompt=system_prompt,
        extra_system_prompt=extra_system_prompt,
        tool_schemas=tool_schemas,
    ).total
    completion_tokens = count_text_tokens(response_content)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "model": model,
        "estimated": True,
    }


def estimate_request_tokens(
    messages: list[dict[str, Any]],
    system_prompt: str = "",
    extra_system_prompt: str = "",
    tool_schemas: list[dict[str, Any]] | None = None,
) -> RequestTokenBreakdown:
    """Estimate the total token cost of a full LLM request.

    Accounts for message history, system prompt (default + extra),
    and tool schemas using the same primitives as fallback usage.
    """
    message_tokens = count_message_tokens(messages)

    system_prompt_tokens = _estimate_system_prompt_tokens(
        system_prompt=system_prompt,
        extra_system_prompt=extra_system_prompt,
    )

    tool_schema_tokens = count_tool_schema_tokens(tool_schemas)

    total = message_tokens + system_prompt_tokens + tool_schema_tokens
    return RequestTokenBreakdown(
        message_tokens=message_tokens,
        system_prompt_tokens=system_prompt_tokens,
        tool_schema_tokens=tool_schema_tokens,
        total=total,
    )


def _estimate_system_prompt_tokens(system_prompt: str = "", extra_system_prompt: str = "") -> int:
    """Estimate the system-message component of an active request.

    Providers receive one system message whose content is the dynamic extra
    prompt followed by the base system prompt. This additive form keeps direct
    and cached-overhead estimates on one deterministic accounting basis.
    """
    if not system_prompt and not extra_system_prompt:
        return 0

    total = _SYSTEM_PROMPT_OVERHEAD
    if extra_system_prompt:
        total += count_text_tokens(extra_system_prompt)
    if extra_system_prompt and system_prompt:
        total += count_text_tokens("\n\n")
    if system_prompt:
        total += count_text_tokens(system_prompt)
    return total


def estimate_fixed_request_overhead(
    system_prompt: str,
    tool_schemas: list[dict[str, Any]] | None = None,
) -> RequestFixedOverhead:
    """Estimate the fixed part of an active request once for cheap reuse."""
    breakdown = estimate_request_tokens(
        messages=[],
        system_prompt=system_prompt,
        extra_system_prompt="",
        tool_schemas=tool_schemas,
    )
    return RequestFixedOverhead(
        system_prompt_tokens=breakdown.system_prompt_tokens,
        tool_schema_tokens=breakdown.tool_schema_tokens,
        has_system_prompt=bool(system_prompt),
    )


def estimate_request_tokens_with_overhead(
    messages: list[dict[str, Any]],
    extra_system_prompt: str,
    fixed_overhead: RequestFixedOverhead,
) -> RequestTokenBreakdown:
    """Estimate an active request using cached system/tool overhead."""
    message_tokens = count_message_tokens(messages)
    has_base_system = (
        fixed_overhead.has_system_prompt
        if fixed_overhead.has_system_prompt is not None
        else fixed_overhead.system_prompt_tokens > 0
    )

    system_prompt_tokens = fixed_overhead.system_prompt_tokens
    if extra_system_prompt:
        system_prompt_tokens += count_text_tokens(extra_system_prompt)
        system_prompt_tokens += count_text_tokens("\n\n") if has_base_system else _SYSTEM_PROMPT_OVERHEAD

    total = message_tokens + system_prompt_tokens + fixed_overhead.tool_schema_tokens
    return RequestTokenBreakdown(
        message_tokens=message_tokens,
        system_prompt_tokens=system_prompt_tokens,
        tool_schema_tokens=fixed_overhead.tool_schema_tokens,
        total=total,
    )


def request_breakdown_to_metadata(
    breakdown: RequestTokenBreakdown,
    *,
    token_threshold: int | None = None,
    threshold_field: str = "token_threshold",
) -> dict[str, int]:
    """Convert a request breakdown to stable UI/API metadata fields."""
    metadata = {
        "estimated_tokens": breakdown.total,
        "message_tokens": breakdown.message_tokens,
        "system_prompt_tokens": breakdown.system_prompt_tokens,
        "tool_schema_tokens": breakdown.tool_schema_tokens,
    }
    if token_threshold is not None:
        metadata[threshold_field] = token_threshold
    return metadata
