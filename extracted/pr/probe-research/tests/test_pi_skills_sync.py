"""The pi package's skill copies must match the canonical `skills/`.

`plugins/probe-research-pi/skills/` is a COPY of `skills/`, not a symlink —
same contract as `plugins/probe-research/agent-skills/` (guarded by
`tests/test_skills_sync.py`) and `plugins/probe-research-tap/tap/` (guarded
by `tests/test_tap_core_sync.py`): the pi package ships self-contained, so
pi's own package manager can read it without reaching outside the package
root. `make sync-pi-skills` reconciles them.

Unlike the Claude Code plugin, this package also needs the skill names
declared explicitly in `package.json`'s `"pi": {"skills": [...]}` block — pi
only treats a directory as a package RESOURCE (as opposed to a plain file
sitting there) when its manifest says so. That declaration can drift from
the vendored directories independently of the file-content drift the other
sync guards catch, so this file also pins the manifest list.

Same failure mode as the sibling guards: everything still passes, the model
just gets old instructions — and here, drift in the OTHER direction (a
skill vendored but not declared) is invisible in an even worse way: pi's
resource loader silently resolves zero skills from this package, and
nothing short of live-testing against pi's installed source (which
`plugins/probe-research-pi/tests/skillsManifest.test.ts` does, in the
package's own vitest suite) would show it.
"""

from __future__ import annotations

import filecmp
import json
import re
import subprocess
from pathlib import Path

import pytest

from probe import skill_versions
from tests.held_for_plugin_release import HELD_NEW_SKILLS, HELD_SKILLS, REASON

_ROOT = Path(__file__).resolve().parent.parent

_CANONICAL = _ROOT / "skills"
#: Skills only the Capy bundle ships (profiles.json "capy"): the public mirror
#: renders them under capy/skills/, and no pi package carries them.
_PROFILES = json.loads((_CANONICAL / "profiles.json").read_text())
_CAPY_ONLY = set(_PROFILES["capy"]) - set(_PROFILES["full"])
_PI_PLUGIN = _ROOT / "plugins" / "probe-research-pi" / "skills"
_PI_PACKAGE_JSON = _ROOT / "plugins" / "probe-research-pi" / "package.json"

# Mirrors the Makefile's sync-pi-skills list.
_SYNCED = (
    "probe",
    "track-work",
    "visualize-progress",
    "instrument-code",
    "audit-team-note",
    "edit-notes",
    "notes-audit",
    "plan-research-review",
    # writer-owns-summary (D2): the recorder keeps summaries and Metrics-center visuals
    "write-summary",
    "overview-visuals",
)


def _files(root: Path) -> dict[str, Path]:
    """Every file under `root`, keyed by its path relative to root."""
    return {
        str(path.relative_to(root)): path
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


@pytest.mark.parametrize(
    "skill",
    [pytest.param(s, marks=pytest.mark.xfail(strict=True, reason=REASON)) if s in HELD_SKILLS else s
     for s in _SYNCED],
)
def test_pi_skill_copy_matches_canonical(skill: str) -> None:
    canonical, plugin = _CANONICAL / skill, _PI_PLUGIN / skill
    assert canonical.is_dir(), f"canonical skill {skill} is missing"
    assert plugin.is_dir(), f"pi package copy of {skill} is missing; run `make sync-pi-skills`"

    left, right = _files(canonical), _files(plugin)
    if (canonical / skill_versions.VERSIONS).is_dir():
        # One base, one version per reader: the copy is the MAIN AGENT's version
        # and carries no `versions/` (the writer's header never reaches it).
        left = {k: v for k, v in left.items() if not k.startswith(skill_versions.VERSIONS + "/")}
        assert (plugin / "SKILL.md").read_text(encoding="utf-8") == skill_versions.render(
            canonical, skill_versions.MAIN_AGENT), f"{skill}: not the main agent's version -- run `make sync-plugin`"
        left.pop("SKILL.md")
        right = {k: v for k, v in right.items() if k != "SKILL.md"}
    assert sorted(left) == sorted(right), (
        f"{skill}: pi package copy has a different file list than skills/{skill} "
        f"— run `make sync-pi-skills`"
    )
    drifted = [name for name in left if not filecmp.cmp(left[name], right[name], shallow=False)]
    assert not drifted, (
        f"{skill}: {drifted} differ from the canonical skills/{skill} "
        f"— run `make sync-pi-skills` (edit skills/, never the pi package copy)"
    )


def test_every_canonical_skill_is_covered_by_this_guard() -> None:
    """A new skill must be added to the Makefile's sync-pi-skills list, to
    package.json's "pi.skills", AND to `_SYNCED` here — otherwise it is
    silently missing from the pi package while every parametrized case
    above still passes."""
    on_disk = {path.name for path in _CANONICAL.iterdir() if path.is_dir()} - _CAPY_ONLY - HELD_NEW_SKILLS
    covered = set(_SYNCED)
    assert on_disk == covered, (
        f"skills/ holds {sorted(on_disk)} but this guard covers {sorted(covered)}; "
        "add it to _SYNCED + the Makefile + package.json's pi.skills"
    )
    assert not {s for s in HELD_NEW_SKILLS if (_PI_PLUGIN / s).exists()}, "empty HELD_NEW_SKILLS"


def test_the_makefile_sync_list_matches_synced() -> None:
    """Parsed, not eyeballed — same contract as test_skills_sync.py's
    equivalent guard, applied to the sync-pi-skills loop instead."""
    # The loop reads agent/skills/profiles.json, so read it as make expands it.
    import subprocess

    dry_run = subprocess.run(
        ["make", "-n", "-C", str(_ROOT), "sync-pi-skills"], capture_output=True, text=True, check=True
    ).stdout
    m = re.search(r"for s in ([^;]+); do", dry_run)
    assert m, "could not parse the sync-pi-skills loop"
    assert set(m.group(1).split()) == set(_SYNCED)


def test_sync_pi_skills_runs_in_the_sync_plugin_composite() -> None:
    """`make sync-plugin` is the "sync everything" umbrella; a target left
    out of it is a sync that only runs if someone remembers its exact name."""
    makefile = (_ROOT / "Makefile").read_text(encoding="utf-8")
    m = re.search(r"^sync-plugin:\s*(.+)$", makefile, re.MULTILINE)
    assert m, "could not find the sync-plugin composite target"
    assert "sync-pi-skills" in m.group(1).split()


def test_package_json_declares_exactly_the_synced_skills() -> None:
    """`pi`'s package manager only treats a directory as a skill RESOURCE
    when package.json's own "pi.skills" manifest names it (verified live
    against the installed @earendil-works/pi-coding-agent package — see
    tests/skillsManifest.test.ts in this package) — vendoring the directory
    alone is not enough. This guards the manifest list against drifting
    from _SYNCED independently of the file-content checks above.
    """
    manifest = json.loads(_PI_PACKAGE_JSON.read_text(encoding="utf-8"))
    declared = manifest.get("pi", {}).get("skills")
    assert declared is not None, "package.json's pi.skills manifest is missing"

    declared_names = set()
    for entry in declared:
        assert entry.startswith("skills/"), (
            f"pi.skills entry {entry!r} is not under skills/ — "
            "the sync target only vendors skills/<name> directories"
        )
        declared_names.add(entry.removeprefix("skills/"))

    assert declared_names == set(_SYNCED), (
        f"package.json declares {sorted(declared_names)} but _SYNCED is "
        f"{sorted(_SYNCED)} — keep pi.skills, the Makefile loop, and _SYNCED "
        "in lockstep"
    )


# ---------------------------------------------------------------------------
# The daemon profile's own skills (pi on the Probe daemon).
# ---------------------------------------------------------------------------

_LEAN_SKILLS = _ROOT / "plugins" / "probe-research-daemon" / "agent-skills"
_PI_DAEMON_SKILLS = _ROOT / "plugins" / "probe-research-pi" / "daemon-skills"


def _hand_kept() -> list[str]:
    """The Makefile's `DAEMON_HAND_KEPT`: the lean plugin's own skills."""
    makefile = (_ROOT / "Makefile").read_text(encoding="utf-8")
    m = re.search(r"^DAEMON_HAND_KEPT := (.+)$", makefile, re.MULTILINE)
    assert m, "the Makefile no longer declares DAEMON_HAND_KEPT"
    return m.group(1).split()


def test_pi_daemon_skills_are_byte_copies_of_the_lean_plugins() -> None:
    """pi's daemon profile tells the agent what Claude Code's lean plugin tells
    it: the extension adds `daemon-skills/<name>` through `resources_discover`,
    and each file must be the lean plugin's skill byte for byte."""
    hand_kept = _hand_kept()
    assert hand_kept == ["probe", "visualize-progress"]
    for name in hand_kept:
        copy = _PI_DAEMON_SKILLS / name / "SKILL.md"
        assert copy.is_file(), f"pi's daemon copy of {name} is missing; run `make sync-pi-daemon-skill`"
        assert copy.read_bytes() == (_LEAN_SKILLS / name / "SKILL.md").read_bytes(), (
            f"plugins/probe-research-pi/daemon-skills/{name}/SKILL.md differs from the lean plugin's; "
            f"run `make sync-pi-daemon-skill` (edit plugins/probe-research-daemon/agent-skills/{name}, never the copy)"
        )
    assert sorted(p.relative_to(_PI_DAEMON_SKILLS).as_posix() for p in _PI_DAEMON_SKILLS.rglob("*") if p.is_file()) == [
        f"{name}/SKILL.md" for name in sorted(hand_kept)
    ], "daemon-skills/ carries only the daemon's own skills"


def test_sync_pi_daemon_skill_copies_those_files_and_runs_in_the_composite() -> None:
    dry = subprocess.run(
        ["make", "-n", "-C", str(_ROOT), "sync-pi-daemon-skill"], capture_output=True, text=True, check=True
    ).stdout
    assert f"for s in {' '.join(_hand_kept())}; do" in dry
    assert (
        "cp plugins/probe-research-daemon/agent-skills/$s/SKILL.md "
        "plugins/probe-research-pi/daemon-skills/$s/SKILL.md"
    ) in dry
    makefile = (_ROOT / "Makefile").read_text(encoding="utf-8")
    composite = re.search(r"^sync-plugin:\s*(.+)$", makefile, re.MULTILINE)
    assert composite and "sync-pi-daemon-skill" in composite.group(1).split()


def test_the_agent_profile_never_loads_the_daemon_skill() -> None:
    """pi loads every skill a package's manifest names. Listing daemon-skills
    there would give an agent-profile session two `probe` skills that disagree
    about who records; the extension adds it only in the daemon profile."""
    manifest = json.loads(_PI_PACKAGE_JSON.read_text(encoding="utf-8"))
    mirror = json.loads((_ROOT / "mirror-package.json").read_text(encoding="utf-8"))
    for declared in (manifest["pi"]["skills"], mirror["pi"]["skills"]):
        assert not [entry for entry in declared if "daemon-skills" in entry]
