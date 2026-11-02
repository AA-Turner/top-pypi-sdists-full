"""Tests for recovered suppression identities, not ordinary native root counts."""

from dataclasses import replace

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import _recovered_suppressed_occurrences


def test_counts_synthetic_and_promoted_occurrences_once() -> None:
    synthetic = ReviewCommentInfo(id=-1, path="", body="", html_url="", source_review_id=100)
    promoted = replace(
        synthetic,
        id=101,
        html_url="https://example/101",
        body="Fix\n<!-- ccr-promoted:100:suppressed:1 -->",
    )
    second = replace(promoted, id=102, body="Fix\n<!-- ccr-promoted:100:suppressed:2 -->")

    assert _recovered_suppressed_occurrences(100, [synthetic, promoted, second], "") == {1, 2}


@pytest.mark.parametrize(
    "changes",
    [
        {"body": "Ordinary native finding", "is_suppressed": True},
        {"source_review_id": 99},
        {"in_reply_to_id": 99},
        {"body": "Fix\n<!-- ccr-promoted:99:suppressed:1 -->"},
        {"body": "Fix\n<!-- ccr-promoted:100:previously_missed:1 -->"},
        {"body": "<!-- ccr-promoted:100:suppressed:1 -->\nNot the final line"},
        {"body": ""},
        {"body": "Fix\n<!-- ccr-promoted:100:suppressed:0 -->"},
    ],
)
def test_does_not_guess_suppression_from_positive_native_roots(changes) -> None:
    root = ReviewCommentInfo(
        id=101,
        path="",
        body="Fix\n<!-- ccr-promoted:100:suppressed:1 -->",
        html_url="https://example/101",
        source_review_id=100,
    )

    assert _recovered_suppressed_occurrences(100, [replace(root, **changes)], "") == set()


def test_counts_explicitly_resolved_body_entries_without_native_roots() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/fixed.py:8**\n"
        "* Resolved since the previous review.\n"
        "**src/open.py:9**\n"
        "* Fix the missing guard.\n"
        "</details>"
    )

    assert _recovered_suppressed_occurrences(100, [], body) == {1}


def test_resolved_parser_echo_is_not_an_extra_occurrence() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Already fixed\n"
        "**File:** `src/fixed.py`\n"
        "**Line:** 8\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    assert _recovered_suppressed_occurrences(100, [], body) == {1}


def test_resolved_missed_findings_are_not_suppressions() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "### [P1] Already fixed\n"
        "**File:** `src/fixed.py`\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    assert _recovered_suppressed_occurrences(100, [], body) == set()
