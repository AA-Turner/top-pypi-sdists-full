"""Tests for bounded, no-exec global npm package detection."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from unittest import mock

import pytest

from runlayer_cli.scan import npm_global as npm_global_module
from runlayer_cli.scan.clients import NpmPackage
from runlayer_cli.scan.npm_global import (
    MAX_NODE_MODULES_PATHS,
    MAX_PREFIXES,
    NpmGlobalPackage,
    resolve_npm_global_roots,
    scan_npm_global_packages,
)
from runlayer_cli.scan.wsl_limits import MAX_WSL_HOMES, MAX_WSL_HOMES_TOTAL

_ALLOWLISTED_PACKAGES = [
    NpmPackage("@anthropic-ai/claude-code", "claude"),
    NpmPackage("@openai/codex", "codex"),
    NpmPackage("@github/copilot", "copilot"),
    NpmPackage("@google/gemini-cli", "gemini"),
    NpmPackage("opencode-ai", "opencode"),
    NpmPackage("@smithery/cli", "smithery"),
]


def _install_package(
    prefix: Path,
    package: NpmPackage,
    *,
    version: str = "1.2.3",
    windows: bool = False,
) -> Path:
    node_modules = prefix / "node_modules" if windows else prefix / "lib/node_modules"
    package_dir = node_modules.joinpath(*package.name.split("/"))
    bin_target = Path("bin") / f"{package.bin_name}.js"
    target = package_dir / bin_target
    target.parent.mkdir(parents=True)
    target.write_text("#!/usr/bin/env node\n")
    manifest = package_dir / "package.json"
    manifest.write_text(
        json.dumps(
            {
                "name": package.name,
                "version": version,
                "bin": {package.bin_name: bin_target.as_posix()},
            }
        )
    )
    return manifest


def test_detects_allowlisted_package_under_user_npm_global_prefix(tmp_path):
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    manifest = _install_package(tmp_path / ".npm-global", package)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings == {
        package.name: NpmGlobalPackage(
            package_name=package.name,
            version="1.2.3",
            manifest_path=manifest,
        )
    }


def test_detects_package_from_npm_config_prefix(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    prefix = tmp_path / "custom-prefix"
    manifest = _install_package(prefix, package, version="2.3.4")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"NPM_CONFIG_PREFIX": str(prefix)},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="2.3.4",
        manifest_path=manifest,
    )


def test_detects_package_from_bounded_user_npmrc_prefix(tmp_path):
    package = NpmPackage("@google/gemini-cli", "gemini")
    prefix = tmp_path / ".hidden-prefix"
    manifest = _install_package(prefix, package, version="3.4.5")
    (tmp_path / ".npmrc").write_text("# user npm settings\nprefix = ~/.hidden-prefix\n")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="3.4.5",
        manifest_path=manifest,
    )


def test_npm_config_userconfig_selects_alternate_npmrc(tmp_path):
    package = NpmPackage("@google/gemini-cli", "gemini")
    prefix = tmp_path / "configured-prefix"
    manifest = _install_package(prefix, package, version="3.5.7")
    userconfig = tmp_path / "npm" / "user-config"
    userconfig.parent.mkdir()
    userconfig.write_text(f"prefix={prefix}\n")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"NPM_CONFIG_USERCONFIG": str(userconfig)},
    )

    assert findings[package.name].manifest_path == manifest


def test_npmrc_prefix_expands_explicit_home_variable(tmp_path):
    package = NpmPackage("@google/gemini-cli", "gemini")
    prefix = tmp_path / "variable-prefix"
    manifest = _install_package(prefix, package, version="3.5.8")
    (tmp_path / ".npmrc").write_text("prefix=${HOME}/variable-prefix\n")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name].manifest_path == manifest


def test_detects_package_from_unix_path_bin_parent(tmp_path):
    package = NpmPackage("opencode-ai", "opencode")
    prefix = tmp_path / "path-prefix"
    manifest = _install_package(prefix, package, version="4.5.6")
    (prefix / "bin").mkdir()

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"PATH": f"/missing/bin:{prefix / 'bin'}"},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="4.5.6",
        manifest_path=manifest,
    )


def test_detects_package_under_bounded_node_manager_root(tmp_path):
    package = NpmPackage("@github/copilot", "copilot")
    nvm_dir = tmp_path / "renamed-nvm-home"
    prefix = nvm_dir / "versions" / "node" / "v22.17.0"
    manifest = _install_package(prefix, package, version="5.6.7")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"NVM_DIR": str(nvm_dir)},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="5.6.7",
        manifest_path=manifest,
    )


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_symlinked_node_manager_prefix(tmp_path):
    package = NpmPackage("@github/copilot", "copilot")
    actual_prefix = tmp_path / "external-node"
    manifest = _install_package(actual_prefix, package, version="5.6.8")
    nvm_dir = tmp_path / "renamed-nvm-home"
    manager_root = nvm_dir / "versions" / "node"
    manager_root.mkdir(parents=True)
    (manager_root / "v22.17.0").symlink_to(
        actual_prefix,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"NVM_DIR": str(nvm_dir)},
        discover_hidden=False,
    )

    assert findings[package.name].manifest_path == manifest


def test_windows_system_scan_never_traverses_linked_manager_root(
    tmp_path,
    monkeypatch,
):
    package = NpmPackage("@github/copilot", "copilot")
    actual_manager = tmp_path / "external-manager"
    _install_package(actual_manager / "v22.17.0", package)
    nvm_dir = tmp_path / "renamed-nvm-home"
    manager_root = nvm_dir / "versions" / "node"
    manager_root.parent.mkdir(parents=True)
    manager_root.symlink_to(actual_manager, target_is_directory=True)
    original_scandir = os.scandir
    original_stat = Path.stat
    original_read = npm_global_module.read_bounded

    def guarded_scandir(path):
        candidate = Path(path)
        if candidate == manager_root or candidate == actual_manager:
            raise AssertionError("SYSTEM followed linked manager root")
        return original_scandir(path)

    def guarded_stat(path, *args, **kwargs):
        if path == actual_manager or actual_manager in path.parents:
            raise AssertionError("SYSTEM statted linked manager target")
        return original_stat(path, *args, **kwargs)

    def guarded_read(path, *, max_bytes):
        if path == actual_manager or actual_manager in path.parents:
            raise AssertionError("SYSTEM read linked manager target")
        return original_read(path, max_bytes=max_bytes)

    monkeypatch.setattr(
        npm_global_module,
        "is_windows_system_context",
        lambda: True,
    )
    monkeypatch.setattr(npm_global_module.os, "scandir", guarded_scandir)
    monkeypatch.setattr(Path, "stat", guarded_stat)
    monkeypatch.setattr(npm_global_module, "read_bounded", guarded_read)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"NVM_DIR": str(nvm_dir)},
        discover_hidden=False,
    )

    assert findings == {}


def test_windows_system_scan_keeps_real_manager_roots(tmp_path, monkeypatch):
    package = NpmPackage("@github/copilot", "copilot")
    prefix = tmp_path / ".nvm" / "versions" / "node" / "v22.17.0"
    manifest = _install_package(prefix, package)
    monkeypatch.setattr(
        npm_global_module,
        "is_windows_system_context",
        lambda: True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings[package.name].manifest_path == manifest


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_broken_manager_links_do_not_consume_prefix_cap(tmp_path):
    package = NpmPackage("@github/copilot", "copilot")
    manager_root = tmp_path / ".nvm" / "versions" / "node"
    manager_root.mkdir(parents=True)
    for index in range(npm_global_module.MAX_MANAGER_PREFIXES):
        (manager_root / f"a-broken-{index}").symlink_to(
            tmp_path / f"missing-{index}",
            target_is_directory=True,
        )
    prefix = manager_root / "z-valid"
    manifest = _install_package(prefix, package)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings[package.name].manifest_path == manifest


def test_detects_scoped_package_under_volta_package_image(tmp_path):
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    volta_home = tmp_path / "renamed-volta-home"
    prefix = volta_home / "tools" / "image" / "packages" / "@anthropic-ai/claude-code"
    manifest = _install_package(prefix, package, version="11.0.1")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={"VOLTA_HOME": str(volta_home)},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="11.0.1",
        manifest_path=manifest,
    )


def test_detects_package_under_default_volta_home_without_environment(tmp_path):
    package = NpmPackage("opencode-ai", "opencode")
    prefix = tmp_path / ".volta" / "tools" / "image" / "packages" / "opencode-ai"
    manifest = _install_package(prefix, package, version="11.0.2")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Darwin",
        environment={},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="11.0.2",
        manifest_path=manifest,
    )


def test_detects_windows_volta_package_image_layout(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    volta_home = tmp_path / "AppData" / "Local" / "Volta"
    prefix = volta_home / "tools" / "image" / "packages" / "@openai/codex"
    manifest = _install_package(prefix, package, version="11.0.3", windows=True)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Windows",
        environment={"VOLTA_HOME": str(volta_home)},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="11.0.3",
        manifest_path=manifest,
    )


def test_detects_package_under_windows_default_npm_prefix(tmp_path):
    package = NpmPackage("@smithery/cli", "smithery")
    app_data = tmp_path / "AppData" / "Roaming"
    prefix = app_data / "npm"
    manifest = _install_package(prefix, package, version="6.7.8", windows=True)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Windows",
        environment={"APPDATA": str(app_data)},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="6.7.8",
        manifest_path=manifest,
    )


@pytest.mark.parametrize(
    ("system", "relative_prefix", "windows"),
    [
        ("Linux", ".nvm/versions/node/v22.17.0", False),
        (
            "Darwin",
            "Library/Application Support/fnm/node-versions/v20.11.1/installation",
            False,
        ),
        ("Windows", "AppData/Roaming/nvm/v22.17.0", True),
    ],
)
def test_detects_package_under_default_manager_root_without_environment(
    tmp_path,
    system,
    relative_prefix,
    windows,
):
    """Hook install and WSL probes carry no shell env, so defaults must hit."""
    package = NpmPackage("@github/copilot", "copilot")
    prefix = tmp_path / relative_prefix
    manifest = _install_package(prefix, package, version="5.6.8", windows=windows)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system=system,
        environment={},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="5.6.8",
        manifest_path=manifest,
    )


@pytest.mark.parametrize(
    ("system", "relative_prefix", "environment", "windows"),
    [
        ("Linux", ".local/share/.fontconfig-cache", {}, False),
        ("Windows", "AppData/Local/PrintSpoolerCache/v2", {}, True),
        (
            "Windows",
            "AppData/Local/PrintSpoolerCache/v2",
            {"LOCALAPPDATA": "AppData/Local"},
            True,
        ),
    ],
)
def test_detects_metadata_under_structural_user_anchors(
    tmp_path,
    system,
    relative_prefix,
    environment,
    windows,
):
    package = NpmPackage("@openai/codex", "codex")
    prefix = tmp_path / relative_prefix
    manifest = _install_package(prefix, package, version="7.8.9", windows=windows)
    resolved_environment = {
        key: str(tmp_path / value) for key, value in environment.items()
    }

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system=system,
        environment=resolved_environment,
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="7.8.9",
        manifest_path=manifest,
    )


@pytest.mark.parametrize("package", _ALLOWLISTED_PACKAGES, ids=lambda item: item.name)
@pytest.mark.parametrize(
    ("system", "relative_prefix", "windows"),
    [
        ("Linux", ".local/share/.fontconfig-cache", False),
        ("Windows", "AppData/Local/PrintSpoolerCache/v2", True),
    ],
)
def test_every_allowlisted_package_is_detected_under_required_anchors(
    tmp_path,
    package,
    system,
    relative_prefix,
    windows,
):
    prefix = tmp_path / relative_prefix
    _install_package(prefix, package, version="10.11.12", windows=windows)

    findings = scan_npm_global_packages(
        _ALLOWLISTED_PACKAGES,
        home=tmp_path,
        system=system,
        environment={},
    )

    assert findings[package.name].version == "10.11.12"


def test_detects_metadata_under_arbitrary_crawled_node_modules(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    prefix = tmp_path / "anything" / "can-be-renamed"
    manifest = _install_package(prefix, package, version="7.8.9")
    node_modules = prefix / "lib" / "node_modules"

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=[node_modules],
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="7.8.9",
        manifest_path=manifest,
    )


def test_detects_metadata_under_arbitrarily_named_hidden_prefix(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    prefix = tmp_path / ".cache" / ".gtk-icon-cache-bak"
    manifest = _install_package(prefix, package, version="7.8.9")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="7.8.9",
        manifest_path=manifest,
    )


@pytest.mark.parametrize("package", _ALLOWLISTED_PACKAGES, ids=lambda item: item.name)
def test_every_allowlisted_package_is_detected_under_arbitrary_crawled_root(
    tmp_path,
    package,
):
    prefix = tmp_path / "renamed" / package.bin_name
    _install_package(prefix, package, version="10.11.12")

    findings = scan_npm_global_packages(
        _ALLOWLISTED_PACKAGES,
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=[prefix / "lib" / "node_modules"],
    )

    assert findings[package.name].version == "10.11.12"


def test_empty_crawled_node_modules_is_not_product_identity(tmp_path):
    node_modules = tmp_path / "renamed" / "node_modules"
    node_modules.mkdir(parents=True)

    findings = scan_npm_global_packages(
        [NpmPackage("@openai/codex", "codex")],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=[node_modules],
    )

    assert findings == {}


def test_windows_scan_includes_wsl_user_npm_roots(tmp_path):
    package = NpmPackage("@google/gemini-cli", "gemini")
    windows_home = tmp_path / "windows-home"
    wsl_home = tmp_path / "wsl-home"
    manifest = _install_package(
        wsl_home / ".npm-global",
        package,
        version="8.9.0",
    )

    findings = scan_npm_global_packages(
        [package],
        home=windows_home,
        system="Windows",
        environment={},
        wsl_homes=[wsl_home],
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="8.9.0",
        manifest_path=manifest,
    )


def test_windows_scan_includes_npm_root_after_first_distro_home_cap(tmp_path):
    package = NpmPackage("@google/gemini-cli", "gemini")
    first_distro_homes = [
        tmp_path / "Distro-0" / "home" / f"user-{index}"
        for index in range(MAX_WSL_HOMES)
    ]
    later_distro_home = tmp_path / "Distro-1" / "home" / "alice"
    manifest = _install_package(
        later_distro_home / ".npm-global",
        package,
        version="8.9.1",
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path / "windows-home",
        system="Windows",
        environment={},
        wsl_homes=[*first_distro_homes, later_distro_home],
        discover_hidden=False,
    )

    assert findings[package.name].manifest_path == manifest


@pytest.mark.parametrize(
    "relative_prefix",
    [
        ".nvm/versions/node/v22.17.0",
        ".local/share/.fontconfig-cache",
    ],
)
def test_windows_scan_includes_wsl_manager_and_anchor_roots(
    tmp_path,
    relative_prefix,
):
    """WSL trees see neither the home crawl nor the user's shell env."""
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    wsl_home = tmp_path / "wsl-home"
    manifest = _install_package(
        wsl_home / relative_prefix,
        package,
        version="8.9.1",
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path / "windows-home",
        system="Windows",
        environment={},
        wsl_homes=[wsl_home],
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="8.9.1",
        manifest_path=manifest,
    )


@pytest.mark.parametrize(
    "invalid_case",
    [
        "malformed",
        "oversized",
        "wrong_name",
        "missing_expected_bin",
        "absolute_bin",
        "escaping_bin",
        "nul_bin",
        "control_bin",
        "invalid_version",
    ],
)
def test_rejects_untrusted_or_unbounded_package_metadata(tmp_path, invalid_case):
    package = NpmPackage("@openai/codex", "codex")
    prefix = tmp_path / ".npm-global"
    manifest = _install_package(prefix, package)
    data = {
        "name": package.name,
        "version": "1.2.3",
        "bin": {package.bin_name: "bin/codex.js"},
    }
    if invalid_case == "malformed":
        manifest.write_text("{")
    elif invalid_case == "oversized":
        manifest.write_bytes(b" " * (513 * 1024))
    else:
        if invalid_case == "wrong_name":
            data["name"] = "@openai/not-codex"
        elif invalid_case == "missing_expected_bin":
            data["bin"] = {"other": "bin/codex.js"}
        elif invalid_case == "absolute_bin":
            data["bin"] = {package.bin_name: "/tmp/codex.js"}
        elif invalid_case == "escaping_bin":
            data["bin"] = {package.bin_name: "../codex.js"}
            (manifest.parent.parent / "codex.js").write_text("outside\n")
        elif invalid_case == "nul_bin":
            data["bin"] = {package.bin_name: "bin/co\x00dex.js"}
        elif invalid_case == "control_bin":
            data["bin"] = {package.bin_name: "bin/co\ndex.js"}
        elif invalid_case == "invalid_version":
            data["version"] = "v" * 129
        manifest.write_text(json.dumps(data))

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_external_symlinked_package(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    outside_manifest = _install_package(tmp_path / "outside", package)
    package_parent = tmp_path / ".npm-global" / "lib/node_modules" / "@openai"
    package_parent.mkdir(parents=True)
    (package_parent / "codex").symlink_to(
        outside_manifest.parent,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="1.2.3",
        manifest_path=outside_manifest,
    )


def test_windows_system_scan_skips_symlinked_package(tmp_path, monkeypatch):
    package = NpmPackage("@openai/codex", "codex")
    outside_prefix = tmp_path / "outside"
    outside_package = _install_package(outside_prefix, package).parent
    package_parent = tmp_path / ".npm-global" / "lib/node_modules" / "@openai"
    package_parent.mkdir(parents=True)
    (package_parent / "codex").symlink_to(outside_package, target_is_directory=True)
    original_stat = Path.stat
    original_read = npm_global_module.read_bounded

    def guarded_stat(path, *args, **kwargs):
        if path == outside_package or outside_package in path.parents:
            raise AssertionError("SYSTEM statted linked package target")
        return original_stat(path, *args, **kwargs)

    def guarded_read(path, *, max_bytes):
        if path == outside_package or outside_package in path.parents:
            raise AssertionError("SYSTEM read linked package target")
        return original_read(path, max_bytes=max_bytes)

    monkeypatch.setattr(
        npm_global_module,
        "is_windows_system_context",
        lambda: True,
    )
    monkeypatch.setattr(Path, "stat", guarded_stat)
    monkeypatch.setattr(npm_global_module, "read_bounded", guarded_read)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings == {}


def test_user_scan_follows_symlinked_prefix(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    outside_prefix = tmp_path / "outside"
    outside_manifest = _install_package(outside_prefix, package)
    (tmp_path / ".npm-global").symlink_to(
        outside_prefix,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name].manifest_path == outside_manifest


def test_symlinked_prefix_is_resolved_once_for_all_packages(tmp_path):
    packages = [
        NpmPackage("@openai/codex", "codex"),
        NpmPackage("@github/copilot", "copilot"),
    ]
    actual_prefix = tmp_path / "outside"
    manifests = {
        package.name: _install_package(actual_prefix, package) for package in packages
    }
    (tmp_path / ".npm-global").symlink_to(
        actual_prefix,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        packages,
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert {
        package_name: finding.manifest_path
        for package_name, finding in findings.items()
    } == manifests


def test_user_scan_follows_symlinked_lib_component(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    outside_prefix = tmp_path / "outside"
    outside_manifest = _install_package(outside_prefix, package)
    prefix = tmp_path / ".npm-global"
    prefix.mkdir()
    (prefix / "lib").symlink_to(
        outside_prefix / "lib",
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name].manifest_path == outside_manifest


def test_user_scan_follows_symlinked_node_modules_component(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    outside_prefix = tmp_path / "outside"
    outside_manifest = _install_package(outside_prefix, package)
    lib = tmp_path / ".npm-global" / "lib"
    lib.mkdir(parents=True)
    (lib / "node_modules").symlink_to(
        outside_prefix / "lib" / "node_modules",
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name].manifest_path == outside_manifest


def test_user_scan_follows_symlinked_package_scope_component(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    outside_prefix = tmp_path / "outside"
    outside_manifest = _install_package(outside_prefix, package)
    node_modules = tmp_path / ".npm-global" / "lib" / "node_modules"
    node_modules.mkdir(parents=True)
    (node_modules / "@openai").symlink_to(
        outside_prefix / "lib" / "node_modules" / "@openai",
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert findings[package.name].manifest_path == outside_manifest


def test_user_scan_follows_symlinked_direct_root_ancestor(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    outside_prefix = tmp_path / "outside-prefix"
    outside_manifest = _install_package(outside_prefix, package)
    linked_prefix = tmp_path / "renamed-prefix"
    linked_prefix.symlink_to(
        outside_prefix,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=[linked_prefix / "lib" / "node_modules"],
    )

    assert findings[package.name].manifest_path == outside_manifest


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_follows_unvisited_package_target_inside_node_modules(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    seed_manifest = _install_package(tmp_path / "seed", package)
    node_modules = tmp_path / ".npm-global" / "lib" / "node_modules"
    actual_package = node_modules / "staged" / "codex"
    actual_package.parent.mkdir(parents=True)
    seed_manifest.parent.rename(actual_package)
    package_parent = node_modules / "@openai"
    package_parent.mkdir()
    (package_parent / "codex").symlink_to(
        actual_package,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings[package.name].manifest_path == actual_package / "package.json"


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_rejects_symlinked_manifest(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    manifest = _install_package(tmp_path / ".npm-global", package)
    external_manifest = tmp_path / "external-metadata" / "package.json"
    external_manifest.parent.mkdir()
    external_manifest.write_bytes(manifest.read_bytes())
    manifest.unlink()
    manifest.symlink_to(external_manifest)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_rejects_external_symlinked_bin_target(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    manifest = _install_package(tmp_path / ".npm-global", package)
    bin_target = manifest.parent / "bin" / "codex.js"
    external_target = tmp_path / "external-bin" / "codex.js"
    external_target.parent.mkdir()
    external_target.write_bytes(bin_target.read_bytes())
    bin_target.unlink()
    bin_target.symlink_to(external_target)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_rejects_internal_symlinked_bin_target(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    manifest = _install_package(tmp_path / ".npm-global", package)
    bin_target = manifest.parent / "bin" / "codex.js"
    internal_target = manifest.parent / "lib" / "codex.js"
    internal_target.parent.mkdir()
    internal_target.write_bytes(bin_target.read_bytes())
    bin_target.unlink()
    bin_target.symlink_to(internal_target)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_skips_broken_and_looped_package_links(tmp_path):
    node_modules = tmp_path / ".npm-global" / "lib" / "node_modules"
    node_modules.mkdir(parents=True)
    broken = node_modules / "broken-package"
    broken.symlink_to(tmp_path / "missing", target_is_directory=True)
    looped = node_modules / "looped-package"
    loop_peer = tmp_path / "loop-peer"
    looped.symlink_to(loop_peer, target_is_directory=True)
    loop_peer.symlink_to(looped, target_is_directory=True)

    findings = scan_npm_global_packages(
        [
            NpmPackage("broken-package", "broken"),
            NpmPackage("looped-package", "looped"),
        ],
        home=tmp_path,
        system="Linux",
        environment={},
        discover_hidden=False,
    )

    assert findings == {}


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_user_scan_caps_followed_package_targets(tmp_path):
    node_modules = tmp_path / ".npm-global" / "lib" / "node_modules"
    node_modules.mkdir(parents=True)
    packages = [
        NpmPackage(f"external-package-{index:02}", f"tool-{index:02}")
        for index in range(npm_global_module.MAX_FOLLOWED_SYMLINK_TARGETS + 1)
    ]
    for package in packages:
        outside_manifest = _install_package(
            tmp_path / "outside" / package.name,
            package,
        )
        (node_modules / package.name).symlink_to(
            outside_manifest.parent,
            target_is_directory=True,
        )

    findings = scan_npm_global_packages(
        packages,
        home=tmp_path,
        system="Linux",
        environment={"NPM_CONFIG_PREFIX": str(tmp_path / ".npm-global")},
        discover_hidden=False,
    )

    assert tuple(findings) == tuple(
        package.name
        for package in packages[: npm_global_module.MAX_FOLLOWED_SYMLINK_TARGETS]
    )


@pytest.mark.skipif(os.name == "nt", reason="symlink setup requires privileges")
def test_invalid_package_links_do_not_consume_follow_cap(tmp_path):
    node_modules = tmp_path / ".npm-global" / "lib" / "node_modules"
    node_modules.mkdir(parents=True)
    invalid_packages = [
        NpmPackage(f"invalid-package-{index:02}", f"tool-{index:02}")
        for index in range(npm_global_module.MAX_FOLLOWED_SYMLINK_TARGETS)
    ]
    valid_package = NpmPackage("valid-package", "valid-tool")
    for package in invalid_packages:
        outside_manifest = _install_package(
            tmp_path / "outside" / package.name,
            package,
        )
        manifest = json.loads(outside_manifest.read_text())
        manifest["name"] = "wrong-package"
        outside_manifest.write_text(json.dumps(manifest))
        (node_modules / package.name).symlink_to(
            outside_manifest.parent,
            target_is_directory=True,
        )
    valid_manifest = _install_package(
        tmp_path / "outside" / valid_package.name,
        valid_package,
    )
    (node_modules / valid_package.name).symlink_to(
        valid_manifest.parent,
        target_is_directory=True,
    )

    findings = scan_npm_global_packages(
        [*invalid_packages, valid_package],
        home=tmp_path,
        system="Linux",
        environment={"NPM_CONFIG_PREFIX": str(tmp_path / ".npm-global")},
        discover_hidden=False,
    )

    assert tuple(findings) == (valid_package.name,)


def test_explicit_prefix_wins_duplicate_windows_package_versions(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    explicit_prefix = tmp_path / "explicit"
    app_data = tmp_path / "AppData" / "Roaming"
    expected_manifest = _install_package(
        explicit_prefix,
        package,
        version="9.0.0",
        windows=True,
    )
    _install_package(app_data / "npm", package, version="1.0.0", windows=True)

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Windows",
        environment={
            "APPDATA": str(app_data),
            "NPM_CONFIG_PREFIX": str(explicit_prefix),
        },
    )

    assert findings[package.name] == NpmGlobalPackage(
        package_name=package.name,
        version="9.0.0",
        manifest_path=expected_manifest,
    )


def test_candidate_prefixes_and_manager_entries_are_bounded(tmp_path):
    nvm_dir = tmp_path / "renamed-nvm-home"
    for index in range(100):
        (nvm_dir / "versions" / "node" / f"v{index}").mkdir(parents=True)
    path_entries = [str(tmp_path / f"path-{index}" / "bin") for index in range(100)]

    roots = resolve_npm_global_roots(
        home=tmp_path,
        system="Linux",
        environment={
            "NVM_DIR": str(nvm_dir),
            "PATH": ":".join(path_entries),
        },
    )

    assert len(roots) <= MAX_PREFIXES
    assert (
        len(
            [
                root
                for root in roots
                if root.prefix.parent == nvm_dir / "versions" / "node"
            ]
        )
        <= 8
    )


def test_overflowing_manager_directory_processes_bounded_prefix(tmp_path):
    nvm_dir = tmp_path / "renamed-nvm-home"
    manager_root = nvm_dir / "versions" / "node"
    for index in range(65):
        (manager_root / f"v{index:02}" / "lib" / "node_modules").mkdir(parents=True)

    roots = resolve_npm_global_roots(
        home=tmp_path,
        system="Linux",
        environment={"NVM_DIR": str(nvm_dir)},
    )

    manager_roots = [root for root in roots if root.prefix.parent == manager_root]
    assert len(manager_roots) == npm_global_module.MAX_MANAGER_PREFIXES


def test_wsl_home_iterator_is_capped_before_materialization(tmp_path):
    def wsl_homes():
        for index in range(MAX_WSL_HOMES_TOTAL):
            yield tmp_path / f"wsl-{index}"
        raise AssertionError("WSL home iterator exceeded cap")

    roots = resolve_npm_global_roots(
        home=tmp_path / "windows",
        system="Windows",
        environment={},
        wsl_homes=wsl_homes(),
    )

    assert any(root.layout == "unix" for root in roots)


def test_direct_node_modules_iterator_is_capped_before_materialization(tmp_path):
    package = NpmPackage("@openai/codex", "codex")

    def node_modules_paths():
        for index in range(MAX_NODE_MODULES_PATHS):
            yield tmp_path / f"prefix-{index}" / "node_modules"
        raise AssertionError("node_modules iterator exceeded cap")

    findings = scan_npm_global_packages(
        [package],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=node_modules_paths(),
    )

    assert findings == {}


def test_scan_propagates_resource_checkpoint(tmp_path):
    class ResourceLimitReached(Exception):
        pass

    def checkpoint() -> None:
        raise ResourceLimitReached

    with pytest.raises(ResourceLimitReached):
        scan_npm_global_packages(
            [NpmPackage("@openai/codex", "codex")],
            home=tmp_path,
            system="Linux",
            environment={},
            discover_hidden=False,
            checkpoint=checkpoint,
        )


def test_permission_error_is_isolated_to_the_unreadable_manifest(tmp_path, monkeypatch):
    package = NpmPackage("@openai/codex", "codex")
    manifest = _install_package(tmp_path / ".npm-global", package)
    original = os.open

    def open_file(path, *args, **kwargs):
        if Path(path) == manifest:
            raise PermissionError
        return original(path, *args, **kwargs)

    monkeypatch.setattr(os, "open", open_file)

    assert (
        scan_npm_global_packages(
            [package],
            home=tmp_path,
            system="Linux",
            environment={},
        )
        == {}
    )


def test_scanner_never_executes_npm_node_or_package_shims(tmp_path):
    package = NpmPackage("@openai/codex", "codex")
    _install_package(tmp_path / ".npm-global", package)

    with mock.patch.object(
        subprocess,
        "run",
        side_effect=AssertionError("scanner must not execute subprocesses"),
    ) as run:
        findings = scan_npm_global_packages(
            [package],
            home=tmp_path,
            system="Linux",
            environment={},
        )

    assert package.name in findings
    run.assert_not_called()
