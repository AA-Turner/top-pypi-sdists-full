"""`agent_source()` distinguishes "nothing was asked" from "asked and misspelled".

The pi integration produced roughly twenty silent bugs from one shape: agent
logic written as `if source == "codex": ... else: <claude_code>`, where the
else arm quietly meant "everything that is not codex". Four of those reached
into Claude Code's own files and two were destructive -- one wizard path could
uninstall the Probe block from a researcher's real CLAUDE.md, another ran
`claude plugin update` against their real install as a side effect of updating
pi.

An audit made ~44 of those branches explicitly handle all three sources. That
only holds if the value reaching them is trustworthy, which is this
normalizer's job: an unrecognized PROBE_AGENT must NOT be laundered into
claude_code, or harness #4 impersonates Claude Code exactly as pi did.

The live-capture daemon's normalizer sits on the opposite side of the same
seam on purpose -- see tap/config.py::capture_source(). Do not unify them.
"""

from __future__ import annotations

import pytest

from probe.cli.capabilities import UnrecognizedAgentSourceWarning, agent_source

ENV = "PROBE_AGENT"


def test_unset_is_claude_code(monkeypatch: pytest.MonkeyPatch) -> None:
    """Load-bearing: every install that never sets PROBE_AGENT depends on it."""
    monkeypatch.delenv(ENV, raising=False)
    assert agent_source() == "claude_code"


def test_whitespace_only_counts_as_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV, "   ")
    assert agent_source() == "claude_code"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("claude", "claude_code"),
        ("claude_code", "claude_code"),
        ("CLAUDE_CODE", "claude_code"),
        ("codex", "codex"),
        ("Codex", "codex"),
        ("pi", "pi"),
        ("PI", "pi"),
    ],
)
def test_recognized_values_resolve(
    monkeypatch: pytest.MonkeyPatch, value: str, expected: str
) -> None:
    monkeypatch.setenv(ENV, value)
    assert agent_source() == expected


def test_an_unrecognized_value_warns_loudly_and_falls_back_to_claude_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A typo stays DISCOVERABLE (the warning) without breaking the machine
    on upgrade (the fallback) -- Mahit's call, 2026-08-28. A silent default
    was the old bug class; a hard raise was the regression risk."""
    monkeypatch.setenv(ENV, "pi2")
    with pytest.warns(UnrecognizedAgentSourceWarning):
        assert agent_source() == "claude_code"


def test_the_warning_names_the_offending_value_and_the_accepted_ones(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A loud warning that does not say what was wrong is barely louder."""
    monkeypatch.setenv(ENV, "claude-code")  # hyphen, a plausible typo
    with pytest.warns(UnrecognizedAgentSourceWarning) as caught:
        assert agent_source() == "claude_code"
    message = str(caught[0].message)
    assert "claude-code" in message
    for accepted in ("claude", "codex", "pi"):
        assert accepted in message
    assert "claude_code" in message  # says what it fell back to


def test_a_future_harness_warns_instead_of_silently_impersonating_claude_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Harness #4 is the case this exists for; pi is what taught us. It must
    surface -- as a warning -- while the machine keeps working."""
    monkeypatch.setenv(ENV, "some-future-harness")
    with pytest.warns(UnrecognizedAgentSourceWarning):
        assert agent_source() == "claude_code"
