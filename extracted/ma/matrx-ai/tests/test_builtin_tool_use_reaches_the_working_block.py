"""Feedback 017807f4: a provider built-in web search showed citations but no working-block card.
The executor now streams a tool_started + tool_completed pair per built-in tool."""

import asyncio

from matrx_connect.context.events import ToolEventPayload

from matrx_ai.config.builtin_tool_use import announce_builtin_tool_use, builtin_tool_events

BUILTIN = {"web_search": {"count": 2, "queries": ["harbor ferry schedule", "ferry fares 2027"], "sources_cited": 4}}


def test_frames_are_valid_tool_events_with_the_queries() -> None:
    frames = builtin_tool_events(BUILTIN, call_key="abcd1234-1-1")
    assert [f["event"] for f in frames] == ["tool_started", "tool_completed"]
    for frame in frames:
        payload = ToolEventPayload.model_validate(frame)
        assert payload.tool_name == "provider_web_search"
        assert payload.call_id == "builtin-web_search-abcd1234-1-1"
    assert frames[0]["message"] == "Searched the web: harbor ferry schedule, ferry fares 2027"
    assert frames[0]["data"]["arguments"] == {"queries": ["harbor ferry schedule", "ferry fares 2027"]}
    assert frames[1]["data"]["result"]["sources_cited"] == 4


def test_announce_sends_each_frame_and_never_raises() -> None:
    sent: list[dict] = []

    class Emitter:
        async def send_tool_event(self, frame: dict) -> None:
            sent.append(frame)

    class Broken:
        async def send_tool_event(self, frame: dict) -> None:
            raise RuntimeError("socket gone")

    asyncio.run(announce_builtin_tool_use(Emitter(), BUILTIN, call_key="k"))
    assert len(sent) == 2
    asyncio.run(announce_builtin_tool_use(Broken(), BUILTIN, call_key="k"))
    asyncio.run(announce_builtin_tool_use(None, BUILTIN, call_key="k"))
    asyncio.run(announce_builtin_tool_use(Emitter(), None, call_key="k"))
