"""
Utility functions for Google ADK integration.

Provides agent-specific utilities for:
- Google ADK availability and version checking
- Sensitive data masking for agent inputs/outputs
- Gemini model utilities
- Tool and agent metadata extraction
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
    # Google Cloud credentials
    (
        r"\b[A-Za-z0-9_-]{24}\.apps\.googleusercontent\.com\b",
        "[GOOGLE_CLIENT_ID]",
        "Google client IDs",
    ),
    (r"ya29\.[A-Za-z0-9_-]+", "[GOOGLE_ACCESS_TOKEN]", "Google access tokens"),
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


def is_google_adk_available() -> bool:
    """
    Check if Google ADK is installed and available.

    Returns:
        True if google-adk is available, False otherwise.
    """
    try:
        import google.adk

        return True
    except ImportError:
        return False


def get_google_adk_version() -> str | None:
    """
    Get the installed Google ADK version.

    Returns:
        Version string if installed, None otherwise.
    """
    try:
        import google.adk

        return getattr(google.adk, "__version__", "unknown")
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
    Extract the name from a Google ADK tool.

    Args:
        tool: Google ADK tool object

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


def extract_agent_info(agent: Any) -> dict[str, Any]:
    """
    Extract metadata from a Google ADK Agent (LlmAgent).

    Args:
        agent: Google ADK Agent object

    Returns:
        Dictionary with agent metadata
    """
    info = {
        "type": type(agent).__name__,
    }

    # Name
    if hasattr(agent, "name"):
        info["name"] = str(agent.name)

    # Model info
    if hasattr(agent, "model"):
        info["model"] = str(agent.model)

    # Tools
    if hasattr(agent, "tools"):
        tools = agent.tools
        if tools:
            info["tools"] = [extract_tool_name(t) for t in tools]
            info["tool_count"] = len(tools)

    # Instruction/system prompt
    if hasattr(agent, "instruction"):
        instruction = agent.instruction
        if instruction:
            info["instruction_preview"] = truncate_text(str(instruction), 200)

    # Sub-agents
    if hasattr(agent, "sub_agents"):
        sub_agents = agent.sub_agents
        if sub_agents:
            info["sub_agent_count"] = len(sub_agents)

    return info


def extract_response_tokens(response: Any) -> dict[str, int]:
    """
    Extract token usage from a Gemini response.

    Args:
        response: Gemini response object

    Returns:
        Dictionary with token counts
    """
    tokens = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
    }

    # Try usage_metadata (Gemini pattern)
    if hasattr(response, "usage_metadata"):
        usage = response.usage_metadata
        if hasattr(usage, "prompt_token_count"):
            tokens["input_tokens"] = usage.prompt_token_count
        if hasattr(usage, "candidates_token_count"):
            tokens["output_tokens"] = usage.candidates_token_count
        if hasattr(usage, "total_token_count"):
            tokens["total_tokens"] = usage.total_token_count

    # Calculate total if not provided
    if tokens["total_tokens"] == 0:
        tokens["total_tokens"] = tokens["input_tokens"] + tokens["output_tokens"]

    return tokens


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
    Normalize Gemini model names for consistent pricing lookup.

    Args:
        model: Raw model name

    Returns:
        Normalized model name
    """
    if not model:
        return "unknown"

    model = model.lower().strip()

    # Gemini normalizations
    normalizations = {
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
        "gemini-1.0-pro": "gemini-1.0-pro",
        "gemini-pro": "gemini-1.0-pro",
        "gemini-pro-vision": "gemini-1.0-pro-vision",
        "gemini-ultra": "gemini-ultra",
        "models/gemini-1.5-pro": "gemini-1.5-pro",
        "models/gemini-1.5-flash": "gemini-1.5-flash",
        "models/gemini-pro": "gemini-1.0-pro",
    }

    for key, value in normalizations.items():
        if key in model:
            return value

    return model


def is_gemini_model(model: str) -> bool:
    """
    Check if a model name is a Gemini model.

    Args:
        model: Model name

    Returns:
        True if Gemini model, False otherwise
    """
    if not model:
        return False
    return "gemini" in model.lower()


def get_gemini_model_tier(model: str) -> str:
    """
    Get the tier of a Gemini model (pro, flash, ultra).

    Args:
        model: Model name

    Returns:
        Model tier (pro, flash, ultra, unknown)
    """
    if not model:
        return "unknown"

    model_lower = model.lower()

    if "ultra" in model_lower:
        return "ultra"
    if "flash" in model_lower:
        return "flash"
    if "pro" in model_lower:
        return "pro"
    return "unknown"


def extract_event_type(event: Any) -> str:
    """
    Extract the type from a Google ADK event.

    Args:
        event: Google ADK event object

    Returns:
        Event type as string
    """
    if event is None:
        return "unknown"

    if hasattr(event, "type"):
        return str(event.type)

    if hasattr(event, "__class__"):
        return event.__class__.__name__

    return type(event).__name__


def parse_function_call(call: Any) -> dict[str, Any]:
    """
    Parse a function call from a Gemini response.

    Args:
        call: Function call object

    Returns:
        Parsed function call dictionary
    """
    result = {
        "name": "unknown",
        "args": {},
    }

    if hasattr(call, "name"):
        result["name"] = call.name

    if hasattr(call, "args"):
        args = call.args
        if isinstance(args, dict):
            result["args"] = args
        elif hasattr(args, "items"):
            result["args"] = dict(args.items())

    return result


def is_streaming_response(response: Any) -> bool:
    """
    Check if a response is a streaming response.

    Args:
        response: Response object

    Returns:
        True if streaming, False otherwise
    """
    if hasattr(response, "__aiter__") or hasattr(response, "__iter__"):
        type_name = type(response).__name__.lower()
        if any(x in type_name for x in ["stream", "generator", "iterator", "async"]):
            return True

    return False
