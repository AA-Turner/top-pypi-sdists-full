"""Behavior tests for JetBrains plugin inventory."""

from pathlib import Path
from types import SimpleNamespace
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from runlayer_cli.scan import orchestrator
from runlayer_cli.scan import jetbrains_plugins as jetbrains_plugins_module
from runlayer_cli.scan.jetbrains_plugins import scan_jetbrains_plugins
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    SymlinkLayoutResolver,
)


def _write_jar_plugin(
    home: Path,
    *,
    product: str,
    folder: str,
    plugin_id: str,
    name: str,
    version: str,
    vendor: str = "Example Vendor",
) -> Path:
    plugin_dir = home / ".local" / "share" / "JetBrains" / product / folder
    jar_path = plugin_dir / "lib" / f"{folder}.jar"
    jar_path.parent.mkdir(parents=True)
    xml = f"""\
<idea-plugin>
  <id>{plugin_id}</id>
  <name>{name}</name>
  <version>{version}</version>
  <vendor>{vendor}</vendor>
  <description>Example description</description>
</idea-plugin>
"""
    with ZipFile(jar_path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("META-INF/plugin.xml", xml)
    return plugin_dir


def test_scan_jetbrains_plugins_reads_plugin_xml_from_jar(tmp_path: Path):
    install_path = _write_jar_plugin(
        tmp_path,
        product="IdeaIC2025.2",
        folder="github-copilot",
        plugin_id="com.github.copilot",
        name="GitHub Copilot",
        version="1.5.2",
    )

    artifacts = scan_jetbrains_plugins(home=tmp_path)

    assert len(artifacts) == 1
    artifact = artifacts[0]
    assert artifact.name == "GitHub Copilot"
    assert artifact.identifier is not None
    assert artifact.version == "1.5.2"
    assert artifact.plugin_type == "jetbrains_plugin"
    assert artifact.client == "intellij_idea_community"
    assert artifact.source_identifier == "com.github.copilot"
    assert artifact.install_path == str(install_path)
    assert artifact.marketplace == "jetbrains-marketplace"
    assert artifact.author == "Example Vendor"
    assert artifact.description == "Example description"


def test_scan_jetbrains_plugins_prioritizes_main_jar_in_fat_plugin(
    monkeypatch,
    tmp_path: Path,
):
    install_path = _write_jar_plugin(
        tmp_path,
        product="IdeaIC2025.2",
        folder="ej",
        plugin_id="org.jetbrains.junie",
        name="Junie",
        version="252.819.54",
    )
    lib_dir = install_path / "lib"
    (lib_dir / "ej.jar").rename(lib_dir / "ej-1.0.jar")
    for index in range(150):
        (lib_dir / f"aaa-{index:03}.jar").write_bytes(b"not a zip")

    real_jar_paths = jetbrains_plugins_module._jar_paths

    def alphabetic_jar_paths(path: Path):
        yield from sorted(real_jar_paths(path))

    monkeypatch.setattr(
        jetbrains_plugins_module,
        "_jar_paths",
        alphabetic_jar_paths,
    )

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.source_identifier == "org.jetbrains.junie"
    assert artifact.name == "Junie"


def test_scan_jetbrains_plugins_bounds_manifest_fields(tmp_path: Path):
    _write_jar_plugin(
        tmp_path,
        product="IdeaIC2025.2",
        folder="github-copilot",
        plugin_id="com.github.copilot",
        name="N" * 300,
        version="1" * 150,
        vendor="A" * 300,
    )

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert len(artifact.name) == 255
    assert artifact.version is not None
    assert len(artifact.version) == 100
    assert artifact.author is not None
    assert len(artifact.author) == 255


def test_scan_jetbrains_plugins_rejects_oversized_marketplace_id(tmp_path: Path):
    _write_jar_plugin(
        tmp_path,
        product="IdeaIC2025.2",
        folder="oversized",
        plugin_id="p" * 256,
        name="Oversized",
        version="1.0.0",
    )

    assert scan_jetbrains_plugins(home=tmp_path) == []


def test_scan_jetbrains_plugins_covers_both_linux_layouts(tmp_path: Path):
    """Flat <Product>/ and nested <Product>/plugins/ installs both inventory."""
    product_dir = tmp_path / ".local" / "share" / "JetBrains" / "Vexlark2031.4"

    flat_manifest = product_dir / "quorlin-assist" / "META-INF" / "plugin.xml"
    flat_manifest.parent.mkdir(parents=True)
    flat_manifest.write_text(
        """\
<idea-plugin>
  <id>io.quorlin.assist</id>
  <name>Quorlin Assist</name>
  <version>0.4.1</version>
</idea-plugin>
"""
    )

    nested_manifest = (
        product_dir / "plugins" / "brenwick-ai" / "META-INF" / "plugin.xml"
    )
    nested_manifest.parent.mkdir(parents=True)
    nested_manifest.write_text(
        """\
<idea-plugin>
  <id>dev.brenwick.ai</id>
  <name>Brenwick AI</name>
  <version>3.0.0</version>
</idea-plugin>
"""
    )

    artifacts = scan_jetbrains_plugins(home=tmp_path)

    identifiers = sorted(
        artifact.source_identifier
        for artifact in artifacts
        if artifact.source_identifier is not None
    )
    assert identifiers == ["dev.brenwick.ai", "io.quorlin.assist"]
    assert len(artifacts) == 2


def test_scan_jetbrains_plugins_reads_unpacked_plugin_from_wsl_home(tmp_path: Path):
    native_home = tmp_path / "native"
    wsl_home = tmp_path / "wsl" / "home" / "alex"
    plugin_dir = (
        wsl_home / ".local" / "share" / "JetBrains" / "PyCharm2025.2" / "continue"
    )
    manifest = plugin_dir / "META-INF" / "plugin.xml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        """\
<idea-plugin>
  <id>com.continue.intellij</id>
  <name>Continue</name>
  <version>2.1.0</version>
</idea-plugin>
"""
    )

    [artifact] = scan_jetbrains_plugins(
        home=native_home,
        extra_home_roots=[wsl_home],
    )

    assert artifact.name == "Continue"
    assert artifact.version == "2.1.0"
    assert artifact.client == "pycharm"
    assert artifact.install_path == str(plugin_dir)


@pytest.mark.parametrize(
    ("plugin_id", "name"),
    [
        ("amazon.q", "Amazon Q"),
        ("com.codeium.intellij", "Codeium"),
        ("com.github.continuedev.continueintellijextension", "Continue"),
        ("com.github.copilot", "GitHub Copilot"),
        ("com.intellij.ml.llm", "AI Assistant"),
        ("org.jetbrains.junie", "Junie"),
        ("com.tabnine.TabNine", "Tabnine"),
    ],
)
def test_scan_jetbrains_plugins_surfaces_each_seeded_plugin(
    tmp_path: Path,
    plugin_id: str,
    name: str,
):
    _write_jar_plugin(
        tmp_path,
        product="IdeaIC2025.2",
        folder=plugin_id.replace(".", "-"),
        plugin_id=plugin_id,
        name=name,
        version="9.8.7",
    )

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.name == name
    assert artifact.source_identifier == plugin_id
    assert artifact.version == "9.8.7"
    assert artifact.client == "intellij_idea_community"
    assert artifact.identifier is not None


def test_plugin_artifact_phase_includes_jetbrains_plugins_and_wsl_roots(
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
        "scan_vscode_extensions",
    ):
        monkeypatch.setattr(orchestrator, scanner_name, lambda **kwargs: [])

    def scan_jetbrains_plugins_stub(*, extra_home_roots, checkpoint):
        captured["extra_home_roots"] = extra_home_roots
        captured["checkpoint"] = checkpoint
        return [expected]

    monkeypatch.setattr(
        orchestrator,
        "scan_jetbrains_plugins",
        scan_jetbrains_plugins_stub,
        raising=False,
    )

    result = orchestrator._scan_plugin_artifact_phase(
        governor=SimpleNamespace(checkpoint=governor_checkpoint),
        extra_home_roots=[tmp_path],
    )

    assert result == [expected]
    assert captured["extra_home_roots"] == [tmp_path]
    assert captured["checkpoint"] is governor_checkpoint


def test_scan_jetbrains_plugins_covers_windows_and_macos_roots(tmp_path: Path):
    roots = [
        (
            tmp_path / "AppData" / "Roaming" / "JetBrains",
            "IdeaIU2025.2",
            "intellij_idea_ultimate",
        ),
        (
            tmp_path / "Library" / "Application Support" / "JetBrains",
            "WebStorm2025.2",
            "webstorm",
        ),
    ]
    for root, product, _client in roots:
        manifest = root / product / "plugins" / "tabnine" / "META-INF" / "plugin.xml"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            f"""\
<idea-plugin>
  <id>com.tabnine.{product}</id>
  <name>Tabnine</name>
  <version>1.0.0</version>
</idea-plugin>
"""
        )

    artifacts = scan_jetbrains_plugins(home=tmp_path)

    assert {artifact.client for artifact in artifacts} == {
        "intellij_idea_ultimate",
        "webstorm",
    }


def test_scan_jetbrains_plugins_reads_native_windows_appdata_root(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    appdata = tmp_path / "RedirectedAppData" / "Roaming"
    plugin_dir = appdata / "JetBrains" / "IdeaIC2025.2" / "plugins" / "github-copilot"
    jar_path = plugin_dir / "lib" / "github-copilot.jar"
    jar_path.parent.mkdir(parents=True)
    with ZipFile(jar_path, "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "META-INF/plugin.xml",
            """\
<idea-plugin>
  <id>com.github.copilot</id>
  <name>GitHub Copilot</name>
  <version>1.5.2</version>
</idea-plugin>
""",
        )
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("APPDATA", str(appdata))
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)

    [artifact] = scan_jetbrains_plugins()

    assert artifact.source_identifier == "com.github.copilot"
    assert artifact.client == "intellij_idea_community"
    assert artifact.install_path == str(plugin_dir)


def test_scan_jetbrains_plugins_ignores_malformed_manifest(tmp_path: Path):
    manifest = (
        tmp_path
        / ".local"
        / "share"
        / "JetBrains"
        / "IdeaIC2025.2"
        / "broken"
        / "META-INF"
        / "plugin.xml"
    )
    manifest.parent.mkdir(parents=True)
    manifest.write_text("<idea-plugin><id>broken")

    assert scan_jetbrains_plugins(home=tmp_path) == []


def test_scan_jetbrains_plugins_follows_symlinked_install(tmp_path: Path):
    target = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="target",
        plugin_id="example.target",
        name="Target",
        version="1.0.0",
    )
    plugin_root = tmp_path / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    plugin_root.mkdir(parents=True)
    (plugin_root / "target").symlink_to(target, target_is_directory=True)

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.source_identifier == "example.target"
    assert artifact.install_path == str(target.resolve())


def test_intermediate_manifest_link_uses_shared_follow_cap(tmp_path: Path):
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()
    metadata_target = tmp_path / "metadata"
    metadata_target.mkdir()
    manifest = metadata_target / "plugin.xml"
    manifest.write_text("<idea-plugin><id>linked.metadata</id></idea-plugin>")
    (plugin_dir / "META-INF").symlink_to(
        metadata_target,
        target_is_directory=True,
    )
    later_target = tmp_path / "later-target"
    later_target.mkdir()
    later_link = tmp_path / "later-link"
    later_link.symlink_to(later_target, target_is_directory=True)
    policy = SymlinkFollowPolicy(scan_areas=[], max_followed=1)
    resolver = SymlinkLayoutResolver(
        policy=policy,
        windows_system_context=False,
    )

    assert (
        jetbrains_plugins_module._read_xml_file(
            plugin_dir,
            Path("META-INF") / "plugin.xml",
            resolver=resolver,
        )
        == manifest.read_bytes()
    )
    assert policy.evaluate(later_link) is None


def test_scan_jetbrains_plugins_follows_in_area_install_beyond_scan_depth(
    tmp_path: Path,
):
    plugin_root = tmp_path / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    target = plugin_root / "stash" / "target"
    manifest = target / "META-INF" / "plugin.xml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        """\
<idea-plugin>
  <id>example.target</id>
  <name>Target</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    (plugin_root / "linked").symlink_to(target, target_is_directory=True)

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.install_path == str(target.resolve())


def test_scan_jetbrains_plugins_follows_symlinked_plugin_root(tmp_path: Path):
    outside_root = tmp_path / "outside-plugins"
    manifest = outside_root / "continue" / "META-INF" / "plugin.xml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        """\
<idea-plugin>
  <id>com.github.continuedev.continueintellijextension</id>
  <name>Continue</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    product_dir = (
        tmp_path / "Library" / "Application Support" / "JetBrains" / "IdeaIC2025.2"
    )
    product_dir.mkdir(parents=True)
    (product_dir / "plugins").symlink_to(outside_root, target_is_directory=True)

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.source_identifier == (
        "com.github.continuedev.continueintellijextension"
    )
    assert artifact.install_path == str((outside_root / "continue").resolve())


def test_scan_jetbrains_plugins_reuses_symlinked_product_for_nested_layout(
    tmp_path: Path,
):
    outside_product = tmp_path / "outside-product"
    plugin_dir = outside_product / "plugins" / "continue"
    manifest = plugin_dir / "META-INF" / "plugin.xml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        """\
<idea-plugin>
  <id>com.continue.intellij</id>
  <name>Continue</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    collection_root = tmp_path / ".local" / "share" / "JetBrains"
    collection_root.mkdir(parents=True)
    (collection_root / "IdeaIC2025.2").symlink_to(
        outside_product,
        target_is_directory=True,
    )

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.install_path == str(plugin_dir.resolve())


def test_scan_jetbrains_plugins_resolves_covered_product_before_distinct_tail(
    tmp_path: Path,
):
    collection_root = tmp_path / "Library" / "Application Support" / "JetBrains"
    shared_product = collection_root / "IdeaIC2025.2" / "plugins"
    first_plugin = shared_product / "first"
    first_manifest = first_plugin / "META-INF" / "plugin.xml"
    first_manifest.parent.mkdir(parents=True)
    first_manifest.write_text(
        """\
<idea-plugin>
  <id>example.first</id>
  <name>First</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    nested_plugin = shared_product / "plugins" / "continue"
    nested_manifest = nested_plugin / "META-INF" / "plugin.xml"
    nested_manifest.parent.mkdir(parents=True)
    nested_manifest.write_text(
        """\
<idea-plugin>
  <id>com.continue.intellij</id>
  <name>Continue</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    (collection_root / "ZAlias").symlink_to(
        shared_product,
        target_is_directory=True,
    )

    artifacts = scan_jetbrains_plugins(home=tmp_path)

    assert {artifact.install_path for artifact in artifacts} == {
        str(first_plugin.resolve()),
        str(nested_plugin.resolve()),
    }


def test_scan_jetbrains_plugins_follows_dotfiles_relocation(tmp_path: Path):
    home = tmp_path / "home"
    home.mkdir()
    relocated_local = tmp_path / "relocated-local"
    plugin_dir = (
        relocated_local
        / "share"
        / "JetBrains"
        / "IdeaIC2025.2"
        / "plugins"
        / "github-copilot"
    )
    manifest = plugin_dir / "META-INF" / "plugin.xml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        """\
<idea-plugin>
  <id>com.github.copilot</id>
  <name>GitHub Copilot</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    (home / ".local").symlink_to(relocated_local, target_is_directory=True)

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.source_identifier == "com.github.copilot"
    assert artifact.install_path == str(plugin_dir.resolve())


def test_scan_jetbrains_plugins_follows_relocated_xdg_data_home(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    home.mkdir()
    relocated_data = tmp_path / "relocated-data"
    plugin_dir = (
        relocated_data / "JetBrains" / "IdeaIC2025.2" / "plugins" / "github-copilot"
    )
    manifest = plugin_dir / "META-INF" / "plugin.xml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        """\
<idea-plugin>
  <id>com.github.copilot</id>
  <name>GitHub Copilot</name>
  <version>1.0.0</version>
</idea-plugin>
"""
    )
    xdg_data_home = tmp_path / "xdg-data-home"
    xdg_data_home.symlink_to(relocated_data, target_is_directory=True)
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setenv("XDG_DATA_HOME", str(xdg_data_home))
    monkeypatch.delenv("APPDATA", raising=False)

    [artifact] = scan_jetbrains_plugins()

    assert artifact.install_path == str(plugin_dir.resolve())


def test_scan_jetbrains_plugins_follows_symlinked_collection_root(tmp_path: Path):
    home = tmp_path / "home"
    target = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="github-copilot",
        plugin_id="com.github.copilot",
        name="GitHub Copilot",
        version="1.0.0",
    )
    collection_parent = home / ".local" / "share"
    collection_parent.mkdir(parents=True)
    (collection_parent / "JetBrains").symlink_to(
        tmp_path / "outside" / ".local" / "share" / "JetBrains",
        target_is_directory=True,
    )

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.install_path == str(target.resolve())


def test_scan_jetbrains_plugins_refuses_links_in_windows_system_context(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    target = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="target",
        plugin_id="example.target",
        name="Target",
        version="1.0.0",
    )
    plugin_root = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    plugin_root.mkdir(parents=True)
    (plugin_root / "target").symlink_to(target, target_is_directory=True)
    monkeypatch.setattr(
        jetbrains_plugins_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert scan_jetbrains_plugins(home=home) == []


def test_scan_jetbrains_plugins_follows_symlinked_home_for_user(tmp_path: Path):
    external_home = tmp_path / "external-home"
    target = _write_jar_plugin(
        external_home,
        product="IdeaIC2025.2",
        folder="github-copilot",
        plugin_id="com.github.copilot",
        name="GitHub Copilot",
        version="1.0.0",
    )
    home = tmp_path / "home"
    try:
        home.symlink_to(external_home, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.source_identifier == "com.github.copilot"
    assert artifact.install_path == str(target.resolve())


def test_scan_jetbrains_plugins_refuses_symlinked_home_as_system(
    monkeypatch,
    tmp_path: Path,
):
    external_home = tmp_path / "external-home"
    _write_jar_plugin(
        external_home,
        product="IdeaIC2025.2",
        folder="github-copilot",
        plugin_id="com.github.copilot",
        name="GitHub Copilot",
        version="1.0.0",
    )
    home = tmp_path / "home"
    try:
        home.symlink_to(external_home, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(
        jetbrains_plugins_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert scan_jetbrains_plugins(home=home) == []


def test_scan_jetbrains_plugins_does_not_read_redirected_marker_ancestors_as_system(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    plugin_root = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    meta_plugin = plugin_root / "redirected-meta"
    meta_plugin.mkdir(parents=True)
    external_meta = tmp_path / "external-meta"
    external_meta.mkdir()
    (external_meta / "plugin.xml").write_text(
        "<idea-plugin><id>redirected.meta</id></idea-plugin>"
    )
    (meta_plugin / "META-INF").symlink_to(external_meta, target_is_directory=True)

    external_plugin = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="redirected-lib",
        plugin_id="redirected.lib",
        name="Redirected Lib",
        version="1.0.0",
    )
    lib_plugin = plugin_root / "redirected-lib"
    lib_plugin.mkdir()
    safe_meta = lib_plugin / "META-INF"
    safe_meta.mkdir()
    (safe_meta / "plugin.xml").write_text(
        "<idea-plugin><id>safe.before.redirect</id></idea-plugin>"
    )
    (lib_plugin / "lib").symlink_to(
        external_plugin / "lib",
        target_is_directory=True,
    )
    monkeypatch.setattr(
        jetbrains_plugins_module,
        "is_windows_system_context",
        lambda: True,
    )

    def fail_read(*_args, **_kwargs):
        raise AssertionError("redirected marker must not reach a read helper")

    monkeypatch.setattr(
        jetbrains_plugins_module,
        "read_safe_relative_file",
        fail_read,
    )
    monkeypatch.setattr(jetbrains_plugins_module, "_read_xml_from_jar", fail_read)

    assert scan_jetbrains_plugins(home=home) == []


def test_scan_jetbrains_plugins_shares_follow_cap_across_homes(
    monkeypatch,
    tmp_path: Path,
):
    native_home = tmp_path / "native"
    extra_home = tmp_path / "extra"
    for index, current_home in enumerate((native_home, extra_home)):
        target = _write_jar_plugin(
            tmp_path / f"outside-{index}",
            product="IdeaIC2025.2",
            folder=f"target-{index}",
            plugin_id=f"example.target.{index}",
            name=f"Target {index}",
            version="1.0.0",
        )
        plugin_root = current_home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
        plugin_root.mkdir(parents=True)
        (plugin_root / target.name).symlink_to(target, target_is_directory=True)
    monkeypatch.setattr(
        jetbrains_plugins_module,
        "MAX_FOLLOWED_SYMLINK_TARGETS",
        1,
    )

    artifacts = scan_jetbrains_plugins(
        home=native_home,
        extra_home_roots=[extra_home],
    )

    assert len(artifacts) == 1


def test_scan_jetbrains_plugins_caps_distinct_intermediate_targets(
    monkeypatch,
    tmp_path: Path,
):
    home = tmp_path / "home"
    home.mkdir()
    first_plugin = _write_jar_plugin(
        tmp_path / "first",
        product="IdeaIC2025.2",
        folder="first",
        plugin_id="example.first",
        name="First",
        version="1.0.0",
    )
    second_root = tmp_path / "second"
    second_manifest = (
        second_root
        / "Application Support"
        / "JetBrains"
        / "IdeaIC2025.2"
        / "plugins"
        / "second"
        / "META-INF"
        / "plugin.xml"
    )
    second_manifest.parent.mkdir(parents=True)
    second_manifest.write_text("<idea-plugin><id>example.second</id></idea-plugin>")
    (home / ".local").symlink_to(
        tmp_path / "first" / ".local",
        target_is_directory=True,
    )
    (home / "Library").symlink_to(second_root, target_is_directory=True)
    monkeypatch.setattr(
        jetbrains_plugins_module,
        "MAX_RESOLVED_INTERMEDIATE_LINKS",
        1,
    )

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.install_path == str(first_plugin.resolve())


def test_scan_jetbrains_plugins_skips_duplicate_broken_and_looped_links(
    tmp_path: Path,
):
    home = tmp_path / "home"
    target = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="target",
        plugin_id="example.target",
        name="Target",
        version="1.0.0",
    )
    plugin_root = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    plugin_root.mkdir(parents=True)
    (plugin_root / "first").symlink_to(target, target_is_directory=True)
    (plugin_root / "duplicate").symlink_to(target, target_is_directory=True)
    (plugin_root / "broken").symlink_to(
        tmp_path / "missing",
        target_is_directory=True,
    )
    (plugin_root / "loop-a").symlink_to(
        plugin_root / "loop-b",
        target_is_directory=True,
    )
    (plugin_root / "loop-b").symlink_to(
        plugin_root / "loop-a",
        target_is_directory=True,
    )

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.install_path == str(target.resolve())


def test_scan_jetbrains_plugins_follows_top_level_symlinked_jar(tmp_path: Path):
    home = tmp_path / "home"
    external_jar = tmp_path / "outside" / "real.jar"
    external_jar.parent.mkdir()
    with ZipFile(external_jar, "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "META-INF/plugin.xml",
            """\
<idea-plugin>
  <id>example.linked.jar</id>
  <name>Linked Jar</name>
  <version>1.0.0</version>
  <vendor>Example Vendor</vendor>
</idea-plugin>
""",
        )
    plugin_root = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    plugin_root.mkdir(parents=True)
    linked_jar = plugin_root / "linked.jar"
    try:
        linked_jar.symlink_to(external_jar)
    except OSError:
        pytest.skip("file symlinks unavailable")

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.source_identifier == "example.linked.jar"
    assert artifact.install_path == str(external_jar.resolve())


def test_scan_jetbrains_plugins_does_not_follow_symlinked_jar_manifest(
    tmp_path: Path,
):
    home = tmp_path / "home"
    external_plugin = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="target",
        plugin_id="example.target",
        name="Target",
        version="1.0.0",
    )
    external_jar = external_plugin / "lib" / "target.jar"
    plugin_dir = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2" / "linked-jar"
    lib_dir = plugin_dir / "lib"
    lib_dir.mkdir(parents=True)
    (lib_dir / "linked.jar").symlink_to(external_jar)

    assert scan_jetbrains_plugins(home=home) == []


def test_scan_jetbrains_plugins_follows_symlinked_lib_directory(tmp_path: Path):
    home = tmp_path / "home"
    external_plugin = _write_jar_plugin(
        tmp_path / "outside",
        product="IdeaIC2025.2",
        folder="target",
        plugin_id="example.linked.lib",
        name="Linked Lib",
        version="1.0.0",
    )
    plugin_dir = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2" / "linked-lib"
    plugin_dir.mkdir(parents=True)
    try:
        (plugin_dir / "lib").symlink_to(
            external_plugin / "lib",
            target_is_directory=True,
        )
    except OSError:
        pytest.skip("directory symlinks unavailable")

    [artifact] = scan_jetbrains_plugins(home=home)

    assert artifact.source_identifier == "example.linked.lib"
    assert artifact.install_path == str(plugin_dir.resolve())


def test_scan_jetbrains_plugins_reads_symlinked_lib_from_visited_plugin(
    tmp_path: Path,
    monkeypatch,
):
    home = tmp_path / "home"
    plugin_root = home / ".local" / "share" / "JetBrains" / "IdeaIC2025.2"
    first_plugin = plugin_root / "a-first"
    direct_manifest = first_plugin / "META-INF" / "plugin.xml"
    direct_manifest.parent.mkdir(parents=True)
    direct_manifest.write_text(
        "<idea-plugin><id>example.first</id><name>First</name></idea-plugin>"
    )
    with ZipFile(first_plugin / "shared.jar", "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "META-INF/plugin.xml",
            "<idea-plugin><id>example.shared</id><name>Shared</name></idea-plugin>",
        )
    later_plugin = plugin_root / "z-later"
    later_plugin.mkdir()
    try:
        (later_plugin / "lib").symlink_to(first_plugin, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    real_iter_directory_entries = jetbrains_plugins_module.iter_directory_entries

    def sorted_directory_entries(directory: Path):
        yield from sorted(real_iter_directory_entries(directory))

    monkeypatch.setattr(
        jetbrains_plugins_module,
        "iter_directory_entries",
        sorted_directory_entries,
    )

    artifacts = scan_jetbrains_plugins(home=home)

    assert {artifact.source_identifier for artifact in artifacts} == {
        "example.first",
        "example.shared",
    }
    assert {artifact.install_path for artifact in artifacts} == {
        str(first_plugin.resolve()),
        str(later_plugin.resolve()),
    }


def test_scan_jetbrains_plugins_continues_after_permission_failure(
    monkeypatch,
    tmp_path: Path,
):
    denied_root = tmp_path / ".local" / "share" / "JetBrains"
    denied_root.mkdir(parents=True)
    readable_manifest = (
        tmp_path
        / "Library"
        / "Application Support"
        / "JetBrains"
        / "IdeaIC2025.2"
        / "plugins"
        / "continue"
        / "META-INF"
        / "plugin.xml"
    )
    readable_manifest.parent.mkdir(parents=True)
    readable_manifest.write_text(
        """\
<idea-plugin>
  <id>com.continue.intellij</id>
  <name>Continue</name>
  <version>2.1.0</version>
</idea-plugin>
"""
    )
    original_iterdir = Path.iterdir

    def guarded_iterdir(path: Path):
        if path == denied_root:
            raise PermissionError("denied")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", guarded_iterdir)

    [artifact] = scan_jetbrains_plugins(home=tmp_path)

    assert artifact.name == "Continue"


def test_jar_enumeration_closes_and_jar_reads_are_capped(monkeypatch, tmp_path: Path):
    """Jar enumeration closes deterministically while archive reads stay capped."""
    plugin_dir = _write_jar_plugin(
        tmp_path,
        product="IdeaIC2025.2",
        folder="many-jars",
        plugin_id="example.many.jars",
        name="Many Jars",
        version="1.0.0",
    )
    lib_dir = plugin_dir / "lib"
    for index in range(3):
        (lib_dir / f"extra-{index}.jar").write_bytes(b"not a zip")

    opened: list[Path] = []
    closed: list[Path] = []
    read_paths: list[Path] = []
    real_jar_paths = jetbrains_plugins_module._jar_paths

    def tracking_jar_paths(lib_path: Path):
        opened.append(lib_path)
        try:
            yield from real_jar_paths(lib_path)
        finally:
            closed.append(lib_path)

    def tracking_read(jar_path: Path):
        read_paths.append(jar_path)
        return None

    monkeypatch.setattr(jetbrains_plugins_module, "_jar_paths", tracking_jar_paths)
    monkeypatch.setattr(
        jetbrains_plugins_module,
        "_read_xml_from_jar",
        tracking_read,
    )
    monkeypatch.setattr(jetbrains_plugins_module, "MAX_JARS_PER_PLUGIN", 1)

    scan_jetbrains_plugins(home=tmp_path)

    assert opened == [lib_dir]
    assert closed == opened
    assert read_paths == [lib_dir / "many-jars.jar"]


def test_product_dir_cap_closes_suspended_directory_iterator(
    monkeypatch,
    tmp_path: Path,
):
    """Hitting MAX_PRODUCT_DIRS_PER_ROOT must close the directory generator."""
    for index in range(4):
        _write_jar_plugin(
            tmp_path,
            product=f"IdeaIC2025.{index}",
            folder="tabnine",
            plugin_id="com.tabnine.TabNine",
            name="Tabnine",
            version="1.0.0",
        )

    opened: list[Path] = []
    closed: list[Path] = []
    real_iter_directory_entries = jetbrains_plugins_module.iter_directory_entries

    def tracking_iter_directory_entries(directory: Path):
        opened.append(directory)
        try:
            yield from real_iter_directory_entries(directory)
        finally:
            closed.append(directory)

    monkeypatch.setattr(
        jetbrains_plugins_module,
        "iter_directory_entries",
        tracking_iter_directory_entries,
    )
    monkeypatch.setattr(jetbrains_plugins_module, "MAX_PRODUCT_DIRS_PER_ROOT", 1)

    scan_jetbrains_plugins(home=tmp_path)

    assert opened
    assert sorted(closed) == sorted(opened)


def test_scan_jetbrains_plugins_cap_is_scan_wide_fair_and_checkpointed(
    monkeypatch,
    tmp_path: Path,
):
    for index in range(3):
        _write_jar_plugin(
            tmp_path,
            product="IdeaIC2025.2",
            folder=f"plugin-{index}",
            plugin_id=f"example.plugin.{index}",
            name=f"Plugin {index}",
            version="1.0.0",
        )
    _write_jar_plugin(
        tmp_path,
        product="PyCharm2025.2",
        folder="continue",
        plugin_id="com.github.continuedev.continueintellijextension",
        name="Continue",
        version="1.0.0",
    )
    monkeypatch.setattr(jetbrains_plugins_module, "MAX_PLUGINS_PER_SCAN", 2)
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    artifacts = scan_jetbrains_plugins(home=tmp_path, checkpoint=checkpoint)

    assert {artifact.client for artifact in artifacts} == {
        "intellij_idea_community",
        "pycharm",
    }
    assert len(artifacts) == 2
    assert checkpoints >= 2
