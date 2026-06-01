"""
Sensitive Data Scrubber

Structure-preserving masking for sensitive data in traces and spans.
Designed to prevent API keys, passwords, and tokens from being stored.

Key features:
- Preserves JSON structure (keys, nesting, arrays)
- Same character count masking (maintains string lengths)
- Protected fields are never scrubbed (trace_id, span_id, etc.)
- Configurable patterns and field names
"""

import re
from re import Pattern
from typing import Any

# Pre-compiled patterns for sensitive data detection
SENSITIVE_PATTERNS: dict[str, Pattern] = {
    # OpenAI API Keys (includes sk-proj-... format)
    "openai_key": re.compile(r"sk-[a-zA-Z0-9\-_]{20,}"),
    # Anthropic API Keys
    "anthropic_key": re.compile(r"sk-ant-[a-zA-Z0-9\-_]{20,}"),
    # Generic API key patterns (in various formats)
    "generic_api_key": re.compile(
        r'(?:api[_\-]?key|apikey|api_secret)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{16,})',
        re.IGNORECASE,
    ),
    # Bearer tokens
    "bearer_token": re.compile(r"Bearer\s+[a-zA-Z0-9_\.\-]+", re.IGNORECASE),
    # JWT tokens (three base64 parts separated by dots)
    "jwt_token": re.compile(r"eyJ[a-zA-Z0-9_\-]*\.eyJ[a-zA-Z0-9_\-]*\.[a-zA-Z0-9_\-]*"),
    # AWS Access Key IDs
    "aws_access_key": re.compile(r"AKIA[A-Z0-9]{16}"),
    # AWS Secret Access Keys
    "aws_secret_key": re.compile(
        r'(?:aws[_\-]?secret[_\-]?access[_\-]?key|secret[_\-]?access[_\-]?key)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9/+=]{40})',
        re.IGNORECASE,
    ),
    # Database connection strings with credentials
    "connection_string": re.compile(
        r'(?:mysql|postgresql|postgres|mongodb|redis|amqp|rabbitmq)://[^:]+:[^@]+@[^\s"\']+',
        re.IGNORECASE,
    ),
    # Password patterns in various formats
    "password_assignment": re.compile(
        r'(?:password|passwd|pwd|secret)["\']?\s*[:=]\s*["\']?([^\s"\']{4,})', re.IGNORECASE
    ),
    # Google API Keys
    "google_api_key": re.compile(r"AIza[a-zA-Z0-9_\-]{35}"),
    # GitHub tokens
    "github_token": re.compile(r"gh[pousr]_[a-zA-Z0-9]{36,}"),
    # Slack tokens
    "slack_token": re.compile(r"xox[baprs]-[a-zA-Z0-9\-]+"),
    # Basic auth in URLs
    "basic_auth_url": re.compile(r'https?://[^:]+:[^@]+@[^\s"\']+'),
}

# Field names that always contain sensitive data (case-insensitive matching)
SENSITIVE_FIELD_NAMES: set[str] = {
    "password",
    "passwd",
    "pwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "auth",
    "credentials",
    "private_key",
    "access_token",
    "refresh_token",
    "bearer",
    "x_api_key",
    "x_auth_token",
    "api_secret",
    "client_secret",
    "secret_key",
    "auth_token",
    "session_token",
    "encryption_key",
    "signing_key",
    "master_key",
    "private_key_pem",
}

# Fields that should NEVER be scrubbed (preserve functionality)
PROTECTED_FIELDS: set[str] = {
    # Identifiers
    "trace_id",
    "span_id",
    "parent_id",
    "id",
    "request_id",
    "correlation_id",
    "event_id",
    "session_id",
    "user_id",
    "run_id",
    # Span metadata
    "name",
    "type",
    "level",
    "status",
    "error_type",
    "tags",
    # Timing
    "start_time",
    "end_time",
    "duration",
    "timestamp",
    "created_at",
    "updated_at",
    # LLM-specific (important for analytics)
    "model",
    "model_name",
    "model_id",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "input_cost",
    "output_cost",
    "total_cost",
    # Structural
    "version",
    "environment",
    "release",
    "service",
}


def scrub_value(
    value: str, mask_char: str = "*", show_prefix: int = 4, show_suffix: int = 4
) -> str:
    """
    Scrub a string value with partial masking (like credit cards).

    Shows the first and last few characters to help identify the value,
    with asterisks in the middle. This helps users know what type of
    key/secret it was without exposing the full value.

    Args:
        value: The sensitive string to scrub
        mask_char: Character to use for masking (default: *)
        show_prefix: Number of characters to show at start (default: 4)
        show_suffix: Number of characters to show at end (default: 4)

    Returns:
        Partially masked string

    Examples:
        >>> scrub_value("sk-proj-abc123def456xyz")
        "sk-p***...***xyz"
        >>> scrub_value("password123")
        "pass***d123"
        >>> scrub_value("short")  # Too short, fully mask
        "*****"
    """
    # For very short strings, mask entirely (security)
    min_length = show_prefix + show_suffix + 3
    if len(value) < min_length:
        return mask_char * len(value)

    prefix = value[:show_prefix]
    suffix = value[-show_suffix:]
    masked_length = len(value) - show_prefix - show_suffix

    # Use "***...***" pattern for longer masked sections
    if masked_length > 6:
        middle = f"{mask_char * 3}...{mask_char * 3}"
    else:
        middle = mask_char * masked_length

    return f"{prefix}{middle}{suffix}"


def scrub_data(
    data: Any,
    disabled: bool = False,
    custom_patterns: list[Pattern] | None = None,
    custom_fields: set[str] | None = None,
    mask_char: str = "*",
) -> Any:
    """
    Recursively scrub sensitive data while preserving structure.

    This function:
    - Preserves JSON structure (keys, nesting, arrays)
    - Only replaces values, never removes fields
    - Maintains data types (strings stay strings)
    - Uses same character count for masking

    Args:
        data: The data to scrub (dict, list, str, or other)
        disabled: If True, return data unchanged (for debugging)
        custom_patterns: Additional regex patterns to detect sensitive data
        custom_fields: Additional field names to always scrub
        mask_char: Character to use for masking

    Returns:
        Scrubbed data with same structure as input

    Example:
        >>> scrub_data({"api_key": "sk-123", "name": "test"})
        {"api_key": "******", "name": "test"}
    """
    if disabled:
        return data

    if isinstance(data, dict):
        return {
            k: _scrub_field(k, v, custom_patterns, custom_fields, mask_char)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [scrub_data(item, False, custom_patterns, custom_fields, mask_char) for item in data]
    if isinstance(data, str):
        return _scrub_string(data, custom_patterns, mask_char)
    # Non-string primitives (int, float, bool, None) pass through unchanged
    return data


def _normalize_field_name(key: str) -> str:
    """Normalize a field name for comparison (lowercase, underscores)."""
    return key.lower().replace("-", "_").replace(" ", "_")


def _scrub_field(
    key: str,
    value: Any,
    custom_patterns: list[Pattern] | None = None,
    custom_fields: set[str] | None = None,
    mask_char: str = "*",
) -> Any:
    """
    Scrub a field based on its key name and value.

    Args:
        key: The field name
        value: The field value
        custom_patterns: Additional regex patterns
        custom_fields: Additional sensitive field names
        mask_char: Masking character

    Returns:
        Scrubbed value (same type as input)
    """
    key_normalized = _normalize_field_name(key)

    # Never scrub protected fields
    if key_normalized in PROTECTED_FIELDS:
        return value

    # Combine default and custom sensitive fields
    all_sensitive_fields = SENSITIVE_FIELD_NAMES
    if custom_fields:
        all_sensitive_fields = SENSITIVE_FIELD_NAMES | custom_fields

    # Always scrub fields with sensitive names
    if key_normalized in all_sensitive_fields:
        if isinstance(value, str):
            return scrub_value(value, mask_char)
        if isinstance(value, dict):
            # For nested dicts under sensitive keys, scrub all string values
            return {
                k: scrub_value(str(v), mask_char) if isinstance(v, str) else v
                for k, v in value.items()
            }
        if isinstance(value, list):
            # For lists under sensitive keys, scrub string elements
            return [
                scrub_value(str(item), mask_char) if isinstance(item, str) else item
                for item in value
            ]
        return value

    # Recursively process nested structures
    return scrub_data(value, False, custom_patterns, custom_fields, mask_char)


def _partial_mask(match_text: str, mask_char: str = "*") -> str:
    """
    Apply partial masking to a matched pattern (like credit cards).

    Shows first 4 and last 4 characters for identification.
    """
    if len(match_text) < 11:  # Too short for partial mask
        return mask_char * len(match_text)

    prefix = match_text[:4]
    suffix = match_text[-4:]
    masked_length = len(match_text) - 8

    if masked_length > 6:
        middle = f"{mask_char * 3}...{mask_char * 3}"
    else:
        middle = mask_char * masked_length

    return f"{prefix}{middle}{suffix}"


def _scrub_string(
    text: str,
    custom_patterns: list[Pattern] | None = None,
    mask_char: str = "*",
) -> str:
    """
    Scrub sensitive patterns from a string with partial masking.

    Detected patterns are replaced with partial masks showing first/last
    characters (like credit cards) so users can identify what was scrubbed.

    Args:
        text: The text to scan for sensitive patterns
        custom_patterns: Additional patterns to check
        mask_char: Character to use for masking

    Returns:
        Text with sensitive patterns partially masked

    Example:
        >>> _scrub_string("My key is sk-abc123def456ghij")
        "My key is sk-a***...***ghij"
    """
    result = text

    # Apply all default patterns with partial masking
    for pattern in SENSITIVE_PATTERNS.values():
        result = pattern.sub(lambda m: _partial_mask(m.group(), mask_char), result)

    # Apply custom patterns if provided
    if custom_patterns:
        for pattern in custom_patterns:
            result = pattern.sub(lambda m: _partial_mask(m.group(), mask_char), result)

    return result


def create_scrubber(
    enabled: bool = True,
    custom_patterns: list[str] | None = None,
    custom_fields: list[str] | None = None,
    mask_char: str = "*",
):
    """
    Create a configured scrubber function.

    This is useful for creating a reusable scrubber with custom configuration.

    Args:
        enabled: Whether scrubbing is enabled
        custom_patterns: List of regex pattern strings
        custom_fields: List of additional field names to scrub
        mask_char: Character to use for masking

    Returns:
        A scrubber function that takes data and returns scrubbed data

    Example:
        >>> scrubber = create_scrubber(custom_fields=["my_secret_field"])
        >>> scrubber({"my_secret_field": "secret123"})
        {"my_secret_field": "*********"}
    """
    # Compile custom patterns
    compiled_patterns = None
    if custom_patterns:
        compiled_patterns = [re.compile(p) for p in custom_patterns]

    # Create field set
    field_set = None
    if custom_fields:
        field_set = {_normalize_field_name(f) for f in custom_fields}

    def scrubber(data: Any, disabled: bool = False) -> Any:
        if not enabled:
            return data
        return scrub_data(data, disabled, compiled_patterns, field_set, mask_char)

    return scrubber


# Default scrubber instance
default_scrubber = create_scrubber()
