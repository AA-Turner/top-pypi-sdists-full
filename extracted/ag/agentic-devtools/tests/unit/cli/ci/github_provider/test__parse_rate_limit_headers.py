"""Tests for _parse_rate_limit_headers()."""

from agentic_devtools.cli.ci.github_provider import _parse_rate_limit_headers


def test_parse_rate_limit_headers_skips_malformed_duplicate_values() -> None:
    assert _parse_rate_limit_headers(
        {
            "retry-after": "bad, 5",
            "x-ratelimit-reset": "bad, 100",
            "x-ratelimit-remaining": "bad, 0",
        }
    ) == (5, 100, 0)
    assert _parse_rate_limit_headers(
        {"retry-after": "nan,-1", "x-ratelimit-reset": "nan,0", "x-ratelimit-remaining": "-1"}
    ) == (None, None, None)


def test_parse_rate_limit_headers_aggregates_duplicates_conservatively() -> None:
    assert _parse_rate_limit_headers(
        {
            "retry-after": "30, 120, bad",
            "x-ratelimit-reset": "100, 450, bad",
            "x-ratelimit-remaining": "1, 0, bad",
        }
    ) == (120, 450, 0)
