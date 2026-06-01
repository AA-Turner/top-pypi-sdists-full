"""
Utility functions for Agno integration.

Provides agent-specific utilities for:
- Agno availability and version checking
- Sensitive data masking for agent inputs/outputs
- Tool and agent metadata extraction
- Response parsing and formatting
"""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


# Sensitive patterns for agent input/output masking
SENSITIVE_PATTERNS: list[tuple[str, str, str]] = [
    # API keys and tokens
    (
        r'\b(?:api[_-]?key|apikey)\s*[=:]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?',
        "[API_KEY]",
        "API keys",
    ),
    (r'\b(?:token|bearer)\s*[=:]\s*["\']?([A-Za-z0-9_\-\.]{20,})["\']?', "[TOKEN]", "Auth tokens"),
    (
        r'\b(?:secret|password|passwd|pwd)\s*[=:]\s*["\']?([^\s"\']{8,})["\']?',
        "[SECRET]",
        "Secrets/passwords",
    ),
    # AWS credentials
    (r"\bAKIA[0-9A-Z]{16}\b", "[AWS_ACCESS_KEY]", "AWS access keys"),
    (r"\b[A-Za-z0-9/+=]{40}\b(?=.*aws)", "[AWS_SECRET_KEY]", "AWS secret keys"),
    # Email addresses
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", "Email addresses"),
    # Phone numbers
    (r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]", "Phone numbers"),
    # Credit card numbers
    (r"\b(?:\d{4}[-\s]?){3}\d{4}\b", "[CREDIT_CARD]", "Credit card numbers"),
    # SSN
    (r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b", "[SSN]", "Social Security Numbers"),
    # Private keys
    (
        r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----[\s\S]*?-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----",
        "[PRIVATE_KEY]",
        "Private keys",
    ),
]


def is_agno_available() -> bool:
    """
    Check if Agno is installed and available.

    Returns:
        True if agno is available, False otherwise.
    """
    try:
        import agno

        return True
    except ImportError:
        return False


def get_agno_version() -> str | None:
    """
    Get the installed Agno version.

    Returns:
        Version string if installed, None otherwise.
    """
    try:
        import agno

        return getattr(agno, "__version__", "unknown")
    except ImportError:
        return None


def mask_sensitive_content(
    text: str,
    patterns: list[tuple[str, str, str]] | None = None,
) -> str:
    """
    Mask sensitive information in text content.

    Args:
        text: Text to mask
        patterns: Optional custom patterns (regex, replacement, description)

    Returns:
        Text with sensitive information masked
    """
    if not text:
        return text

    patterns_to_use = patterns if patterns is not None else SENSITIVE_PATTERNS
    result = text

    for pattern, replacement, _ in patterns_to_use:
        try:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        except re.error:
            continue

    return result


def mask_sensitive_data(
    data: Any,
    patterns: list[tuple[str, str, str]] | None = None,
    max_depth: int = 10,
) -> Any:
    """
    Recursively mask sensitive data in various data structures.

    Args:
        data: Data to mask (string, dict, list, or nested)
        patterns: Optional custom patterns
        max_depth: Maximum recursion depth

    Returns:
        Data with sensitive information masked
    """
    if max_depth <= 0:
        return data

    patterns_to_use = patterns if patterns is not None else SENSITIVE_PATTERNS

    if isinstance(data, str):
        return mask_sensitive_content(data, patterns_to_use)
    if isinstance(data, dict):
        return {k: mask_sensitive_data(v, patterns_to_use, max_depth - 1) for k, v in data.items()}
    if isinstance(data, list):
        return [mask_sensitive_data(item, patterns_to_use, max_depth - 1) for item in data]
    if isinstance(data, tuple):
        return tuple(mask_sensitive_data(item, patterns_to_use, max_depth - 1) for item in data)
    return data


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
        "ssn",
        "social_security",
        "credit_card",
        "card_number",
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


def safe_str(value: Any, max_length: int = 1000) -> str:
    """
    Safely convert a value to string with length limit.

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
    if not text:
        return text
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def extract_tool_name(tool: Any) -> str:
    """
    Extract the name from an Agno tool.

    Args:
        tool: Agno tool object

    Returns:
        Tool name as string
    """
    if tool is None:
        return "unknown"

    # Try common attribute names
    for attr in ["name", "__name__", "tool_name", "_name"]:
        if hasattr(tool, attr):
            value = getattr(tool, attr)
            if value:
                return str(value)

    # Try callable name
    if callable(tool):
        return getattr(tool, "__name__", type(tool).__name__)

    return type(tool).__name__


def extract_tool_description(tool: Any) -> str | None:
    """
    Extract the description from an Agno tool.

    Args:
        tool: Agno tool object

    Returns:
        Tool description or None
    """
    for attr in ["description", "__doc__", "tool_description"]:
        if hasattr(tool, attr):
            value = getattr(tool, attr)
            if value:
                return str(value)[:500]
    return None


def extract_agent_info(agent: Any) -> dict[str, Any]:
    """
    Extract metadata from an Agno Agent.

    Args:
        agent: Agno Agent object

    Returns:
        Dictionary with agent metadata
    """
    info = {
        "type": type(agent).__name__,
    }

    # Name
    if hasattr(agent, "name") and agent.name:
        info["name"] = str(agent.name)

    # Model info
    if hasattr(agent, "model"):
        model = agent.model
        if model is not None:
            if hasattr(model, "id"):
                info["model_id"] = str(model.id)
            else:
                info["model"] = str(model)
    if hasattr(agent, "model_id"):
        info["model_id"] = str(agent.model_id)

    # Tools
    if hasattr(agent, "tools"):
        tools = agent.tools
        if tools:
            info["tools"] = [extract_tool_name(t) for t in tools]
            info["tool_count"] = len(tools)

    # Instructions / system prompt
    if hasattr(agent, "instructions"):
        instructions = agent.instructions
        if instructions:
            info["instructions_preview"] = truncate_text(str(instructions), 200)

    # Max turns/iterations
    if hasattr(agent, "max_turns"):
        info["max_turns"] = agent.max_turns
    if hasattr(agent, "max_iterations"):
        info["max_iterations"] = agent.max_iterations

    return info


def extract_response_tokens(response: Any) -> dict[str, int]:
    """
    Extract token usage from an Agno RunResponse.

    Agno's RunResponse has a metrics dict with token fields.

    Args:
        response: Agno RunResponse object

    Returns:
        Dictionary with token counts
    """
    tokens = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
    }

    # Agno RunResponse.metrics is a dict
    if hasattr(response, "metrics") and isinstance(response.metrics, dict):
        metrics = response.metrics
        tokens["input_tokens"] = metrics.get("input_tokens", 0) or 0
        tokens["output_tokens"] = metrics.get("output_tokens", 0) or 0
        tokens["total_tokens"] = metrics.get("total_tokens", 0) or 0

    # Try usage attribute (some providers)
    if hasattr(response, "usage"):
        usage = response.usage
        if hasattr(usage, "input_tokens"):
            tokens["input_tokens"] = usage.input_tokens
        if hasattr(usage, "output_tokens"):
            tokens["output_tokens"] = usage.output_tokens
        if hasattr(usage, "total_tokens"):
            tokens["total_tokens"] = usage.total_tokens

    # Fallback to direct attributes
    for attr, key in [
        ("input_tokens", "input_tokens"),
        ("output_tokens", "output_tokens"),
        ("prompt_tokens", "input_tokens"),
        ("completion_tokens", "output_tokens"),
    ]:
        if hasattr(response, attr):
            val = getattr(response, attr, 0)
            if val:
                tokens[key] = val

    # Calculate total if not provided
    if tokens["total_tokens"] == 0:
        tokens["total_tokens"] = tokens["input_tokens"] + tokens["output_tokens"]

    return tokens


def extract_model_from_response(response: Any) -> str | None:
    """
    Extract the model name from an Agno RunResponse.

    Args:
        response: Agno RunResponse object

    Returns:
        Model name or None
    """
    # RunResponse.model is a direct field
    for attr in ["model", "model_id", "model_name"]:
        if hasattr(response, attr):
            value = getattr(response, attr)
            if value:
                return str(value)
    return None


def format_duration_ms(duration_ms: float | None) -> str:
    """
    Format a duration in milliseconds to human-readable string.

    Args:
        duration_ms: Duration in milliseconds

    Returns:
        Formatted duration string
    """
    if duration_ms is None:
        return "N/A"

    if duration_ms < 1000:
        return f"{duration_ms:.0f}ms"
    if duration_ms < 60000:
        return f"{duration_ms / 1000:.1f}s"
    minutes = int(duration_ms // 60000)
    seconds = (duration_ms % 60000) / 1000
    return f"{minutes}m {seconds:.1f}s"


def normalize_model_name(model: str) -> str:
    """
    Normalize model names for consistent pricing lookup.

    Args:
        model: Raw model name

    Returns:
        Normalized model name
    """
    if not model:
        return "unknown"

    model = model.lower().strip()

    # Common normalizations for Agno-supported models
    normalizations = {
        # Anthropic Claude
        "claude-3-opus": "claude-3-opus",
        "claude-3-sonnet": "claude-3-sonnet",
        "claude-3-haiku": "claude-3-haiku",
        "claude-3.5-sonnet": "claude-3-5-sonnet",
        "claude-3-5-sonnet": "claude-3-5-sonnet",
        # AWS Bedrock Claude
        "anthropic.claude-3-opus": "claude-3-opus",
        "anthropic.claude-3-sonnet": "claude-3-sonnet",
        "anthropic.claude-3-haiku": "claude-3-haiku",
        # OpenAI
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        # Google
        "gemini-2.0-flash": "gemini-2.0-flash",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
        "gemini-pro": "gemini-pro",
        # Mistral
        "mistral-large": "mistral-large-latest",
        "mistral-small": "mistral-small-latest",
    }

    for key, value in normalizations.items():
        if key in model:
            return value

    return model


def get_provider_from_model(model: str) -> str:
    """
    Determine the provider from a model name.

    Args:
        model: Model name

    Returns:
        Provider name (anthropic, openai, google, bedrock, mistral, meta, unknown)
    """
    if not model:
        return "unknown"

    model_lower = model.lower()

    if "claude" in model_lower:
        if "anthropic." in model_lower or "bedrock" in model_lower:
            return "bedrock"
        return "anthropic"
    if (
        "gpt" in model_lower
        or "openai" in model_lower
        or model_lower.startswith("o1")
        or model_lower.startswith("o3")
    ):
        return "openai"
    if "gemini" in model_lower or "google" in model_lower or "nova" in model_lower:
        return "google"
    if "mistral" in model_lower or "mixtral" in model_lower:
        return "mistral"
    if "llama" in model_lower:
        return "meta"
    return "unknown"


def parse_tool_result(result: Any) -> dict[str, Any]:
    """
    Parse a tool execution result into a standardized format.

    Args:
        result: Raw tool result

    Returns:
        Parsed result dictionary
    """
    parsed = {
        "success": True,
        "result_type": type(result).__name__,
    }

    if result is None:
        parsed["value"] = None
    elif isinstance(result, (str, int, float, bool)):
        parsed["value"] = result
    elif isinstance(result, dict):
        parsed["value"] = result
        if "error" in result:
            parsed["success"] = False
            parsed["error"] = result["error"]
    elif isinstance(result, Exception):
        parsed["success"] = False
        parsed["error"] = str(result)
        parsed["error_type"] = type(result).__name__
    else:
        parsed["value"] = safe_str(result, 500)

    return parsed


def is_streaming_response(response: Any) -> bool:
    """
    Check if a response is a streaming response.

    Args:
        response: Response object

    Returns:
        True if streaming, False otherwise
    """
    # Check for common streaming indicators
    if hasattr(response, "__aiter__") or hasattr(response, "__iter__"):
        # Could be a generator/iterator
        type_name = type(response).__name__.lower()
        if any(x in type_name for x in ["stream", "generator", "iterator", "async"]):
            return True

    return bool(hasattr(response, "stream") and response.stream)
