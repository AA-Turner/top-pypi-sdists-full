"""Shared types for the web_fetch builtin."""

from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator

DEFAULT_TIMEOUT_SECONDS = 30
MAX_TIMEOUT_SECONDS = 120


class WebFetchArgs(BaseModel):
    url: str = Field(description="URL to fetch (http/https).")
    timeout: int = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        description=f"Timeout in seconds (max {MAX_TIMEOUT_SECONDS}).",
    )

    @field_validator("url")
    @classmethod
    def _normalize_url_input(cls, value: str) -> str:
        url = value.strip()
        if not url:
            raise ValueError("URL cannot be empty")

        raw = url.lstrip("/") if url.startswith("//") else url
        parsed = urlparse(raw)
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Must be http or https.")
        if raw.startswith(("http://", "https://")):
            return raw
        return "https://" + raw

    @field_validator("timeout", mode="before")
    @classmethod
    def _default_timeout(cls, value: Any) -> Any:
        if value is None:
            return DEFAULT_TIMEOUT_SECONDS
        return value

    @field_validator("timeout")
    @classmethod
    def _validate_timeout(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Timeout must be a positive number")
        if value > MAX_TIMEOUT_SECONDS:
            raise ValueError(f"Timeout cannot exceed {MAX_TIMEOUT_SECONDS} seconds")
        return value


class WebFetchResult(BaseModel):
    url: str
    content: str
    content_type: str
    was_truncated: bool = False
