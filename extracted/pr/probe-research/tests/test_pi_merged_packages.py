"""The merged global+project pi `packages` read, and what it says about filters."""

from __future__ import annotations

import json

import pytest

from probe.cli import pi_config


@pytest.fixture
def agent_dir(tmp_path, monkeypatch):
    d = tmp_path / "pi-agent"
    d.mkdir()
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(d))
    return d


def _write(path, packages):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"packages": packages}), encoding="utf-8")


def test_global_only_install_is_found(agent_dir, tmp_path):
    _write(agent_dir / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    assert pi_config.package_entry_installed(cwd=tmp_path) is True


def test_project_only_install_is_found(agent_dir, tmp_path):
    _write(agent_dir / "settings.json", [])
    _write(tmp_path / ".pi" / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    assert pi_config.package_entry_installed(cwd=tmp_path) is True


def test_no_install_anywhere_is_not_found(agent_dir, tmp_path):
    _write(agent_dir / "settings.json", [])
    assert pi_config.package_entry_installed(cwd=tmp_path) is False


def test_project_entry_wins_over_global(agent_dir, tmp_path):
    _write(agent_dir / "settings.json", [{"source": pi_config.MIRROR_GIT_SOURCE}])
    _write(
        tmp_path / ".pi" / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": ["index.ts"]}],
    )
    entry = pi_config.merged_package_entry(cwd=tmp_path)
    assert entry.scope == "project"
    assert entry.extensions_filter == ["index.ts"]


def test_autoload_false_applies_as_a_delta_over_global(agent_dir, tmp_path):
    """pi's own rule (docs/packages.md, Scope and Deduplication)."""
    _write(
        agent_dir / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": ["index.ts"]}],
    )
    _write(
        tmp_path / ".pi" / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "autoload": False, "skills": []}],
    )
    entry = pi_config.merged_package_entry(cwd=tmp_path)
    assert entry.extensions_filter == ["index.ts"]
    assert entry.skills_filter == []


def test_an_empty_extensions_filter_excludes_our_extension(agent_dir, tmp_path):
    """The strand-ai shape."""
    _write(
        agent_dir / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": []}],
    )
    entry = pi_config.merged_package_entry(cwd=tmp_path)
    assert entry.installed is True
    assert entry.extension_filtered_out is True
    assert entry.scope == "global"


def test_no_filter_means_the_extension_loads(agent_dir, tmp_path):
    _write(agent_dir / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    entry = pi_config.merged_package_entry(cwd=tmp_path)
    assert entry.extension_filtered_out is False


def test_a_force_included_extension_path_is_not_filtered_out(agent_dir, tmp_path):
    """The shape seen on a live customer machine: a project entry that pins the
    mirror's own extension path with `+` (an exact force-include, per pi's
    docs/packages.md "Package Filtering"). That LOADS our extension -- reading
    it as filtered out would make doctor cry wolf on a healthy install."""
    _write(
        tmp_path / ".pi" / "settings.json",
        [
            {
                "source": pi_config.MIRROR_GIT_SOURCE,
                "autoload": False,
                "extensions": ["+plugins/probe-research-pi/index.ts"],
            }
        ],
    )
    entry = pi_config.merged_package_entry(cwd=tmp_path)
    assert entry.installed is True
    assert entry.scope == "project"
    assert entry.extension_filtered_out is False


def test_an_excluded_extension_path_does_not_count_as_loading_it(agent_dir, tmp_path):
    """`!pattern` excludes and `-path` force-excludes -- neither is evidence
    that anything loads our `index.ts`."""
    _write(
        agent_dir / "settings.json",
        [
            {
                "source": pi_config.MIRROR_GIT_SOURCE,
                "extensions": ["!plugins/probe-research-pi/index.ts"],
            }
        ],
    )
    assert pi_config.merged_package_entry(cwd=tmp_path).extension_filtered_out is True

    _write(
        agent_dir / "settings.json",
        [
            {
                "source": pi_config.MIRROR_GIT_SOURCE,
                "extensions": ["-plugins/probe-research-pi/index.ts"],
            }
        ],
    )
    assert pi_config.merged_package_entry(cwd=tmp_path).extension_filtered_out is True


def test_unreadable_project_settings_degrade_to_global(agent_dir, tmp_path):
    _write(agent_dir / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    bad = tmp_path / ".pi" / "settings.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text("{not json", encoding="utf-8")
    assert pi_config.package_entry_installed(cwd=tmp_path) is True


def test_existing_callers_keep_global_only_behaviour(agent_dir, tmp_path):
    """`cwd=None` is the pre-change contract: global settings, nothing else."""
    _write(agent_dir / "settings.json", [])
    _write(tmp_path / ".pi" / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    assert pi_config.package_entry_installed() is False
