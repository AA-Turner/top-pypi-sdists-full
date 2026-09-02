"""Validation utilities for structured LLM output schemas.

Provides validate_llm_output() and SchemaValidationError for parsing LLM responses.
"""

from __future__ import annotations

import hashlib
import inspect
import logging
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from ._fallback import run_fallback_pipeline

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class SchemaValidationError(Exception):
    """Raised when LLM output cannot be validated against the target schema.

    Contains diagnostic information including:
    - The target model name
    - A truncated preview of the raw input (200 bytes UTF-8)
    - A SHA-256 digest of the full raw input for correlation
    - Field-path specific validation errors
    - Optionally, the full raw input (opt-in)
    """

    def __init__(
        self,
        *,
        model_name: str,
        raw_input: str,
        errors: list[dict[str, object]],
        include_raw: bool = False,
    ) -> None:
        self.model_name = model_name
        self.raw_input_preview = _truncate_utf8(raw_input, 200)
        self.raw_input_digest = hashlib.sha256(raw_input.encode()).hexdigest()
        self.errors = errors
        self.full_raw_input = raw_input if include_raw else None

        error_summary = "; ".join(f"{_format_error_path(e)}: {e.get('msg', 'unknown error')}" for e in errors[:5])
        message = (
            f"Failed to validate LLM output against {model_name}. "
            f"Errors: {error_summary}. "
            f"Input preview: {self.raw_input_preview!r} "
            f"[sha256:{self.raw_input_digest[:12]}]"
        )
        super().__init__(message)


def _truncate_utf8(text: str, max_bytes: int) -> str:
    """Truncate text to at most max_bytes when encoded as UTF-8."""
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    if max_bytes <= 0:
        return ""
    ellipsis = "..."
    ellipsis_bytes = len(ellipsis.encode("utf-8"))
    if max_bytes <= ellipsis_bytes:
        return "." * max_bytes
    # Truncate at byte boundary, decode with error handling
    truncated = encoded[: max_bytes - ellipsis_bytes].decode("utf-8", errors="ignore")
    return truncated + ellipsis


def _format_error_path(error: dict[str, object]) -> str:
    """Format a Pydantic validation error location as a dot-notation path."""
    loc = error.get("loc", ())
    if not loc:
        return "<root>"
    if not isinstance(loc, (list, tuple)):
        return str(loc)
    return ".".join(str(part) for part in loc)


def validate_llm_output(
    model_class: type[T],
    raw_response: str,
    *,
    include_raw_on_error: bool = False,
) -> T:
    """Validate raw LLM response text against a Pydantic model schema.

    Attempts direct JSON parsing first, then applies the fallback pipeline
    for common LLM output deviations. Returns a validated model instance
    on success, or raises SchemaValidationError with detailed diagnostics.

    Both argument orderings are supported:
        validate_llm_output(ModelClass, raw_text)   # canonical
        validate_llm_output(raw_text, ModelClass)   # documented alias

    Args:
        model_class: The Pydantic model class to validate against.
        raw_response: The raw string response from the LLM.
        include_raw_on_error: If True, include full raw input in the error.

    Returns:
        A validated instance of model_class.

    Raises:
        SchemaValidationError: If the response cannot be parsed/validated.
    """
    # Support both (ModelClass, raw) and (raw, ModelClass) call orders
    if not (inspect.isclass(model_class) and issubclass(model_class, BaseModel)):
        model_class, raw_response = raw_response, model_class  # type: ignore[assignment]
        if not (inspect.isclass(model_class) and issubclass(model_class, BaseModel)):
            raise TypeError(
                "validate_llm_output() requires a Pydantic BaseModel subclass as one of its "
                f"first two positional arguments; got {type(raw_response)!r} and {type(model_class)!r}"
            )

    # Try direct JSON parse
    try:
        return model_class.model_validate_json(raw_response)
    except (ValidationError, ValueError):
        pass

    # Run fallback pipeline
    result = run_fallback_pipeline(model_class, raw_response)
    if result is not None:
        return result

    # All strategies failed — collect error details
    try:
        model_class.model_validate_json(raw_response)
    except ValidationError as e:
        # Strip the 'input' key from each error entry unless the caller
        # explicitly opted in to raw data exposure via include_raw_on_error,
        # preventing accidental leakage of the raw LLM response through the
        # structured error details.
        validation_errors: list[dict[str, object]] = [
            {k: v for k, v in dict(err).items() if include_raw_on_error or k != "input"}
            for err in e.errors()  # type: ignore[arg-type]
        ]
    except ValueError:
        validation_errors = [{"loc": (), "msg": "Invalid JSON", "type": "json_invalid"}]

    raise SchemaValidationError(
        model_name=model_class.__name__,
        raw_input=raw_response,
        errors=validation_errors,
        include_raw=include_raw_on_error,
    )
