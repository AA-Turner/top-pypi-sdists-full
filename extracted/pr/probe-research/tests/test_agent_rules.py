"""The CLAUDE.md pointer block writes into a file the researcher owns.

Every test here is about not damaging that file. The block is worth writing only
because `CLAUDE.md` is always in context; the rules a researcher wrote for
themselves are the reason the file matters, and clobbering them would be a worse
outcome than never having written anything.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from probe.cli import agent_rules

#: The agent tree, for the prose surfaces the block now routes to.
_AGENT_TREE = Path(__file__).resolve().parents[1]


def _hook_constant(module: str, name: str) -> str:
    """A hook module's string constant, read from SOURCE via ast -- never the
    whole file (a phrase surviving only in a comment must not pass), and never
    an import (the hook modules read env and state at import time)."""
    import ast

    path = _AGENT_TREE / "plugins" / "probe-research" / "hooks" / f"{module}.py"
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            assert isinstance(node.value, ast.Constant), name
            return node.value.value
    raise AssertionError(f"{module}.{name} not found")

_USER_TEXT = """# My rules

## Highest priority: worktree only

- Never write in a Git repo's primary checkout or on `main`/`master`.
"""


@pytest.fixture()
def memory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    return tmp_path / "CLAUDE.md"


def test_claude_config_dir_moves_the_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A researcher who moved their config dir must not get a second, dead file.

    Writing to a hardcoded ~/.claude there produces a CLAUDE.md Claude Code
    never reads, and the wizard would report success over a file with no effect.
    """
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "elsewhere"))
    assert agent_rules.memory_path() == tmp_path / "elsewhere" / "CLAUDE.md"

    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    assert agent_rules.memory_path() == Path.home() / ".claude" / "CLAUDE.md"


def test_codex_home_uses_the_global_agents_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex does not read Claude's global CLAUDE.md."""
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    assert agent_rules.memory_path("codex") == tmp_path / "codex-home" / "AGENTS.md"

    monkeypatch.delenv("CODEX_HOME")
    assert agent_rules.memory_path("codex") == Path.home() / ".codex" / "AGENTS.md"


def test_pi_coding_agent_dir_uses_the_global_agents_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pi reads neither Claude's CLAUDE.md nor Codex's AGENTS.md location.

    `PI_CODING_AGENT_DIR` is not a guess -- it is pi 0.86.0's (and 0.84.3's) own
    `dist/config.js`: `ENV_AGENT_DIR` is derived as
    `${APP_NAME.toUpperCase()}_CODING_AGENT_DIR` (`APP_NAME` is `"pi"` absent
    a white-label `piConfig.name`, which the installed package does not set),
    and `getAgentDir()` -- read by every pi entry point, including the one
    that resolves the global `AGENTS.md`/`AGENTS.override.md` -- returns it
    verbatim when set.

    UNLIKE `CODEX_HOME`, the override names the agent directory itself, not a
    parent `CODEX_HOME`-style directory Codex appends `AGENTS.md` onto -- so
    nothing is appended here either; this is the one place that detail could
    silently regress.
    """
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent-dir"))
    assert agent_rules.memory_path("pi") == tmp_path / "pi-agent-dir" / "AGENTS.md"

    monkeypatch.delenv("PI_CODING_AGENT_DIR")
    assert agent_rules.memory_path("pi") == Path.home() / ".pi" / "agent" / "AGENTS.md"


def test_pi_is_reached_through_probe_agent_env_like_the_other_two(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The implicit selection path (no explicit `source` argument) also picks
    up pi -- this is how `probe notes sync`, invoked with `PROBE_AGENT=pi` by
    the pi extension's detached sync (never with an explicit --agent flag),
    actually resolves the right file."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent-dir"))
    assert agent_rules.memory_path() == tmp_path / "pi-agent-dir" / "AGENTS.md"


def test_pi_does_not_disturb_the_existing_codex_and_claude_branches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Adding the pi branch must not have touched the other two. An
    unrecognized/absent source still falls back to claude_code, exactly as
    before pi existed."""
    for key in ("PROBE_AGENT", "CLAUDE_CONFIG_DIR", "CODEX_HOME", "PI_CODING_AGENT_DIR"):
        monkeypatch.delenv(key, raising=False)

    assert agent_rules.memory_path() == Path.home() / ".claude" / "CLAUDE.md"
    assert agent_rules.memory_path("codex") == Path.home() / ".codex" / "AGENTS.md"
    assert agent_rules.memory_path("bogus") == Path.home() / ".claude" / "CLAUDE.md"

    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude-cfg"))
    assert agent_rules.memory_path("claude_code") == tmp_path / "claude-cfg" / "CLAUDE.md"


def test_codex_wizard_writes_agents_md_not_claude_md(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from probe.cli import setup as wizard

    monkeypatch.setenv("PROBE_AGENT", "codex")
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude-home"))

    messages = wizard.apply_agent_rules(True)

    assert messages
    assert (tmp_path / "codex-home" / "AGENTS.md").exists()
    assert not (tmp_path / "claude-home" / "CLAUDE.md").exists()


def test_install_creates_the_file_and_its_parent(memory: Path) -> None:
    assert not memory.exists()
    assert agent_rules.install(memory) is True
    assert agent_rules.is_installed(memory)
    assert agent_rules.is_current(memory)
    # Assert the heading, not a skill name: the block names `track-work` and
    # `instrument-code` since 2026-09-17, but a rename there is a POINTER_VERSION
    # bump, not a reason for this install test to move.
    assert "## Probe Research" in memory.read_text()


def test_install_preserves_existing_content_byte_for_byte(memory: Path) -> None:
    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_text(_USER_TEXT)

    agent_rules.install(memory)
    after = memory.read_text()

    assert after.startswith(_USER_TEXT)
    assert agent_rules.BEGIN_MARKER in after


def test_install_is_idempotent(memory: Path) -> None:
    """A second wizard run must not append a second block.

    Re-running the wizard is normal -- it is how a capability gets turned on
    later -- so an append-only install would stack blocks until the file is
    mostly ours.
    """
    agent_rules.install(memory)
    first = memory.read_text()

    assert agent_rules.install(memory) is False
    assert memory.read_text() == first
    assert first.count(agent_rules.BEGIN_MARKER) == 1


def test_a_stale_block_is_rewritten_in_place(memory: Path) -> None:
    """The wording is versioned, and this file is unreachable by a release.

    A machine that ticked the row once and never re-ran the wizard is the only
    place an outdated block can live, so the refresh has to replace rather than
    append -- and must not disturb what surrounds it.
    """
    memory.parent.mkdir(parents=True, exist_ok=True)
    old = agent_rules.render_block(version=agent_rules.POINTER_VERSION - 1)
    memory.write_text(f"{_USER_TEXT}\n{old}\n## After\n\nmine\n")

    assert agent_rules.installed_version(memory) == agent_rules.POINTER_VERSION - 1
    assert agent_rules.is_installed(memory) and not agent_rules.is_current(memory)

    assert agent_rules.install(memory) is True
    after = memory.read_text()

    assert after.count(agent_rules.BEGIN_MARKER) == 1
    assert agent_rules.is_current(memory)
    assert after.startswith(_USER_TEXT)
    assert "## After" in after and "mine" in after


def test_remove_takes_only_the_block(memory: Path) -> None:
    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_text(_USER_TEXT)
    agent_rules.install(memory)

    assert agent_rules.remove(memory) is True
    after = memory.read_text()

    assert agent_rules.BEGIN_MARKER not in after
    assert "Never write in a Git repo's primary checkout" in after
    assert agent_rules.remove(memory) is False


def test_remove_leaves_a_file_we_created_empty_rather_than_deleting_it(memory: Path) -> None:
    """Unticking a row is not permission to unlink a file in the user's home."""
    agent_rules.install(memory)
    agent_rules.remove(memory)

    assert memory.exists()
    assert memory.read_text() == ""


def test_an_opening_marker_with_no_close_is_refused_not_nested(memory: Path) -> None:
    """Hand-deleting the end marker must not produce a block inside a block.

    Treating a half-open block as absent and appending would leave the file with
    an unterminated marker wrapping our new one, and every later read would then
    span both.
    """
    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_text(f"{_USER_TEXT}\n{agent_rules.BEGIN_MARKER}\nhalf a block\n")

    # PRESENT-and-unusable, not absent: absent is what made the caller append.
    assert agent_rules.installed_version(memory) == 0
    with pytest.raises(agent_rules.DamagedBlock):
        agent_rules.install(memory)

    assert memory.read_text() == f"{_USER_TEXT}\n{agent_rules.BEGIN_MARKER}\nhalf a block\n"


def test_a_stray_marker_never_eats_the_researchers_own_rules(memory: Path) -> None:
    """The one that got away.

    An orphan BEGIN made `install` append (None read as "absent"), leaving TWO
    opens and one close. The NEXT run then spanned from the orphan open to our
    real close and rewrote everything between -- the researcher's own rules,
    gone, while the wizard printed "Refreshed the Probe block". Two ordinary
    runs, no warning, no backup.

    A researcher can get a stray marker just by pasting the PR that introduced
    it: #153's body quotes the marker in a fenced block.
    """
    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_text(f"{agent_rules.BEGIN_MARKER}\n\n{_USER_TEXT}")

    for _ in range(2):
        with pytest.raises(agent_rules.DamagedBlock):
            agent_rules.install(memory)

    assert "Never write in a Git repo's primary checkout" in memory.read_text()


def test_a_second_complete_block_is_damage_not_a_target(memory: Path) -> None:
    """Two full pairs: rewriting either one is a guess about which is ours."""
    memory.parent.mkdir(parents=True, exist_ok=True)
    agent_rules.install(memory)
    memory.write_text(memory.read_text() + _USER_TEXT + agent_rules.render_block())

    with pytest.raises(agent_rules.DamagedBlock):
        agent_rules.install(memory)
    with pytest.raises(agent_rules.DamagedBlock):
        agent_rules.remove(memory)
    assert "Never write in a Git repo's primary checkout" in memory.read_text()


def test_a_file_we_cannot_decode_is_reported_not_raised(memory: Path) -> None:
    """One latin-1 character in a researcher's own CLAUDE.md used to take the
    whole wizard down with a traceback, mid-install: UnicodeDecodeError is a
    ValueError, so the `except OSError` around the call never saw it."""
    from probe.cli import setup as wizard

    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_bytes("# Caf\xe9 rules\n".encode("latin-1"))

    with pytest.raises(UnicodeDecodeError):
        agent_rules.install(memory)

    messages = wizard.apply_agent_rules(True)
    assert messages and "Could not update" in messages[0]
    assert memory.read_bytes() == "# Caf\xe9 rules\n".encode("latin-1")


def test_removal_reports_a_file_it_could_not_read(memory: Path) -> None:
    """Swallowing the read error rendered as silence: the researcher unticked
    the row, saw nothing printed, and the rule kept firing every session."""
    from probe.cli import setup as wizard

    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_bytes("caf\xe9\n".encode("latin-1"))

    messages = wizard.apply_agent_rules(False)
    assert messages and "Could not update" in messages[0]


def test_the_write_is_atomic(memory: Path) -> None:
    """A truncate-then-write on the user's global memory file leaves it in
    pieces if the process dies mid-write -- and a truncated file is exactly the
    stray-marker state that costs the researcher their rules."""
    import inspect

    source = inspect.getsource(agent_rules)
    assert "write_text_atomic" in source
    assert ".write_text(" not in source, "every write to CLAUDE.md must be atomic"


def test_a_block_with_an_unparseable_version_is_present_not_absent(memory: Path) -> None:
    """Version 0, never None -- None would make the caller append a duplicate."""
    memory.parent.mkdir(parents=True, exist_ok=True)
    memory.write_text(
        f"{agent_rules.BEGIN_MARKER}\n<!-- vBOGUS -->\nbody\n{agent_rules.END_MARKER}\n"
    )

    assert agent_rules.installed_version(memory) == 0
    assert agent_rules.is_installed(memory)
    assert not agent_rules.is_current(memory)

    agent_rules.install(memory)
    assert memory.read_text().count(agent_rules.BEGIN_MARKER) == 1


def test_the_rule_is_conditional_on_the_work_being_the_teams_ml_work() -> None:
    """This file is user-global, so it loads while fixing an unrelated CSS bug.

    An unconditional "register a project before you start" in that position
    teaches the agent that the block does not apply to it, which costs the
    block its authority everywhere including the sessions it was written for.
    The 2026-09-17 rewrite keeps the DOMAIN gate (ML work) and names the work
    that SUPPORTS it -- the frontier categories the trigger eval showed dropping
    to 0% when only the core shapes were listed -- and keeps the cadence rule.
    """
    body = " ".join(agent_rules.POINTER_BODY.split())
    assert "ML work" in body
    assert "and what supports them" in body
    # 35: WHAT to record (the shapes, the cadence, the tie-break) moved to the
    # `track-work` skill the block names; the block keeps the domain gate.
    assert "The `track-work` skill dictates what to record" in body
    assert "Do not call Probe for" in body, "the restraint half must stay explicit"


def test_the_rule_requires_prior_knowledge_search_before_design() -> None:
    """The global file is the only instruction loaded before skill selection.

    The standing rule must make the read step explicit while leaving tool
    procedure to the MCP sheet (which carries the ladder since 2026-09-17:
    local context, then `browse`, then `search_knowledge`, then `entity`).
    The one clause that must stay HERE is the unavailable-surface rule: an
    agent with no MCP must say so, not proceed as if no prior work exists.
    """
    body = " ".join(agent_rules.POINTER_BODY.split())
    assert "Before proposing any new ML work" in body
    assert "check the team's prior work" in body
    assert "Follow MCP instructions" in body
    assert "If the MCP is unavailable, say so" in body
    from probe.mcp import server

    sheet = " ".join(server.MCP_INSTRUCTIONS.split())
    assert "HOW TO READ (in order)" in sheet
    assert sheet.index("local context") < sheet.index("`browse`") < sheet.index("`search_knowledge`")


def test_the_rule_distinguishes_visible_summary_from_hidden_notes() -> None:
    """The authored Markdown below AI Summary is the RESEARCHER's by policy
    since 2026-09-17 (`probe <kind> set --summary` still exists; agents are
    told not to use it). The always-loaded block must therefore not teach a
    summary write, and the skill that routes prose must say who owns that
    document and where agent prose goes instead."""
    body = " ".join(agent_rules.POINTER_BODY.split())
    assert "--summary" not in body
    assert "summary_markdown" not in body and "document" not in body
    skill = " ".join((_AGENT_TREE / "skills" / "track-work" / "SKILL.md").read_text().split())
    assert "the RESEARCHER's - never write it" in skill
    assert "hidden prose" in skill
    assert "`edit-notes`" in skill


def test_the_block_names_only_the_doctrine_skills_and_nothing_that_can_rot() -> None:
    """Procedures rot, and this copy is unreachable by a release. Until
    2026-09-17 the block therefore named NO skill: v11 blocks in the field name
    `probe-research:toggle-research-tracking` and two other slugs no plugin
    ships, and an agent handed a name it cannot invoke goes looking on the
    filesystem (281 shell reads of SKILL.md from Codex in 30 days).

    The rewrite names the two skills that carry the write doctrine and the
    switch, BARE, because the trigger eval showed an agent told only "use a
    skill" improvising CLI calls instead. The bargain: those three names are
    the whole allow-list, a rename of any of them is a POINTER_VERSION bump,
    and the block still names no namespaced id and no command that can rot.
    """
    body = agent_rules.POINTER_BODY
    assert re.findall(r"probe-research:[a-z-]+", body) == [], "namespaced ids rot"
    named = {m for m in re.findall(r"`([a-z][a-z-]*)`", body) if "-" in m or m == "probe"}
    # `probe-research` is the PyPI package the SDK line names, not a skill.
    assert named <= {"track-work", "instrument-code", "probe", "probe-research"}, named
    for rotted in ("probe note add", "--kind ", "--supersedes", "probe notes write", "notes append", "--hypothesis"):
        assert rotted not in body, f"block names a command that can rot: {rotted}"
    for removed in (
        "start-research-work", "track-research-work", "toggle-research-tracking",
        "research-tracking", "instrument-training-runs", "show-research-status",
        "notes-audit", "pull-rules",
    ):
        assert removed not in body, f"block names a removed skill: {removed}"


def test_the_block_does_not_gate_reading_on_tracking_state() -> None:
    """D10, as it survives the third state. `read` stops WRITES only.

    Connor Lee objected twice that his agent kept reaching for Probe after he
    had switched tracking off, and the agent was reading the block correctly:
    "this whole block is off" was immediately glossed by two write-only
    examples, so an agent concluded the read mandate survived. Say which half
    the switch governs, in the same breath.

    Since 2026-09-17 the block names the three states and hands the rest to
    the `probe` skill and the session-start hook, which are pinned here as the
    carriers of "reads survive `read`".
    """
    body = " ".join(agent_rules.POINTER_BODY.split())
    assert "(on / daemon / read / off)" in body
    assert "Reading is NOT part of that switch" not in body
    assert "tracking state never gates it" not in body
    skill = (_AGENT_TREE / "skills" / "probe" / "SKILL.md").read_text()
    assert "Keep searching" in skill
    assert "read commands like `session status`) are fine" in _hook_constant("version_check", "TRACKING_OFF_CONTEXT")


def test_the_block_says_what_off_costs_and_forbids_claiming_absence() -> None:
    """`off` gates reads, so somebody owes the agent the consequence.

    An agent that cannot search does not experience an empty result differently
    from a genuine absence -- both look like "nothing found". Left unsaid, the
    honest failure mode of `off` is an agent confidently reporting that no prior
    work exists. Since 2026-09-17 the carriers are the two `off` hook strings
    (session start, and the per-call refusal) and the `probe` skill; the
    behaviour eval dropped from 100% to 0% on the off-state history question
    when these sentences were cut, and back to 80% when restored.
    """
    off = _hook_constant("version_check", "TRACKING_FULLY_OFF_CONTEXT")
    # The refusal moved to `_session_marker` so the CLI's own write gate and the
    # hook print the same words; tracking_guard re-exports it.
    deny = _hook_constant("_session_marker", "DENY_REASON_OFF")
    assert "make no Probe calls at all" in off
    assert "say you could not look" in off
    assert "never report that none exists" in off
    assert "say you could not look" in deny
    assert "cannot know what you missed" in deny
    assert "does not backfill" in deny
    assert "do not route around it" in deny
    skill = (_AGENT_TREE / "skills" / "probe" / "SKILL.md").read_text()
    assert "never backfills anything" in skill
    assert "never report that no prior work exists" in skill


def test_tracking_on_means_everything_with_no_judgment_escape() -> None:
    """v15 removed the skip list. The failure it fixes was measured, not
    imagined: a tenant's agents wrote 140k characters of notes and uploaded
    ZERO files, because the block enumerated four prose categories and the
    agent -- correctly -- logged exactly what it was told to. Any judgment
    escape hatch ("skip mechanical edits") becomes the reason a category of
    work is missing; the researcher's toggle is the only opt-out.

    The block keeps the tie-break ("it does") and the switch ownership; the
    consent sentence itself lives in the track-work skill it governs.
    """
    body = " ".join(agent_rules.POINTER_BODY.split())
    for escape in ("Skip only", "mechanical edits", "nothing durable", "version bumps"):
        assert escape not in body, f"a judgment escape survived: {escape}"
    assert "the researcher's: never move it yourself" in body
    skill = " ".join((_AGENT_TREE / "skills" / "track-work" / "SKILL.md").read_text().split())
    assert "Tracking on means everything is recorded; do not curate" in skill


def test_files_are_routed_with_safety_lineage_and_a_catch_all() -> None:
    """The four rules the Anthrogen investigation produced, each load-bearing:
    files have a destination at all (the original gap), secrets stay off the
    platform, provenance survives cross-anchor uploads, and nothing falls on
    the floor for want of a matching row. They moved from the block into the
    track-work skill on 2026-09-17 (the block now routes to the skill); the
    block keeps only that files are a destination at all.
    """
    body = " ".join(agent_rules.POINTER_BODY.split())
    assert "files (artifacts)" in body
    skill = " ".join((_AGENT_TREE / "skills" / "track-work" / "SKILL.md").read_text().split())
    assert "Every file that directly affects an entity should be uploaded as an artifact" in skill
    assert "NEVER UPLOAD SECRETS" in skill
    assert "`--reference`" in skill
    assert "lowest entity" in skill
    assert "records lineage back to it" in skill
    assert "a file with no better home goes to the project's artifacts, prose to its notes" in skill
    assert "Drop nothing" in skill
    assert "Automatically tracked" in skill and "transcripts" in skill


def test_pointer_body_edits_force_a_version_bump() -> None:
    """Editing POINTER_BODY without bumping POINTER_VERSION leaves every
    installed block stale-but-current forever: is_current() stays true, the
    wizard never rewrites, and no release can reach the file. The pin makes
    the pair move together — edit the body, bump the version, re-pin here.
    """
    import hashlib

    digest = hashlib.sha256(agent_rules.POINTER_BODY.encode()).hexdigest()[:12]
    # 34 / 939ac4c962dc: 0231 added `experiment` to the kind list this body
    # prints. The edit shipped in T2 WITHOUT the bump, which left every
    # installed block stale-but-current -- exactly what this pin exists to
    # catch, and it caught it (on main, where agent-ci runs; there is no
    # pull_request trigger, so nothing said so until the next push).
    # 35 / 040aff362906: the `daemon` state -- the switch line names four
    # states and the block says who writes in each; WHAT to record moved to
    # `track-work`.
    # 36 / 0000e2602370: daemon v2 -- in `daemon` the agent only instruments its
    # runs; the daemon records everything else, containers included.
    assert (agent_rules.POINTER_VERSION, digest) == (36, "0000e2602370"), (
        "POINTER_BODY changed: bump POINTER_VERSION and re-pin this digest"
    )


def test_the_plugin_refuses_to_call_a_cli_that_cannot_do_the_work() -> None:
    """THE SKEW THAT SHIPPED. The plugin and the CLI update on independent
    schedules, so a machine routinely runs a new plugin against an old CLI.
    Plugin 0.44.0 called `probe notes sync` against CLI 0.104.0, which did not
    have it, and the spawn discards its output -- so the team note silently
    stopped syncing on every machine with that pairing and nothing said so.

    The floor turns that into a sentence. An unparseable version passes, because
    that is a development checkout far more often than an old release.
    """
    import sys

    sys.path.insert(0, "plugins/probe-research/hooks")
    import version_check

    original = version_check._local_cli
    major, minor, patch = version_check._triplet(version_check.TEAM_NOTE_MIN_CLI)
    # DERIVED FROM THE FLOOR, never written out. Hard-coded versions here go
    # stale the moment the floor moves, and they go stale as a PASS: the suite
    # would keep asserting that a CLI which is now too old is acceptable, which
    # is the failure this test exists to catch.
    below = f"probe {major}.{minor}.{patch - 1}" if patch else f"probe {major}.{minor - 1}.0"
    try:
        version_check._local_cli = lambda _binary, v=below: v
        stale = version_check._team_note_cli_too_old("probe")
        assert stale is not None
        assert version_check.TEAM_NOTE_MIN_CLI in stale
        assert "uv tool upgrade" in stale, "the message must name the fix"

        for good in (
            f"probe {major}.{minor}.{patch}",
            f"probe {major}.{minor + 1}.2",
            f"probe {major + 1}.0.0",
        ):
            version_check._local_cli = lambda _binary, v=good: v
            assert version_check._team_note_cli_too_old("probe") is None, good

        version_check._local_cli = lambda _binary: None
        assert version_check._team_note_cli_too_old("probe") is None
    finally:
        version_check._local_cli = original


def test_the_minimum_cli_is_not_ahead_of_the_shipped_one() -> None:
    """A floor above the released CLI would tell every machine to upgrade to a
    version that does not exist yet, which is worse than the silence it fixes."""
    import sys
    from probe._compat import tomllib
    from pathlib import Path

    sys.path.insert(0, "plugins/probe-research/hooks")
    import version_check

    shipped = tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
    assert version_check._triplet(version_check.TEAM_NOTE_MIN_CLI) <= version_check._triplet(
        shipped
    ), f"floor {version_check.TEAM_NOTE_MIN_CLI} is ahead of the shipped CLI {shipped}"


def test_team_note_brief_names_the_real_path(monkeypatch) -> None:
    """The hook's path and the CLI's path must be the same path.

    The brief tells every arriving agent where the document is. `version_check`
    duplicates that resolution rather than importing it (it is a hook, run by
    whatever bare python3 the harness has, with no guarantee `probe` is
    importable), so nothing but this test stops the two drifting apart -- and a
    briefing that names the wrong file is worse than one that names none, because
    the agent edits what it was told to and believes it wrote to the team note.

    All three harnesses, and their env overrides, since those are the cases
    where the two implementations could plausibly disagree. pi was added to
    `version_check._document_path()` without this test ever being extended to
    exercise it -- exactly the "a test would have caught it" gap this whole
    audit is about: the hook's own docstring claims this test pins it against
    drift, and until this case existed that claim was not true for pi.
    """
    import sys
    from pathlib import Path

    sys.path.insert(0, "plugins/probe-research/hooks")
    import version_check

    from probe.cli import team_note_file

    for env, _source in (
        ({}, None),  # nothing exported: the default branch both sides fall into
        ({"PROBE_AGENT": "claude_code"}, "claude_code"),
        ({"PROBE_AGENT": "codex"}, "codex"),
        ({"PROBE_AGENT": "pi"}, "pi"),
        ({"PROBE_AGENT": "claude_code", "CLAUDE_CONFIG_DIR": "/tmp/cfg"}, "claude_code"),
        ({"PROBE_AGENT": "codex", "CODEX_HOME": "/tmp/codex"}, "codex"),
        ({"PROBE_AGENT": "pi", "PI_CODING_AGENT_DIR": "/tmp/pi-agent"}, "pi"),
        # The state directory is where the document actually lives now, so its
        # override is the one that MUST move all three resolvers together. A
        # matrix without it would have passed while a hook read `~/.local/state`
        # on a machine whose CLI was writing somewhere else entirely.
        ({"XDG_STATE_HOME": "/tmp/state"}, None),
        ({"XDG_STATE_HOME": "/tmp/state", "PROBE_AGENT": "codex"}, "codex"),
        ({"XDG_STATE_HOME": "/tmp/state", "PROBE_AGENT": "pi"}, "pi"),
        # Harness roots pointed somewhere else entirely: the document must not
        # follow them anywhere. This is the ping-pong, as an assertion.
        (
            {
                "CLAUDE_CONFIG_DIR": "/tmp/cfg",
                "CODEX_HOME": "/tmp/codex",
                "PI_CODING_AGENT_DIR": "/tmp/pi-agent",
                "PROBE_AGENT": "codex",
            },
            "codex",
        ),
    ):
        for key in (
            "PROBE_AGENT",
            "CLAUDE_CONFIG_DIR",
            "CODEX_HOME",
            "PI_CODING_AGENT_DIR",
            "XDG_STATE_HOME",
        ):
            monkeypatch.delenv(key, raising=False)
        for key, value in env.items():
            monkeypatch.setenv(key, value)

        # `paths().document` is what actually WRITES the file, so that is what
        # the hooks have to agree with. Re-deriving it here as
        # `memory_path(...).parent / DOCUMENT_NAME` would only pin them against a
        # copy of one line of team_note_file, and a change to `paths()` -- moving
        # the document into a subdirectory, say -- would leave the brief naming a
        # file nothing syncs while this test stayed green.
        from_cli = team_note_file.paths().document
        assert Path(version_check._document_path()) == from_cli, env

    # And the name itself is one string in two places, not two strings that
    # happen to match today.
    assert version_check.DOCUMENT_NAME == team_note_file.DOCUMENT_NAME


def test_a_note_render_leaves_the_pointer_block_intact(tmp_path) -> None:
    """REGRESSION, and the reason `BlockSpec` exists.

    The team-note block was originally going to be written into the
    `probe-research:begin/end` markers -- whose body is POINTER_BODY, the live
    operational instructions. Rendering the note there deletes them, silently,
    on every machine. Two blocks, two marker pairs, one file.
    """
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    path.write_text("# my own rules\n\nkeep me\n", encoding="utf-8")

    assert agent_rules.install(path) is True
    assert agent_rules.install(
        path,
        spec=agent_rules.NOTE_BLOCK,
        block=agent_rules.render_note_block("## note\n\nbody", document=str(path)),
    ) is True

    text = path.read_text(encoding="utf-8")
    # Both blocks present, exactly once each.
    assert text.count(agent_rules.BEGIN_MARKER) == 1
    assert text.count(agent_rules.NOTE_BLOCK.begin) == 1
    # The pointer block's BODY survived the note render.
    assert "## Probe Research" in text
    # And so did the researcher's own prose, outside both blocks.
    assert "keep me" in text
    # Note block sits AFTER the pointer block: action items before context.
    assert text.index(agent_rules.BEGIN_MARKER) < text.index(agent_rules.NOTE_BLOCK.begin)


def test_removing_one_block_leaves_the_other(tmp_path) -> None:
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    path.write_text("mine\n", encoding="utf-8")
    agent_rules.install(path)
    agent_rules.install(
        path,
        spec=agent_rules.NOTE_BLOCK,
        block=agent_rules.render_note_block("## note", document=str(path)),
    )
    assert agent_rules.remove(path, spec=agent_rules.NOTE_BLOCK) is True

    text = path.read_text(encoding="utf-8")
    assert agent_rules.NOTE_BLOCK.begin not in text
    assert "## Probe Research" in text
    assert "mine" in text


def test_the_note_stamp_moves_with_content_not_just_version(tmp_path) -> None:
    """`POINTER_VERSION` cannot notice that prose changed -- a constant does not
    move when somebody edits a note. The stamp carries a source hash so drift is
    detectable at all."""
    from probe.cli import agent_rules

    doc = str(tmp_path / "probe-team-note.md")
    first = agent_rules.note_source_hash("## a\n\nbody", doc)
    second = agent_rules.note_source_hash("## a\n\nbody edited", doc)
    assert first != second
    # And a move of the editable file invalidates too.
    assert agent_rules.note_source_hash("## a\n\nbody", doc + "x") != first


def test_note_block_is_current_short_circuits_only_on_identical_content(tmp_path) -> None:
    """The `Stop`-every-turn short circuit. Without it, 13 sessions on one box
    rewrite two files per turn for content that changes a few times a day."""
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    doc = str(tmp_path / "probe-team-note.md")
    body = "## rules\n\n- one"

    assert agent_rules.note_block_is_current(path, body, doc) is False  # absent
    agent_rules.install(
        path,
        spec=agent_rules.NOTE_BLOCK,
        block=agent_rules.render_note_block(body, document=doc),
    )
    assert agent_rules.note_block_is_current(path, body, doc) is True
    assert agent_rules.note_block_is_current(path, body + "\n- two", doc) is False


def test_the_pointer_only_form_carries_no_note_content(tmp_path) -> None:
    """Over budget writes a pointer, never a truncated note: partial content
    under a header saying "a copy of the team note" reads as complete."""
    from probe.cli import agent_rules

    doc = str(tmp_path / "probe-team-note.md")
    secret = "SENTINEL-NOTE-BODY"
    block = agent_rules.render_note_block(secret, document=doc, pointer_only=True)
    assert secret not in block
    assert "did not fit here" in block
    assert doc in block


def _stale_block(path, version: int) -> None:
    """Install a pointer block stamped with an OLD version."""
    from probe.cli import agent_rules

    path.write_text(
        agent_rules.render_block(version=version) + "\n# my own rules\n",
        encoding="utf-8",
    )


def test_refresh_rewrites_a_stale_block_and_leaves_a_current_one(tmp_path) -> None:
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    _stale_block(path, agent_rules.POINTER_VERSION - 1)

    assert agent_rules.refresh_pointer(path) == agent_rules.POINTER_REFRESHED
    assert agent_rules.installed_version(path) == agent_rules.POINTER_VERSION
    # The researcher's own prose outside the markers is untouched.
    assert "# my own rules" in path.read_text(encoding="utf-8")

    # Second pass is a no-op: the short circuit that keeps Stop cheap.
    assert agent_rules.refresh_pointer(path) == agent_rules.POINTER_CURRENT


def test_refresh_never_installs_into_a_file_that_opted_out(tmp_path) -> None:
    """ABSENT IS A DECISION, not a gap.

    No block means this machine never opted in -- or unticked the wizard row,
    which leaves the same bytes. A background sync that adds standing
    instructions to somebody's memory file uninvited is a different act from
    keeping an existing one current.
    """
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    path.write_text("# just my rules\n", encoding="utf-8")

    assert agent_rules.refresh_pointer(path) == agent_rules.POINTER_ABSENT
    assert path.read_text(encoding="utf-8") == "# just my rules\n"


def test_refresh_leaves_a_block_from_a_newer_cli_alone(tmp_path) -> None:
    """Two CLIs on one machine must not rewrite each other every turn."""
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    _stale_block(path, agent_rules.POINTER_VERSION + 5)

    assert agent_rules.refresh_pointer(path) == agent_rules.POINTER_CURRENT
    assert agent_rules.installed_version(path) == agent_rules.POINTER_VERSION + 5


def test_refresh_refuses_a_damaged_block(tmp_path) -> None:
    from probe.cli import agent_rules

    path = tmp_path / "CLAUDE.md"
    path.write_text(f"{agent_rules.BEGIN_MARKER}\n<!-- v1 -->\norphan, no end\n", encoding="utf-8")

    with pytest.raises(agent_rules.DamagedBlock):
        agent_rules.refresh_pointer(path)


def test_the_document_path_fixture_is_what_the_cli_produces(monkeypatch, tmp_path) -> None:
    """The fixture pi's suite reads must describe THIS implementation.

    `tests/fixtures/team-note-document-path.json` is the only thing keeping the
    TypeScript resolver (`probe-research-pi/src/paths.ts`) honest -- it cannot
    import the CLI, and pi briefs a session from whatever that resolver returns.
    A fixture that drifted from the CLI would pin the wrong answer on both sides
    and read as agreement.
    """
    import json
    import os
    from pathlib import Path

    from probe.cli import team_note_file

    cases = json.loads(Path("tests/fixtures/team-note-document-path.json").read_text())["cases"]
    assert cases, "an empty fixture pins nothing"
    home = tmp_path / "home"
    home.mkdir()
    keys = (
        "XDG_STATE_HOME",
        "PROBE_AGENT",
        "CLAUDE_CONFIG_DIR",
        "CODEX_HOME",
        "PI_CODING_AGENT_DIR",
    )
    for case in cases:
        for key in keys:
            monkeypatch.delenv(key, raising=False)
        monkeypatch.setenv("HOME", str(home))
        for key, value in case["env"].items():
            monkeypatch.setenv(key, value)
        expected = case["path"].replace("~", str(home), 1)
        assert str(team_note_file.paths().document) == expected, case["why"]
        assert os.path.isabs(expected), case["why"]
