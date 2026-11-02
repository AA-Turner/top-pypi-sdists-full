import pytest

from agentic_devtools.ai_providers.dispatch_policy import DispatchInputError, build_dispatch_marker


def test_build_dispatch_marker_is_deterministic() -> None:
    marker = build_dispatch_marker("owner/repo", 42, "a" * 40, 2)
    assert marker == "<!-- agdt:agent-task-dispatch:v1 repo=owner/repo pr=42 sha=" + "a" * 40 + " ordinal=2 -->"


def test_build_dispatch_marker_canonicalizes_repo_case() -> None:
    marker = build_dispatch_marker("Owner/Repo", 42, "a" * 40, 2)
    assert "repo=owner/repo" in marker


@pytest.mark.parametrize(
    "args",
    [
        ("owner/-->", 42, "a" * 40, 1),
        ("", 42, "a" * 40, 1),
        ("owner/repo/extra", 42, "a" * 40, 1),
        ("owner/repo", True, "a" * 40, 1),
        ("owner/repo", 0, "a" * 40, 1),
        ("owner/repo", 42, "A" * 40, 1),
        ("owner/repo", 42, "not-a-sha", 1),
        ("owner/repo", 42, "a" * 7, 1),
        ("owner/repo", 42, "a" * 39, 1),
        ("owner/repo", 42, "a" * 41, 1),
        ("owner/repo", 42, "a" * 40, 0),
        ("owner/repo", 42, "a" * 40, 4),
    ],
)
def test_build_dispatch_marker_rejects_invalid_identity_or_ordinal(args: tuple[object, ...]) -> None:
    with pytest.raises(DispatchInputError):
        build_dispatch_marker(*args)  # type: ignore[arg-type]
