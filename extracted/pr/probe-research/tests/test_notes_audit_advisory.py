"""The audit advisory: a line the RENDER writes into the team-note block.

WHAT THIS REPLACED. Until 2026-09-09 a SessionStart hook printed "the team note
is due for its periodic audit" onto the additionalContext channel. That hook
existed for one reason: the render runs from `team-note-sync.sh` at Stop and
SessionEnd, detached, with stdout and stderr discarded, so a timer had no other
way to reach the model. But a timer on the context channel is the wrong shape --
it spends the session's context to say something about a document already in
that context -- and the block the render writes IS read at the next session
start. So the line moved inside the block, and the hook is gone.

These cases are the hook's, ported: the same conditions, the same 24-hour floor,
the same churn guard.

TWO THINGS CHANGED ON 2026-09-16, and they pull in opposite directions.

The INTERVAL came back, for one half only: size fires the tightening half and
always did; the calendar fires the TRUTH half, which nothing else was closing --
the on-read prong corrects only claims a reader happens to hold evidence
against. The overdue sentence says NOT to tighten, so a small note never buys a
compaction it does not need.

And the line left the BLOCK. `CLAUDE.md` is read by every session of a harness,
including the ones nobody is sitting in, so the dispatch now travels on the
UserPromptSubmit hook and `session_is_automated` filters the automated
submitters. `audit_advisory` itself is unchanged in shape: it still answers
"is this due, and which half".
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json

import pytest

from pathlib import Path

from probe.cli import agent_rules, team_note_file as tnf

TODAY = dt.date(2026, 9, 3)
STAMPED = "<!-- audited 2026-08-01 -->\n## note\nbody"
#: Inside the interval, so the calendar is silent and a case can isolate size.
FRESH = "<!-- audited 2026-09-01 -->\n## note\nbody"


#: OVER BUDGET BY DEFAULT, because size is the only trigger: a content assertion
#: has nothing to assert against unless the advisory fires. Cases about WHEN it
#: fires pass `pct` explicitly.
def _advisory(document=STAMPED, *, source="claude_code", pct=0.95, baseline=None, today=TODAY):
    return tnf.audit_advisory(
        document, source=source, pct=pct, baseline=baseline, today=today
    )


def _baseline(document: str) -> dict:
    stamp = tnf.AUDIT_STAMP_RE.search(document).group(1)
    return {
        "stamp": stamp,
        "content_sha256": hashlib.sha256(document.strip().encode()).hexdigest(),
    }


# --- SIZE is the only trigger --------------------------------------------------


@pytest.mark.parametrize(
    ("pct", "fires"),
    [
        (None, False),   # no measurement: nothing to act on
        (0.10, False),
        (0.79, False),   # just under
        (0.80, True),    # the threshold
        (0.99, True),
    ],
)
def test_only_size_fires_an_audit(pct, fires: bool) -> None:
    """On a note audited two days ago, size is the only thing left to fire."""
    assert bool(_advisory(FRESH, pct=pct)) is fires


@pytest.mark.parametrize(
    "document",
    [
        "<!-- audited 2026-08-01 -->\nbody",   # 33 days old
        "<!-- audited 2020-01-01 -->\nbody",   # years old
        "## note\nno stamp at all",            # never audited
        "<!-- audited garbage -->\nbody",      # malformed
    ],
)
def test_the_calendar_fires_the_truth_half_on_a_note_that_fits(document: str) -> None:
    """THE DESIGN CALL (Richard, 2026-09-16), reversing 3055a3973: a small note
    was re-checked by nothing. The on-read prong corrects a claim only when a
    reader happens to hold the evidence against it, so the quiet claims -- the
    ones nobody is testing -- went stale unopposed.

    What the calendar must NOT do is compact: a date says nothing about length.
    """
    text = _advisory(document, pct=0.10)
    assert text, "an overdue note fires even when it fits"
    assert "Do NOT tighten" in text
    assert "still TRUE" in text and "Tighten what stays" not in text


def test_a_recently_audited_note_that_fits_says_nothing() -> None:
    assert _advisory(FRESH, pct=0.10) == ""


def test_size_wins_when_a_note_is_both_overdue_and_oversized() -> None:
    """Tightening subsumes the truth pass -- the auditor re-checks either way."""
    text = _advisory(STAMPED, pct=0.95)
    assert "outgrown its budget" in text
    assert "Tighten what stays" in text


def test_the_interval_knob_switches_the_calendar_off(monkeypatch) -> None:
    """The escape hatch for anyone who wants size-only back."""
    monkeypatch.setenv("PROBE_NOTES_AUDIT_INTERVAL_DAYS", "0")
    assert _advisory(STAMPED, pct=0.10) == ""
    assert _advisory(STAMPED, pct=0.95), "size still fires with the calendar off"


def test_neither_sentence_cites_a_section_number() -> None:
    """The method lives in a skill that has renumbered twice. A stale section
    pointer sends a background agent to the wrong rules, and nothing here can
    tell that it has."""
    for text in (_advisory(STAMPED, pct=0.95), _advisory(STAMPED, pct=0.10)):
        assert "\u00a7" not in text, text


def test_the_skill_guard_and_the_trigger_floor_agree_on_the_boundary() -> None:
    """RESTORED. `01891b5aa` added this after a real audit refused the cycle it
    was dispatched for: the trigger speaks from a note stamped YESTERDAY while
    the skill said "today's or yesterday's ... STOP", so every day a background
    agent was dispatched, read the skill, and did nothing. `3055a3973` deleted
    the test when it deleted the calendar -- "there is no longer an interval for
    the skill to disagree with". The calendar is back, and the weekly wording is
    fresh bait for the same mistake ("audited this week -> stop" would refuse at
    exactly the age the dispatcher fires).

    Globbed, because the skill directory is being renamed in a parallel change.
    """
    skills = sorted(
        p for p in (Path(__file__).resolve().parents[1] / "skills").glob("*audit*/SKILL.md")
        # `notes-audit` is a one-release rename stub (2026-09-17), not an audit skill.
        if p.parent.name != "notes-audit"
    )
    assert skills, "no audit skill on disk"
    for skill in skills:
        body = skill.read_text(encoding="utf-8")
        assert "If it is TODAY's date" in body, f"{skill}: the STOP rule must claim TODAY"
        lowered = body.lower()
        for wider in ("or yesterday", "within the week", "audited this week"):
            assert wider not in lowered, f"{skill}: guard is wider than the trigger ({wider})"

    # The trigger half, in the same place: silent at 0 days, speaking at 1.
    assert _advisory("<!-- audited 2026-09-03 -->\nbody", pct=0.99) == ""
    assert _advisory("<!-- audited 2026-09-02 -->\nbody", pct=0.99)


# --- the rate limit, which is not a schedule -----------------------------------


def test_a_note_stamped_today_is_not_asked_again_however_large() -> None:
    assert _advisory("<!-- audited 2026-09-03 -->\nbody", pct=0.99) == ""


def test_an_unchanged_note_is_not_tightened_twice() -> None:
    """It cannot have grown since the last pass, so there is nothing to find.

    Stamped inside the interval, so the truth half is not asking either.
    """
    doc = "<!-- audited 2026-09-02 -->\n## note\nbody"
    assert _advisory(doc, pct=0.95, baseline=_baseline(doc)) == ""
    assert _advisory(doc + " appended", pct=0.95, baseline=_baseline(doc))


# --- what it says ------------------------------------------------------------
def test_it_says_delete_not_strike() -> None:
    """The hook advertised the retired strike-and-expire contract for a while
    after the skill stopped teaching it, which told one agent both rules."""
    text = _advisory()
    assert "Delete what the evidence disproves." in text
    assert "strike" not in text.lower()


def test_horizon_zero_disarms_deletion(monkeypatch) -> None:
    monkeypatch.setenv("PROBE_NOTES_AUDIT_HORIZON_DAYS", "0")
    assert "Deletion is DISABLED" in _advisory()


def test_an_unreadable_knob_falls_back_rather_than_raising(monkeypatch) -> None:
    monkeypatch.setenv("PROBE_NOTES_AUDIT_HORIZON_DAYS", "not-a-number")
    assert "Delete what the evidence disproves" in _advisory()


# --- lane accuracy, which the block gets for free ----------------------------


def test_each_harness_is_told_what_it_can_actually_do() -> None:
    """The hook sniffed PROBE_AGENT for this. The render already writes one
    block per instruction file, so the source is simply in hand -- and a Codex
    block can never again inherit Claude Code's dispatch."""
    assert "BACKGROUND subagent" in _advisory(source="claude_code")
    codex = _advisory(source="codex")
    assert "YOURSELF now" in codex
    assert "BACKGROUND subagent" not in codex


# --- the churn guard ---------------------------------------------------------


# --- the block itself --------------------------------------------------------


def test_the_advisory_is_inside_the_block_hash() -> None:
    """THE TRAP. `note_block_is_current` short-circuits on the stamp, so an
    advisory outside the hash would pin the stalest possible version of the one
    sentence whose entire job is to be timely."""
    plain = agent_rules.note_source_hash("body", "/n.md")
    withit = agent_rules.note_source_hash("body", "/n.md", advisory="> due")
    assert plain != withit
    # ...and an empty advisory must hash exactly as it did before this existed,
    # or every machine re-renders once on upgrade to say nothing new.
    assert agent_rules.note_source_hash("body", "/n.md", advisory="") == plain


def test_it_rides_the_pointer_form_too() -> None:
    """A note that did not fit reaches NOBODY, which is precisely when someone
    needs to be told to audit it."""
    block = agent_rules.render_note_block(
        "body", document="/n.md", pointer_only=True, advisory="> **due for audit**"
    )
    assert "did not fit here" in block
    assert "> **due for audit**" in block


def test_no_advisory_leaves_the_block_byte_identical() -> None:
    assert agent_rules.render_note_block(
        "body", document="/n.md"
    ) == agent_rules.render_note_block("body", document="/n.md", advisory="")


def test_the_render_reads_the_previous_measurement_not_this_one(tmp_path, monkeypatch) -> None:
    """The advisory reports fullness, and writing it changes the length being
    reported. It must therefore quote the LAST render, or the number chases its
    own tail."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    health = tmp_path / "probe" / "team-note"
    health.mkdir(parents=True)
    (health / "health.json").write_text(
        json.dumps({"sources": {"claude_code": {"pct": 0.93}}}), encoding="utf-8"
    )
    payload = json.loads((health / "health.json").read_text())
    assert "93% of its render budget" in _advisory(
        pct=payload["sources"]["claude_code"]["pct"]
    )


def test_the_sentence_reads_as_a_sentence() -> None:
    """The dispatch clause used to open in lowercase after a full stop."""
    for source in ("claude_code", "codex"):
        text = _advisory(source=source)
        assert "). Run the" in text, text
        assert ". run the" not in text


