"""A not-found reason word this SDK does not know still parses.

The gateway owns the reason vocabulary and can add a word after a release is
published: it added ``unavailable`` after 0.61.2 shipped, and that release
raised on it. The type names the known words and stays open, so the word
arrives as-is on both the typed per-SKU methods and the generic ``run``.
"""

from __future__ import annotations

from getanyapi.types import OutputNotFound
from conftest import json_response, make_sync_client

_FUTURE_REASON = "blocked_in_region"


def test_an_unknown_reason_keeps_its_word_on_typed_and_generic_calls() -> None:
    body = {
        "output": {"found": False, "data": None, "reason": _FUTURE_REASON},
        "provider": "AnyAPI",
        "costUsd": 0.0,
        "items": 0,
        "replayed": False,
    }
    client, _ = make_sync_client(lambda _request: json_response(200, body))

    typed = client.amazon.reviews(product="B07")
    generic = client.run("custom.result", {})

    for result in (typed, generic):
        assert isinstance(result.output, OutputNotFound)
        assert result.output.found is False
        assert result.output.reason == _FUTURE_REASON
