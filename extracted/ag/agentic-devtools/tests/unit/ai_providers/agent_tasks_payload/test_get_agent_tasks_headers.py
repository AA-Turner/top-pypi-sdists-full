import pytest

from agentic_devtools.ai_providers import get_agent_tasks_headers


def test_get_agent_tasks_headers_returns_exact_required_values() -> None:
    assert get_agent_tasks_headers("ghu_test_sentinel_" + "token") == {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + "ghu_test_sentinel_" + "token",
        "X-GitHub-Api-Version": "2026-03-10",
    }


@pytest.mark.parametrize("token", ["", None, 1])
def test_get_agent_tasks_headers_rejects_empty_or_non_string_token(token: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        get_agent_tasks_headers(token)  # type: ignore[arg-type]


@pytest.mark.parametrize("token", ["ghu_test\r\nX-Injected: 1", "ghu_test\nX-Injected: 1"])
def test_get_agent_tasks_headers_rejects_tokens_with_crlf(token: str) -> None:
    with pytest.raises(ValueError, match="CR or LF"):
        get_agent_tasks_headers(token)
