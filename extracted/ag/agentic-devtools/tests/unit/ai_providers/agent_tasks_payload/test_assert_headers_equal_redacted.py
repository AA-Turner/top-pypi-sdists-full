import pytest

from agentic_devtools.ai_providers import assert_headers_equal_redacted


def test_assert_headers_equal_redacted_compares_complete_headers() -> None:
    assert_headers_equal_redacted(
        {"Authorization": "Bearer " + "one", "Accept": "application/vnd.github+json"},
        {"Authorization": "Bearer " + "one", "Accept": "application/vnd.github+json"},
    )


def test_assert_headers_equal_redacted_hides_tokens_in_failure() -> None:
    sentinel = "ghu_test_sentinel_" + "token"

    with pytest.raises(AssertionError) as caught:
        assert_headers_equal_redacted(
            {"Authorization": "Bearer " + sentinel},
            {"Authorization": "Bearer " + "other"},
        )

    message = str(caught.value)
    assert "<redacted>" in message
    assert sentinel not in message
    assert "Bearer " + "other" not in message
