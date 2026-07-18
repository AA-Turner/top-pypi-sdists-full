# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Text processing utilities for MotherDuck query diagnostics.

Handles query text normalization, hashing, metadata extraction,
subtype detection, and string constant redaction.
"""

from __future__ import annotations

import hashlib
import json
import re

_LEADING_COMMENT_RE = re.compile(r"^\s*/\*(.*?)\*/", re.DOTALL)
"""Match a leading C-style block comment (non-greedy).

Captures everything between `/*` and the first `*/`. Used to find a
potential JSON metadata object at the start of a query.

Examples:
- `/* {"app": "sonar"} */ SELECT 1` -> captures ` {"app": "sonar"} `
- `/* {"a": {"b": 1}} */ SELECT 1` -> captures ` {"a": {"b": 1}} `
- `/* {"a": 1} */ SELECT '}' */` -> captures ` {"a": 1} ` (stops at first `*/`)
"""

_STRING_LITERAL_RE = re.compile(
    r"'"  # opening single quote
    r"(?:"  # non-capture group for string content
    r"[^'\\]"  # normal char (not a quote or backslash)
    r"|\\."  # backslash escape (e.g. \' or \n)
    r"|''"  # SQL doubled-quote escape
    r")*"  # zero or more content segments
    r"'"  # closing single quote
)
"""Match a SQL single-quoted string literal, handling both escape styles.

Handles backslash escapes (`\\'`) and SQL-standard doubled-quote escapes (`''`).

Examples:
- `'hello'` -> matches `'hello'`
- `'it''s'` -> matches the full `'it''s'` (doubled-quote escape)
- `'line\\nbreak'` -> matches `'line\\nbreak'` (backslash escape)
"""

_QUERY_SUBTYPE_KEYWORDS: set[str] = {
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
    "COPY",
    "CREATE",
    "DROP",
    "ALTER",
    "ATTACH",
    "DETACH",
    "USE",
    "SET",
    "EXPLAIN",
    "DESCRIBE",
    "SHOW",
    "INSTALL",
    "LOAD",
    "CALL",
    "WITH",
    "FROM",
    "PRAGMA",
}

_FIRST_KEYWORD_RE = re.compile(r"^\s*(\w+)", re.IGNORECASE)


def extract_metadata(query_text: str) -> dict[str, object] | None:
    """Extract JSON metadata from a leading C-style comment if present.

    Looks for a pattern like `/* {"key": "value", ...} */` at the start
    of the query text and parses the JSON contents.

    Returns the parsed dict, or `None` if no metadata comment is found
    or parsing fails.
    """
    match = _LEADING_COMMENT_RE.match(query_text)
    if not match:
        return None
    content = match.group(1).strip()
    if not content.startswith("{"):
        return None
    try:
        return json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return None


def strip_metadata_comment(query_text: str) -> str:
    """Remove the leading C-comment from query text if it looks like JSON metadata.

    Strips a leading `/* ... */` comment when its trimmed contents start with
    `{`, matching the metadata shape that `extract_metadata` looks for. This is
    intentionally lenient: the comment is removed based on the `{` prefix alone,
    even if the contents are not strictly valid JSON.
    """
    match = _LEADING_COMMENT_RE.match(query_text)
    if not match:
        return query_text
    content = match.group(1).strip()
    if not content.startswith("{"):
        return query_text
    return query_text[match.end() :]


def normalize_query(query_text: str) -> str:
    """Normalize query text for hashing: strip metadata comment and whitespace."""
    stripped = strip_metadata_comment(query_text)
    return stripped.strip()


def compute_query_hash(query_text: str) -> str:
    """Compute SHA-256 hex digest of the normalized query text."""
    normalized = normalize_query(query_text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def detect_query_subtype(query_text: str) -> str:
    """Detect the query subtype by matching the first keyword token.

    Returns an upper-case keyword string (e.g. `SELECT`, `INSERT`, `CREATE`)
    or `UNKNOWN` if the first token does not match any known keyword.

    NOTE: This implementation is for analytics/insights only. This is _not_
    a valid algorithm for blocking non-read-only (non-SELECT) query types, and
    should _not_ be relied upon for security-related use cases.
    """
    normalized = normalize_query(query_text)
    match = _FIRST_KEYWORD_RE.match(normalized)
    if not match:
        return "UNKNOWN"
    keyword = match.group(1).upper()
    if keyword in _QUERY_SUBTYPE_KEYWORDS:
        return keyword
    return "UNKNOWN"


def redact_string_constants(query_text: str) -> str:
    """Replace string literals in SQL with `?` to avoid exposing PII."""
    return _STRING_LITERAL_RE.sub("?", query_text)


def apply_query_text_treatment(
    query_text: str,
    *,
    char_limit: int,
    redact_strings: bool,
) -> str:
    """Apply treatment options to query text before returning to caller.

    Processing order: redact string constants (if enabled), then truncate.
    """
    result = normalize_query(query_text)
    if redact_strings:
        result = redact_string_constants(result)
    if len(result) > char_limit:
        if char_limit <= 3:
            result = result[:char_limit]
        else:
            result = result[: char_limit - 3] + "..."
    return result
