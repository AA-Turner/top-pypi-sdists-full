"""Tests for decode_paginated_file_entries."""

import pytest

from agentic_devtools.cli.ci.github_pr_files import decode_paginated_file_entries


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        ("[]", []),
        ('[{"filename":"a"}] [{"filename":"b"}]', [{"filename": "a"}, {"filename": "b"}]),
        ("[]  ", []),
        ("", None),
        ("   ", None),
        ("{}", None),
        ("[]{}", None),
        ("[{", None),
    ],
)
def test_decodes_only_nonempty_concatenated_array_pages(response: str, expected: list[object] | None) -> None:
    assert decode_paginated_file_entries(response) == expected
