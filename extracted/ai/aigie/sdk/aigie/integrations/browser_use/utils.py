"""
Utility functions for browser-use integration.
"""

import base64
import io
from typing import Any


def is_browser_use_available() -> bool:
    """Check if browser-use is installed and available."""
    try:
        import browser_use

        return True
    except ImportError:
        return False


def get_browser_use_version() -> str | None:
    """Get the installed browser-use version."""
    try:
        import browser_use

        return getattr(browser_use, "__version__", "unknown")
    except ImportError:
        return None


def compress_screenshot(
    screenshot_bytes: bytes,
    quality: int = 80,
    max_size: int = 500_000,
) -> bytes:
    """Compress a screenshot image.

    Args:
        screenshot_bytes: Raw screenshot bytes (PNG format)
        quality: JPEG quality (1-100)
        max_size: Maximum output size in bytes

    Returns:
        Compressed image bytes
    """
    try:
        from PIL import Image
    except ImportError:
        # If PIL not available, return original
        return screenshot_bytes

    # Open the image
    img = Image.open(io.BytesIO(screenshot_bytes))

    # Convert to RGB if necessary (for JPEG)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Try to compress
    output = io.BytesIO()
    img.save(output, format="JPEG", quality=quality, optimize=True)
    result = output.getvalue()

    # If still too large, reduce dimensions
    while len(result) > max_size and quality > 20:
        quality -= 10
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        result = output.getvalue()

    # If still too large, downscale
    if len(result) > max_size:
        scale = 0.8
        while len(result) > max_size and scale > 0.2:
            new_size = (int(img.width * scale), int(img.height * scale))
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            output = io.BytesIO()
            resized.save(output, format="JPEG", quality=quality, optimize=True)
            result = output.getvalue()
            scale -= 0.1

    return result


def screenshot_to_base64(screenshot_bytes: bytes) -> str:
    """Convert screenshot bytes to base64 string."""
    return base64.b64encode(screenshot_bytes).decode("utf-8")


def extract_action_info(action: Any) -> dict[str, Any]:
    """Extract relevant information from a browser-use action.

    Args:
        action: A browser-use action object

    Returns:
        Dictionary with action information
    """
    info = {
        "type": type(action).__name__,
    }

    # Extract common attributes
    for attr in ["selector", "text", "url", "x", "y", "key", "index"]:
        if hasattr(action, attr):
            value = getattr(action, attr)
            if value is not None:
                info[attr] = value

    return info


def safe_str(value: Any, max_length: int = 1000) -> str:
    """Safely convert value to string with length limit."""
    try:
        s = str(value)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception:
        return "<non-serializable>"


def mask_sensitive_text(text: str, patterns: list | None = None) -> str:
    """Mask potentially sensitive information in text.

    Args:
        text: Text to mask
        patterns: Optional list of regex patterns to mask

    Returns:
        Text with sensitive data masked
    """
    import re

    if patterns is None:
        # Default patterns for common sensitive data
        patterns = [
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
            (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
            (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),
            (r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b", "[SSN]"),
            (r"(?i)(password|passwd|pwd|secret|token|api_key|apikey)[\s:=]+\S+", "[REDACTED]"),
        ]

    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)

    return result
