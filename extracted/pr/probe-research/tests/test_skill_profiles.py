"""agent/skills/profiles.json: the ONE list of which skills each install
profile ships ("full" = the agent records; "daemon" = the Probe daemon records).

The skill syncs (plugins/VENDORED.json, made by tools/vendor.py) read it.
The static manifests that cannot (the pi package.json, mirror-package.json),
the lean daemon plugin's shipped skills and the pi extension's constants are
held to it here and in tests/test_pi_daemon_profile.py.
"""

from __future__ import annotations

import json
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


def _synced_skills(group: str) -> list[str]:
    """The skills `make <group>` copies as trees, in order, as tools/vendor.py expands them."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_vendor", AGENT / "tools" / "vendor.py")
    vendor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vendor)
    return [Path(op.sources[0]).name for op in vendor.plan(group) if op.kind == "tree"]


def test_the_skill_syncs_expand_to_the_profiles():
    for group in ("sync-plugin-skills", "sync-pi-skills"):
        assert _synced_skills(group) == PROFILES["full"], group
    hand_kept = json.loads((AGENT / "plugins" / "VENDORED.json").read_text())["lists"]["daemon_hand_kept"]
    assert set(hand_kept) <= set(PROFILES["daemon"])
    assert _synced_skills("sync-daemon-plugin") == [s for s in PROFILES["daemon"] if s not in hand_kept]


def test_the_lean_daemon_plugin_ships_the_daemon_profile():
    shipped = sorted(
        p.name
        for p in (AGENT / "plugins" / "probe-research-daemon" / "agent-skills").iterdir()
        if p.is_dir()
    )
    assert shipped == sorted(PROFILES["daemon"])
