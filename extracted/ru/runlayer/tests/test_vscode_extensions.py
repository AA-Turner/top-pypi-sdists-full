"""Behavior tests for VS Code-family extension inventory."""

import json
import platform
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import orchestrator
from runlayer_cli.scan import vscode_extensions as vscode_extensions_module
from runlayer_cli.scan.completeness import ScanCompletionStatus
from runlayer_cli.scan.vscode_extensions import scan_vscode_extensions
from tests.hostile_inputs import DEEP_NESTING_BYTES

_DEFAULT_BUILTIN_ROOT_LAYOUTS = vscode_extensions_module._BUILTIN_ROOT_LAYOUTS


def _write_extension(
    home: Path,
    host_dir: str,
    folder: str,
    manifest: dict[str, object],
) -> Path:
    extension_dir = home / host_dir / "extensions" / folder
    extension_dir.mkdir(parents=True)
    (extension_dir / "package.json").write_text(json.dumps(manifest))
    return extension_dir


def _write_builtin_extension(
    root: Path,
    folder: str,
    manifest: dict[str, object],
) -> Path:
    extension_dir = root / folder
    extension_dir.mkdir(parents=True)
    (extension_dir / "package.json").write_text(json.dumps(manifest))
    return extension_dir


def _absolute_builtin_layout(
    root: Path,
) -> dict[str, vscode_extensions_module._BuiltinRootLayout]:
    return {"Darwin": (("vscode", Path(root.name), (("absolute", str(root.parent)),)),)}


@pytest.fixture(autouse=True)
def _isolate_system_builtin_roots(monkeypatch):
    home_layouts = {
        system: tuple(
            (
                client,
                app_tail,
                tuple(base for base in base_dirs if base[0] != "absolute"),
            )
            for client, app_tail, base_dirs in layout
        )
        for system, layout in vscode_extensions_module._BUILTIN_ROOT_LAYOUTS.items()
    }
    monkeypatch.setattr(vscode_extensions_module, "_BUILTIN_ROOT_LAYOUTS", home_layouts)
    monkeypatch.delenv("ProgramFiles", raising=False)
    monkeypatch.delenv("ProgramFiles(x86)", raising=False)


def test_scan_vscode_extensions_inventories_builtin_copilot(
    monkeypatch,
    tmp_path: Path,
):
    builtin_root = tmp_path / "vscode-app" / "extensions"
    install_path = _write_builtin_extension(
        builtin_root,
        "copilot",
        {
            "publisher": "GitHub",
            "name": "copilot-chat",
            "displayName": "GitHub Copilot",
            "version": "0.30.0",
        },
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.name == "GitHub Copilot"
    assert artifact.source_identifier == "github.copilot-chat"
    assert artifact.version == "0.30.0"
    assert artifact.client == "vscode"
    assert artifact.scope == "builtin"
    assert artifact.install_path == str(install_path)


def test_scan_vscode_extensions_covers_macos_user_application_install(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    user_root = (
        home
        / "Applications"
        / "Visual Studio Code.app"
        / "Contents"
        / "Resources"
        / "app"
        / "extensions"
    )
    install_path = _write_builtin_extension(
        user_root,
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")

    [artifact] = scan_vscode_extensions(home=home, machine_scope=False)

    assert artifact.install_path == str(install_path)
    assert artifact.scope == "builtin"


@pytest.mark.parametrize(
    ("client", "app_bundle"),
    [
        ("cursor", "Cursor.app"),
        ("windsurf", "Windsurf.app"),
        ("windsurf", "Devin.app"),
    ],
)
def test_macos_editor_builtin_layouts_cover_user_and_machine_installs(
    client: str,
    app_bundle: str,
) -> None:
    assert (
        client,
        Path(app_bundle) / "Contents" / "Resources" / "app" / "extensions",
        (("home", "Applications"), ("absolute", "/Applications")),
    ) in _DEFAULT_BUILTIN_ROOT_LAYOUTS["Darwin"]


@pytest.mark.parametrize(
    ("client", "app_bundle"),
    [
        ("cursor", "Cursor.app"),
        ("windsurf", "Windsurf.app"),
        ("windsurf", "Devin.app"),
    ],
)
def test_macos_editor_builtin_roots_preserve_device_scope(
    monkeypatch,
    tmp_path: Path,
    client: str,
    app_bundle: str,
) -> None:
    home = tmp_path / "home"
    machine_applications = tmp_path / "Applications"
    app_tail = Path(app_bundle) / "Contents" / "Resources" / "app" / "extensions"
    user_path = _write_builtin_extension(
        home / "Applications" / app_tail,
        "user-ai",
        {"publisher": "Vendor", "name": "user-ai", "version": "1.0.0"},
    )
    machine_path = _write_builtin_extension(
        machine_applications / app_tail,
        "machine-ai",
        {"publisher": "Vendor", "name": "machine-ai", "version": "2.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        {
            "Darwin": (
                (
                    client,
                    app_tail,
                    (
                        ("home", "Applications"),
                        ("absolute", str(machine_applications)),
                    ),
                ),
            )
        },
    )

    artifacts = scan_vscode_extensions(home=home)
    by_path = {artifact.install_path: artifact for artifact in artifacts}

    assert by_path[str(user_path)].client == client
    assert by_path[str(user_path)].device_scope is False
    assert by_path[str(machine_path)].client == client
    assert by_path[str(machine_path)].device_scope is True


def test_scan_vscode_extensions_covers_windows_user_and_system_installs(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    user_root = (
        home
        / "AppData"
        / "Local"
        / "Programs"
        / "Microsoft VS Code"
        / "resources"
        / "app"
        / "extensions"
    )
    program_files = tmp_path / "Program Files"
    system_root = (
        program_files
        / "Microsoft VS Code Insiders"
        / "resources"
        / "app"
        / "extensions"
    )
    user_path = _write_builtin_extension(
        user_root,
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    system_path = _write_builtin_extension(
        system_root,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "2.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setenv("programfiles", str(program_files))

    artifacts = scan_vscode_extensions(home=home)

    assert {artifact.install_path for artifact in artifacts} == {
        str(user_path),
        str(system_path),
    }
    assert all(artifact.scope == "builtin" for artifact in artifacts)


def test_machine_scope_false_skips_windows_system_builtins_only(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    user_root = (
        home
        / "AppData"
        / "Local"
        / "Programs"
        / "Microsoft VS Code"
        / "resources"
        / "app"
        / "extensions"
    )
    program_files = tmp_path / "Program Files"
    system_root = (
        program_files / "Microsoft VS Code" / "resources" / "app" / "extensions"
    )
    user_path = _write_builtin_extension(
        user_root,
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    _write_builtin_extension(
        system_root,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "2.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setenv("ProgramFiles", str(program_files))

    artifacts = scan_vscode_extensions(home=home, machine_scope=False)

    assert [artifact.install_path for artifact in artifacts] == [str(user_path)]
    assert artifacts[0].scope == "builtin"


@pytest.mark.parametrize(
    ("client", "app_dir"),
    [
        ("cursor", "cursor"),
        ("windsurf", "Windsurf"),
        ("windsurf", "Devin"),
    ],
)
def test_windows_editor_builtin_roots_cover_user_and_machine_layouts(
    monkeypatch,
    tmp_path: Path,
    client: str,
    app_dir: str,
) -> None:
    home = tmp_path / "home"
    program_files_x86 = tmp_path / "Program Files (x86)"
    relative = Path(app_dir) / "resources" / "app" / "extensions"
    user_path = _write_builtin_extension(
        home / "AppData" / "Local" / "Programs" / relative,
        "user-ai",
        {"publisher": "Vendor", "name": "user-ai", "version": "1.0.0"},
    )
    machine_path = _write_builtin_extension(
        program_files_x86 / relative,
        "machine-ai",
        {"publisher": "Vendor", "name": "machine-ai", "version": "2.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setenv("ProgramFiles(x86)", str(program_files_x86))

    artifacts = scan_vscode_extensions(home=home)
    by_path = {artifact.install_path: artifact for artifact in artifacts}

    assert set(by_path) == {str(user_path), str(machine_path)}
    assert by_path[str(user_path)].client == client
    assert by_path[str(user_path)].device_scope is False
    assert by_path[str(machine_path)].client == client
    assert by_path[str(machine_path)].device_scope is True


@pytest.mark.parametrize(
    ("client", "app_tail"),
    [
        ("cursor", Path("cursor/resources/app/extensions")),
        ("windsurf", Path("devin-desktop/resources/app/extensions")),
        ("vscode", Path("codium/resources/app/extensions")),
        (
            "vscode",
            Path(
                "com.visualstudio.code/current/active/files/extra/vscode/"
                "resources/app/extensions"
            ),
        ),
        (
            "vscode",
            Path(
                "com.vscodium.codium/current/active/files/share/codium/"
                "resources/app/extensions"
            ),
        ),
    ],
)
def test_scan_vscode_extensions_attributes_linux_builtin_roots(
    monkeypatch,
    tmp_path: Path,
    client: str,
    app_tail: Path,
):
    base = tmp_path / "system-apps"
    install_path = _write_builtin_extension(
        base / app_tail,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "1.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        {"Linux": ((client, app_tail, (("absolute", str(base)),)),)},
    )

    [artifact] = scan_vscode_extensions(home=tmp_path / "home")

    assert artifact.client == client
    assert artifact.scope == "builtin"
    assert artifact.install_path == str(install_path)


def test_scan_vscode_extensions_follows_symlinked_linux_builtin_base(
    monkeypatch,
    tmp_path: Path,
) -> None:
    real_base = tmp_path / "real-snap"
    linked_base = tmp_path / "snap"
    app_tail = Path("code/current/usr/share/code/resources/app/extensions")
    install_path = _write_builtin_extension(
        real_base / app_tail,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "1.0.0"},
    )
    linked_base.symlink_to(real_base, target_is_directory=True)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        {"Linux": (("vscode", app_tail, (("absolute", str(linked_base)),)),)},
    )

    [artifact] = scan_vscode_extensions(home=tmp_path / "home")

    assert artifact.scope == "builtin"
    assert artifact.install_path == str(install_path)


def test_scan_vscode_extensions_skips_builtin_base_below_symlinked_parent(
    monkeypatch,
    tmp_path: Path,
) -> None:
    real_parent = tmp_path / "real-parent"
    linked_parent = tmp_path / "linked-parent"
    real_base = tmp_path / "real-snap"
    app_tail = Path("code/current/usr/share/code/resources/app/extensions")
    _write_builtin_extension(
        real_base / app_tail,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "1.0.0"},
    )
    real_parent.mkdir()
    (real_parent / "snap").symlink_to(real_base, target_is_directory=True)
    linked_parent.symlink_to(real_parent, target_is_directory=True)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        {
            "Linux": (
                (
                    "vscode",
                    app_tail,
                    (("absolute", str(linked_parent / "snap")),),
                ),
            )
        },
    )

    assert scan_vscode_extensions(home=tmp_path / "home") == []


def test_scan_vscode_extensions_covers_user_flatpak_builtin(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    builtin_root = (
        home
        / ".local"
        / "share"
        / "flatpak"
        / "app"
        / "com.vscodium.codium"
        / "current"
        / "active"
        / "files"
        / "share"
        / "codium"
        / "resources"
        / "app"
        / "extensions"
    )
    install_path = _write_builtin_extension(
        builtin_root,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "1.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    [artifact] = scan_vscode_extensions(home=home)

    assert artifact.client == "vscode"
    assert artifact.scope == "builtin"
    assert artifact.install_path == str(install_path)


def test_scan_vscode_extensions_covers_remote_server_bundles(tmp_path: Path):
    home = tmp_path / "home"
    extra_home = tmp_path / "wsl" / "home" / "alex"
    legacy_root = home / ".vscode-server" / "bin" / "commit-a" / "extensions"
    cli_root = (
        extra_home
        / ".vscode-server-insiders"
        / "cli"
        / "servers"
        / "commit-b"
        / "server"
        / "extensions"
    )
    cursor_root = home / ".cursor-server" / "bin" / "commit-c" / "extensions"
    windsurf_root = (
        extra_home
        / ".windsurf-server"
        / "cli"
        / "servers"
        / "commit-d"
        / "server"
        / "extensions"
    )
    legacy_path = _write_builtin_extension(
        legacy_root,
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    cli_path = _write_builtin_extension(
        cli_root,
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "2.0.0"},
    )
    cursor_path = _write_builtin_extension(
        cursor_root,
        "cursor-ai",
        {"publisher": "Cursor", "name": "cursor-ai", "version": "3.0.0"},
    )
    windsurf_path = _write_builtin_extension(
        windsurf_root,
        "windsurf-ai",
        {"publisher": "Windsurf", "name": "windsurf-ai", "version": "4.0.0"},
    )

    artifacts = scan_vscode_extensions(
        home=home,
        extra_home_roots=[extra_home],
        machine_scope=False,
    )

    artifacts_by_path = {artifact.install_path: artifact for artifact in artifacts}
    assert set(artifacts_by_path) == {
        str(legacy_path),
        str(cli_path),
        str(cursor_path),
        str(windsurf_path),
    }
    assert all(artifact.scope == "builtin" for artifact in artifacts)
    assert artifacts_by_path[str(cursor_path)].client == "cursor"
    assert artifacts_by_path[str(windsurf_path)].client == "windsurf"


def test_scan_vscode_extensions_covers_devin_server_remote_roots(tmp_path: Path):
    home = tmp_path / "home"
    user_path = _write_extension(
        home,
        ".devin-server",
        "vendor.user-ai-1.0.0",
        {"publisher": "Vendor", "name": "user-ai", "version": "1.0.0"},
    )
    builtin_path = _write_builtin_extension(
        home / ".devin-server" / "bin" / "commit-a" / "extensions",
        "vendor-builtin-ai",
        {"publisher": "Vendor", "name": "builtin-ai", "version": "2.0.0"},
    )

    artifacts = scan_vscode_extensions(home=home, machine_scope=False)
    artifacts_by_path = {artifact.install_path: artifact for artifact in artifacts}

    assert set(artifacts_by_path) == {str(user_path), str(builtin_path)}
    assert artifacts_by_path[str(user_path)].client == "windsurf"
    assert artifacts_by_path[str(user_path)].scope == "global"
    assert artifacts_by_path[str(builtin_path)].client == "windsurf"
    assert artifacts_by_path[str(builtin_path)].scope == "builtin"


def test_scan_vscode_extensions_reuses_one_followed_remote_host_layout(
    tmp_path: Path,
):
    external_host = tmp_path / "external-vscode-server"
    user_target = _write_builtin_extension(
        external_host / "extensions",
        "github.copilot-1.0.0",
        {"publisher": "GitHub", "name": "copilot", "version": "1.0.0"},
    )
    builtin_target = _write_builtin_extension(
        external_host / "bin" / "commit-a" / "extensions",
        "github.copilot-chat",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    home = tmp_path / "home"
    home.mkdir()
    (home / ".vscode-server").symlink_to(
        external_host,
        target_is_directory=True,
    )

    artifacts = scan_vscode_extensions(home=home)

    assert {artifact.install_path for artifact in artifacts} == {
        str(user_target.resolve()),
        str(builtin_target.resolve()),
    }
    assert {artifact.scope for artifact in artifacts} == {"global", "builtin"}


def test_scan_vscode_extensions_symlinked_remote_layout_survives_exhausted_follow_budget(
    monkeypatch,
    tmp_path: Path,
):
    external_host = tmp_path / "external-vscode-server"
    user_target = _write_builtin_extension(
        external_host / "extensions",
        "github.copilot-1.0.0",
        {"publisher": "GitHub", "name": "copilot", "version": "1.0.0"},
    )
    home = tmp_path / "home"
    home.mkdir()
    (home / ".vscode-server").symlink_to(external_host, target_is_directory=True)
    # Model an exhausted shared follow budget. The claim_final=False
    # _extension_collection_root resolution must not spend any slot on the
    # relocated extensions directory; with the bug it would admit the target,
    # drop the layout, and mark the scan incomplete.
    monkeypatch.setattr(vscode_extensions_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 0)
    scan_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(home=home, scan_status=scan_status)

    assert {artifact.install_path for artifact in artifacts} == {
        str(user_target.resolve()),
    }
    assert scan_status.complete is True
    assert "vscode_extension_symlink_follow_capped" not in scan_status.reasons


def test_scan_vscode_extensions_bounds_remote_server_root_candidates(
    monkeypatch,
    tmp_path: Path,
):
    for index in range(2):
        remote_root = (
            tmp_path / ".vscode-server" / "bin" / f"commit-{index}" / "extensions"
        )
        _write_builtin_extension(
            remote_root,
            f"vendor-ai-{index}",
            {
                "publisher": "Vendor",
                "name": f"vendor-ai-{index}",
                "version": "1.0.0",
            },
        )
    monkeypatch.setattr(
        vscode_extensions_module,
        "MAX_REMOTE_SERVER_ROOT_CANDIDATES_PER_HOME",
        1,
    )
    scan_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(home=tmp_path, scan_status=scan_status)

    assert len(artifacts) == 1
    assert artifacts[0].scope == "builtin"
    assert scan_status.complete is False
    assert "vscode_remote_server_root_scan_capped" in scan_status.reasons


def test_explicit_extension_root_cap_marks_scan_incomplete(monkeypatch, tmp_path: Path):
    roots = [tmp_path / "one", tmp_path / "two"]
    for root in roots:
        root.mkdir()
    monkeypatch.setattr(
        vscode_extensions_module,
        "MAX_EXPLICIT_EXTENSION_ROOTS",
        1,
    )
    scan_status = ScanCompletionStatus()

    scan_vscode_extensions(
        extra_extension_roots=[
            vscode_extensions_module.VSCodeExtensionRoot(
                path=root,
                client="vscode",
            )
            for root in roots
        ],
        include_standard_roots=False,
        scan_status=scan_status,
    )

    assert "vscode_explicit_extension_roots_capped" in scan_status.reasons


def test_unresolvable_explicit_extension_root_marks_scan_incomplete(tmp_path: Path):
    scan_status = ScanCompletionStatus()

    scan_vscode_extensions(
        extra_extension_roots=[
            vscode_extensions_module.VSCodeExtensionRoot(
                path=tmp_path / "missing",
                client="vscode",
            )
        ],
        include_standard_roots=False,
        scan_status=scan_status,
    )

    assert "vscode_explicit_extension_root_unresolved" in scan_status.reasons


def test_wsl_process_extension_root_artifacts_keep_distro_identity(tmp_path: Path):
    root = tmp_path / "extensions"
    _write_builtin_extension(
        root,
        "github.copilot-chat-1.0.0",
        {
            "publisher": "GitHub",
            "name": "copilot-chat",
            "version": "1.0.0",
        },
    )

    artifacts = vscode_extensions_module.scan_vscode_extension_roots(
        [
            vscode_extensions_module.VSCodeExtensionRoot(
                path=root,
                client="vscode",
                wsl_distro="Ubuntu",
            )
        ]
    )

    assert len(artifacts) == 1
    assert artifacts[0].scope == "process_override"
    assert artifacts[0].wsl_distro == "Ubuntu"


def test_scan_vscode_extensions_filters_builtin_platform_noise(
    monkeypatch,
    tmp_path: Path,
):
    builtin_root = tmp_path / "vscode-app" / "extensions"
    _write_builtin_extension(
        builtin_root,
        "git",
        {"publisher": "VSCode", "name": "git", "version": "1.0.0"},
    )
    _write_builtin_extension(
        builtin_root,
        "github.copilot-chat-1.0.0",
        {},
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )
    device_status = ScanCompletionStatus()

    assert scan_vscode_extensions(home=tmp_path, device_scan_status=device_status) == []
    assert device_status.complete is True


def test_windows_device_builtin_reparse_manifest_marks_device_incomplete(
    monkeypatch,
    tmp_path: Path,
):
    builtin_root = tmp_path / "vscode-app" / "extensions"
    install_path = builtin_root / "vendor-ai"
    install_path.mkdir(parents=True)
    manifest_target = tmp_path / "external-package.json"
    manifest_target.write_text(
        json.dumps({"publisher": "Vendor", "name": "ai", "version": "1.0.0"})
    )
    (install_path / "package.json").symlink_to(manifest_target)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )
    monkeypatch.setattr(
        vscode_extensions_module,
        "is_windows_system_context",
        lambda: True,
    )
    host_status = ScanCompletionStatus()
    device_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(
        home=tmp_path,
        scan_status=host_status,
        device_scan_status=device_status,
    )

    assert artifacts == []
    assert host_status.complete is True
    assert device_status.complete is False
    assert "vscode_builtin_manifest_read_failed" in device_status.reasons


@pytest.mark.parametrize("manifest_content", [b"{", b"x" * (1024 * 1024 + 1)])
def test_device_builtin_manifest_failure_marks_device_incomplete(
    monkeypatch,
    tmp_path: Path,
    manifest_content: bytes,
):
    builtin_root = tmp_path / "vscode-app" / "extensions"
    install_path = builtin_root / "vendor-ai"
    install_path.mkdir(parents=True)
    (install_path / "package.json").write_bytes(manifest_content)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )
    host_status = ScanCompletionStatus()
    device_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(
        home=tmp_path,
        scan_status=host_status,
        device_scan_status=device_status,
    )

    assert artifacts == []
    assert host_status.complete is True
    assert device_status.complete is False
    assert "vscode_builtin_manifest_read_failed" in device_status.reasons


def test_unreadable_device_builtin_manifest_marks_device_incomplete(
    monkeypatch,
    tmp_path: Path,
):
    builtin_root = tmp_path / "vscode-app" / "extensions"
    _write_builtin_extension(
        builtin_root,
        "vendor-ai",
        {"publisher": "Vendor", "name": "ai", "version": "1.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )
    monkeypatch.setattr(
        vscode_extensions_module, "read_bounded", lambda *_a, **_k: None
    )
    device_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(
        home=tmp_path,
        device_scan_status=device_status,
    )

    assert artifacts == []
    assert device_status.complete is False
    assert "vscode_builtin_manifest_read_failed" in device_status.reasons


def test_device_builtin_directory_error_preserves_user_findings(
    monkeypatch,
    tmp_path: Path,
):
    user_path = _write_extension(
        tmp_path,
        ".vscode",
        "vendor.ai-1.0.0",
        {"publisher": "Vendor", "name": "ai", "version": "1.0.0"},
    )
    builtin_root = tmp_path / "vscode-app" / "extensions"
    _write_builtin_extension(
        builtin_root,
        "vendor-ai",
        {"publisher": "Vendor", "name": "ai", "version": "1.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )
    original_iterdir = Path.iterdir

    def iterdir(path: Path):
        if path == builtin_root:
            raise OSError("denied")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", iterdir)
    host_status = ScanCompletionStatus()
    device_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(
        home=tmp_path,
        scan_status=host_status,
        device_scan_status=device_status,
    )

    assert [artifact.install_path for artifact in artifacts] == [str(user_path)]
    assert host_status.complete is True
    assert device_status.complete is False
    assert "vscode_extension_directory_read_failed" in device_status.reasons


def test_user_directory_error_marks_host_status_only(
    monkeypatch,
    tmp_path: Path,
) -> None:
    user_root = tmp_path / ".vscode" / "extensions"
    user_root.mkdir(parents=True)
    original_iterdir = Path.iterdir

    def iterdir(path: Path):
        if path == user_root:
            raise OSError("denied")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", iterdir)
    host_status = ScanCompletionStatus()
    device_status = ScanCompletionStatus()

    assert (
        scan_vscode_extensions(
            home=tmp_path,
            scan_status=host_status,
            device_scan_status=device_status,
        )
        == []
    )
    assert host_status.complete is False
    assert "vscode_extension_directory_read_failed" in host_status.reasons
    assert device_status.complete is True


def test_scan_vscode_extensions_dedupes_builtin_and_user_copy_by_identifier(
    monkeypatch,
    tmp_path: Path,
):
    builtin_root = tmp_path / "vscode-app" / "extensions"
    manifest = {
        "publisher": "GitHub",
        "name": "copilot-chat",
        "version": "1.2.3",
    }
    _write_builtin_extension(builtin_root, "copilot", manifest)
    _write_extension(
        tmp_path,
        ".vscode",
        "github.copilot-chat-1.2.3",
        manifest,
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )

    artifacts = scan_vscode_extensions(home=tmp_path)
    artifacts_by_scope = {artifact.scope: artifact for artifact in artifacts}

    assert set(artifacts_by_scope) == {"builtin", "global"}
    assert (
        artifacts_by_scope["builtin"].identifier
        == artifacts_by_scope["global"].identifier
    )


def test_scan_vscode_extensions_emits_manifest_identity_and_host(tmp_path: Path):
    install_path = _write_extension(
        tmp_path,
        ".vscode",
        "github.copilot-1.2.3",
        {
            "publisher": "github",
            "name": "copilot",
            "displayName": "GitHub Copilot",
            "version": "1.2.3",
            "description": "AI pair programmer",
            "author": {"name": "GitHub"},
        },
    )

    artifacts = scan_vscode_extensions(home=tmp_path)

    assert len(artifacts) == 1
    artifact = artifacts[0]
    assert artifact.name == "GitHub Copilot"
    assert artifact.identifier is not None
    assert artifact.version == "1.2.3"
    assert artifact.plugin_type == "vscode_extension"
    assert artifact.client == "vscode"
    assert artifact.source_identifier == "github.copilot"
    assert artifact.install_path == str(install_path)
    assert artifact.marketplace == "visual-studio-marketplace"
    assert artifact.description == "AI pair programmer"
    assert artifact.author == "GitHub"
    assert artifact.to_api_payload()["source_identifier"] == "github.copilot"


def test_scan_vscode_extensions_normalizes_marketplace_id_before_hashing(
    tmp_path: Path,
):
    manifest_home = tmp_path / "manifest"
    fallback_home = tmp_path / "fallback"
    _write_extension(
        manifest_home,
        ".vscode",
        "GitHub.copilot-1.2.3",
        {"publisher": "GitHub", "name": "copilot", "version": "1.2.3"},
    )
    fallback_dir = fallback_home / ".vscode" / "extensions" / "github.copilot-1.2.3"
    fallback_dir.mkdir(parents=True)
    (fallback_dir / "package.json").write_text("{not-json")

    [manifest_artifact] = scan_vscode_extensions(home=manifest_home)
    [fallback_artifact] = scan_vscode_extensions(home=fallback_home)

    assert manifest_artifact.source_identifier == "github.copilot"
    assert fallback_artifact.source_identifier == "github.copilot"
    assert manifest_artifact.identifier == fallback_artifact.identifier


def test_scan_vscode_extensions_bounds_manifest_fields(tmp_path: Path):
    _write_extension(
        tmp_path,
        ".vscode",
        "github.copilot-1.2.3",
        {
            "publisher": "github",
            "name": "copilot",
            "displayName": "N" * 300,
            "version": "1" * 150,
            "author": {"name": "A" * 300},
        },
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert len(artifact.name) == 255
    assert artifact.version is not None
    assert len(artifact.version) == 100
    assert artifact.author is not None
    assert len(artifact.author) == 255


def test_scan_vscode_extensions_rejects_oversized_marketplace_id(tmp_path: Path):
    _write_extension(
        tmp_path,
        ".vscode",
        "oversized.extension-1.2.3",
        {
            "publisher": "p" * 250,
            "name": "n" * 10,
            "version": "1.2.3",
        },
    )

    assert scan_vscode_extensions(home=tmp_path) == []


def test_scan_vscode_extensions_falls_back_to_versioned_folder_name(
    tmp_path: Path,
):
    extension_dir = tmp_path / ".cursor" / "extensions" / "continue.continue-1.0.7"
    extension_dir.mkdir(parents=True)
    (extension_dir / "package.json").write_text("{not-json")

    artifacts = scan_vscode_extensions(home=tmp_path)

    assert len(artifacts) == 1
    artifact = artifacts[0]
    assert artifact.name == "continue.continue"
    assert artifact.version == "1.0.7"
    assert artifact.client == "cursor"
    assert artifact.identifier is not None


def test_scan_vscode_extensions_fallback_handles_platform_suffix(tmp_path: Path):
    extension_dir = (
        tmp_path / ".vscode" / "extensions" / "anthropic.claude-code-2.1.42-linux-x64"
    )
    extension_dir.mkdir(parents=True)
    (extension_dir / "package.json").write_text("{not-json")

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.source_identifier == "anthropic.claude-code"
    assert artifact.version == "2.1.42"


def test_scan_vscode_extensions_covers_native_and_wsl_host_roots(tmp_path: Path):
    native_home = tmp_path / "native"
    wsl_home = tmp_path / "wsl" / "home" / "alex"
    _write_extension(
        native_home,
        ".windsurf",
        "codeium.codeium-2.0.0",
        {"publisher": "codeium", "name": "codeium", "version": "2.0.0"},
    )
    _write_extension(
        wsl_home,
        ".vscode-server",
        "github.copilot-chat-0.30.0",
        {
            "publisher": "github",
            "name": "copilot-chat",
            "version": "0.30.0",
        },
    )

    artifacts = scan_vscode_extensions(
        home=native_home,
        extra_home_roots=[wsl_home],
    )

    assert {(artifact.client, artifact.name) for artifact in artifacts} == {
        ("windsurf", "codeium.codeium"),
        ("vscode", "github.copilot-chat"),
    }


def test_plugin_artifact_phase_includes_vscode_extensions_and_wsl_roots(
    monkeypatch,
    tmp_path: Path,
):
    expected = object()
    captured: dict[str, object] = {}

    def governor_checkpoint() -> None:
        pass

    for scanner_name in (
        "scan_cursor_native_plugins",
        "scan_cursor_user_local_plugins",
        "scan_claude_code_plugin_artifacts",
        "scan_claude_desktop_connectors",
        "scan_codex_plugin_artifacts",
        "scan_opencode_plugin_artifacts",
        "scan_jetbrains_plugins",
    ):
        monkeypatch.setattr(orchestrator, scanner_name, lambda **kwargs: [])

    def scan_vscode_extensions_stub(
        *,
        extra_home_roots,
        machine_scope,
        checkpoint,
        scan_status,
        device_scan_status,
    ):
        captured["extra_home_roots"] = extra_home_roots
        captured["machine_scope"] = machine_scope
        captured["checkpoint"] = checkpoint
        return [expected]

    monkeypatch.setattr(
        orchestrator,
        "scan_vscode_extensions",
        scan_vscode_extensions_stub,
        raising=False,
    )

    result = orchestrator._scan_plugin_artifact_phase(
        governor=SimpleNamespace(checkpoint=governor_checkpoint),
        extra_home_roots=[tmp_path],
    )

    assert result == [expected]
    assert captured["extra_home_roots"] == [tmp_path]
    assert captured["machine_scope"] is True
    assert captured["checkpoint"] is governor_checkpoint


def test_plugin_artifact_phase_passes_wsl_homes_to_artifact_scanners(
    monkeypatch,
    tmp_path: Path,
):
    scanner_names = (
        "scan_cursor_native_plugins",
        "scan_cursor_user_local_plugins",
        "scan_claude_code_plugin_artifacts",
        "scan_claude_desktop_connectors",
        "scan_codex_plugin_artifacts",
        "scan_opencode_plugin_artifacts",
    )
    calls: dict[str, list[Path | None]] = {name: [] for name in scanner_names}

    def make_stub(name: str):
        def stub(**kwargs):
            calls[name].append(kwargs.get("home"))
            return []

        return stub

    for scanner_name in scanner_names:
        monkeypatch.setattr(orchestrator, scanner_name, make_stub(scanner_name))
    monkeypatch.setattr(orchestrator, "scan_vscode_extensions", lambda **kwargs: [])
    monkeypatch.setattr(orchestrator, "scan_jetbrains_plugins", lambda **kwargs: [])

    wsl_home = tmp_path / "wsl-home"
    orchestrator._scan_plugin_artifact_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        extra_home_roots=[wsl_home],
    )

    for scanner_name in scanner_names:
        assert calls[scanner_name] == [None, wsl_home]


@pytest.mark.parametrize(
    ("host_dir", "client"),
    [
        (".local/share/code-server", "vscode"),
        (".openvscode-server", "vscode"),
        (".devin", "windsurf"),
        (".var/app/com.visualstudio.code/data/vscode", "vscode"),
        (".var/app/com.vscodium.codium/data/codium", "vscode"),
    ],
)
def test_scan_vscode_extensions_covers_additional_user_roots(
    tmp_path: Path,
    host_dir: str,
    client: str,
):
    install_path = _write_extension(
        tmp_path,
        host_dir,
        "github.copilot-1.0.0",
        {"publisher": "GitHub", "name": "copilot", "version": "1.0.0"},
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.client == client
    assert artifact.install_path == str(install_path)


@pytest.mark.parametrize(
    "extension_id",
    [
        "amazonwebservices.amazon-q-vscode",
        "blackboxapp.blackbox",
        "anthropic.claude-code",
        "saoudrizwan.claude-dev",
        "continue.continue",
        "github.copilot",
        "github.copilot-chat",
        "kilocode.kilo-code",
        "codium.codium",
        "tabnine.tabnine-vscode",
        "codeium.codeium",
    ],
)
def test_scan_vscode_extensions_surfaces_each_seeded_extension(
    tmp_path: Path,
    extension_id: str,
):
    publisher, name = extension_id.split(".", 1)
    _write_extension(
        tmp_path,
        ".vscode",
        f"{extension_id}-9.8.7",
        {"publisher": publisher, "name": name, "version": "9.8.7"},
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.name == extension_id
    assert artifact.source_identifier == extension_id
    assert artifact.version == "9.8.7"
    assert artifact.client == "vscode"
    assert artifact.identifier is not None


def test_scan_vscode_extensions_follows_external_symlinked_installs(tmp_path: Path):
    target = _write_extension(
        tmp_path / "outside",
        ".vscode",
        "evil.escape-1.0.0",
        {"publisher": "evil", "name": "escape", "version": "1.0.0"},
    )
    extension_root = tmp_path / ".vscode" / "extensions"
    extension_root.mkdir(parents=True)
    (extension_root / "evil.escape-1.0.0").symlink_to(target, target_is_directory=True)

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.source_identifier == "evil.escape"
    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_uses_link_name_for_folder_identity(tmp_path: Path):
    target = tmp_path / "outside" / "target-without-extension-identity"
    target.mkdir(parents=True)
    extension_root = tmp_path / ".vscode" / "extensions"
    extension_root.mkdir(parents=True)
    linked_extension = extension_root / "publisher.extension-1.2.3"
    try:
        linked_extension.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.source_identifier == "publisher.extension"
    assert artifact.version == "1.2.3"
    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_checks_link_to_scheduled_root_ancestor(
    tmp_path: Path,
):
    cursor_root = tmp_path / ".cursor"
    (cursor_root / "extensions").mkdir(parents=True)
    (cursor_root / "package.json").write_text(
        json.dumps({"publisher": "evil", "name": "hidden", "version": "9.9.9"})
    )
    extension_root = tmp_path / ".vscode" / "extensions"
    extension_root.mkdir(parents=True)
    linked_extension = extension_root / "evil.hidden-9.9.9"
    try:
        linked_extension.symlink_to(cursor_root, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.source_identifier == "evil.hidden"
    assert artifact.install_path == str(cursor_root.resolve())


def test_scan_vscode_extensions_follows_in_area_install_beyond_scan_depth(
    tmp_path: Path,
):
    extension_root = tmp_path / ".vscode" / "extensions"
    target = _write_builtin_extension(
        extension_root / "stash",
        "evil.escape-1.0.0",
        {"publisher": "evil", "name": "escape", "version": "1.0.0"},
    )
    (extension_root / "evil.escape-1.0.0").symlink_to(
        target,
        target_is_directory=True,
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_refuses_links_in_windows_system_context(
    monkeypatch,
    tmp_path: Path,
):
    target = _write_extension(
        tmp_path / "outside",
        ".vscode",
        "evil.escape-1.0.0",
        {"publisher": "evil", "name": "escape", "version": "1.0.0"},
    )
    extension_root = tmp_path / ".vscode" / "extensions"
    extension_root.mkdir(parents=True)
    (extension_root / "evil.escape-1.0.0").symlink_to(
        target,
        target_is_directory=True,
    )
    monkeypatch.setattr(
        vscode_extensions_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert scan_vscode_extensions(home=tmp_path) == []


def test_scan_vscode_extensions_reads_symlinked_manifest_metadata_for_user(
    tmp_path: Path,
):
    extension_dir = tmp_path / ".vscode" / "extensions" / "evil.escape-1.0.0"
    extension_dir.mkdir(parents=True)
    external_manifest = tmp_path / "outside-package.json"
    external_manifest.write_text(
        json.dumps(
            {
                "publisher": "evil",
                "name": "escape",
                "version": "2.0.0",
                "displayName": "Escaped Metadata",
                "author": {"name": "External Author"},
                "description": "Metadata from the resolved manifest target",
            }
        )
    )
    try:
        (extension_dir / "package.json").symlink_to(external_manifest)
    except OSError:
        pytest.skip("file symlinks unavailable")

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.name == "Escaped Metadata"
    assert artifact.version == "2.0.0"
    assert artifact.author == "External Author"
    assert artifact.description == "Metadata from the resolved manifest target"


def test_scan_vscode_extensions_does_not_read_redirected_manifest_as_system(
    monkeypatch,
    tmp_path: Path,
):
    extension_dir = tmp_path / ".vscode" / "extensions" / "evil.escape-1.0.0"
    extension_dir.mkdir(parents=True)
    external_manifest = tmp_path / "outside-package.json"
    external_manifest.write_text(
        json.dumps({"publisher": "evil", "name": "escape", "version": "1.0.0"})
    )
    (extension_dir / "package.json").symlink_to(external_manifest)
    monkeypatch.setattr(
        vscode_extensions_module,
        "is_windows_system_context",
        lambda: True,
    )

    def fail_read(*_args, **_kwargs):
        raise AssertionError("redirected manifest must not reach read_bounded")

    monkeypatch.setattr(vscode_extensions_module, "read_bounded", fail_read)

    assert scan_vscode_extensions(home=tmp_path) == []


def test_scan_vscode_extensions_follows_symlinked_home_for_user(tmp_path: Path):
    external_home = tmp_path / "external-home"
    target = _write_extension(
        external_home,
        ".vscode",
        "github.copilot-1.0.0",
        {"publisher": "github", "name": "copilot", "version": "1.0.0"},
    )
    home = tmp_path / "home"
    try:
        home.symlink_to(external_home, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    [artifact] = scan_vscode_extensions(home=home)

    assert artifact.source_identifier == "github.copilot"
    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_refuses_symlinked_home_as_system(
    monkeypatch,
    tmp_path: Path,
):
    external_home = tmp_path / "external-home"
    _write_extension(
        external_home,
        ".vscode",
        "github.copilot-1.0.0",
        {"publisher": "github", "name": "copilot", "version": "1.0.0"},
    )
    home = tmp_path / "home"
    try:
        home.symlink_to(external_home, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(
        vscode_extensions_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert scan_vscode_extensions(home=home) == []


def test_scan_vscode_extensions_refuses_unknown_home_component_as_system(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    _write_extension(
        home,
        ".vscode",
        "github.copilot-1.0.0",
        {"publisher": "github", "name": "copilot", "version": "1.0.0"},
    )
    monkeypatch.setattr(
        vscode_extensions_module,
        "is_windows_system_context",
        lambda: True,
    )
    real_lstat = Path.lstat

    def deny_parent_lstat(path, *args, **kwargs):
        if path == tmp_path:
            raise PermissionError("denied")
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", deny_parent_lstat)

    assert scan_vscode_extensions(home=home) == []


def test_scan_vscode_extensions_follows_symlinked_collection_root(tmp_path: Path):
    outside_home = tmp_path / "outside"
    target = _write_extension(
        outside_home,
        ".vscode",
        "github.copilot-1.0.0",
        {"publisher": "github", "name": "copilot", "version": "1.0.0"},
    )
    home = tmp_path / "home"
    host_root = home / ".vscode"
    host_root.mkdir(parents=True)
    (host_root / "extensions").symlink_to(
        outside_home / ".vscode" / "extensions",
        target_is_directory=True,
    )

    [artifact] = scan_vscode_extensions(home=home)

    assert artifact.source_identifier == "github.copilot"
    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_skips_collection_alias_already_scanned(
    tmp_path: Path,
):
    target = _write_extension(
        tmp_path,
        ".cursor",
        "github.copilot-1.0.0",
        {"publisher": "github", "name": "copilot", "version": "1.0.0"},
    )
    vscode_root = tmp_path / ".vscode"
    vscode_root.mkdir()
    (vscode_root / "extensions").symlink_to(
        tmp_path / ".cursor" / "extensions",
        target_is_directory=True,
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.client == "cursor"
    assert artifact.install_path == str(target)


def test_scan_vscode_extensions_shares_follow_cap_across_homes(
    monkeypatch,
    tmp_path: Path,
):
    native_home = tmp_path / "native"
    extra_home = tmp_path / "extra"
    for index, current_home in enumerate((native_home, extra_home)):
        target = _write_extension(
            tmp_path / f"outside-{index}",
            ".vscode",
            f"example.linked-{index}.0.0",
            {
                "publisher": "example",
                "name": f"linked-{index}",
                "version": "1.0.0",
            },
        )
        extension_root = current_home / ".vscode" / "extensions"
        extension_root.mkdir(parents=True)
        (extension_root / target.name).symlink_to(target, target_is_directory=True)
    monkeypatch.setattr(
        vscode_extensions_module,
        "MAX_FOLLOWED_SYMLINK_TARGETS",
        1,
    )

    artifacts = scan_vscode_extensions(
        home=native_home,
        extra_home_roots=[extra_home],
    )

    assert len(artifacts) == 1


def test_scan_vscode_extensions_caps_distinct_intermediate_targets(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    home.mkdir()
    vscode_target = _write_extension(
        tmp_path / "vscode-target",
        ".vscode",
        "example.vscode-1.0.0",
        {"publisher": "example", "name": "vscode", "version": "1.0.0"},
    )
    _write_extension(
        tmp_path / "cursor-target",
        ".cursor",
        "example.cursor-1.0.0",
        {"publisher": "example", "name": "cursor", "version": "1.0.0"},
    )
    (home / ".vscode").symlink_to(
        tmp_path / "vscode-target" / ".vscode",
        target_is_directory=True,
    )
    (home / ".cursor").symlink_to(
        tmp_path / "cursor-target" / ".cursor",
        target_is_directory=True,
    )
    monkeypatch.setattr(
        vscode_extensions_module,
        "MAX_RESOLVED_INTERMEDIATE_LINKS",
        1,
    )

    [artifact] = scan_vscode_extensions(home=home)

    assert artifact.install_path == str(vscode_target.resolve())


def test_scan_vscode_extensions_skips_duplicate_broken_and_looped_links(
    tmp_path: Path,
):
    target = _write_extension(
        tmp_path / "outside",
        ".vscode",
        "example.linked-1.0.0",
        {"publisher": "example", "name": "linked", "version": "1.0.0"},
    )
    extension_root = tmp_path / ".vscode" / "extensions"
    extension_root.mkdir(parents=True)
    (extension_root / "first").symlink_to(target, target_is_directory=True)
    (extension_root / "duplicate").symlink_to(target, target_is_directory=True)
    (extension_root / "broken").symlink_to(
        tmp_path / "missing",
        target_is_directory=True,
    )
    (extension_root / "loop-a").symlink_to(
        extension_root / "loop-b",
        target_is_directory=True,
    )
    (extension_root / "loop-b").symlink_to(
        extension_root / "loop-a",
        target_is_directory=True,
    )

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_follows_symlinked_builtin_and_remote_roots(
    monkeypatch,
    tmp_path: Path,
):
    outside_system_root = tmp_path / "outside-system" / "extensions"
    builtin_target = _write_builtin_extension(
        outside_system_root,
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    system_root = tmp_path / "vscode-app" / "extensions"
    system_root.parent.mkdir(parents=True)
    system_root.symlink_to(outside_system_root, target_is_directory=True)

    outside_commit = tmp_path / "outside-commit"
    remote_target = _write_builtin_extension(
        outside_commit / "extensions",
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "2.0.0"},
    )
    home = tmp_path / "home"
    commit = home / ".vscode-server" / "bin" / "commit-a"
    commit.parent.mkdir(parents=True)
    commit.symlink_to(outside_commit, target_is_directory=True)

    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(system_root),
    )

    artifacts = scan_vscode_extensions(home=home)

    assert {artifact.install_path for artifact in artifacts} == {
        str(builtin_target.resolve()),
        str(remote_target.resolve()),
    }
    assert all(artifact.scope == "builtin" for artifact in artifacts)


def test_scan_vscode_extensions_follows_intermediate_symlink_in_allowed_system_root(
    monkeypatch,
    tmp_path: Path,
):
    outside_app = tmp_path / "outside-app"
    target = _write_builtin_extension(
        outside_app / "extensions",
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    applications = tmp_path / "Applications"
    applications.mkdir()
    (applications / "vscode-app").symlink_to(outside_app, target_is_directory=True)

    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        {
            "Darwin": (
                (
                    "vscode",
                    Path("vscode-app/extensions"),
                    (("absolute", str(applications)),),
                ),
            )
        },
    )

    [artifact] = scan_vscode_extensions(home=tmp_path / "home")

    assert artifact.install_path == str(target.resolve())


def test_scan_vscode_extensions_resolves_covered_root_before_distinct_tail(
    tmp_path: Path,
):
    shared_root = tmp_path / ".vscode" / "extensions"
    user_target = _write_builtin_extension(
        shared_root,
        "user-tool-1.0.0",
        {"publisher": "User", "name": "user-tool", "version": "1.0.0"},
    )
    builtin_target = _write_builtin_extension(
        shared_root / "extensions",
        "vendor-ai",
        {"publisher": "Vendor", "name": "vendor-ai", "version": "2.0.0"},
    )
    candidate = tmp_path / ".vscode-server" / "bin" / "commit-a"
    candidate.parent.mkdir(parents=True)
    candidate.symlink_to(shared_root, target_is_directory=True)

    artifacts = scan_vscode_extensions(home=tmp_path)

    assert {(artifact.scope, artifact.install_path) for artifact in artifacts} == {
        ("global", str(user_target.resolve())),
        ("builtin", str(builtin_target.resolve())),
    }


def test_scan_vscode_extensions_follows_symlinked_absolute_layout_base(
    monkeypatch,
    tmp_path: Path,
):
    actual_applications = tmp_path / "actual-applications"
    install_path = _write_builtin_extension(
        actual_applications / "vscode-app" / "extensions",
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    linked_applications = tmp_path / "linked-applications"
    linked_applications.symlink_to(actual_applications, target_is_directory=True)
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        {
            "Darwin": (
                (
                    "vscode",
                    Path("vscode-app/extensions"),
                    (("absolute", str(linked_applications)),),
                ),
            )
        },
    )

    [artifact] = scan_vscode_extensions(home=home)

    assert artifact.install_path == str(install_path)


def test_scan_vscode_extensions_continues_after_permission_failure(
    monkeypatch,
    tmp_path: Path,
):
    denied_root = tmp_path / ".vscode" / "extensions"
    denied_root.mkdir(parents=True)
    _write_extension(
        tmp_path,
        ".cursor",
        "continue.continue-1.0.0",
        {"publisher": "continue", "name": "continue", "version": "1.0.0"},
    )
    original_iterdir = Path.iterdir

    def guarded_iterdir(path: Path):
        if path == denied_root:
            raise PermissionError("denied")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", guarded_iterdir)

    [artifact] = scan_vscode_extensions(home=tmp_path)

    assert artifact.client == "cursor"


def test_scan_vscode_extensions_enforces_scan_wide_cap(
    monkeypatch,
    tmp_path: Path,
):
    extra_home = tmp_path / "wsl-home"
    builtin_root = tmp_path / "vscode-app" / "extensions"
    for home, prefix in ((tmp_path, "native"), (extra_home, "wsl")):
        for index in range(2):
            _write_extension(
                home,
                ".vscode",
                f"example.{prefix}-{index}.0.0",
                {
                    "publisher": "example",
                    "name": f"{prefix}-{index}",
                    "version": f"{index}.0.0",
                },
            )
    _write_builtin_extension(
        builtin_root,
        "copilot",
        {"publisher": "GitHub", "name": "copilot-chat", "version": "1.0.0"},
    )
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        vscode_extensions_module,
        "_BUILTIN_ROOT_LAYOUTS",
        _absolute_builtin_layout(builtin_root),
    )
    monkeypatch.setattr(vscode_extensions_module, "MAX_EXTENSIONS_PER_SCAN", 3)

    artifacts = scan_vscode_extensions(
        home=tmp_path,
        extra_home_roots=[extra_home],
    )

    assert len(artifacts) == 3
    assert any(
        artifact.install_path.startswith(str(extra_home)) for artifact in artifacts
    )
    assert any(artifact.scope == "builtin" for artifact in artifacts)


def test_scan_vscode_extensions_cap_is_scan_wide_fair_and_checkpointed(
    monkeypatch,
    tmp_path: Path,
):
    for index in range(3):
        _write_extension(
            tmp_path,
            ".vscode",
            f"example.extension-{index}.0.0",
            {
                "publisher": "example",
                "name": f"extension-{index}",
                "version": f"{index}.0.0",
            },
        )
    _write_extension(
        tmp_path,
        ".cursor",
        "github.copilot-1.0.0",
        {"publisher": "github", "name": "copilot", "version": "1.0.0"},
    )
    monkeypatch.setattr(vscode_extensions_module, "MAX_EXTENSIONS_PER_SCAN", 2)
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    scan_status = ScanCompletionStatus()
    artifacts = scan_vscode_extensions(
        home=tmp_path,
        checkpoint=checkpoint,
        scan_status=scan_status,
    )

    assert len(artifacts) == 2
    assert {artifact.client for artifact in artifacts} == {"vscode", "cursor"}
    assert checkpoints >= 2
    assert "vscode_extension_scan_capped" in scan_status.reasons


def test_scan_vscode_extensions_exact_capacity_remains_complete(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    for index in range(2):
        _write_extension(
            tmp_path,
            ".vscode",
            f"example.extension-{index}.0.0",
            {
                "publisher": "example",
                "name": f"extension-{index}",
                "version": "1.0.0",
            },
        )
    monkeypatch.setattr(vscode_extensions_module, "MAX_EXTENSIONS_PER_SCAN", 2)
    scan_status = ScanCompletionStatus()

    artifacts = scan_vscode_extensions(home=tmp_path, scan_status=scan_status)

    assert len(artifacts) == 2
    assert "vscode_extension_scan_capped" not in scan_status.reasons


def test_deeply_nested_extension_manifest_is_rejected_not_raised():
    """RecursionError from json.loads must stay inside the parser (ISS-01)."""
    assert (
        vscode_extensions_module.parse_vscode_extension_manifest(DEEP_NESTING_BYTES)
        is None
    )
