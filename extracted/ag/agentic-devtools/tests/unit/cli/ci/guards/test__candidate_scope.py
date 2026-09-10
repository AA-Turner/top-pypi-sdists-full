from agentic_devtools.cli.ci.guards import _candidate_scope


def test_normalizes_supported_scope_shapes() -> None:
    assert _candidate_scope({"pull_request": {"number": 8}, "repo": "repo"}) == ("repo", 8)
    assert _candidate_scope({"repo": "owner/repo", "pull_request_id": 8}) == ("repo", 8)
    assert _candidate_scope({"repo": "repo", "repository": "owner/repo", "pr_number": 8, "pull_request_id": 8}) == (
        "repo",
        8,
    )


def test_rejects_invalid_scope_shapes() -> None:
    assert _candidate_scope({"repo": "a/b/c", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "/repo", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "./repo", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "owner/", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "owner/..", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": ".", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "repo", "pull_request_id": "8"}) == (None, None)
    assert _candidate_scope({"repo": 7, "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "repo"}) == (None, None)
    assert _candidate_scope({"repo": "repo", "repository": "wrong", "pull_request_id": 8}) == (None, None)
    assert _candidate_scope({"repo": "repo", "pull_request_id": 8, "pr_number": 9}) == (None, None)
    assert _candidate_scope({"repo": "repo", "pull_request_id": 8, "pull_request": "wrong"}) == (None, None)
    assert _candidate_scope({"repo": "repo", "pull_request_id": 8, "pull_request": {"node_id": "x"}}) == (None, None)
