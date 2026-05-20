"""Regression: specialist math/science tools must be hidden from API
tools[] on Gemma 4 when the user's first prompt isn't math-flavored.

Saves ~6.5K tokens per request on typical coding sessions while still
exposing the full toolset when the prompt looks mathy (same gate as
_maybe_inject_math_docs).
"""
from __future__ import annotations

from unittest.mock import MagicMock

from drydock.core.agent_loop import AgentLoop


def _make_loop():
    loop = AgentLoop.__new__(AgentLoop)
    loop._math_docs_injected = False
    return loop


def _make_tool(name: str):
    t = MagicMock()
    t.function = MagicMock()
    t.function.name = name
    return t


def _all_tools():
    # mix coding + math/science
    names = [
        "read_file", "write_file", "bash", "grep",
        "logic", "algebra", "number_theory", "solve", "prolog",
        "math", "count", "memory", "verify",
    ]
    return [_make_tool(n) for n in names]


def test_gemma_non_mathy_hides_specialists():
    loop = _make_loop()
    model = MagicMock()
    model.name = "gemma4"
    out = loop._hide_specialist_math_tools(_all_tools(), model)
    names = {t.function.name for t in out}
    # Specialists gone
    assert "logic" not in names
    assert "algebra" not in names
    assert "solve" not in names
    assert "prolog" not in names
    # Coding tools stay
    assert "read_file" in names
    assert "bash" in names
    # General-purpose tools stay
    assert "math" in names
    assert "memory" in names


def test_math_injected_keeps_specialists():
    loop = _make_loop()
    loop._math_docs_injected = True  # mathy prompt — math docs were injected
    model = MagicMock()
    model.name = "gemma4"
    out = loop._hide_specialist_math_tools(_all_tools(), model)
    names = {t.function.name for t in out}
    # Specialists stay
    assert "logic" in names
    assert "solve" in names
    assert "prolog" in names


def test_non_gemma_model_keeps_specialists():
    loop = _make_loop()
    model = MagicMock()
    model.name = "devstral-small-latest"
    out = loop._hide_specialist_math_tools(_all_tools(), model)
    names = {t.function.name for t in out}
    # Non-Gemma: pass through unchanged
    assert "logic" in names
    assert "algebra" in names


def test_no_model_passes_through():
    loop = _make_loop()
    out = loop._hide_specialist_math_tools(_all_tools(), None)
    names = {t.function.name for t in out}
    assert "logic" in names


def test_specialist_set_matches_expected():
    """The 10 specialists are exactly the tools that lived in
    gemma4_math.md before the lazy-injection split."""
    expected = {
        "logic", "algebra", "number_theory", "set", "linear_algebra",
        "stats", "units", "chemistry", "solve", "prolog",
    }
    assert AgentLoop._SPECIALIST_MATH_TOOLS == expected
