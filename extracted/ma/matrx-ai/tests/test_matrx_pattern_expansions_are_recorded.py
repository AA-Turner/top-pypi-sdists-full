"""Every <<MATRX>> expansion is model input a person can ask to see (owner law 2026-10-01).

The pattern is gone once resolved, so the expansion must be recorded where it happens:
``SystemInstruction.matrx_expansions`` (through a per-object fetch cache, so the host's receipt
capture and the wire render hold the same bytes) and ``UnifiedConfig.matrx_message_expansions``.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, TextContent, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.instructions.matrx_fetcher import MatrxFetcher
from matrx_ai.instructions.pattern_parser import expand_matrx_patterns, resolve_matrx_patterns

POLICY = "<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>pet-policy<</MATRX>>"


@pytest.fixture
def fetches(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    calls: list[str] = []
    texts = iter(["Cats allowed.", "Cats and dogs allowed."])  # the row changes between reads

    def _fetch(_cls: Any, pattern: Any) -> str:
        calls.append(pattern.value)
        return next(texts)

    monkeypatch.setattr(MatrxFetcher, "fetch_one", classmethod(_fetch))
    return calls


def test_expand_reports_each_replacement(fetches: list[str]) -> None:
    text, pairs = expand_matrx_patterns(f"Policy: {POLICY} End.")
    assert text == "Policy: Cats allowed. End."
    assert pairs == [(POLICY, "Cats allowed.")]
    assert expand_matrx_patterns("no patterns") == ("no patterns", [])


def test_a_system_instruction_renders_one_fetch_for_every_render(fetches: list[str]) -> None:
    si = SystemInstruction(base_instruction=f"Policy: {POLICY}", include_date=False)
    assert si.matrx_expansions() == [(POLICY, "Cats allowed.")]
    # The wire renders after the capture: the SAME bytes, never a second (drifted) fetch.
    assert str(si) == "Policy: Cats allowed."
    assert str(si) == "Policy: Cats allowed."
    assert fetches == ["pet-policy"]
    # The module-level resolver keeps its old behavior (no shared cache).
    assert resolve_matrx_patterns(POLICY) == "Cats and dogs allowed."


def test_a_configs_message_expansions_are_recorded(fetches: list[str]) -> None:
    message = UnifiedMessage(role=Role.USER, content=[TextContent(text=f"Dog ok? {POLICY}")])
    config = UnifiedConfig(model="test-model", messages=MessageList(_messages=[message]), tools=[])
    assert message.content[0].text == "Dog ok? Cats allowed."
    assert config.matrx_message_expansions == [(POLICY, "Cats allowed.")]
