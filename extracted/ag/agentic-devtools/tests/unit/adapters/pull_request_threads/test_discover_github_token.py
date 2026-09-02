from agentic_devtools.adapters.pull_request_threads import discover_github_token


def test_discovers_tokens_in_priority_order() -> None:
    assert discover_github_token({"SPECKIT_PR_TOKEN": "  token  "}) == "token"
    assert discover_github_token({"GH_TOKEN": "fallback"}) == "fallback"
    assert discover_github_token({}) == ""
