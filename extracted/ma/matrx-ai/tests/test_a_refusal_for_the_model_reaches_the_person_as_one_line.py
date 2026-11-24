"""A REFUSAL WRITTEN TO THE MODEL REACHES THE PERSON AS ONE HONEST LINE, on the server's own event.

Live (lane GAP-D, 2026-11-07): the Understanding ask guard refused an ask (``subject_settled``) with a paragraph
written to the model — "Nothing was asked: … has id understanding.industry …". The ``tool_error`` event carried that
paragraph as its ``message``, so the iPhone drew it in red. The web hid it only because its own client keeps a list of
these error types. The model reads the refusal from the tool result, never from this event; the event every client
draws carries a short line for the person and nothing written to the model.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.fault import MODEL_REFUSAL_PERSON_TEXT, REFUSALS_FOR_THE_MODEL
from matrx_ai.tools.streaming import ToolStreamManager

RAW = "Nothing was asked: \"Is the shop a storefront?\" has id understanding.industry, the item \"Industry\" (…)."


class _Emitter:
    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []

    async def send_tool_event(self, payload: dict[str, Any]) -> None:
        self.sent.append(payload)


@pytest.mark.asyncio
@pytest.mark.parametrize("error_type", sorted(REFUSALS_FOR_THE_MODEL))
async def test_a_refusal_for_the_model_streams_one_line_for_the_person(error_type: str) -> None:
    emitter = _Emitter()
    stream = ToolStreamManager(emitter, call_id="toolu_x", tool_name="ask_person")
    await stream.error(RAW, error_type)
    [wire] = emitter.sent
    assert wire["event"] == "tool_error"
    assert wire["message"] == MODEL_REFUSAL_PERSON_TEXT
    assert wire["data"]["error_type"] == error_type
    assert "Nothing was asked" not in str(wire) and "understanding." not in str(wire)
    # what is saved with the turn (reload) is the same line
    [saved] = stream.get_events_for_persistence()
    assert "Nothing was asked" not in str(saved)


@pytest.mark.asyncio
async def test_an_ordinary_error_keeps_its_own_message() -> None:
    emitter = _Emitter()
    stream = ToolStreamManager(emitter, call_id="toolu_y", tool_name="web_search")
    await stream.error("The search provider timed out.", "timeout")
    assert emitter.sent[0]["message"] == "The search provider timed out."


def test_the_person_line_is_short() -> None:
    assert len(MODEL_REFUSAL_PERSON_TEXT) <= 40 and "\n" not in MODEL_REFUSAL_PERSON_TEXT
