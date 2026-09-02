"""Tests for cross-platform AI-client install probes."""

from __future__ import annotations

import plistlib
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest import mock

import pytest

from runlayer_cli.scan import client_presence as presence_module
from runlayer_cli.scan.client_presence import (
    DetectedClient,
    _windows_uninstall_entries,
    detect_client_presence,
    merge_client_presence,
)
from runlayer_cli.scan.clients import (
    ConfigPath,
    InstallProbe,
    MCPClientDefinition,
    NpmPackage,
    PipPackage,
    PlatformPath,
    get_client_by_name,
)
from runlayer_cli.scan.hidden_space_sweep import HiddenSpaceScanResult
from runlayer_cli.scan.wsl_limits import (
    MAX_WSL_CLIENT_CONTEXTS,
    MAX_WSL_HOMES,
    MAX_WSL_HOMES_TOTAL,
)
from runlayer_cli.scan.wsl_presence import (
    WSLBinaryFinding,
    WSLClientContext,
)


def _client(
    *,
    name: str = "test",
    display_name: str = "Test",
    paths: list[ConfigPath] | None = None,
    probe: InstallProbe | None = None,
) -> MCPClientDefinition:
    return MCPClientDefinition(
        name=name,
        display_name=display_name,
        paths=paths or [],
        install_probe=probe,
    )


def test_detected_client_caps_wsl_contexts_to_wire_limit():
    detected = DetectedClient(client="test", display_name="Test")

    for index in range(MAX_WSL_CLIENT_CONTEXTS + 1):
        detected.add_detection(
            "cli",
            wsl_context=WSLClientContext(
                distro=f"distro-{index}",
                user="alice",
            ),
        )

    assert len(detected.wsl_contexts) == MAX_WSL_CLIENT_CONTEXTS


def test_wsl_binary_finding_is_attributed_to_detected_client(
    tmp_path,
    monkeypatch,
):
    binary_path = tmp_path / "wsl" / "home" / "alice" / ".local" / "bin" / "claude"
    context = WSLClientContext(distro="Ubuntu", user="alice")
    distro = SimpleNamespace(name="Ubuntu", is_running=True)
    monkeypatch.setattr(presence_module, "_wsl_homes", lambda: [])
    monkeypatch.setattr(
        presence_module,
        "scan_wsl_cli_binaries",
        lambda *_args, **_kwargs: [
            WSLBinaryFinding(
                client="test",
                binary="claude",
                path=binary_path,
                context=context,
            )
        ],
    )

    detected = detect_client_presence(
        [_client(probe=InstallProbe(cli_binaries=["claude"]))],
        home=tmp_path,
        system="Windows",
        environment={},
        wsl_distros=[distro],
    )

    assert len(detected) == 1
    assert detected[0].detected_via == ["cli"]
    assert detected[0].config_paths == [str(binary_path)]
    assert detected[0].wsl_contexts == [context]


def test_macos_app_bundle_reads_info_plist_version(tmp_path, monkeypatch):
    applications = tmp_path / "Applications"
    bundle = applications / "Test.app"
    info_plist = bundle / "Contents" / "Info.plist"
    info_plist.parent.mkdir(parents=True)
    with info_plist.open("wb") as file:
        plistlib.dump({"CFBundleShortVersionString": "2.4.1"}, file)

    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._macos_app_roots",
        lambda _home: (applications,),
    )

    detected = detect_client_presence(
        [_client(probe=InstallProbe(macos_app_bundles=["Test.app"]))],
        home=tmp_path,
        system="Darwin",
    )

    assert detected == [
        DetectedClient(
            client="test",
            display_name="Test",
            client_version="2.4.1",
            detected_via=["app"],
        )
    ]


def test_renamed_shim_detected_by_resolved_target_identity(tmp_path):
    tool = tmp_path / "vendor" / "tarquin" / "norvex"
    tool.parent.mkdir(parents=True)
    tool.write_text("#!/bin/sh\n")
    tool.chmod(0o755)
    shim = tmp_path / ".local" / "bin" / "font-cache-refresh"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(tool)

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    cli_binaries=["norvex"],
                    probe_cli_version=False,
                )
            )
        ],
        home=tmp_path,
        system="Linux",
    )

    [client] = detected
    assert client.detected_via == ["cli"]
    assert client.config_paths == [str(tool.resolve())]


def test_renamed_npm_shim_detected_with_package_version(tmp_path):
    package_dir = tmp_path / "opt-tools" / "node_modules" / "@vex" / "quibler-cli"
    entry = package_dir / "bin" / "quibler.js"
    entry.parent.mkdir(parents=True)
    entry.write_text("console.log('hi')\n")
    (package_dir / "package.json").write_text(
        '{"name": "@vex/quibler-cli", "version": "9.9.1",'
        ' "bin": {"quibler": "bin/quibler.js"}}'
    )
    shim = tmp_path / ".local" / "bin" / "daily-report-sync"
    shim.parent.mkdir(parents=True)
    shim.symlink_to(entry)

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    npm_packages=[
                        NpmPackage(name="@vex/quibler-cli", bin_name="quibler")
                    ],
                )
            )
        ],
        home=tmp_path,
        system="Linux",
    )

    [client] = detected
    assert "cli" in client.detected_via
    assert client.client_version == "9.9.1"
    assert str(entry.resolve()) in client.config_paths


def test_linux_cli_uses_common_bin_dirs_and_bounded_version(tmp_path, monkeypatch):
    binary = tmp_path / ".local" / "bin" / "test-cli"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)

    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )
    version_probe = mock.Mock(return_value="1.7.0")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.get_cli_version",
        version_probe,
    )

    detected = detect_client_presence(
        [_client(probe=InstallProbe(cli_binaries=["test-cli"]))],
        home=tmp_path,
        system="Linux",
    )

    assert detected[0].detected_via == ["cli"]
    assert detected[0].client_version == "1.7.0"
    version_probe.assert_called_once_with(binary)


def test_global_npm_metadata_is_client_presence_with_package_version(tmp_path):
    package = NpmPackage("@vendor/test-cli", "test-cli")
    package_dir = (
        tmp_path
        / "anything"
        / "renamed-prefix"
        / "node_modules"
        / "@vendor"
        / "test-cli"
    )
    bin_target = package_dir / "bin" / "test-cli.js"
    bin_target.parent.mkdir(parents=True)
    bin_target.write_text("#!/usr/bin/env node\n")
    manifest = package_dir / "package.json"
    manifest.write_text(
        '{"name":"@vendor/test-cli","version":"2.4.6",'
        '"bin":{"test-cli":"bin/test-cli.js"}}'
    )

    detected = detect_client_presence(
        [_client(probe=InstallProbe(npm_packages=[package]))],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=[tmp_path / "anything" / "renamed-prefix" / "node_modules"],
    )

    assert detected == [
        DetectedClient(
            client="test",
            display_name="Test",
            client_version="2.4.6",
            detected_via=["npm_global"],
            config_paths=[str(manifest)],
        )
    ]


def test_malformed_npm_bin_target_does_not_abort_other_client_presence(tmp_path):
    malformed_package = NpmPackage("@vendor/malformed-cli", "malformed-cli")
    valid_package = NpmPackage("@vendor/valid-cli", "valid-cli")
    node_modules = tmp_path / "prefix" / "node_modules"

    malformed_dir = node_modules / "@vendor" / "malformed-cli"
    malformed_dir.mkdir(parents=True)
    malformed_manifest = malformed_dir / "package.json"
    malformed_manifest.write_text(
        '{"name":"@vendor/malformed-cli","version":"1.0.0",'
        '"bin":{"malformed-cli":"bin/malformed\\u0000.js"}}'
    )

    valid_dir = node_modules / "@vendor" / "valid-cli"
    valid_target = valid_dir / "bin" / "valid-cli.js"
    valid_target.parent.mkdir(parents=True)
    valid_target.write_text("#!/usr/bin/env node\n")
    valid_manifest = valid_dir / "package.json"
    valid_manifest.write_text(
        '{"name":"@vendor/valid-cli","version":"3.2.1",'
        '"bin":{"valid-cli":"bin/valid-cli.js"}}'
    )

    detected = detect_client_presence(
        [
            _client(
                name="malformed",
                display_name="Malformed",
                probe=InstallProbe(npm_packages=[malformed_package]),
            ),
            _client(
                name="valid",
                display_name="Valid",
                probe=InstallProbe(npm_packages=[valid_package]),
            ),
        ],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=[node_modules],
    )

    assert detected == [
        DetectedClient(
            client="valid",
            display_name="Valid",
            client_version="3.2.1",
            detected_via=["npm_global"],
            config_paths=[str(valid_manifest)],
        )
    ]


@pytest.mark.parametrize(
    "hidden_prefix",
    [".fontconfig-cache", ".gtk-icon-cache-bak"],
)
def test_global_npm_identity_is_found_below_generically_hidden_prefix(
    tmp_path,
    hidden_prefix,
):
    package = NpmPackage("@vendor/test-cli", "test-cli")
    package_dir = (
        tmp_path
        / ".cache"
        / hidden_prefix
        / "lib"
        / "node_modules"
        / "@vendor"
        / "test-cli"
    )
    bin_target = package_dir / "bin" / "test-cli.js"
    bin_target.parent.mkdir(parents=True)
    bin_target.write_text("#!/usr/bin/env node\n")
    manifest = package_dir / "package.json"
    manifest.write_text(
        '{"name":"@vendor/test-cli","version":"2.4.6",'
        '"bin":{"test-cli":"bin/test-cli.js"}}'
    )

    detected = detect_client_presence(
        [_client(probe=InstallProbe(npm_packages=[package]))],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert detected[0].detected_via == ["npm_global"]
    assert detected[0].config_paths == [str(manifest)]


def test_wsl_hidden_npm_identity_found_on_standalone_fallback_path(
    tmp_path,
    monkeypatch,
):
    """The fallback hidden sweep covers WSL homes like the orchestrator's does.

    Standalone callers (no precomputed hidden_space_result) pass
    discover_hidden=False to the npm probe, so hidden WSL node_modules are
    only reachable if the fallback sweep itself walks the WSL homes.
    """
    package = NpmPackage("@vendor/test-cli", "test-cli")
    windows_home = tmp_path / "windows-home"
    windows_home.mkdir()
    wsl_home = tmp_path / "wsl-home"
    package_dir = (
        wsl_home
        / ".cache"
        / ".fontconfig-cache"
        / "lib"
        / "node_modules"
        / "@vendor"
        / "test-cli"
    )
    bin_target = package_dir / "bin" / "test-cli.js"
    bin_target.parent.mkdir(parents=True)
    bin_target.write_text("#!/usr/bin/env node\n")
    manifest = package_dir / "package.json"
    manifest.write_text(
        '{"name":"@vendor/test-cli","version":"2.4.6",'
        '"bin":{"test-cli":"bin/test-cli.js"}}'
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._wsl_homes",
        lambda: [wsl_home],
    )

    detected = detect_client_presence(
        [_client(probe=InstallProbe(npm_packages=[package]))],
        home=windows_home,
        system="Windows",
        environment={},
    )

    assert detected[0].detected_via == ["npm_global"]
    assert detected[0].config_paths == [str(manifest)]


def test_package_fallback_caps_wsl_homes_before_hidden_sweep(
    tmp_path,
    monkeypatch,
):
    package = NpmPackage("@vendor/test-cli", "test-cli")
    homes = [tmp_path / f"wsl-home-{index}" for index in range(MAX_WSL_HOMES_TOTAL + 1)]
    captured_roots = []

    def capture_hidden_spaces(**kwargs):
        captured_roots.extend(kwargs["extra_home_roots"])
        return HiddenSpaceScanResult()

    monkeypatch.setattr(presence_module, "_wsl_homes", lambda: homes)
    monkeypatch.setattr(
        presence_module,
        "scan_hidden_spaces",
        capture_hidden_spaces,
    )
    monkeypatch.setattr(
        presence_module,
        "scan_npm_global_packages",
        lambda *_args, **_kwargs: {},
    )
    monkeypatch.setattr(
        presence_module,
        "scan_wsl_cli_binaries",
        lambda *_args, **_kwargs: [],
    )

    detect_client_presence(
        [_client(probe=InstallProbe(npm_packages=[package]))],
        home=tmp_path,
        system="Windows",
        environment={},
        wsl_distros=[],
    )

    assert captured_roots == homes[:MAX_WSL_HOMES_TOTAL]


def test_package_fallback_includes_homes_from_each_wsl_distro(
    tmp_path,
    monkeypatch,
):
    package = NpmPackage("@vendor/test-cli", "test-cli")
    homes = [
        Path(rf"\\wsl.localhost\Distro-{distro}\home\user-{user}")
        for distro in range(2)
        for user in range(MAX_WSL_HOMES)
    ]
    captured_roots = []

    def capture_hidden_spaces(**kwargs):
        captured_roots.extend(kwargs["extra_home_roots"])
        return HiddenSpaceScanResult()

    monkeypatch.setattr(presence_module, "_wsl_homes", lambda: homes)
    monkeypatch.setattr(
        presence_module,
        "scan_hidden_spaces",
        capture_hidden_spaces,
    )
    monkeypatch.setattr(
        presence_module,
        "scan_npm_global_packages",
        lambda *_args, **_kwargs: {},
    )
    monkeypatch.setattr(
        presence_module,
        "scan_wsl_cli_binaries",
        lambda *_args, **_kwargs: [],
    )

    detect_client_presence(
        [_client(probe=InstallProbe(npm_packages=[package]))],
        home=tmp_path,
        system="Windows",
        environment={},
        wsl_distros=[],
    )

    assert captured_roots == homes


def test_precomputed_hidden_package_roots_respect_wsl_home_cap(
    tmp_path,
    monkeypatch,
):
    npm_package = NpmPackage("@vendor/test-cli", "test-cli")
    pip_package = PipPackage("test-cli")
    homes = [
        Path(rf"\\wsl.localhost\Distro-{index}\home\alice")
        for index in range(MAX_WSL_HOMES_TOTAL + 1)
    ]
    host_node_modules = tmp_path / "host-cache" / "node_modules"
    host_python_env = tmp_path / "host-python"
    wsl_node_modules = [home / ".cache" / "node_modules" for home in homes]
    wsl_python_envs = [home / ".cache" / "venv" for home in homes]
    captured_node_modules = []
    captured_python_envs = []

    def capture_npm(_packages, **kwargs):
        captured_node_modules.extend(kwargs["node_modules_paths"])
        return {}

    def capture_pip(_packages, **kwargs):
        captured_python_envs.extend(kwargs["python_env_roots"])
        return {}

    monkeypatch.setattr(presence_module, "_wsl_homes", lambda: homes)
    monkeypatch.setattr(
        presence_module,
        "_windows_uninstall_entries",
        lambda **_kwargs: [],
    )
    monkeypatch.setattr(
        presence_module,
        "scan_npm_global_packages",
        capture_npm,
    )
    monkeypatch.setattr(
        presence_module,
        "scan_pip_global_packages",
        capture_pip,
    )
    monkeypatch.setattr(
        presence_module,
        "sweep_shim_identities",
        lambda **_kwargs: ({}, {}),
    )
    monkeypatch.setattr(
        presence_module,
        "scan_wsl_cli_binaries",
        lambda *_args, **_kwargs: [],
    )

    detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    npm_packages=[npm_package],
                    pip_packages=[pip_package],
                )
            )
        ],
        home=tmp_path,
        system="Windows",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(
            node_modules_paths=[host_node_modules, *wsl_node_modules],
            python_env_roots=[host_python_env, *wsl_python_envs],
        ),
        wsl_distros=[],
    )

    assert captured_node_modules == [
        host_node_modules,
        *wsl_node_modules[:MAX_WSL_HOMES_TOTAL],
    ]
    assert captured_python_envs == [
        host_python_env,
        *wsl_python_envs[:MAX_WSL_HOMES_TOTAL],
    ]


def test_hidden_and_project_node_modules_are_interleaved(monkeypatch, tmp_path):
    package = NpmPackage("@vendor/test-cli", "test-cli")
    hidden_paths = [
        tmp_path / "hidden-1" / "node_modules",
        tmp_path / "hidden-2" / "node_modules",
    ]
    project_paths = [
        tmp_path / "project-1" / "node_modules",
        tmp_path / "project-2" / "node_modules",
    ]
    captured_paths = []

    def capture_roots(_packages, **kwargs):
        captured_paths.extend(kwargs["node_modules_paths"])
        return {}

    monkeypatch.setattr(presence_module, "scan_npm_global_packages", capture_roots)

    detect_client_presence(
        [_client(probe=InstallProbe(npm_packages=[package]))],
        home=tmp_path,
        system="Linux",
        environment={},
        node_modules_paths=project_paths,
        hidden_space_result=HiddenSpaceScanResult(
            node_modules_paths=hidden_paths,
        ),
    )

    assert captured_paths == [
        hidden_paths[0],
        project_paths[0],
        hidden_paths[1],
        project_paths[1],
    ]


def test_pip_metadata_identity_is_client_presence_when_console_script_is_renamed(
    tmp_path,
):
    venv = tmp_path / ".cache" / ".updater-state" / "runtime"
    (venv / "pyvenv.cfg").parent.mkdir(parents=True)
    (venv / "pyvenv.cfg").write_text("home = /usr/bin")
    metadata = (
        venv
        / "lib"
        / "python3.13"
        / "site-packages"
        / "aider_chat-0.82.1.dist-info"
        / "METADATA"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text("Name: aider-chat\nVersion: 0.82.1\n")
    renamed_script = venv / "bin" / "colorprofile"
    renamed_script.parent.mkdir()
    renamed_script.write_text("#!/bin/sh\n")

    detected = detect_client_presence(
        [
            _client(
                name="aider",
                display_name="Aider",
                probe=InstallProbe(pip_packages=[PipPackage("aider-chat")]),
            )
        ],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert detected == [
        DetectedClient(
            client="aider",
            display_name="Aider",
            client_version="0.82.1",
            detected_via=["pip_global"],
            config_paths=[str(metadata)],
        )
    ]


def test_npm_version_precedes_cli_execution_and_methods_dedupe(tmp_path, monkeypatch):
    package = NpmPackage("@vendor/test-cli", "test-cli")
    package_dir = (
        tmp_path / ".npm-global" / "lib" / "node_modules" / "@vendor" / "test-cli"
    )
    package_bin = package_dir / "bin" / "test-cli.js"
    package_bin.parent.mkdir(parents=True)
    package_bin.write_text("#!/usr/bin/env node\n")
    manifest = package_dir / "package.json"
    manifest.write_text(
        '{"name":"@vendor/test-cli","version":"3.5.7",'
        '"bin":{"test-cli":"bin/test-cli.js"}}'
    )
    shim = tmp_path / ".local" / "bin" / "test-cli"
    shim.parent.mkdir(parents=True)
    shim.write_text("#!/bin/sh\n")
    shim.chmod(0o755)
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )
    version_probe = mock.Mock()
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.get_cli_version",
        version_probe,
    )

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    npm_packages=[package],
                    cli_binaries=["test-cli"],
                )
            )
        ],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert detected == [
        DetectedClient(
            client="test",
            display_name="Test",
            client_version="3.5.7",
            detected_via=["cli", "npm_global"],
            config_paths=[str(manifest)],
        )
    ]
    version_probe.assert_not_called()


def test_npm_backed_probe_never_executes_shim_when_metadata_is_absent(
    tmp_path, monkeypatch
):
    shim = tmp_path / ".local" / "bin" / "test-cli"
    shim.parent.mkdir(parents=True)
    shim.write_text("#!/bin/sh\n")
    shim.chmod(0o755)
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )
    version_probe = mock.Mock(return_value="unsafe-version")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.get_cli_version",
        version_probe,
    )

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    npm_packages=[NpmPackage("@vendor/test-cli", "test-cli")],
                    cli_binaries=["test-cli"],
                )
            )
        ],
        home=tmp_path,
        system="Linux",
        environment={},
    )

    assert detected == [
        DetectedClient(
            client="test",
            display_name="Test",
            detected_via=["cli"],
        )
    ]
    version_probe.assert_not_called()


def test_gui_launcher_probe_does_not_run_version_command(tmp_path, monkeypatch):
    binary = tmp_path / ".local" / "bin" / "test-gui"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )
    version_probe = mock.Mock()
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.get_cli_version",
        version_probe,
    )

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    cli_binaries=["test-gui"],
                    probe_cli_version=False,
                )
            )
        ],
        home=tmp_path,
        system="Linux",
    )

    assert detected[0].detected_via == ["cli"]
    assert detected[0].client_version is None
    version_probe.assert_not_called()


def test_linux_desktop_file_detects_gui_app(tmp_path, monkeypatch):
    applications = tmp_path / "share" / "applications"
    applications.mkdir(parents=True)
    (applications / "dev.test.Test.desktop").write_text("[Desktop Entry]\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._linux_desktop_roots",
        lambda _home: (applications,),
    )

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(linux_desktop_ids=["dev.test.Test"]),
            )
        ],
        home=tmp_path,
        system="Linux",
    )

    assert detected[0].detected_via == ["app"]


@pytest.mark.parametrize(
    "host_dir",
    [".vscode", ".cursor", ".windsurf", ".vscode-oss", ".vscode-server"],
)
def test_claude_code_extension_is_app_presence(tmp_path, monkeypatch, host_dir):
    extension = (
        tmp_path / host_dir / "extensions" / "anthropic.claude-code-2.1.42-win32-x64"
    )
    extension.mkdir(parents=True)
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.locate_cli_binary",
        lambda *_args, **_kwargs: None,
    )
    client = get_client_by_name("claude_code")

    assert client is not None
    assert detect_client_presence(
        [client],
        home=tmp_path,
        system="Windows",
        environment={"USERPROFILE": str(tmp_path)},
        include_current_user_registry=False,
    ) == [
        DetectedClient(
            client="claude_code",
            display_name="Claude Code",
            client_version="2.1.42",
            detected_via=["app"],
        )
    ]


def test_claude_code_vscode_insiders_extension_is_app_presence_on_macos(
    tmp_path, monkeypatch
):
    home = tmp_path / "Users" / "alice"
    extension = (
        home / ".vscode-insiders" / "extensions" / "Anthropic.Claude-Code-2.0.13"
    )
    extension.mkdir(parents=True)
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.locate_cli_binary",
        lambda *_args, **_kwargs: None,
    )
    client = get_client_by_name("claude_code")

    assert client is not None
    assert detect_client_presence([client], home=home, system="Darwin") == [
        DetectedClient(
            client="claude_code",
            display_name="Claude Code",
            client_version="2.0.13",
            detected_via=["app"],
        )
    ]


def test_vscode_extension_probe_ignores_other_extensions_and_files(tmp_path):
    extensions = tmp_path / ".vscode" / "extensions"
    (extensions / "anthropic.other-1.0.0").mkdir(parents=True)
    (extensions / "anthropic.claude-code-3.0.0-linux-x64").write_text("")
    client = _client(probe=InstallProbe(vscode_extension_ids=["anthropic.claude-code"]))

    assert detect_client_presence([client], home=tmp_path, system="Linux") == []


def test_vscode_extension_presence_allows_unparseable_version(tmp_path):
    extension = (
        tmp_path
        / ".vscode"
        / "extensions"
        / "anthropic.claude-code-prerelease-linux-x64"
    )
    extension.mkdir(parents=True)
    client = _client(probe=InstallProbe(vscode_extension_ids=["anthropic.claude-code"]))

    assert detect_client_presence([client], home=tmp_path, system="Linux") == [
        DetectedClient(
            client="test",
            display_name="Test",
            detected_via=["app"],
        )
    ]


def test_windows_wsl_extension_is_config_presence(tmp_path, monkeypatch):
    windows_home = tmp_path / "windows-home"
    windows_home.mkdir()
    wsl_home = tmp_path / "wsl-home"
    extension = (
        wsl_home
        / ".vscode-server"
        / "extensions"
        / "anthropic.claude-code-2.1.42-linux-x64"
    )
    extension.mkdir(parents=True)
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._wsl_homes",
        lambda: [wsl_home],
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence.locate_cli_binary",
        lambda *_args, **_kwargs: None,
    )
    client = get_client_by_name("claude_code")

    assert client is not None
    assert detect_client_presence(
        [client],
        home=windows_home,
        system="Windows",
        environment={"USERPROFILE": str(windows_home)},
        include_current_user_registry=False,
    ) == [
        DetectedClient(
            client="claude_code",
            display_name="Claude Code",
            client_version="2.1.42",
            detected_via=["config"],
            config_paths=[str(extension)],
        )
    ]


def test_existing_config_parent_is_trace_signal(tmp_path):
    config_dir = tmp_path / ".test"
    config_dir.mkdir()
    client = _client(
        paths=[ConfigPath("~/.test/config.json", platform="linux")],
    )

    detected = detect_client_presence([client], home=tmp_path, system="Linux")

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(config_dir)]


def test_shared_config_parent_can_be_suppressed(tmp_path):
    config_dir = tmp_path / ".shared"
    config_dir.mkdir()
    config_file = config_dir / "config.json"
    client = _client(
        paths=[ConfigPath("~/.shared/config.json", platform="linux")],
        probe=InstallProbe(probe_config_parents=False),
    )

    assert detect_client_presence([client], home=tmp_path, system="Linux") == []

    config_file.write_text("{}")
    detected = detect_client_presence([client], home=tmp_path, system="Linux")

    assert detected[0].detected_via == ["config"]
    assert detected[0].config_paths == [str(config_file)]


def test_home_parent_is_not_a_presence_signal(tmp_path):
    client = _client(
        paths=[ConfigPath("~/.test.json", platform="linux")],
    )

    assert detect_client_presence([client], home=tmp_path, system="Linux") == []


def test_presence_only_client_can_probe_config_dir(tmp_path):
    config_dir = tmp_path / ".presence-only"
    config_dir.mkdir()
    client = _client(
        paths=[],
        probe=InstallProbe(
            config_dirs=[
                PlatformPath("~/.presence-only", platform="linux"),
            ]
        ),
    )

    detected = detect_client_presence([client], home=tmp_path, system="Linux")

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(config_dir)]


def test_intellij_presence_expands_versioned_config_directory(tmp_path):
    config_dir = tmp_path / ".config" / "JetBrains" / "IdeaIC2025.2"
    config_dir.mkdir(parents=True)
    (config_dir / "options.xml").write_text("<application />")
    client = get_client_by_name("intellij_idea_community")

    assert client is not None
    detected = detect_client_presence([client], home=tmp_path, system="Linux")

    assert detected == [
        DetectedClient(
            client="intellij_idea_community",
            display_name="IntelliJ IDEA Community",
            detected_via=["trace"],
            config_paths=[str(config_dir)],
        )
    ]


def test_exact_non_runlayer_config_file_stays_config(tmp_path):
    config_file = tmp_path / ".test.conf.yml"
    config_file.write_text("model: test\n")
    client = _client(
        paths=[],
        probe=InstallProbe(
            config_files=[
                PlatformPath("~/.test.conf.yml", platform="all"),
            ]
        ),
    )

    detected = detect_client_presence([client], home=tmp_path, system="Linux")

    assert detected[0].detected_via == ["config"]
    assert detected[0].config_paths == [str(config_file)]


def test_explicit_config_file_does_not_use_parent_as_presence(tmp_path):
    config_dir = tmp_path / ".hermes"
    config_dir.mkdir()
    (config_dir / "config.toml").write_text("[global]\n")
    client = _client(
        probe=InstallProbe(
            config_files=[
                PlatformPath("~/.hermes/config.yaml", platform="all"),
            ]
        ),
    )

    assert detect_client_presence([client], home=tmp_path, system="Linux") == []


def test_hermes_runlayer_artifact_alone_is_ignored(tmp_path):
    config_file = tmp_path / ".hermes" / "config.yaml"
    config_file.parent.mkdir()
    config_file.write_text("hooks: {}\n")
    client = _client(
        name="hermes",
        paths=[],
        probe=InstallProbe(
            config_files=[
                PlatformPath("~/.hermes/config.yaml", platform="all"),
            ]
        ),
    )

    assert detect_client_presence([client], home=tmp_path, system="Linux") == []


@pytest.mark.parametrize(
    ("name", "config_template", "artifact_paths", "environment"),
    [
        (
            "cursor",
            "~/.cursor/mcp.json",
            (".cursor/hooks.json",),
            {},
        ),
        (
            "codex",
            "~/.codex/mcp.json",
            (".codex/hooks.json", ".codex/config.toml"),
            {},
        ),
        (
            "github_copilot_cli",
            "$COPILOT_HOME/mcp-config.json",
            ("copilot-home/settings.json",),
            {"COPILOT_HOME": "copilot-home"},
        ),
        (
            "github_copilot_cli",
            "~/.copilot/mcp-config.json",
            (".copilot/settings.json", ".copilot/hooks/runlayer.json"),
            {},
        ),
        (
            "grok_cli",
            "~/.grok/settings.json",
            (".grok/hooks/runlayer.json",),
            {},
        ),
        (
            "grok_cli",
            "$GROK_HOME/settings.json",
            ("grok-home/hooks/runlayer.json",),
            {"GROK_HOME": "grok-home"},
        ),
        (
            "vscode",
            "~/.config/Code/User/mcp.json",
            (".config/Code/User/settings.json",),
            {},
        ),
    ],
)
def test_runlayer_artifact_only_parent_is_ignored_then_other_child_restores_trace(
    tmp_path,
    name,
    config_template,
    artifact_paths,
    environment,
):
    resolved_environment = {
        key: str(tmp_path / value) for key, value in environment.items()
    }
    for relative_path in artifact_paths:
        artifact = tmp_path / relative_path
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("{}")
    client = _client(
        name=name,
        paths=[ConfigPath(config_template, platform="all")],
        probe=InstallProbe(
            config_dirs=[
                PlatformPath(config_template.rsplit("/", 1)[0], platform="all"),
            ]
        ),
    )

    assert (
        detect_client_presence(
            [client],
            home=tmp_path,
            system="Linux",
            environment=resolved_environment,
        )
        == []
    )

    config_parent = config_template.rsplit("/", 1)[0]
    if config_parent.startswith("~/"):
        parent = tmp_path / config_parent[2:]
    else:
        variable = config_parent.removeprefix("$")
        parent = tmp_path / environment[variable]
    (parent / "client-state.json").write_text("{}")

    detected = detect_client_presence(
        [client],
        home=tmp_path,
        system="Linux",
        environment=resolved_environment,
    )

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(parent)]


def test_codex_home_override_is_not_treated_as_runlayer_written(tmp_path):
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text("[features]\nhooks = true\n")
    client = _client(
        name="codex",
        paths=[],
        probe=InstallProbe(
            config_dirs=[
                PlatformPath("$CODEX_HOME", platform="all"),
            ]
        ),
    )

    detected = detect_client_presence(
        [client],
        home=tmp_path,
        system="Linux",
        environment={"CODEX_HOME": str(codex_home)},
    )

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(codex_home)]


def test_windows_codex_mdm_artifacts_alone_are_ignored(tmp_path):
    codex_home = tmp_path / ".codex"
    codex_home.mkdir()
    (codex_home / "hooks.json").write_text("{}")
    (codex_home / "managed_config.toml").write_text("[features]\nhooks = true\n")
    client = _client(
        name="codex",
        paths=[],
        probe=InstallProbe(
            config_dirs=[
                PlatformPath("%USERPROFILE%/.codex", platform="windows"),
            ]
        ),
    )

    detected = detect_client_presence(
        [client],
        home=tmp_path,
        system="Windows",
        environment={"USERPROFILE": str(tmp_path)},
    )

    assert detected == []


@pytest.mark.parametrize(
    ("system", "config_template", "settings_path", "environment"),
    [
        (
            "Darwin",
            "~/Library/Application Support/Code/User/mcp.json",
            "Library/Application Support/Code/User/settings.json",
            {},
        ),
        (
            "Windows",
            "%APPDATA%/Code/User/mcp.json",
            "AppData/Roaming/Code/User/settings.json",
            {"APPDATA": "AppData/Roaming"},
        ),
    ],
)
def test_vscode_platform_settings_alone_is_ignored(
    tmp_path,
    system,
    config_template,
    settings_path,
    environment,
):
    settings = tmp_path / settings_path
    settings.parent.mkdir(parents=True)
    settings.write_text("{}")
    resolved_environment = {
        key: str(tmp_path / value) for key, value in environment.items()
    }
    client = _client(
        name="vscode",
        paths=[ConfigPath(config_template, platform="all")],
    )

    assert (
        detect_client_presence(
            [client],
            home=tmp_path,
            system=system,
            environment=resolved_environment,
            include_current_user_registry=False,
        )
        == []
    )


def test_windows_registry_and_program_exe_are_detected(tmp_path, monkeypatch):
    programs = tmp_path / "Programs"
    install_dir = programs / "Test"
    install_dir.mkdir(parents=True)
    (install_dir / "Test.exe").write_bytes(b"")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._windows_uninstall_entries",
        lambda: [("Test Client (User)", "5.2.0")],
    )

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    windows_display_name_prefixes=["Test Client"],
                    windows_install_dirs=["%LOCALAPPDATA%/Programs/Test"],
                )
            )
        ],
        home=tmp_path,
        system="Windows",
    )

    assert detected[0].client_version == "5.2.0"
    assert detected[0].detected_via == ["app", "registry"]


def test_windows_probe_accepts_console_user_environment_and_registry_sid(
    tmp_path, monkeypatch
):
    console_home = tmp_path / "Users" / "alice"
    local_appdata = console_home / "AppData" / "Local"
    install_dir = local_appdata / "Programs" / "Test"
    install_dir.mkdir(parents=True)
    (install_dir / "Test.exe").write_bytes(b"")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "systemprofile"))

    seen: dict[str, str | None] = {}

    def registry_entries(user_sid=None):
        seen["user_sid"] = user_sid
        return [("Test Client (User)", "5.2.0")]

    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._windows_uninstall_entries",
        registry_entries,
    )

    detected = detect_client_presence(
        [
            _client(
                probe=InstallProbe(
                    windows_display_name_prefixes=["Test Client"],
                    windows_install_dirs=["%LOCALAPPDATA%/Programs/Test"],
                )
            )
        ],
        home=console_home,
        system="Windows",
        environment={
            "USERPROFILE": str(console_home),
            "APPDATA": str(console_home / "AppData" / "Roaming"),
            "LOCALAPPDATA": str(local_appdata),
        },
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert seen == {"user_sid": "S-1-5-21-1-2-3-1001"}
    assert detected[0].client_version == "5.2.0"
    assert detected[0].detected_via == ["app", "registry"]


def test_windows_dollar_environment_expansion_is_case_insensitive(tmp_path):
    copilot_home = tmp_path / "Copilot"
    config_path = copilot_home / "mcp-config.json"
    config_path.parent.mkdir()
    config_path.write_text("{}")

    detected = detect_client_presence(
        [_client(paths=[ConfigPath("$COPILOT_HOME/mcp-config.json", platform="all")])],
        home=tmp_path,
        system="Windows",
        environment={"copilot_home": str(copilot_home)},
        include_current_user_registry=False,
    )

    assert detected[0].config_paths == [str(config_path)]


def test_windows_registry_reader_checks_all_uninstall_hives(monkeypatch):
    hklm = object()
    hkcu = object()
    uninstall = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    wow = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    rows = {
        (hklm, uninstall): {"Native": {"DisplayName": "Native", "DisplayVersion": "1"}},
        (hklm, wow): {"Wow": {"DisplayName": "Wow", "DisplayVersion": "2"}},
        (hkcu, uninstall): {"User": {"DisplayName": "User", "DisplayVersion": "3"}},
    }

    class Key:
        def __init__(self, location, values=None):
            self.location = location
            self.values = values

    def open_key(parent, path):
        if isinstance(parent, Key):
            values = rows[parent.location][path]
            return Key(parent.location, values)
        location = (parent, path)
        if location not in rows:
            raise OSError
        return Key(location)

    def enum_key(key, index):
        try:
            return list(rows[key.location])[index]
        except IndexError as exc:
            raise OSError from exc

    def query_value(key, name):
        if name not in key.values:
            raise OSError
        return key.values[name], None

    fake_winreg = SimpleNamespace(
        HKEY_LOCAL_MACHINE=hklm,
        HKEY_CURRENT_USER=hkcu,
        OpenKey=open_key,
        EnumKey=enum_key,
        QueryValueEx=query_value,
        CloseKey=lambda _key: None,
    )
    monkeypatch.setitem(sys.modules, "winreg", fake_winreg)

    assert _windows_uninstall_entries() == [
        ("Native", "1"),
        ("Wow", "2"),
        ("User", "3"),
    ]


def test_windows_registry_reader_uses_supplied_user_hive(monkeypatch):
    hklm = object()
    hkcu = object()
    hku = object()
    sid = "S-1-5-21-1-2-3-1001"
    uninstall = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    rows = {
        (hklm, uninstall): {},
        (
            hklm,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        ): {},
        (hkcu, uninstall): {
            "System": {"DisplayName": "SYSTEM Client", "DisplayVersion": "0"}
        },
        (hku, rf"{sid}\{uninstall}"): {
            "User": {"DisplayName": "User Client", "DisplayVersion": "3"}
        },
    }

    class Key:
        def __init__(self, location, values=None):
            self.location = location
            self.values = values

    def open_key(parent, path):
        if isinstance(parent, Key):
            values = rows[parent.location][path]
            return Key(parent.location, values)
        location = (parent, path)
        if location not in rows:
            raise OSError
        return Key(location)

    def enum_key(key, index):
        try:
            return list(rows[key.location])[index]
        except IndexError as exc:
            raise OSError from exc

    def query_value(key, name):
        if name not in key.values:
            raise OSError
        return key.values[name], None

    fake_winreg = SimpleNamespace(
        HKEY_LOCAL_MACHINE=hklm,
        HKEY_CURRENT_USER=hkcu,
        HKEY_USERS=hku,
        OpenKey=open_key,
        EnumKey=enum_key,
        QueryValueEx=query_value,
        CloseKey=lambda _key: None,
    )
    monkeypatch.setitem(sys.modules, "winreg", fake_winreg)

    assert _windows_uninstall_entries(user_sid=sid) == [("User Client", "3")]


def test_windows_includes_wsl_linux_config_dirs(tmp_path, monkeypatch):
    config_dir = tmp_path / ".test"
    config_dir.mkdir()
    (config_dir / "state.json").write_text("{}")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._resolve_wsl_linux_paths",
        lambda _template: [config_dir / "config.json"],
    )
    client = _client(
        paths=[ConfigPath("~/.test/config.json", platform="linux")],
    )

    detected = detect_client_presence([client], home=tmp_path, system="Windows")

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(config_dir)]


def test_windows_includes_wsl_all_platform_state_dirs(tmp_path, monkeypatch):
    windows_home = tmp_path / "windows-home"
    windows_home.mkdir()
    config_dir = tmp_path / "wsl-home" / ".test"
    config_dir.mkdir(parents=True)
    (config_dir / "state.json").write_text("{}")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._resolve_wsl_linux_paths",
        lambda _template: [config_dir],
    )
    client = _client(
        probe=InstallProbe(
            config_dirs=[PlatformPath("~/.test", platform="all")],
        ),
    )

    detected = detect_client_presence(
        [client],
        home=windows_home,
        system="Windows",
    )

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(config_dir)]


def test_windows_wsl_runlayer_artifact_only_tree_is_ignored(tmp_path, monkeypatch):
    windows_home = tmp_path / "windows-home"
    windows_home.mkdir()
    wsl_home = tmp_path / "wsl-home"
    codex_dir = wsl_home / ".codex"
    codex_dir.mkdir(parents=True)
    (codex_dir / "hooks.json").write_text("{}")
    (codex_dir / "config.toml").write_text("[features]\nhooks = true\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._wsl_homes",
        lambda: [wsl_home],
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._resolve_wsl_linux_paths",
        lambda template: [wsl_home / template[2:]],
    )
    client = _client(
        name="codex",
        paths=[ConfigPath("~/.codex/mcp.json", platform="linux")],
    )

    assert (
        detect_client_presence(
            [client],
            home=windows_home,
            system="Windows",
            include_current_user_registry=False,
        )
        == []
    )

    (codex_dir / "sessions").mkdir()

    detected = detect_client_presence(
        [client],
        home=windows_home,
        system="Windows",
        include_current_user_registry=False,
    )

    assert detected[0].detected_via == ["trace"]
    assert detected[0].config_paths == [str(codex_dir)]


def test_windows_wsl_runlayer_config_file_is_not_config_evidence(tmp_path, monkeypatch):
    windows_home = tmp_path / "windows-home"
    windows_home.mkdir()
    wsl_home = tmp_path / "wsl-home"
    config_file = wsl_home / ".hermes" / "config.yaml"
    config_file.parent.mkdir(parents=True)
    config_file.write_text("hooks: {}\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._wsl_homes",
        lambda: [wsl_home],
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._resolve_wsl_linux_paths",
        lambda template: [wsl_home / template[2:]],
    )
    client = _client(
        name="hermes",
        paths=[],
        probe=InstallProbe(
            config_files=[
                PlatformPath("~/.hermes/config.yaml", platform="all"),
            ]
        ),
    )

    assert (
        detect_client_presence(
            [client],
            home=windows_home,
            system="Windows",
            include_current_user_registry=False,
        )
        == []
    )


def test_one_bad_client_probe_does_not_abort_remaining_clients(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._windows_uninstall_entries",
        lambda: [],
    )

    def resolve_wsl(template):
        if template == "~/.bad/config.json":
            raise RuntimeError("unavailable WSL home")
        return []

    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._resolve_wsl_linux_paths",
        resolve_wsl,
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda binary: f"C:/{binary}.exe" if binary in {"bad", "good"} else None,
    )
    bad = _client(
        name="bad",
        paths=[ConfigPath("~/.bad/config.json", platform="all")],
        probe=InstallProbe(cli_binaries=["bad"]),
    )
    good = _client(
        name="good",
        display_name="Good",
        probe=InstallProbe(cli_binaries=["good"]),
    )

    detected = detect_client_presence(
        [bad, good],
        home=tmp_path,
        system="Windows",
    )

    assert detected == [
        DetectedClient(
            client="bad",
            display_name="Test",
            detected_via=["cli"],
        ),
        DetectedClient(
            client="good",
            display_name="Good",
            detected_via=["cli"],
        ),
    ]


def test_merge_artifact_signals_uses_client_ids_and_includes_containers():
    clients = [
        _client(name="cursor", display_name="Cursor"),
        _client(name="gemini_cli", display_name="Gemini CLI"),
    ]
    configurations = [
        SimpleNamespace(
            client="cursor",
            client_version=None,
            config_path="/home/test/.cursor/mcp.json",
            config_scope="global",
            servers=[object()],
        ),
        SimpleNamespace(
            client="gemini_cli",
            config_path="/container/.gemini/settings.json",
            config_scope="container",
            servers=[object()],
        ),
    ]
    skills = [
        SimpleNamespace(tool="cursor"),
        SimpleNamespace(tool="multi"),
    ]
    plugins = [
        SimpleNamespace(client="gemini_cli", plugin_type="gemini_extension"),
    ]

    detected = merge_client_presence(
        [],
        clients=clients,
        configurations=configurations,
        skills=skills,
        plugins=plugins,
        extension_clients=["cursor"],
    )

    assert detected == [
        DetectedClient(
            client="cursor",
            display_name="Cursor",
            detected_via=["config", "server", "skill", "extension"],
            config_paths=["/home/test/.cursor/mcp.json"],
        ),
        DetectedClient(
            client="gemini_cli",
            display_name="Gemini CLI",
            detected_via=["container", "server", "extension"],
            config_paths=["/container/.gemini/settings.json"],
        ),
    ]


def test_merge_container_skill_marks_client_present():
    client = _client(name="goose", display_name="Goose")

    detected = merge_client_presence(
        [],
        clients=[client],
        skills=[SimpleNamespace(tool="goose", container_id="container-1")],
    )

    assert detected == [
        DetectedClient(
            client="goose",
            display_name="Goose",
            detected_via=["container", "skill"],
        )
    ]


def test_merge_container_agent_definition_marks_client_present():
    client = _client(name="codex", display_name="Codex")

    detected = merge_client_presence(
        [],
        clients=[client],
        agent_definitions=[SimpleNamespace(client="codex", container_id="container-1")],
    )

    assert detected == [
        DetectedClient(
            client="codex",
            display_name="Codex",
            detected_via=["container", "config"],
        )
    ]


def test_merge_host_agent_definition_marks_client_present():
    """A host-side agent definition (no container) still records a method.

    Regression: the loop only added "container" when ``container_id`` was set, so
    a host-only agent definition created an empty ``DetectedClient`` via
    ``result_for()`` and reported the client with an empty ``detected_via``. The
    backend persists that verbatim, so it also cleared any previously detected
    methods for the installation.
    """
    client = _client(name="codex", display_name="Codex")

    detected = merge_client_presence(
        [],
        clients=[client],
        agent_definitions=[SimpleNamespace(client="codex", container_id=None)],
    )

    assert detected == [
        DetectedClient(
            client="codex",
            display_name="Codex",
            detected_via=["config"],
        )
    ]


def test_merge_host_agent_definition_does_not_clear_probe_signal():
    """A host agent definition enriches, never blanks, an existing signal."""
    client = _client(name="codex", display_name="Codex")
    probed = DetectedClient(
        client="codex",
        display_name="Codex",
        detected_via=["app"],
    )

    detected = merge_client_presence(
        [probed],
        clients=[client],
        agent_definitions=[SimpleNamespace(client="codex", container_id=None)],
    )

    assert detected == [
        DetectedClient(
            client="codex",
            display_name="Codex",
            detected_via=["app", "config"],
        )
    ]


def test_merge_empty_config_file_is_client_presence():
    client = _client(name="opencode", display_name="OpenCode")
    config = SimpleNamespace(
        client="opencode",
        client_version=None,
        config_path="/home/test/.config/opencode/opencode.json",
        config_scope="global",
        servers=[],
    )

    detected = merge_client_presence(
        [],
        clients=[client],
        configurations=[config],
    )

    assert detected == [
        DetectedClient(
            client="opencode",
            display_name="OpenCode",
            detected_via=["config"],
            config_paths=["/home/test/.config/opencode/opencode.json"],
        )
    ]


def test_merge_wsl_config_uses_normalized_config_path():
    client = _client(name="cursor", display_name="Cursor")
    config = SimpleNamespace(
        client="cursor",
        client_version=None,
        config_path="/home/alice/.cursor/mcp.json",
        config_scope="wsl",
        servers=[object()],
    )

    detected = merge_client_presence(
        [],
        clients=[client],
        configurations=[config],
    )

    assert detected == [
        DetectedClient(
            client="cursor",
            display_name="Cursor",
            detected_via=["config", "server"],
            config_paths=["/home/alice/.cursor/mcp.json"],
        )
    ]
