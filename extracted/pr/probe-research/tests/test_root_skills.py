"""Probe's skills in the agent's own folder: install, refresh, switch, remove.

The behaviour these pin, in the order it can hurt:

1. A Who-records switch must leave EXACTLY the new profile's skills. A
   `track-work` left behind on the daemon profile tells the agent to record
   inline while the daemon records the same session.
2. We never write over or delete a folder we cannot prove is ours. `probe`,
   `track-work` and `edit-notes` are generic names, and gstack already keeps ~50
   skills in that same directory.
3. The refresh is what keeps the plugin the delivery channel. If it stopped
   copying, new wording would reach nobody -- the `POINTER_VERSION` mistake.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe import root_skills_core as core
from probe.cli import root_skills


def _plugin(tmp_path, *slugs, name="probe-research"):
    """A plugin tree whose `agent-skills/` holds `slugs`."""
    root = tmp_path / "cache" / name
    for slug in slugs:
        folder = root / core.PLUGIN_SKILLS_DIR / slug
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(f"---\nname: {slug}\n---\n# {slug}\n")
    return root


def _skills(tmp_path):
    return tmp_path / "home" / ".claude" / "skills"


def test_install_puts_each_skill_at_the_root_with_our_marker(tmp_path):
    plugin = _plugin(tmp_path, "probe", "track-work")
    root = _skills(tmp_path)

    report = core.apply(root, plugin, ("probe", "track-work"))

    assert sorted(report["installed"]) == ["probe", "track-work"]
    assert (root / "probe" / "SKILL.md").is_file()
    marker = json.loads((root / "probe" / core.MARKER).read_text())
    assert marker["source"] == "probe-research" and marker["skill"] == "probe"


def test_a_second_pass_rewrites_nothing(tmp_path):
    """The SessionStart hook runs this every start. Rewriting a folder a live
    session is reading from is both pointless and a way to hand it half a file."""
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    core.apply(root, plugin, ("probe",))
    before = (root / "probe" / "SKILL.md").stat().st_mtime_ns

    report = core.apply(root, plugin, ("probe",))

    assert report == {"installed": [], "refreshed": [], "removed": [], "renamed": [], "notes": []}
    assert (root / "probe" / "SKILL.md").stat().st_mtime_ns == before


def test_new_plugin_wording_reaches_the_root_copy(tmp_path):
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    core.apply(root, plugin, ("probe",))

    (plugin / core.PLUGIN_SKILLS_DIR / "probe" / "SKILL.md").write_text("---\nname: probe\n---\n# new wording\n")
    report = core.apply(root, plugin, ("probe",))

    assert report["refreshed"] == ["probe"]
    assert "new wording" in (root / "probe" / "SKILL.md").read_text()


def test_switching_profiles_removes_the_other_profiles_skills(tmp_path):
    """The failure this exists for: `track-work` surviving the switch to the
    daemon profile, where the daemon is already recording the session."""
    full = _plugin(tmp_path, "probe", "track-work", "instrument-code")
    lean = _plugin(tmp_path, "probe", "instrument-code", name="probe-research-daemon")
    root = _skills(tmp_path)
    core.apply(root, full, ("probe", "track-work", "instrument-code"))
    assert (root / "track-work").is_dir()

    report = core.apply(root, lean, ("probe", "instrument-code"))

    assert report["removed"] == ["track-work"]
    assert not (root / "track-work").exists()
    assert sorted(p.name for p in root.iterdir() if p.is_dir()) == ["instrument-code", "probe"]


def test_a_foreign_skill_of_the_same_name_is_never_touched(tmp_path):
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    (root / "probe").mkdir(parents=True)
    (root / "probe" / "SKILL.md").write_text("# someone else's probe skill\n")

    report = core.apply(root, plugin, ("probe",))

    assert "someone else's" in (root / "probe" / "SKILL.md").read_text()
    assert report["renamed"] == ["probe-probe"]
    assert (root / "probe-probe" / "SKILL.md").is_file()
    assert any("already a skill of yours" in note for note in report["notes"])


def test_prune_leaves_a_foreign_skill_alone(tmp_path):
    root = _skills(tmp_path)
    (root / "mine").mkdir(parents=True)
    (root / "mine" / "SKILL.md").write_text("# not ours\n")
    (root / "ours").mkdir()
    (root / "ours" / core.MARKER).write_text("{}\n")

    assert core.prune(root, keep=frozenset()) == ("ours",)
    assert (root / "mine").is_dir() and not (root / "ours").exists()


def test_an_older_plugin_beside_a_newer_cli_changes_nothing(tmp_path):
    """The release-pairing window: a plugin that still has `skills/` is one whose
    own sessions list the skills themselves. Installing from a guess is worse."""
    plugin = tmp_path / "cache" / "probe-research"
    (plugin / "skills" / "probe").mkdir(parents=True)
    (plugin / "skills" / "probe" / "SKILL.md").write_text("# old layout\n")
    root = _skills(tmp_path)

    report = core.apply(root, plugin, ("probe",))

    assert report["installed"] == [] and any(core.PLUGIN_SKILLS_DIR in n for n in report["notes"])
    assert not root.exists() or not any(root.iterdir())


@pytest.mark.parametrize(
    ("source", "expected"),
    [("claude_code", "skills"), ("codex", None), ("pi", None), ("kimi_code", None)],
)
def test_only_claude_code_gets_a_root_skills_folder(source, expected, tmp_path, monkeypatch):
    """Codex and Kimi read the plugin's `agent-skills/` by manifest key, and pi
    its package manifest. Writing into their homes would duplicate, not move."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi"))
    monkeypatch.setenv("KIMI_CODE_HOME", str(tmp_path / "kimi"))

    root = root_skills.skills_root(source)

    assert (root.name if root else None) == expected


def _ledger(tmp_path, **roots):
    """A ledger in production's shape: one entry per plugin key, carrying
    `scope`, in INSTALL ORDER -- which is what made the switch pick wrong."""
    ledger = tmp_path / "installed_plugins.json"
    ledger.write_text(json.dumps({"version": 2, "plugins": {
        f"{name}@research-os-agent": [{"scope": "user", "installPath": str(root)}]
        for name, root in roots.items()
    }}))
    return ledger


def test_the_switch_picks_the_plugin_BEING_INSTALLED_not_the_one_being_left(tmp_path, monkeypatch):
    """The failure this guards, reproduced before the fix: `Who records` ->
    daemon installs the new plugin, applies skills, and only THEN uninstalls the
    old one, so the ledger briefly holds both -- old first. Picking the first
    match installed the FULL profile's skills, landing `track-work`, which tells
    the agent to record inline while the daemon records the same session."""
    full = _plugin(tmp_path / "full", "probe", "track-work")
    lean = _plugin(tmp_path / "lean", "probe", name="probe-research-daemon")
    # Install order: the profile being LEFT is in the ledger first.
    monkeypatch.setenv("PROBE_INSTALLED_PLUGINS_JSON",
                       str(_ledger(tmp_path, **{"probe-research": full, "probe-research-daemon": lean})))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))

    assert root_skills.installed_plugin_root("probe-research-daemon") == lean
    root_skills.apply("claude_code", root_skills.installed_plugin_root("probe-research-daemon"))

    root = tmp_path / "claude" / "skills"
    assert sorted(p.name for p in root.iterdir() if p.is_dir()) == ["probe"]
    assert not (root / "track-work").exists(), "track-work on the daemon profile = double recording"


def test_a_plugin_not_in_the_ledger_yet_installs_nothing(tmp_path, monkeypatch):
    """Rather than fall back to the other profile, which is the bug above."""
    full = _plugin(tmp_path / "full", "probe", "track-work")
    monkeypatch.setenv("PROBE_INSTALLED_PLUGINS_JSON",
                       str(_ledger(tmp_path, **{"probe-research": full})))

    assert root_skills.installed_plugin_root("probe-research-daemon") is None


def test_a_user_scope_entry_wins_over_another_scope(tmp_path, monkeypatch):
    project = _plugin(tmp_path / "proj", "probe")
    user = _plugin(tmp_path / "user", "probe")
    ledger = tmp_path / "installed_plugins.json"
    ledger.write_text(json.dumps({"version": 2, "plugins": {"probe-research@research-os-agent": [
        {"scope": "project", "installPath": str(project)},
        {"scope": "user", "installPath": str(user)},
    ]}}))
    monkeypatch.setenv("PROBE_INSTALLED_PLUGINS_JSON", str(ledger))

    assert root_skills.installed_plugin_root("probe-research") == user


def test_no_plugin_installs_nothing_and_says_nothing(tmp_path, monkeypatch):
    """An older plugin beside a newer CLI, or a machine with no plugin at all.
    Quiet on purpose: the wizard already reports what it installed, and the
    SessionStart hook installs these the moment a plugin arrives. A complaint
    here fired on every `Who records` switch in a test env and read as a fault."""
    monkeypatch.setenv("PROBE_INSTALLED_PLUGINS_JSON", str(tmp_path / "absent.json"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))

    assert root_skills.installed_plugin_root() is None
    assert root_skills.apply("claude_code", None) == []
    assert not (tmp_path / "claude" / "skills").exists()


def test_an_interrupted_write_leaves_no_unmarked_folder(tmp_path, monkeypatch):
    """The marker goes in before the folder takes its name, so a crash mid-copy
    cannot leave our own folder looking like the researcher's. Unmarked, the
    next pass forked a `probe-probe` duplicate that nothing ever healed."""
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    real = core.shutil.copytree
    armed = {"on": True}

    def explode(src, dst, *a, **k):
        real(src, dst, *a, **k)
        if armed["on"]:
            raise KeyboardInterrupt  # killed hook, full disk, Ctrl-C

    monkeypatch.setattr(core.shutil, "copytree", explode)
    with pytest.raises(KeyboardInterrupt):
        core.apply(root, plugin, ("probe",))

    # Never monkeypatch.undo() here: it also undoes conftest's home isolation.
    armed["on"] = False
    assert not (root / "probe").exists(), "a half-written skill must not take the real name"
    report = core.apply(root, plugin, ("probe",))
    assert report["installed"] == ["probe"] and not (root / "probe-probe").exists()


def test_an_unmarked_copy_of_our_own_bytes_is_re_adopted(tmp_path):
    """Recovery for any folder already orphaned by the old non-atomic write:
    identical bytes mean it IS ours, so re-mark it instead of duplicating."""
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    root.mkdir(parents=True)
    core.shutil.copytree(plugin / core.PLUGIN_SKILLS_DIR / "probe", root / "probe")
    assert not core.is_ours(root / "probe")

    report = core.apply(root, plugin, ("probe",))

    assert report["refreshed"] == ["probe"] and not (root / "probe-probe").exists()
    assert core.is_ours(root / "probe")


def test_a_symlinked_folder_is_left_alone_and_does_not_stop_the_sync(tmp_path):
    """`rmtree` raises on a symlink and the hook swallows exceptions, so one
    symlinked folder stopped that machine's sync for good, with no signal."""
    plugin = _plugin(tmp_path, "probe", "track-work")
    root = _skills(tmp_path)
    core.apply(root, plugin, ("probe", "track-work"))
    (root / "track-work").rename(root / "elsewhere")
    (root / "track-work").symlink_to(root / "elsewhere")

    report = core.apply(root, plugin, ("probe",))

    # The symlink itself is never ours to delete, and -- the point -- the pass
    # completes: `probe` is installed and nothing raised. The folder it points
    # at still carries our marker, so prune treats it as the skill it is.
    assert (root / "track-work").is_symlink()
    assert core.is_ours(root / "probe") and report["removed"] == ["elsewhere"]
    assert core.prune(root, keep=frozenset()) == ("probe",)


def test_a_foreign_folder_at_the_fallback_name_is_also_left_alone(tmp_path):
    """The collision path wrote `probe-<slug>` without an ownership check, so
    the rule it had just enforced was dropped one line later."""
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    for name in ("probe", "probe-probe"):
        (root / name).mkdir(parents=True)
        (root / name / "SKILL.md").write_text(f"# their {name}\n")

    report = core.apply(root, plugin, ("probe",))

    assert "their probe-probe" in (root / "probe-probe" / "SKILL.md").read_text()
    assert report["installed"] == [] and report["renamed"] == []
    assert any("did not install ours" in n for n in report["notes"])


def test_only_one_session_installs_at_a_time(tmp_path):
    """Interleaved, each racer computed its own keep-set and `prune` deleted what
    the others had just written -- a session left with no `probe` skill at all,
    which is the consent and off switch."""
    plugin = _plugin(tmp_path, "probe")
    root = _skills(tmp_path)
    with core._one_writer(root) as holder:
        assert holder
        report = core.apply(root, plugin, ("probe",))

    assert report["installed"] == [] and any("another session" in n for n in report["notes"])
    assert not (root / "probe").exists(), "the pass is skipped, never half-applied"


def test_a_benign_collision_is_not_reported_as_a_failure(tmp_path, monkeypatch):
    """The wizard reads a leading `!` as a failed step, so owning a skill called
    `probe` painted the plugin install red."""
    plugin = _plugin(tmp_path, "probe")
    monkeypatch.setenv("PROBE_INSTALLED_PLUGINS_JSON",
                       str(_ledger(tmp_path, **{"probe-research": plugin})))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    mine = tmp_path / "claude" / "skills" / "probe"
    mine.mkdir(parents=True)
    (mine / "SKILL.md").write_text("# mine\n")

    lines = root_skills.apply("claude_code", root_skills.installed_plugin_root("probe-research"))

    assert lines and not any(line.startswith("!") for line in lines), lines


def test_neither_plugin_still_carries_a_scanned_skills_folder(tmp_path):
    """The entire no-duplicates premise: Claude Code scans `skills/`. One
    habitual `cp -R` back into it reinstates double listing in every session."""
    plugins = Path(__file__).resolve().parents[1] / "plugins"
    for name in ("probe-research", "probe-research-daemon"):
        assert not (plugins / name / "skills").exists(), f"{name} must ship only agent-skills/"


@pytest.mark.parametrize(
    ("install_path", "expected"),
    [
        ("cache/research-os-agent/probe-research-daemon/0.130.0", "probe-research-daemon"),
        ("cache/research-os-agent/probe-research/1.2.3", "probe-research"),
        ("some/dev/probe-research", "probe-research"),
    ],
)
def test_the_marker_names_the_plugin_not_its_version(install_path, expected, tmp_path):
    """Shipped reading `"source": "0.130.0"`: Claude Code installs to
    `.../<plugin>/<version>/`, so the basename is the version, and naming where
    the folder came from is the only thing this field is for."""
    plugin = tmp_path / install_path
    (plugin / core.PLUGIN_SKILLS_DIR / "probe").mkdir(parents=True)
    (plugin / core.PLUGIN_SKILLS_DIR / "probe" / "SKILL.md").write_text("---\nname: probe\n---\n")
    root = _skills(tmp_path)

    core.apply(root, plugin, ("probe",))

    assert json.loads((root / "probe" / core.MARKER).read_text())["source"] == expected
