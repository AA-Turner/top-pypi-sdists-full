import pytest

from agentic_devtools.ai_providers.dispatch_policy import (
    DispatchInputError,
    build_dispatch_marker,
    parse_dispatch_marker,
)


def test_parse_dispatch_marker_reads_valid_marker() -> None:
    marker = build_dispatch_marker("owner/repo", 42, "a" * 40, 2)
    parsed = parse_dispatch_marker(marker)
    assert parsed.repo == "owner/repo"
    assert parsed.pull_request_id == 42
    assert parsed.sha == "a" * 40
    assert parsed.ordinal == 2


def test_parse_dispatch_marker_canonicalizes_repo_case() -> None:
    parsed = parse_dispatch_marker(
        "<!-- agdt:agent-task-dispatch:v1 repo=Owner/Repo pr=42 sha=" + "a" * 40 + " ordinal=2 -->"
    )
    assert parsed.repo == "owner/repo"


def test_parse_dispatch_marker_rejects_extra_or_duplicate_fields() -> None:
    marker = build_dispatch_marker("owner/repo", 42, "a" * 40, 2)
    with pytest.raises(DispatchInputError):
        parse_dispatch_marker(marker + " ")
    with pytest.raises(DispatchInputError):
        parse_dispatch_marker(marker.replace(" -->", " pr=42 -->"))


def test_parse_dispatch_marker_rejects_non_string_and_mismatched_fields() -> None:
    with pytest.raises(DispatchInputError):
        parse_dispatch_marker(None)  # type: ignore[arg-type]
    with pytest.raises(DispatchInputError):
        parse_dispatch_marker(
            "<!-- agdt:agent-task-dispatch:v1 repo=owner/repo pr=0 sha=" + "a" * 40 + " ordinal=1 -->"
        )
