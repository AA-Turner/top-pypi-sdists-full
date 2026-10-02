"""One doctrine, three prose surfaces — anchored so the copies cannot drift.

The tracking criterion lives, at different altitudes, in the always-loaded
pointer (agent_rules.POINTER_BODY) and the track-work skill description. The
MCP server instructions carried it too until 2026-09-05, when the write
doctrine was cut from that read-only surface (see test_doctrine_sync's module
docstring for the decision). What this file guards is the criterion phrases
the pointer and the track-work skill description must keep carrying — neither
can be held to the rule by construction, only by this census.

The pointer was an f-string over `probe/doctrine.py` fragments until 2026-09-13;
it is one literal now, so this file reads it directly instead of re-rendering
placeholders.

Each surface is reduced to its OPERATIVE string before asserting — never the
whole file: a whole-file scan goes green when the anchor survives only in a
comment. Reading by PATH rather than importing keeps this honest in a
worktree, where `import probe` can resolve to another checkout's editable
install.
"""

from __future__ import annotations

import re
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]

#: The domain gate and its breadth, per carrier: the block says the work that
#: SUPPORTS ML counts; the description says ALL related work does. Rewritten
#: 2026-09-17 -- the trigger eval showed the breadth clause is what keeps the
#: frontier categories (infra, dashboards, config flips) firing.
#: Pointer 35 (2026-09-23, the `daemon` state) handed the breadth list and the
#: cadence to the `track-work` skill the block names, in the researcher's own
#: rewrite; the block keeps the domain gate and what supports it.
ANCHORS = {
    "pointer": ("ML work", "what supports them", "`track-work` skill dictates what to record"),
    "track-work": ("ML work", "ALL related work"),
}
#: v15 replaced the exclusion list with consent: recording is not curated, and
#: the researcher's toggle is the only opt-out.
CONSENT = "everything is recorded"


def _extract(pattern: str, path: str) -> str:
    text = (AGENT_ROOT / path).read_text(encoding="utf-8")
    m = re.search(pattern, text, re.DOTALL)
    assert m, f"could not extract the operative string from {path}"
    return " ".join(m.group(1).split())


def _pointer() -> str:
    return _extract(r'POINTER_BODY = """(.*?)"""', "src/probe/cli/agent_rules.py")


def _skill_description(name: str) -> str:
    return _extract(r"^description: (.+)$".replace("^", "(?m)^"), f"skills/{name}/SKILL.md")


RULE_SURFACES = {
    "pointer": _pointer,
    "track-work": lambda: _skill_description("track-work"),
}


def test_every_rule_surface_carries_both_anchors() -> None:
    missing = []
    for name, read in RULE_SURFACES.items():
        text = read()
        for anchor in ANCHORS[name]:
            if anchor not in text:
                missing.append(f"{name}: {anchor!r}")
    assert not missing, "criterion drifted on: " + "; ".join(missing)


def test_consent_replaced_the_exclusion_list_on_every_surface() -> None:
    """v15's inversion of the restraint half. The old exclusion phrases asked
    the agent to judge what deserved recording, and the measured result was a
    tenant whose agents logged prose diligently and uploaded zero files. Every
    surface must now carry consent — and none may resurrect an escape hatch."""
    # The consent sentence lives in the skill the block routes to; the block
    # must never grow an escape hatch.
    consent_surfaces = {
        "pointer": lambda: _pointer(),
        "track-work": lambda: " ".join((AGENT_ROOT / "skills/track-work/SKILL.md").read_text().split()),
    }
    assert CONSENT in consent_surfaces["track-work"](), "consent rule missing from track-work"
    for name, read in consent_surfaces.items():
        text = read()
        for escape in ("mechanical edits with no rejected alternative", "produced nothing durable"):
            assert escape not in text, f"{name} resurrected an exclusion: {escape!r}"


# -- who decides that a session is tracked -----------------------------------

_SKILLS = AGENT_ROOT / "skills"


def test_starting_is_the_agents_call_and_stopping_is_the_researchers() -> None:
    """THE ASYMMETRY IS THE DESIGN, and the merge had to keep it. Tracking
    happens because a standing rule makes STARTING automatic — the recorded
    failure is a session that read Probe perfectly and never registered a
    project. STOPPING is the researcher's.

    Pre-merge, the protection was two separate skills; post-merge it was the
    bare-TOOL-CALL rule inside one. THE SWITCH HAS NOW MOVED BACK OUT, into
    `probe`, so the asymmetry is carried by TWO descriptions and this checks
    both. track-work keeps the unprompted trigger (the recorded failure is a
    session that read Probe perfectly and never registered a project); `probe`
    keeps the stop half and the promise that an agent's own bare invocation
    never moves the state.

    Splitting them is what lets `probe` flip bare at all: the carve-out existed
    because track-work is also a manual an agent opens dozens of times a
    session, and a switch with no manual has nothing to be confused with.
    """
    desc = _skill_description("track-work")
    assert "triggered unprompted during any ML work" in desc, (
        "track-work must keep the unprompted trigger — without it, tracking "
        "only happens when someone remembers to ask"
    )

    switch = _skill_description("probe")
    assert "`off`" in switch and "`on`" in switch, (
        "the switch half must stay discoverable from the description"
    )
    # Since pointer 35 the always-loaded block carries "never move it", once.
    assert "never move it yourself" in _pointer(), (
        "an agent must be told it cannot move the state — it is what keeps the "
        "opt-out the researcher's"
    )


def test_the_hook_not_the_prose_enforces_the_bare_invocation_rule() -> None:
    """The description PROMISES a bare tool call never moves the switch; the
    guard is what makes it true. This pins the two to each other.

    BOTH live skills are excluded from the bare flip on the tool surface, and
    `probe` was nearly not. The reasoning that almost left it out -- a
    switch-only skill has no manual for an agent to open bare, so a bare
    sighting can only be a person -- misses that a skill is a TOOL the model can
    call. An agent asked what state Probe is in invokes it, and on the bare class
    that ADVANCES the cycle: from `off`, the model reading the switch's own
    documentation turns Probe back on. Only the legacy toggles keep the bare
    flip everywhere; they had no body to read.
    """
    guard = (
        AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "tracking_guard.py"
    ).read_text(encoding="utf-8")
    assert 'GUIDANCE_SLUGS = frozenset({"track-work", "probe"})' in guard
    assert '"probe"' not in guard.split("BARE_FLIP_SLUGS = frozenset(")[1].split(")")[0], (
        "the switch skill must never be in the bare-flip class: an agent's own "
        "tool call would advance the cycle and undo an `off`"
    )
    assert "def _bare_flips(slug: str, shape: str) -> bool:" in guard, (
        "the surface-aware bare rule must stay a named, documented decision "
        "rather than an inline slug check at each call site"
    )
    assert "    return slug in BARE_FLIP_SLUGS" in guard, (
        "the tool surface must grant the bare flip to the legacy slugs ONLY"
    )
    assert '"toggle-research-tracking"' in guard and '"research-tracking"' in guard, (
        "the legacy slugs must stay matched: a resumed transcript can invoke "
        "the pre-rename name against this newer hook file"
    )
