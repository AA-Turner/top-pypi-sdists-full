from agentic_devtools.adapters.pull_request_threads import discover_github_token


def test_discovers_tokens_in_priority_order() -> None:
    assert discover_github_token({"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "  token  "}) == "token"
    assert discover_github_token({"GH_TOKEN": "fallback"}) == ""
    assert (
        discover_github_token(
            {"GH_TOKEN": "fallback", "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"}
        )
        == "fallback"
    )
    assert discover_github_token({}) == ""
