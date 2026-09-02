"""Regression: the system instruction must survive an unlimited number of
persist↔reload cycles WITHOUT accumulating auto-injected decorations.

The bug: ``UnifiedConfig.to_storage_dict`` persisted the RESOLVED system text
(``str(SystemInstruction)`` — date/tools/guidelines/context baked in) into
``cx_conversation.system_instruction``. On every DB reload (server restart,
cache eviction, delegation ``/resume``) that rendered string was re-ingested as
``base_instruction`` with ``include_date=True``, so the renderer prepended the
date AGAIN — one extra ``Current date: …`` line per cycle. A long, error-prone
conversation that reloaded N times showed N dates.

The fix is two-layered and both layers are asserted here:
  1. ``to_storage_text()`` freezes one fully rendered prompt, with one marked date.
  2. ``from_value(str)`` strips the marked ``Current date: …`` block on ingest,
     self-healing any already-rendered string fed back in.
"""

from __future__ import annotations


def test_persist_reload_never_accumulates_date():
    from matrx_ai.instructions.core import SystemInstruction

    si = SystemInstruction(base_instruction="You are a professional assistant.")
    for turn in range(10):
        wire = str(si)  # what the provider sees
        stored = si.to_storage_text()  # what we persist (cx_conversation column)
        si = SystemInstruction.from_value(stored)  # reload from DB next turn

        assert wire.count("Current date:") == 1, (
            f"turn {turn}: wire carried {wire.count('Current date:')} dates"
        )
        assert stored.count("Current date:") == 1, (
            f"turn {turn}: stored text carried {stored.count('Current date:')} dates"
        )
        assert "You are a professional assistant." in wire


def test_from_value_self_heals_already_rendered_string():
    from matrx_ai.instructions.core import DATE_BLOCK_OPEN, SystemInstruction

    corrupted = (
        "Current date: 2026-06-15\n\n"
        "Current date: 2026-06-15\n\n"
        "Current date: 2026-06-15\n\n"
        "<available_skills>\n\nYou are a professional assistant."
    )
    out = str(SystemInstruction.from_value(corrupted))
    assert out.count("Current date:") == 1
    # The single surviving date is the freshly-rendered, sentinel-wrapped block.
    assert out.startswith(DATE_BLOCK_OPEN)
    assert "<available_skills>" in out
    assert "You are a professional assistant." in out


def test_sentinel_marked_date_never_doubles_even_with_an_intro():
    """The old leading-only strip failed when an intro pushed the date off the
    front. The sentinel is stripped ANYWHERE, so re-ingest never doubles it."""
    from matrx_ai.instructions.core import SystemInstruction

    si = SystemInstruction(base_instruction="Base directive.", intro="Intro line.")
    # Feed a fully-rendered string (date is NOT leading — it sits after intro)
    # straight back in as base_instruction, many times.
    for _ in range(5):
        rendered = str(si)
        assert rendered.count("Current date:") == 1
        si = SystemInstruction(base_instruction=rendered, intro="Intro line.")
    assert str(si).count("Current date:") == 1


def test_strip_helper_is_a_noop_on_clean_text():
    from matrx_ai.instructions.core import strip_date_decorations, strip_leading_date_decorations

    clean = "You are a helpful assistant.\n\nCurrent date: discussed below."
    # A bare "Current date:" mid-text (not our sentinel block) is author content
    # and must be preserved.
    assert strip_date_decorations(clean) == clean
    assert strip_date_decorations("") == ""
    # Back-compat alias routes through the same robust strip.
    assert strip_leading_date_decorations is strip_date_decorations


def test_date_anchor_pins_value_and_survives_midnight():
    """An explicit anchor is used verbatim and never recomputed, so the
    system prefix is byte-identical no matter when it renders."""
    from matrx_ai.instructions.core import SystemInstruction

    si = SystemInstruction(base_instruction="Base.", date_anchor="2026-01-01")
    first = str(si)
    assert "Current date: 2026-01-01" in first
    # Byte-stable across repeated renders (the caching contract).
    assert str(si) == first
    assert si.effective_date() == "2026-01-01"


def test_no_anchor_memoizes_now_once():
    """Without an anchor the date is computed once and reused — a single live
    object never drifts, even if renders straddle a midnight boundary."""
    from matrx_ai.instructions.core import SystemInstruction

    si = SystemInstruction(base_instruction="Base.")
    pinned = si.effective_date()
    assert si.effective_date() == pinned
    assert str(si) == str(si)


def test_to_storage_text_freezes_authored_sections_and_resolved_decorations():
    from matrx_ai.instructions.core import SystemInstruction

    si = SystemInstruction(
        base_instruction="Base directive.",
        intro="Intro line.",
        outro="Outro line.",
        include_date=True,
        include_code_guidelines=True,
        tools_list=["search", "fetch"],
    )
    stored = si.to_storage_text()
    assert "Intro line." in stored and "Base directive." in stored and "Outro line." in stored
    assert stored.count("Current date:") == 1
    assert "Tools/Functions Available" in stored
    assert "Code Guidelines" in stored
    assert stored == str(si)
