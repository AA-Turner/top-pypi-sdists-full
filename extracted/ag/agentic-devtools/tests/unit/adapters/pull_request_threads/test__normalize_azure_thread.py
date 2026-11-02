import pytest

from agentic_devtools.adapters.pull_request_threads import _normalize_azure_thread


def test_normalizes_missing_context_and_omits_malformed_comments() -> None:
    result = _normalize_azure_thread({"id": 1, "comments": [None, {"id": 2, "author": None}]})
    assert result.file is None
    assert result.comments[0]["author"] is None
    assert _normalize_azure_thread({"id": 2}).comments == ()


def test_normalizes_malformed_author_payload_to_none() -> None:
    result = _normalize_azure_thread({"id": 1, "comments": [{"id": 2, "author": "user", "content": None}]})
    assert result.comments == ({"id": 2, "author": None, "content": ""},)


@pytest.mark.parametrize("thread_id", [True, {}, []])
def test_rejects_non_scalar_thread_id(thread_id: object) -> None:
    with pytest.raises(ValueError):
        _normalize_azure_thread({"id": thread_id})


def test_rejects_boolean_line() -> None:
    result = _normalize_azure_thread({"id": 1, "threadContext": {"rightFileStart": {"line": True}}})
    assert result.line is None


@pytest.mark.parametrize(
    "payload",
    [None, {}, {"id": 1, "threadContext": [], "comments": []}, {"id": 1, "comments": {}}],
)
def test_rejects_malformed_thread(payload: object) -> None:
    with pytest.raises(ValueError):
        _normalize_azure_thread(payload)
