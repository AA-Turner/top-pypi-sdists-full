"""Tests for parse_complete_pr_file_response."""

import pytest

from agentic_devtools.cli.ci.github_pr_files import parse_complete_pr_file_response


@pytest.mark.parametrize(
    ("response", "expected_count", "expected"),
    [
        ("[]", 0, []),
        ('[{"filename":"a.py"}][{"filename":"b.py"}]', 2, ["a.py", "b.py"]),
        ("", 0, None),
        ('["not a file object"]', 1, None),
        ('[{"filename":"a.py"}]', 2, None),
        ('[{"filename":""}]', 1, None),
        ('[{"filename":"a.py"}]', 3000, None),
        ("[]", True, None),
        ("[]", -1, None),
        ("[]", None, None),
    ],
)
def test_requires_complete_inventory_matching_expected_count(
    response: str, expected_count: object, expected: list[str] | None
) -> None:
    assert parse_complete_pr_file_response(response, expected_count) == expected  # type: ignore[arg-type]
