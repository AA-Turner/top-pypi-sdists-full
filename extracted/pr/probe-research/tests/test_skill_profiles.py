"""agent/skills/profiles.json: the ONE list of which skills each install
profile ships ("full" = the agent records; "daemon" = the Probe daemon records).

The Makefile's skill syncs read it (`PROFILE_FULL`, `PROFILE_DAEMON_COPIED`).
The static manifests that cannot (the pi package.json, mirror-package.json),
the lean daemon plugin's shipped skills and the pi extension's constants are
held to it here and in tests/test_pi_daemon_profile.py.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]
PROFILES = json.loads((AGENT / "skills" / "profiles.json").read_text())


def test_every_profile_skill_exists():
    for profile, skills in PROFILES.items():
        for skill in skills:
            assert (AGENT / "skills" / skill / "SKILL.md").exists() or (
                AGENT / "skills" / skill
            ).is_dir(), f"{profile} names {skill}, which is not a skill"


def test_the_daemon_profile_is_a_subset_of_full():
    assert set(PROFILES["daemon"]) <= set(PROFILES["full"])


def test_the_pi_package_ships_the_full_profile():
    manifest = json.loads((AGENT / "plugins" / "probe-research-pi" / "package.json").read_text())
    assert [Path(p).name for p in manifest["pi"]["skills"]] == PROFILES["full"]


def test_the_mirror_root_manifest_ships_the_full_profile():
    manifest = json.loads((AGENT / "mirror-package.json").read_text())
    assert [Path(p).name for p in manifest["pi"]["skills"]] == PROFILES["full"]


def _make_dry_run(target: str) -> str:
    return subprocess.run(
        ["make", "-n", "-C", str(AGENT), target], capture_output=True, text=True, check=True
    ).stdout


def test_the_makefile_skill_syncs_expand_to_the_profiles():
    for target in ("sync-plugin-skills", "sync-pi-skills"):
        assert f"for s in {' '.join(PROFILES['full'])}; do" in _make_dry_run(target), target
    copied = [s for s in PROFILES["daemon"] if s != "probe"]
    assert f"for s in {' '.join(copied)}; do" in _make_dry_run("sync-daemon-plugin")


def test_the_lean_daemon_plugin_ships_the_daemon_profile():
    shipped = sorted(
        p.name
        for p in (AGENT / "plugins" / "probe-research-daemon" / "skills").iterdir()
        if p.is_dir()
    )
    assert shipped == sorted(PROFILES["daemon"])
