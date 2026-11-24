"""The live tool_started event names the tool's category (the owner's-words rule reads it; never a name guess)."""

import asyncio

from matrx_ai.tools.streaming import ToolStreamManager


class _Emitter:
    def __init__(self) -> None:
        self.sent: list[dict] = []

    async def send_tool_event(self, event: dict) -> None:
        self.sent.append(event)


def _started(category: str | None) -> dict:
    emitter = _Emitter()
    manager = ToolStreamManager(emitter, "call_1", "kindcomp_patch_code")  # type: ignore[arg-type]
    asyncio.run(manager.started("Patching", arguments={"a": 1}, category=category))
    return emitter.sent[0]["data"]


def test_internal_category_rides_tool_started() -> None:
    assert _started("internal")["category"] == "internal"


def test_no_category_is_none_never_guessed() -> None:
    assert _started(None)["category"] is None
