"""A turn is built from the conversation row as saved, never a remembered copy (Understanding v2 D16, D17).

The person's client writes ``overrides.agent_mode`` straight to the database and a turn patches
``metadata.agent_mode_known`` there, so the copy of the row a server process remembers can hold the mode from an
earlier turn. Built from that copy, a turn told the agent "The person switched the mode by hand" when nobody had.

Fails when: ``get_conversation_data`` reads the row through a remembered copy (any read that does not ask for the
saved row), so the turn carries the old override or the old known mode.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db._cx_managers_impl import CxManagers

SAVED = {"overrides": {"agent_mode": "answer"}, "metadata": {"agent_mode_known": "answer"}}
REMEMBERED = {"overrides": {"agent_mode": "discovery"}, "metadata": {"agent_mode_known": "discovery"}}


def _row(values: dict[str, Any]) -> SimpleNamespace:
    async def _related() -> SimpleNamespace:
        return SimpleNamespace(foreign_keys={}, inverse_foreign_keys={})

    return SimpleNamespace(**values, message_count=0, fetch_all_related=_related)


class _ConversationStore:
    """The saved row answers only a read that asks for it; every other read answers the remembered copy."""

    async def load_item(self, use_cache: bool = True, **_kwargs: Any) -> SimpleNamespace:
        return _row(REMEMBERED if use_cache else SAVED)

    async def load_by_id(self, _item_id: str) -> SimpleNamespace:
        return _row(REMEMBERED)

    async def get_conversation_with_all_related(self, _conversation_id: str):
        row = _row(REMEMBERED)
        return row, await row.fetch_all_related()


@pytest.mark.asyncio
async def test_the_turn_reads_the_saved_row() -> None:
    managers = object.__new__(CxManagers)
    managers.conversation = _ConversationStore()  # type: ignore[assignment]

    data = await managers.get_conversation_data("c0000000-0000-4000-8000-000000000001")

    assert data["conversation"].overrides == SAVED["overrides"]
    assert data["conversation"].metadata == SAVED["metadata"]
