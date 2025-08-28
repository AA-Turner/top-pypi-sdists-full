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
}
REDACTION_VALUE = "[REDACTED]"
CONTENT_MAX_LENGTH = 24 * 1024 * 1024 - 64
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


class ResponseLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)

        if isinstance(record, ResponseLogRecord):
            extras = {
                "method": record.method,
                "url": record.url,
                "status_code": record.status_code,
                "headers": record.headers,
                "content": record.content[:1000] + "..."
                if len(record.content) > 1000
                else record.content,
            }
            message = f"{message}\n Details: {extras}"

        return message


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
    handler = logging.StreamHandler()
    handler.setFormatter(
        ResponseLogFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    response_logger.addHandler(handler)
    return response_logger
