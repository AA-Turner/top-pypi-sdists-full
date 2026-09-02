"""Behavior tests for VS Code-family extension inventory."""

import json
import platform
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import orchestrator
from runlayer_cli.scan import vscode_extensions as vscode_extensions_module
from runlayer_cli.scan.vscode_extensions import scan_vscode_extensions


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
    return {
        "Darwin": (
            (Path(root.name),),
            (("absolute", str(root.parent)),),
        )
    }


@pytest.fixture(autouse=True)
def _isolate_system_builtin_roots(monkeypatch):
    home_layouts = {
        system: (
            app_tails,
            tuple(base for base in base_dirs if base[0] != "absolute"),
        )
        for system, (
            app_tails,
            base_dirs,
        ) in vscode_extensions_module._BUILTIN_ROOT_LAYOUTS.items()
    }
    monkeypatch.setattr(vscode_extensions_module, "_BUILTIN_ROOT_LAYOUTS", home_layouts)
    monkeypatch.delenv("ProgramFiles", raising=False)


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

    [artifact] = scan_vscode_extensions(home=home)

    assert artifact.install_path == str(install_path)
    assert artifact.scope == "builtin"


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

    artifacts = scan_vscode_extensions(
        home=home,
        extra_home_roots=[extra_home],
    )

    assert {artifact.install_path for artifact in artifacts} == {
        str(legacy_path),
        str(cli_path),
    }
    assert all(artifact.scope == "builtin" for artifact in artifacts)


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

    artifacts = scan_vscode_extensions(home=tmp_path)

    assert len(artifacts) == 1
    assert artifacts[0].scope == "builtin"


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

    assert scan_vscode_extensions(home=tmp_path) == []


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
        "scan_claude_code_plugin_artifacts",
        "scan_claude_desktop_connectors",
        "scan_codex_plugin_artifacts",
        "scan_opencode_plugin_artifacts",
        "scan_jetbrains_plugins",
    ):
        monkeypatch.setattr(orchestrator, scanner_name, lambda **kwargs: [])

    def scan_vscode_extensions_stub(*, extra_home_roots, checkpoint):
        captured["extra_home_roots"] = extra_home_roots
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
    assert captured["checkpoint"] is governor_checkpoint


def test_plugin_artifact_phase_passes_wsl_homes_to_artifact_scanners(
    monkeypatch,
    tmp_path: Path,
):
    scanner_names = (
        "scan_cursor_native_plugins",
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
                (Path("vscode-app/extensions"),),
                (("absolute", str(applications)),),
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


def test_scan_vscode_extensions_does_not_follow_ancestor_of_absolute_layout(
    monkeypatch,
    tmp_path: Path,
):
    actual_applications = tmp_path / "actual-applications"
    _write_builtin_extension(
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
                (Path("vscode-app/extensions"),),
                (("absolute", str(linked_applications)),),
            )
        },
    )

    assert scan_vscode_extensions(home=home) == []


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

    artifacts = scan_vscode_extensions(home=tmp_path, checkpoint=checkpoint)

    assert len(artifacts) == 2
    assert {artifact.client for artifact in artifacts} == {"vscode", "cursor"}
    assert checkpoints >= 2
