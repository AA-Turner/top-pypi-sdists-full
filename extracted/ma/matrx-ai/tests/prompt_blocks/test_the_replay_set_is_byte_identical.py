"""P1a referee: every extraction keeps the outbound request BYTE-IDENTICAL on the fixed replay set.

The golden file was written from the code BEFORE any producer was extracted. A producer that moves
one byte on any wire shape × turn phase × block variant fails here, naming the case. Regenerate the
golden ONLY for a change meant to move bytes (P1b+), with ``PROMPT_BLOCKS_REGEN_GOLDEN=1``.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "prompt_blocks_replay_set", Path(__file__).with_name("replay_set.py")
)
assert _spec and _spec.loader
replay_set = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = replay_set
_spec.loader.exec_module(replay_set)

GOLDEN = Path(__file__).with_name("golden") / "replay_set.json"


def _load() -> dict[str, dict[str, str]]:
    return json.loads(GOLDEN.read_text()) if GOLDEN.exists() else {}


@pytest.mark.asyncio
@pytest.mark.parametrize(("shape", "phase", "variant"), replay_set.cases())
async def test_the_outbound_bytes_match_the_golden(shape: str, phase: str, variant: str) -> None:
    raw = await replay_set.build(shape, phase, variant)
    key = replay_set.key(shape, phase, variant)
    if os.environ.get("PROMPT_BLOCKS_REGEN_GOLDEN") == "1":
        golden = _load()
        golden[key] = {"sha256": replay_set.digest(raw), "bytes": raw.decode("utf-8")}
        GOLDEN.parent.mkdir(exist_ok=True)
        GOLDEN.write_text(
            json.dumps(dict(sorted(golden.items())), indent=1, ensure_ascii=False) + "\n"
        )
        return
    expected = _load().get(key)
    assert expected is not None, (
        f"no golden for {key}: the replay set grew without a recorded baseline"
    )
    assert raw.decode("utf-8") == expected["bytes"], f"{key}: the outbound request moved"


@pytest.mark.asyncio
async def test_the_replay_set_is_deterministic() -> None:
    """Two builds of the same case are identical — the referee is not itself noisy."""
    for shape, phase, variant in replay_set.cases():
        assert await replay_set.build(shape, phase, variant) == await replay_set.build(
            shape, phase, variant
        )


@pytest.mark.asyncio
async def test_the_every_block_variant_carries_every_matrx_ai_block() -> None:
    """The fixture really exercises the blocks it claims to (a golden of nothing proves nothing)."""
    text = (await replay_set.build("anthropic", "t1", "every_block")).decode("utf-8")
    for marker in (
        "Current date: 2026-11-13",
        "## Available Kind Directives",
        "<available_skills>",
        "<org_catalog>",
        "knowledge store",
        "under 18",
        "<memory>",
        "<opening_turn",
        "Answer in French.",
        "<live_date>",
    ):
        assert marker in text, marker
