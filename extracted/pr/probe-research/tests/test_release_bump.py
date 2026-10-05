"""agent/tools/release_bump.py: the bump step `release.yml` runs.

The plugin manifests it moves come from the harness registry, so these pin
that the registry-derived list is exactly the set the workflow used to name
by hand, and that a bump changes nothing but the version strings.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
REPO = AGENT.parent
_TOOL = AGENT / "tools" / "release_bump.py"

spec = importlib.util.spec_from_file_location("release_bump", _TOOL)
release_bump = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = release_bump
spec.loader.exec_module(release_bump)

#: What release.yml bumped and committed by name before the registry did it,
#: plus what the registry added since.
_HAND_LIST = {
    "agent/plugins/probe-research/.claude-plugin/plugin.json",
    "agent/plugins/probe-research/.codex-plugin/plugin.json",
    "agent/plugins/probe-research-daemon/.claude-plugin/plugin.json",
    "agent/plugins/probe-research-daemon/.codex-plugin/plugin.json",
    # Kimi Code, the first hook-plugin harness the registry added on its own.
    "agent/plugins/probe-research/.kimi-plugin/plugin.json",
    "agent/plugins/probe-research-daemon/.kimi-plugin/plugin.json",
}


def _copy_release_files(root: Path) -> None:
    for rel in [
        "agent/pyproject.toml",
        "agent/client-version.json",
        "agent/CHANGELOG.md",
        *release_bump.plugin_manifests(),
    ]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, root / rel)


def test_the_registry_names_the_same_manifests_the_workflow_did():
    assert set(release_bump.plugin_manifests()) == _HAND_LIST
    for rel in release_bump.plugin_manifests():
        assert (REPO / rel).is_file(), rel


def test_a_plugin_release_moves_every_manifest_and_nothing_else(tmp_path):
    _copy_release_files(tmp_path)
    before = {rel: (tmp_path / rel).read_text() for rel in release_bump.plugin_manifests()}

    written = release_bump.bump(tmp_path, plugin="9.8.7")

    assert set(written) == _HAND_LIST | {"agent/client-version.json"}
    for rel, text in before.items():
        after = (tmp_path / rel).read_text()
        assert json.loads(after)["version"] == "9.8.7", rel
        old_version = json.loads(text)["version"]
        assert after == text.replace(f'"{old_version}"', '"9.8.7"', 1), rel
    manifest = json.loads((tmp_path / "agent/client-version.json").read_text())
    assert manifest["plugin"]["latest"] == "9.8.7"
    assert (tmp_path / "agent/pyproject.toml").read_text() == (
        REPO / "agent/pyproject.toml"
    ).read_text()


def test_a_cli_release_moves_pyproject_and_stamps_the_changelog(tmp_path):
    _copy_release_files(tmp_path)

    written = release_bump.bump(tmp_path, cli="9.8.7", bump_manifest=True)

    assert written == ["agent/pyproject.toml", "agent/client-version.json", "agent/CHANGELOG.md"]
    assert 'version = "9.8.7"' in (tmp_path / "agent/pyproject.toml").read_text()
    assert (
        json.loads((tmp_path / "agent/client-version.json").read_text())["cli"]["latest"] == "9.8.7"
    )
    assert "## Unreleased\n\n## 9.8.7" in (tmp_path / "agent/CHANGELOG.md").read_text()
    for rel in release_bump.plugin_manifests():
        assert (tmp_path / rel).read_text() == (REPO / rel).read_text(), rel


def test_a_missing_plugin_manifest_fails_the_release(tmp_path):
    _copy_release_files(tmp_path)
    (tmp_path / release_bump.plugin_manifests()[-1]).unlink()
    with pytest.raises(SystemExit, match="a release must bump"):
        release_bump.bump(tmp_path, plugin="9.8.7")


def test_the_cli_writes_the_list_the_workflow_git_adds(tmp_path):
    _copy_release_files(tmp_path)
    out = tmp_path / "bumped"
    assert (
        release_bump.main(["--plugin", "9.8.7", "--written", str(out), "--root", str(tmp_path)])
        == 0
    )
    assert set(out.read_text().split()) == _HAND_LIST | {"agent/client-version.json"}


def test_release_yml_bumps_through_the_script():
    workflow = (REPO / ".github/workflows/release.yml").read_text()
    assert "python agent/tools/release_bump.py" in workflow
    assert 'xargs -a "$RUNNER_TEMP/bumped-files" git add' in workflow
    for rel in _HAND_LIST:
        assert rel not in workflow, f"{rel} is named by hand again; the registry names it"
