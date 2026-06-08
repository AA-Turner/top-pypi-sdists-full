"""Regression: gemma4_math.md must inject only for mathy prompts and
only once per session.
"""
from __future__ import annotations

from unittest.mock import MagicMock


def _make_loop():
    """Build a minimal AgentLoop-like object with just enough state
    for _maybe_inject_math_docs to run. We don't construct a real
    AgentLoop because it pulls in the full config/middleware/tools
    stack — slow + brittle."""
    from drydock.core.agent_loop import AgentLoop
    loop = AgentLoop.__new__(AgentLoop)
    loop._math_docs_injected = False
    loop.messages = []
    # config is a property → mock the agent_manager whose .config attr
    # the property returns.
    cfg = MagicMock()
    cfg.get_active_model.return_value.name = "gemma4"
    am = MagicMock()
    am.config = cfg
    loop.agent_manager = am
    # Provide a no-op _inject_system_note that records calls
    loop._injected = []

    def _record(text, replace_last_tool=False):
        loop._injected.append(text)
    loop._inject_system_note = _record
    return loop


def test_mathy_prompt_injects():
    loop = _make_loop()
    loop._maybe_inject_math_docs("prove that 1+1=2 is a tautology")
    assert loop._math_docs_injected is True
    assert len(loop._injected) == 1
    assert "math/science" in loop._injected[0]


def test_non_mathy_prompt_skips():
    loop = _make_loop()
    loop._maybe_inject_math_docs(
        "review the PRD and finish the slide deck generator"
    )
    assert loop._math_docs_injected is False
    assert loop._injected == []


def test_only_once_per_session():
    loop = _make_loop()
    loop._maybe_inject_math_docs("solve x^2 = 4 for x")
    loop._maybe_inject_math_docs("what is the determinant of [[1,2],[3,4]]")
    assert loop._math_docs_injected is True
    assert len(loop._injected) == 1


def test_non_gemma_model_skips():
    loop = _make_loop()
    loop.config.get_active_model.return_value.name = "devstral-small-latest"
    loop._maybe_inject_math_docs("prove x is prime")
    assert loop._math_docs_injected is False
    assert loop._injected == []


def test_keyword_coverage_mathy_words():
    """A handful of representative math/science/logic phrases should
    all trip the injector."""
    samples = [
        "compute the factorial of 20",
        "is 1000003 a prime",
        "find x such that x^2 + 1 = 0",
        "what is the molar mass of H2O",
        "prove that not (A and B) is equivalent to (not A) or (not B)",
        "calculate the p-value for a one-sided z-test",
        "find all integers where 3x mod 7 == 5",
        "show that the integral of sin(x) is -cos(x) + C",
    ]
    for s in samples:
        loop = _make_loop()
        loop._maybe_inject_math_docs(s)
        assert loop._math_docs_injected is True, f"missed: {s!r}"


def test_keyword_coverage_coding_words():
    """Pure-coding phrases must NOT trigger the math injection."""
    samples = [
        "refactor the User class to use dataclasses",
        "add a --verbose flag to the CLI",
        "write a unit test for the score-tracking logic",
        "fix the ModuleNotFoundError on import",
        "the regex pattern isn't matching the input file",
        "deploy the build to staging via the CI pipeline",
    ]
    for s in samples:
        loop = _make_loop()
        loop._maybe_inject_math_docs(s)
        assert loop._math_docs_injected is False, f"false positive: {s!r}"
