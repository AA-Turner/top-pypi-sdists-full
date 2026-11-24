"""FORCING GUARD — a declared tool-output trim on the Gemini wire is placed, not filed as drift.

Live (system_error ``prompt_cache_prefix_drift``, conversation ae90e431, gemini-3.8-flash, 2026-11-10):
"contents[7] (user) changed (49,980 -> 343 bytes) (possible cause: the send boundary rewrote 1 block(s) it
could not place on the wire)". The send boundary DECLARED the rewrite (by call id), but Gemini's
``functionResponse`` / ``functionCall`` carry no id, so ``place_trim_on_wire`` could never find it and every
lawful Gemini trim was filed as an unproven prefix break. The guard now places a rewrite no id placed on an
id-less function part carrying the trim's own marker, only in an item that changed, never more than declared.

Runs the real send boundary and the real Google translator, then the real guard comparison.
"""

from __future__ import annotations

from matrx_ai.config import MessageList, TextContent, ToolCallContent, ToolResultContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.providers.cache_guard import (
    TrimDeclaration,
    changed_item_positions,
    compare_wire_prefix,
    place_trim_on_wire,
    wire_prefix,
)
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.testing.profile_factory import make_profile

CLEARED = '{"result": "[tool result cleared] Replaced with keys and chars -- Fetch again when necessary"}'


def _send(result_content: str) -> dict:
    config = UnifiedConfig(
        model="m",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="look it up")])]),
    )
    config.system_instruction = "You are careful. " * 40
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="gemini_ab12", name="web", arguments={"q": "x"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="gemini_ab12", name="web", content=result_content)])
    )
    config.messages.append(UnifiedMessage(role="assistant", content=[TextContent(text="Found it.")]))
    config.messages.append(UnifiedMessage(role="user", content=[TextContent(text="and the next one?")]))
    profile = make_profile(model_name="m", wire_format="google_chat")
    prep = order_for_wire(config, profile, iteration=2)
    return GoogleTranslator().build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def test_a_declared_trim_on_the_gemini_wire_is_placed_and_not_filed() -> None:
    before, after = _send("BIG " * 500), _send(CLEARED)
    prev, new = wire_prefix(before), wire_prefix(after)
    assert prev is not None and new is not None
    trim = TrimDeclaration(results=frozenset({"gemini_ab12"}))
    positions, unplaced = place_trim_on_wire(after, trim, changed_at=changed_item_positions(prev, new))
    assert unplaced == 0 and positions, "the declared Gemini trim was not found on the wire"
    drift = compare_wire_prefix(prev, new, trimmed_positions=positions)
    assert not drift.changed, f"a declared Gemini trim was filed as drift: {list(drift.changed)}"


def test_an_unmarked_change_on_the_gemini_wire_is_still_filed() -> None:
    """A changed function response WITHOUT the trim's words is not the declared rewrite: still unplaced."""
    before, after = _send("BIG " * 500), _send("SOMETHING ELSE " * 20)
    prev, new = wire_prefix(before), wire_prefix(after)
    assert prev is not None and new is not None
    trim = TrimDeclaration(results=frozenset({"gemini_ab12"}))
    positions, unplaced = place_trim_on_wire(after, trim, changed_at=changed_item_positions(prev, new))
    assert unplaced == 1 and not positions
    assert compare_wire_prefix(prev, new, trimmed_positions=positions).changed


def test_an_old_trim_in_an_unchanged_item_does_not_whitelist_a_new_change() -> None:
    """An item trimmed in an EARLIER round still carries the marker but did not change: it is never placed."""
    after = _send(CLEARED)
    trim = TrimDeclaration(results=frozenset({"gemini_ab12"}))
    positions, unplaced = place_trim_on_wire(after, trim, changed_at=frozenset())
    assert unplaced == 1 and not positions
