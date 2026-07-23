# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Text processing utilities for MotherDuck query diagnostics.

Handles query text normalization, hashing, metadata extraction,
subtype detection, and string constant redaction.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid

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


_ICEBERG_DATABASE_RE = re.compile(
    r"iceberg_scan\(\s*['\"]s3[a-z0-9]*://[^'\"]*?/data/(?P<database>[A-Za-z0-9_]+)\.db/",
    re.IGNORECASE,
)
"""Match the MotherDuck/Sonar database in an `iceberg_scan('s3://...')` path.

Sonar's full-reload DDL reads iceberg data from an S3 namespace shaped like
`s3://<bucket>/data/<database_name>.db/<table>/...`, so the database name is the
`data/<database_name>.db/` segment. The S3 path (not the unqualified
`CREATE ... TABLE "<table>"` target) is the reliable signal for which
MotherDuck database (Sonar source schema) the query ran against.

Examples:
- `... FROM iceberg_scan('s3://bkt/data/postgres__<uuid>.db/users/...')`
  captures `postgres__<uuid>`.
- `SELECT 1` captures nothing (no match).
"""


def extract_database_name(query_text: str) -> str | None:
    """Extract the MotherDuck database name from a query's `iceberg_scan` path.

    Returns the `data/<database_name>.db/` segment of the first
    `iceberg_scan('s3://...')` path in `query_text`, or `None` when no such path
    is present. In Sonar each MotherDuck database is 1:1 with an Airbyte source,
    so this is the source's database (schema) name.

    This is derived from the raw query text on purpose: MotherDuck's
    `QUERY_HISTORY` / `RECENT_QUERIES` views expose no native database/catalog
    column, so the S3 iceberg path is the only in-band signal.
    """
    match = _ICEBERG_DATABASE_RE.search(query_text)
    if not match:
        return None
    return match.group("database")


def parse_source_id_from_database_name(database_name: str) -> str | None:
    """Parse the Airbyte source UUID from a Sonar MotherDuck database name.

    Sonar database names have the format `{env_prefix}{slug}__{source_id}`, where
    `source_id` is the source UUID with hyphens replaced by underscores (see
    `airbytehq/sonar` `backend/app/core/search/glue_schema.py`
    `_build_prefixed_schema_name`). The `slug` may itself contain single
    underscores, so the source UUID is the trailing component after the final
    `__` (double-underscore) delimiter; any `env_prefix` stays on the leading
    side and does not affect it.

    Returns the canonical hyphenated UUID string, or `None` if `database_name`
    has no `__` delimiter or the trailing segment is not a canonical
    `uuid.UUID`. Fails closed: a malformed or non-UUID trailing segment yields
    `None` rather than a guessed id.
    """
    if not database_name or "__" not in database_name:
        return None
    trailing = database_name.rsplit("__", 1)[-1]
    candidate = trailing.replace("_", "-")
    try:
        parsed = uuid.UUID(candidate)
    except ValueError:
        return None
    # Reject anything that is not already the canonical 8-4-4-4-12 form (e.g. a
    # 32-char hyphenless hex or brace-wrapped value `uuid.UUID` would accept), so
    # the result is a deterministic round-trip of a real Sonar database name.
    if str(parsed) != candidate.lower():
        return None
    return str(parsed)
