from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.guards import build_dispatch_marker_comment, validate_dispatch_identity

SHA = "b" * 40


def test_builds_marker_comment_with_optional_body() -> None:
    identity = validate_dispatch_identity("Repo-Name", 8, SHA, 2)

    assert build_dispatch_marker_comment(identity).startswith("<!-- agdt:ref:sub-dedup-ordering -->")
    assert build_dispatch_marker_comment(identity, "content").endswith("\n\ncontent")


def test_rejects_non_string_body() -> None:
    identity = validate_dispatch_identity("repo-name", 8, SHA, 2)

    with pytest.raises(ValueError):
        build_dispatch_marker_comment(identity, cast(Any, None))
