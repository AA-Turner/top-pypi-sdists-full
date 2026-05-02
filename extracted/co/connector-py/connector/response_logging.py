import logging
import re
from typing import Any

DENYLISTED_HEADERS = {
    "authorization",
    "auth",
    "token",
    "api-key",
    "apikey",
    "x-api-key",
    "client-secret",
    "client_secret",
    "bearer",
    "jwt",
    "session",
    "cookie",
    "set-cookie",
    "x-auth",
    "x-auth-token",
    "basic",
    "password",
    "secret",
    "private-key",
    "access-key",
    "access_key",
    "exo_cert_thumbprint",
}
REDACTION_VALUE = "[REDACTED]"
HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH = 8 * 1024
HTTP_ERROR_CONTENT_PREVIEW_MAX_LENGTH = 12 * 1024
TRUNCATION_SEPARATOR = "...[truncated]..."
SENSITIVE_FIELDS_PATTERN = (
    r"(access_token|refresh_token|temporary_password|token|api[_-]?key|client[_-]?secret|"
    r"password|secret|auth[_-]?token|jwt|bearer|"
    r"ssn|social[_-]?security|tax[_-]?id|ein|"
    r"national[_-]?id|passport[_-]?number|driver[_-]?license|"
    r"date[_-]?of[_-]?birth|birth[_-]?date|dob|"
    r"phone|mobile|cell|telephone|"
    r"email|mail|"
    r"address[_-]?line[0-9]|street|city|state|zip|postal|country|"
    r"card[_-]?number|cvv|cvc|pin|account[_-]?number)"
)


class ResponseLogRecord(logging.LogRecord):
    method: str
    url: str
    status_code: int
    headers: dict[str, str]
    content: str
    content_length_original: int | None
    content_truncated: bool
    content_hash: str | None


class ResponseLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)

        if isinstance(record, ResponseLogRecord):
            # Call sites (httpx, AWS wrapper, Google API client) may not set every field
            # Using getattr to avoid AttributeError if a field is not set in a custom log_response
            extras = {
                "method": getattr(record, "method", ""),
                "url": getattr(record, "url", ""),
                "status_code": getattr(record, "status_code", 0),
                "headers": getattr(record, "headers", {}),
                "content": getattr(record, "content", ""),
                "content_length_original": getattr(record, "content_length_original", None),
                "content_truncated": getattr(record, "content_truncated", False),
                "content_hash": getattr(record, "content_hash", None),
            }
            message = f"{message}\n Details: {extras}"

        return message


def _head_tail_truncate(content: str, max_length: int) -> str:
    """
    Preserves the beginning and end of the content, truncating in the middle.
    """
    if len(content) <= max_length:
        return content

    sep_len = len(TRUNCATION_SEPARATOR)
    if max_length <= sep_len + 2:
        return content[:max_length]

    head_len = (max_length - sep_len) // 2
    tail_len = max_length - sep_len - head_len
    return f"{content[:head_len]}{TRUNCATION_SEPARATOR}{content[-tail_len:]}"


def summarize_response_content(content: str, status_code: int) -> tuple[str, int, bool]:
    """
    Returns a bounded preview while retaining original-size metadata.
    2xx responses get a smaller cap; non-2xx get slightly larger cap.
    """
    original_length = len(content)
    max_length = (
        HTTP_SUCCESS_CONTENT_PREVIEW_MAX_LENGTH
        if 200 <= status_code < 300
        else HTTP_ERROR_CONTENT_PREVIEW_MAX_LENGTH
    )
    preview = _head_tail_truncate(content, max_length)
    truncated = len(preview) < original_length
    return preview, original_length, truncated


def redact_sensitive_data(data: Any) -> Any:
    """
    Redacts sensitive information from dictionaries and strings.
    For dictionaries: Recursively traverses key-value pairs and redacts sensitive values.
    For strings: Uses regex to find and redact sensitive data in JSON-formatted strings.
    """
    if isinstance(data, dict):
        redacted = {}
        for key, value in data.items():
            if isinstance(key, str) and any(
                denylisted in key.lower() for denylisted in DENYLISTED_HEADERS
            ):
                redacted[key] = REDACTION_VALUE
            else:
                redacted[key] = redact_sensitive_data(value) if isinstance(value, dict) else value

        return redacted

    elif isinstance(data, str):
        return re.sub(
            f'"{SENSITIVE_FIELDS_PATTERN}":\\s*"[^"]*"',
            f'"\\1": "{REDACTION_VALUE}"',
            data,
            flags=re.IGNORECASE,
        )

    return data


def create_response_logger(logger_name: str) -> logging.Logger:
    """Create a response logger (same as original httpx_rewrite)"""
    response_logger = logging.getLogger(logger_name)

    # Only add handler if one doesn't already exist
    if not response_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            ResponseLogFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        response_logger.addHandler(handler)

    # Prevent logs from propagating to parent loggers (which might have their own handlers)
    response_logger.propagate = False

    return response_logger
