"""
Utility functions for Claude Agent SDK integration.
"""

import re
from typing import Any

# Default patterns for sensitive data masking
# Format: (pattern, replacement, description)
SENSITIVE_PATTERNS: list[tuple[str, str, str]] = [
    # Email addresses
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", "Email addresses"),
    # Phone numbers (various formats)
    (r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]", "Phone numbers"),
    (r"\b\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]", "International phone"),
    # Credit card numbers
    (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CREDIT_CARD]", "Credit card numbers"),
    (
        r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b",
        "[CREDIT_CARD]",
        "Credit card patterns",
    ),
    # Social Security Numbers
    (r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b", "[SSN]", "Social Security Numbers"),
    # API Keys and tokens (generic patterns)
    (
        r'(?i)(api[_-]?key|apikey|api_token)["\']?\s*[=:]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?',
        r"\1=[REDACTED]",
        "API keys",
    ),
    (
        r'(?i)(secret|password|token|auth)["\']?\s*[=:]\s*["\']?([^\s,\'"]{8,})["\']?',
        r"\1=[REDACTED]",
        "Secrets and passwords",
    ),
    (r"(?i)bearer\s+[A-Za-z0-9_\-\.]+", "Bearer [REDACTED]", "Bearer tokens"),
    # AWS Keys
    (
        r'(?i)(aws[_-]?access[_-]?key[_-]?id)["\']?\s*[=:]\s*["\']?([A-Z0-9]{20})["\']?',
        r"\1=[REDACTED]",
        "AWS access keys",
    ),
    (
        r'(?i)(aws[_-]?secret[_-]?access[_-]?key)["\']?\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})["\']?',
        r"\1=[REDACTED]",
        "AWS secret keys",
    ),
    # IP addresses (optional - might be too aggressive)
    # (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP_ADDRESS]', "IP addresses"),
    # Private keys
    (
        r"-----BEGIN (?:RSA )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA )?PRIVATE KEY-----",
        "[PRIVATE_KEY]",
        "Private keys",
    ),
    # Anthropic API keys
    (r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b", "[ANTHROPIC_KEY]", "Anthropic API keys"),
    # OpenAI API keys
    (r"\bsk-[A-Za-z0-9]{48,}\b", "[OPENAI_KEY]", "OpenAI API keys"),
    # Generic long hex strings (potential secrets)
    (r"\b[0-9a-fA-F]{32,}\b", "[HEX_SECRET]", "Hex secrets"),
]


def mask_sensitive_data(
    data: Any,
    patterns: list[tuple[str, str, str]] | None = None,
    max_depth: int = 10,
) -> Any:
    """
    Recursively mask sensitive data in various data structures.

    Args:
        data: Data to mask (string, dict, list, or nested combination)
        patterns: Optional custom patterns (regex, replacement, description)
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Data with sensitive information masked
    """
    if max_depth <= 0:
        return data

    patterns_to_use = patterns if patterns is not None else SENSITIVE_PATTERNS

    if isinstance(data, str):
        return _mask_string(data, patterns_to_use)
    if isinstance(data, dict):
        return {k: mask_sensitive_data(v, patterns_to_use, max_depth - 1) for k, v in data.items()}
    if isinstance(data, list):
        return [mask_sensitive_data(item, patterns_to_use, max_depth - 1) for item in data]
    if isinstance(data, tuple):
        return tuple(mask_sensitive_data(item, patterns_to_use, max_depth - 1) for item in data)
    return data


def _mask_string(text: str, patterns: list[tuple[str, str, str]]) -> str:
    """Apply masking patterns to a string."""
    if not text:
        return text

    result = text
    for pattern, replacement, _ in patterns:
        try:
            result = re.sub(pattern, replacement, result)
        except re.error:
            # Skip invalid patterns
            continue

    return result


def safe_str(value: Any, max_length: int = 1000) -> str:
    """Safely convert a value to string with length limit.

    Args:
        value: Value to convert
        max_length: Maximum length of output string

    Returns:
        String representation, truncated if necessary
    """
    try:
        if value is None:
            return ""
        s = str(value)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception as e:
        return f"<error: {e}>"


def mask_dict_keys(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    mask_value: str = "[REDACTED]",
) -> dict[str, Any]:
    """
    Mask values for keys that might contain sensitive data.

    Args:
        data: Dictionary to mask
        sensitive_keys: List of key names to mask (case-insensitive partial match)
        mask_value: Value to use as replacement

    Returns:
        Dictionary with sensitive keys masked
    """
    default_sensitive_keys = [
        "password",
        "secret",
        "token",
        "api_key",
        "apikey",
        "auth",
        "credential",
        "private",
        "access_key",
        "secret_key",
        "bearer",
    ]
    keys_to_check = sensitive_keys if sensitive_keys is not None else default_sensitive_keys

    result = {}
    for key, value in data.items():
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in keys_to_check):
            result[key] = mask_value
        elif isinstance(value, dict):
            result[key] = mask_dict_keys(value, keys_to_check, mask_value)
        elif isinstance(value, list):
            result[key] = [
                mask_dict_keys(item, keys_to_check, mask_value) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def extract_text_from_content(content: Any) -> str:
    """
    Extract text content from various Claude message content formats.

    Args:
        content: Message content (str, list of blocks, or other)

    Returns:
        Extracted text as string
    """
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
            elif hasattr(block, "text"):
                text_parts.append(block.text)
            elif isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])
            elif hasattr(block, "type") and block.type == "text":
                text_parts.append(getattr(block, "text", ""))
        return "\n".join(text_parts)

    if hasattr(content, "text"):
        return content.text

    return str(content)


def extract_tool_uses(content: Any) -> list[dict[str, Any]]:
    """
    Extract tool use blocks from message content.

    Args:
        content: Message content

    Returns:
        List of tool use dicts with id, name, input
    """
    tool_uses = []

    if not isinstance(content, list):
        return tool_uses

    for block in content:
        if hasattr(block, "type") and block.type == "tool_use":
            tool_uses.append(
                {
                    "id": getattr(block, "id", ""),
                    "name": getattr(block, "name", ""),
                    "input": getattr(block, "input", {}),
                }
            )
        elif isinstance(block, dict) and block.get("type") == "tool_use":
            tool_uses.append(
                {
                    "id": block.get("id", ""),
                    "name": block.get("name", ""),
                    "input": block.get("input", {}),
                }
            )

    return tool_uses


def extract_tool_results(content: Any) -> list[dict[str, Any]]:
    """
    Extract tool result blocks from message content.

    Args:
        content: Message content

    Returns:
        List of tool result dicts with tool_use_id, content, is_error
    """
    tool_results = []

    if not isinstance(content, list):
        return tool_results

    for block in content:
        if hasattr(block, "type") and block.type == "tool_result":
            tool_results.append(
                {
                    "tool_use_id": getattr(block, "tool_use_id", ""),
                    "content": getattr(block, "content", ""),
                    "is_error": getattr(block, "is_error", False),
                }
            )
        elif isinstance(block, dict) and block.get("type") == "tool_result":
            tool_results.append(
                {
                    "tool_use_id": block.get("tool_use_id", ""),
                    "content": block.get("content", ""),
                    "is_error": block.get("is_error", False),
                }
            )

    return tool_results


def serialize_message(message: Any, max_length: int = 2000) -> dict[str, Any]:
    """
    Serialize a Claude message for tracing.

    Args:
        message: Claude message object
        max_length: Maximum length for content fields

    Returns:
        Serialized message dict
    """
    result = {
        "role": getattr(message, "role", "unknown"),
    }

    if hasattr(message, "content"):
        content = message.content
        if isinstance(content, str):
            result["content"] = content[:max_length]
        elif isinstance(content, list):
            serialized_blocks = []
            for block in content[:10]:  # Limit blocks
                if hasattr(block, "type"):
                    block_dict = {"type": block.type}
                    if block.type == "text":
                        block_dict["text"] = getattr(block, "text", "")[:max_length]
                    elif block.type == "tool_use":
                        block_dict["id"] = getattr(block, "id", "")
                        block_dict["name"] = getattr(block, "name", "")
                        block_dict["input"] = str(getattr(block, "input", {}))[:500]
                    elif block.type == "tool_result":
                        block_dict["tool_use_id"] = getattr(block, "tool_use_id", "")
                        block_dict["is_error"] = getattr(block, "is_error", False)
                        content_str = str(getattr(block, "content", ""))
                        block_dict["content"] = content_str[:500]
                    serialized_blocks.append(block_dict)
                elif isinstance(block, dict):
                    serialized_blocks.append({k: str(v)[:500] for k, v in block.items()})
            result["content"] = serialized_blocks
        else:
            result["content"] = str(content)[:max_length]

    # Add usage if present (for ResultMessage)
    if hasattr(message, "usage"):
        usage = message.usage
        result["usage"] = {
            "input_tokens": getattr(usage, "input_tokens", 0),
            "output_tokens": getattr(usage, "output_tokens", 0),
            "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0),
            "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0),
        }

    if hasattr(message, "total_cost_usd"):
        result["total_cost_usd"] = message.total_cost_usd

    if hasattr(message, "model"):
        result["model"] = message.model

    return result


def serialize_messages(messages: list[Any], max_length: int = 2000) -> list[dict[str, Any]]:
    """
    Serialize a list of Claude messages for tracing.

    Args:
        messages: List of Claude message objects
        max_length: Maximum length for content fields

    Returns:
        List of serialized message dicts
    """
    return [serialize_message(m, max_length) for m in messages]


def extract_usage(result_message: Any) -> dict[str, int]:
    """
    Extract usage information from a ResultMessage.

    Args:
        result_message: Claude ResultMessage object

    Returns:
        Usage dict with token counts
    """
    usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
    }

    if not result_message:
        return usage

    if hasattr(result_message, "usage"):
        usage_obj = result_message.usage
        usage["input_tokens"] = getattr(usage_obj, "input_tokens", 0)
        usage["output_tokens"] = getattr(usage_obj, "output_tokens", 0)
        usage["cache_read_input_tokens"] = getattr(usage_obj, "cache_read_input_tokens", 0)
        usage["cache_creation_input_tokens"] = getattr(usage_obj, "cache_creation_input_tokens", 0)

    return usage


def is_result_message(message: Any) -> bool:
    """
    Check if a message is a ResultMessage (final message with usage/cost).

    Args:
        message: Message to check

    Returns:
        True if message is a ResultMessage
    """
    return hasattr(message, "usage") or hasattr(message, "total_cost_usd")


def get_message_type(message: Any) -> str:
    """
    Get the type of a Claude message.

    Args:
        message: Claude message object

    Returns:
        Message type string
    """
    if hasattr(message, "__class__"):
        return message.__class__.__name__

    if isinstance(message, dict):
        return message.get("type", "unknown")

    return "unknown"


def truncate_text(text: str, max_length: int = 2000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
