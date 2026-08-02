r"""Utilities for parsing raw JSON text emitted by a language model into
a validated Pydantic model.

This module exists to work around language models (particularly small or local
models, e.g. via Ollama) that do not reliably support native structured-output
or tool-calling enforcement. Instead of relying on a framework's structured-output
mechanism (which typically requires the model to emit a tool call), these utilities
take the model's raw text response -- which may contain a JSON object wrapped in
markdown code fences, surrounded by commentary, or with minor syntactic issues
like trailing commas -- and attempt to extract, clean, parse, and validate it
against a target Pydantic schema.

Typical usage:

    from pydantic import BaseModel, Field

    class WeatherReport(BaseModel):
        city: str = Field(min_length=1)
        temperature_celsius: float
        condition: str

    result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
    raw_content = result["messages"][-1].content

    report = parse_json_to_structured(raw_content, WeatherReport)
"""

from __future__ import annotations

__all__ = [
    "JsonStructuredOutputParseError",
    "parse_json_to_structured",
    "parse_json_to_structured_with_retry",
]

import json
import logging
import re
from typing import TYPE_CHECKING, TypeVar

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from collections.abc import Callable

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class JsonStructuredOutputParseError(Exception):
    """Raised when a model's raw text output cannot be converted into
    the target schema.

    This error covers two distinct failure modes, both surfaced through the same
    exception type for simplicity:
      1. No valid JSON object could be extracted or decoded from the raw content.
      2. A JSON object was successfully decoded, but it does not satisfy the
         target Pydantic schema (missing fields, wrong types, failed validators).

    Attributes:
        raw_content: The original, unmodified text that failed to parse or validate.
            Callers can use this for logging, debugging, or triggering a retry
            with a modified prompt.
    """

    def __init__(self, message: str, raw_content: str) -> None:
        super().__init__(message)
        self.raw_content = raw_content


def _strip_code_fences(text: str) -> str:
    """Remove a leading/trailing markdown code fence surrounding a JSON
    payload.

    Handles both fenced variants commonly produced by language models:
    ```json
        { ... }
    ```
    and
    { ... }

    Args:
        text: Raw model output, possibly wrapped in a markdown code fence.

    Returns:
        The text with any surrounding code fence markers and outer whitespace
        removed. If no fence is present, the text is returned stripped but
        otherwise unchanged.
    """
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _extract_json_object(text: str) -> str:
    r"""Extract the first complete, top-level JSON object from arbitrary
    text.

    Scans for the first `{` and then walks the string tracking brace depth,
    while correctly skipping over braces that appear inside string literals
    (including escaped quotes). This is more robust than a greedy regex such
    as `\\{.*\\}`, which would incorrectly span from the first `{` to the very
    last `}` in the text -- producing invalid or truncated JSON whenever the
    surrounding text contains stray braces or the model appends commentary
    with its own punctuation after the object.

    Args:
        text: Arbitrary text that is expected to contain exactly one JSON
            object somewhere within it, optionally surrounded by other text.

    Returns:
        The substring spanning the first balanced `{...}` object found.

    Raises:
        ValueError: If no opening brace is found, or if a matching closing
            brace cannot be found (i.e. the object is unterminated).
    """
    start = text.find("{")
    if start == -1:
        msg = "No opening brace found in content"
        raise ValueError(msg)

    depth = 0
    in_string = False
    escape = False

    for i, char in enumerate(text[start:], start=start):
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    msg = "No matching closing brace found (unterminated JSON object)"
    raise ValueError(msg)


def _fix_common_json_issues(text: str) -> str:
    """Apply best-effort fixes for JSON syntax mistakes common in model
    output.

    Currently handles:
      - Trailing commas before a closing `}` or `]`, which are invalid in
        strict JSON but frequently produced by smaller language models.

    Args:
        text: A JSON-like string that may contain minor syntax issues.

    Returns:
        The text with known issues corrected. This is a heuristic cleanup
        pass, not a full JSON repair -- it will not fix every possible
        malformed input.
    """
    return re.sub(r",\s*([}\]])", r"\1", text)


def parse_json_to_structured(content: str, schema: type[T]) -> T:
    """Parse a model's raw text output into a validated instance of a
    Pydantic schema.

    This is the core conversion function: given the free-form text content of
    a language model's response, it attempts to locate a JSON object within
    that text, decode it, and validate it against `schema`.

    Parsing proceeds through the following stages, stopping at the first
    stage that succeeds:
      1. Strip any surrounding markdown code fence, then attempt `json.loads`
         directly on the result.
      2. Apply common JSON syntax fixes (e.g. trailing comma removal) to the
         fence-stripped text, then attempt `json.loads` again.
      3. Fall back to brace-matched extraction of the first top-level JSON
         object anywhere in the original content, apply the same syntax
         fixes, and attempt `json.loads` on the extracted substring.

    If a JSON object is successfully decoded at any stage, it is then
    validated against `schema` via `schema.model_validate`.

    Args:
        content: The raw text content of a model's response. May be plain
            JSON, JSON wrapped in a markdown code fence, or JSON embedded
            alongside other commentary text.
        schema: The Pydantic model class to validate the decoded JSON against.

    Returns:
        An instance of `schema` populated and validated from the parsed JSON.

    Raises:
        JsonStructuredOutputParseError: If no valid JSON object can be decoded
            from `content` at all, or if a JSON object is decoded but fails
            validation against `schema`. In both cases, `content` is attached
            to the exception via its `raw_content` attribute.
    """
    cleaned = _strip_code_fences(content)

    data = None

    for candidate in (cleaned, _fix_common_json_issues(cleaned)):
        try:
            data = json.loads(candidate)
            break
        except json.JSONDecodeError:
            continue

    if data is None:
        try:
            extracted = _extract_json_object(content)
            extracted = _fix_common_json_issues(extracted)
            data = json.loads(extracted)
        except (ValueError, json.JSONDecodeError) as e:
            msg = f"Could not extract valid JSON from model output: {e}"
            raise JsonStructuredOutputParseError(
                msg,
                raw_content=content,
            ) from e

    try:
        return schema.model_validate(data)
    except ValidationError as e:
        msg = f"JSON parsed but failed schema validation: {e}"
        raise JsonStructuredOutputParseError(
            msg,
            raw_content=content,
        ) from e


def parse_json_to_structured_with_retry(
    invoke_fn: Callable[[], str],
    schema: type[T],
    max_attempts: int = 3,
) -> T:
    """Repeatedly invoke a model and parse its output until it matches a
    schema.

    This provides a bounded retry loop around `parse_json_to_structured` for
    cases where a single generation may occasionally produce invalid or
    unparseable JSON (e.g. a non-deterministic small local model). Each
    attempt performs a fresh model invocation via `invoke_fn` -- this function
    does not reuse or repair a previous failed response, since re-generating
    is typically more reliable than patching malformed output.

    Args:
        invoke_fn: A zero-argument callable that performs one full model or
            agent invocation and returns the raw text content of the response
            (e.g. `lambda: agent.invoke(...)["messages"][-1].content`). This
            function is called once per attempt, up to `max_attempts` times.
        schema: The Pydantic model class each attempt's output is validated
            against.
        max_attempts: The maximum number of invoke-and-parse attempts before
            giving up. Must be at least 1.

    Returns:
        An instance of `schema` from the first attempt that parses and
        validates successfully.

    Raises:
        JsonStructuredOutputParseError: If every attempt up to `max_attempts`
            fails to produce parseable, schema-valid JSON. The raised
            exception is the one from the final failed attempt, with its
            `raw_content` reflecting that last attempt's output.
    """
    last_error: JsonStructuredOutputParseError | None = None

    for attempt in range(1, max_attempts + 1):
        raw_content = invoke_fn()
        try:
            return parse_json_to_structured(raw_content, schema)
        except JsonStructuredOutputParseError as e:
            last_error = e
            logger.warning(
                "Attempt %d/%d failed to parse structured output: %s",
                attempt,
                max_attempts,
                e,
            )

    raise last_error  # type: ignore[misc]
