from agentic_devtools.ai_providers.dispatch_policy import DispatchMarker


def test_dispatch_marker_as_dict() -> None:
    marker = DispatchMarker(repo="owner/repo", pull_request_id=42, sha="a" * 40, ordinal=2)
    assert marker.as_dict() == {
        "repo": "owner/repo",
        "pull_request_id": 42,
        "sha": "a" * 40,
        "ordinal": 2,
    }
