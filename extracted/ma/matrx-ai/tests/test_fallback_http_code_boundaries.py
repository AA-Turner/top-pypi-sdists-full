"""Regression: digit codes in fallback classify must be digit-bounded.

Incident 2026-08-04: an IntegrityError banner carrying
``occurred_at = (2026-08-04 10:31:17.542904+00)`` was classified as
``rate_limit`` / HTTP 429 because microseconds ``542904`` contain the
substring ``429``. The executor then retried a paid Replicate video run.
"""

from __future__ import annotations

from matrx_ai.providers.errors import _fallback_classify


PARTITION_MISS_BANNER = """\x1b[91m
--------------------------------------------------------------------------------
Matrx ORM  |  IntegrityError

Database integrity error: no partition of relation "row_versions" found for row
DETAIL:  Partition key of the failing row contains (occurred_at) = (2026-08-04 10:31:17.542904+00).
  Constraint: check
  DB error:   no partition of relation "row_versions" found for row
DETAIL:  Partition key of the failing row contains (occurred_at) = (2026-08-04 10:31:17.542904+00).

Hint:
  - A CHECK constraint rejected values that violate a database invariant.
  - Read the DB error above for the invariant and offending row.
  - This is not transient; correct the input or the write ordering.
--------------------------------------------------------------------------------
\x1b[0m"""


def test_timestamp_microseconds_do_not_classify_as_rate_limit() -> None:
    result = _fallback_classify(PARTITION_MISS_BANNER, "replicate")
    assert result.error_type != "rate_limit"
    assert result.status_code != 429


def test_real_429_strings_still_classify_as_rate_limit() -> None:
    for message in (
        "HTTP 429 Too Many Requests",
        "status=429",
        "Request was throttled. Your rate limit resets in ~30s.",
        "429",
    ):
        result = _fallback_classify(message, "replicate")
        assert result.error_type == "rate_limit", message
        assert result.status_code == 429, message
