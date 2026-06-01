"""
Utility functions for LangChain integration.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_langchain_available() -> bool:
    """Check if LangChain is installed and importable.

    Returns:
        True if LangChain is available
    """
    try:
        import langchain_core

        return True
    except ImportError:
        return False


def get_langchain_version() -> str | None:
    """Get the installed LangChain version.

    Returns:
        Version string or None if not installed
    """
    try:
        import langchain_core

        return getattr(langchain_core, "__version__", "unknown")
    except ImportError:
        return None


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


def extract_chain_name(serialized: dict | None, kwargs: dict | None = None) -> str:
    """Extract chain name from LangChain's serialized dict.

    Args:
        serialized: The serialized dict from LangChain callbacks
        kwargs: Additional kwargs that may contain chain info

    Returns:
        Chain name string
    """
    if not serialized:
        return "chain_step"

    # Method 1: Extract from serialized["name"]
    name = serialized.get("name")
    if name and name not in ["chain", "Chain", "chain_step", ""]:
        return name

    # Method 2: Extract from serialized["id"]
    chain_id = serialized.get("id")
    if isinstance(chain_id, list) and chain_id:
        for part in reversed(chain_id):
            if isinstance(part, str):
                if "." in part:
                    parts = part.split(".")
                    class_name = parts[-1]
                else:
                    class_name = part

                if class_name and class_name not in [
                    "chain",
                    "Chain",
                    "chain_step",
                    "",
                    "chains",
                    "prompts",
                ]:
                    return class_name

        if chain_id[0]:
            return str(chain_id[0])

    elif isinstance(chain_id, str):
        if "." in chain_id:
            parts = chain_id.split(".")
            class_name = parts[-1]
            if class_name and class_name not in ["chain", "Chain", "chain_step"]:
                return class_name
        elif chain_id not in ["chain", "Chain", "chain_step"]:
            return chain_id

    # Method 3: Try kwargs
    if kwargs:
        chain_obj = kwargs.get("chain") or kwargs.get("chain_instance")
        if chain_obj and hasattr(chain_obj, "__class__"):
            class_name = chain_obj.__class__.__name__
            if class_name and class_name not in ["Chain", "chain_step"]:
                return class_name

    # Method 4: Check _type
    if "_type" in serialized:
        type_val = serialized["_type"]
        if type_val and type_val not in ["chain", "Chain", "chain_step"]:
            return type_val

    return "chain_step"


def mask_sensitive_content(content: str, patterns: list | None = None) -> str:
    """Mask potentially sensitive content in strings.

    Args:
        content: Content to mask
        patterns: Optional list of regex patterns to mask

    Returns:
        Content with sensitive data masked
    """
    import re

    if not content:
        return content

    # Default patterns for common sensitive data
    default_patterns = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),  # Email
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),  # Phone
        (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),  # Credit card
        (r"\b\d{3}[-]?\d{2}[-]?\d{4}\b", "[SSN]"),  # SSN
        (r"(?i)(password|secret|token|api_key|apikey)[\s]*[=:]\s*[^\s,]+", "[REDACTED]"),  # Keys
    ]

    patterns_to_use = patterns if patterns is not None else default_patterns

    result = content
    for pattern, replacement in patterns_to_use:
        result = re.sub(pattern, replacement, result)

    return result
