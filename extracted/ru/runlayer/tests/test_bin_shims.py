"""Tests for the resolved-target shim identity sweep."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from runlayer_cli.scan import bin_shims
from runlayer_cli.scan.bin_shims import sweep_shim_identities
from runlayer_cli.scan.clients import NpmPackage


def _sweep(home: Path, **overrides):
    arguments = {
        "cli_basenames": ["norvex"],
        "npm_packages": {},
        "home": home,
        "system": "Linux",
        "environment": {},
        "include_host_dirs": False,
    }
    arguments.update(overrides)
    return sweep_shim_identities(**arguments)


def _real_tool(home: Path, name: str) -> Path:
    tool = home / "vendor" / "payload" / name
    tool.parent.mkdir(parents=True, exist_ok=True)
    tool.write_text("#!/bin/sh\n")
    tool.chmod(0o755)
    return tool


def test_renamed_shim_matches_resolved_cli_basename(tmp_path):
    tool = _real_tool(tmp_path, "norvex")
    shim = tmp_path / ".local" / "bin" / "gpu-cache-warmer"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(tool)

    by_basename, by_package = _sweep(tmp_path)

    [finding] = by_basename["norvex"]
    assert finding.shim_path == shim
    assert finding.target_path == tool.resolve()
    assert finding.version is None
    assert by_package == {}


def test_renamed_shim_matches_validated_npm_package_target(tmp_path):
    package_dir = tmp_path / "stash" / "node_modules" / "@quor" / "zenlit-cli"
    entry = package_dir / "dist" / "main.js"
    entry.parent.mkdir(parents=True)
    entry.write_text("console.log('hi')\n")
    (package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@quor/zenlit-cli",
                "version": "2.3.4",
                "bin": {"zenlit": "dist/main.js"},
            }
        )
    )
    shim = tmp_path / ".local" / "bin" / "spool-rotate"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(entry)

    by_basename, by_package = _sweep(
        tmp_path,
        cli_basenames=[],
        npm_packages={
            "@quor/zenlit-cli": NpmPackage(name="@quor/zenlit-cli", bin_name="zenlit")
        },
    )

    assert by_basename == {}
    [finding] = by_package["@quor/zenlit-cli"]
    assert finding.shim_path == shim
    assert finding.version == "2.3.4"


def test_shim_to_unknown_target_is_ignored(tmp_path):
    tool = _real_tool(tmp_path, "innocuous-utility")
    shim = tmp_path / ".local" / "bin" / "another-name"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(tool)

    by_basename, by_package = _sweep(tmp_path)

    assert by_basename == {}
    assert by_package == {}


def test_dangling_symlink_is_ignored(tmp_path):
    shim = tmp_path / ".local" / "bin" / "ghost-link"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(tmp_path / "does-not-exist" / "norvex")

    by_basename, by_package = _sweep(tmp_path)

    assert by_basename == {}
    assert by_package == {}


def test_npm_manifest_name_mismatch_rejects_finding(tmp_path):
    package_dir = tmp_path / "stash" / "node_modules" / "brellix-agent"
    entry = package_dir / "cli.js"
    entry.parent.mkdir(parents=True)
    entry.write_text("x\n")
    (package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "some-other-package",
                "version": "1.0.0",
                "bin": {"brellix": "cli.js"},
            }
        )
    )
    shim = tmp_path / ".local" / "bin" / "harmless"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(entry)

    by_basename, by_package = _sweep(
        tmp_path,
        cli_basenames=[],
        npm_packages={
            "brellix-agent": NpmPackage(name="brellix-agent", bin_name="brellix")
        },
    )

    assert by_basename == {}
    assert by_package == {}


def test_copied_renamed_binary_is_not_classified(tmp_path):
    tool = _real_tool(tmp_path, "norvex")
    copied = tmp_path / ".local" / "bin" / "gpu-cache-warmer"
    copied.parent.mkdir(parents=True)
    shutil.copy2(tool, copied)

    by_basename, by_package = _sweep(tmp_path)

    assert by_basename == {}
    assert by_package == {}


def test_path_dirs_swept_only_with_host_dirs_enabled(tmp_path):
    tool = _real_tool(tmp_path, "norvex")
    path_dir = tmp_path / "custom-tools"
    path_dir.mkdir()
    (path_dir / "warmup-task").symlink_to(tool)
    environment = {"PATH": str(path_dir)}

    excluded_basename, _ = _sweep(tmp_path, environment=environment)
    included_basename, _ = _sweep(
        tmp_path,
        environment=environment,
        include_host_dirs=True,
    )

    assert excluded_basename == {}
    assert "norvex" in included_basename


def test_entry_budget_bounds_directory_sweep(tmp_path, monkeypatch):
    monkeypatch.setattr(bin_shims, "MAX_ENTRIES_PER_DIR", 1)
    tool = _real_tool(tmp_path, "norvex")
    bin_dir = tmp_path / ".local" / "bin"
    bin_dir.mkdir(parents=True)
    for index in range(4):
        (bin_dir / f"entry-{index}").symlink_to(tool)

    by_basename, _ = _sweep(tmp_path)

    findings = by_basename.get("norvex", [])
    assert len(findings) <= 1


def test_windows_sweep_is_a_noop(tmp_path):
    by_basename, by_package = _sweep(tmp_path, system="Windows")

    assert by_basename == {}
    assert by_package == {}
