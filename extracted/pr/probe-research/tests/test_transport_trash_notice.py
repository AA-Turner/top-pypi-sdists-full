"""A 410 from a run or project in the server's trash carries its notice beside
a fixed `detail` token; the SDK surfaces the sentence, so a write into the
trash fails with an error a person can act on ("Probe can restore it until
... contact support"), not the bare word `in_trash`."""

from __future__ import annotations

import httpx

from probe.sdk.transport import Transport

_NOTICE = (
    "This run is in the trash since 2026-09-26, deleted by Alice. Nothing can be "
    "read from or written to it. Probe can restore it until 2026-10-17; contact support."
)


def test_a_trash_410_raises_with_the_notice_sentence() -> None:
    body = {
        "detail": "in_trash",
        "message": _NOTICE,
        "kind": "run",
        "restorable_until": "2026-10-17T10:00:00+00:00",
    }
    error = Transport._to_error(None, httpx.Response(410, json=body))  # type: ignore[arg-type]
    assert _NOTICE in str(error)


def test_any_other_error_keeps_its_detail() -> None:
    error = Transport._to_error(None, httpx.Response(404, json={"detail": "run not found"}))  # type: ignore[arg-type]
    assert "run not found" in str(error)


def _transport(responses: list[httpx.Response]) -> tuple[Transport, list[httpx.Request]]:
    from probe.sdk.config import Settings

    seen: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return responses.pop(0)

    settings = Settings(base_url="http://test", token="test-token")
    transport = Transport(
        settings,
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle)),
    )
    return transport, seen


_IN_TRASH = {"detail": "in_trash", "message": _NOTICE, "kind": "run", "trash_id": "t-1"}


def test_a_retried_delete_that_finds_it_in_the_trash_succeeds(monkeypatch) -> None:
    """The first attempt committed and its reply was lost (a 503 from the
    edge); the retry finds the run already in the trash. That is the delete
    having worked: the notice is the answer, not an error."""
    monkeypatch.setattr("probe.sdk.transport.time.sleep", lambda _s: None)
    transport, seen = _transport([httpx.Response(503), httpx.Response(410, json=_IN_TRASH)])
    assert transport.delete("/v1/runs/r-1") == _IN_TRASH
    assert [r.method for r in seen] == ["DELETE", "DELETE"]


def test_a_first_delete_of_something_already_in_the_trash_still_says_so() -> None:
    """No retry: the caller asked to delete what was ALREADY in the trash (or
    went with a parent). The sentence is the error, as for any other 410."""
    import pytest

    from probe.sdk import errors

    transport, _ = _transport([httpx.Response(410, json=_IN_TRASH)])
    with pytest.raises(errors.RosError) as raised:
        transport.delete("/v1/runs/r-1")
    assert _NOTICE in str(raised.value)
