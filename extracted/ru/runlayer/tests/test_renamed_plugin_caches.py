"""Tests for the bounded renamed plugin-cache probe."""

import json
from pathlib import Path

from runlayer_cli.scan import renamed_plugin_caches as probe_module
from runlayer_cli.scan.plugin_scanner import compute_plugin_identifier
from runlayer_cli.scan.renamed_plugin_caches import (
    MAX_PROBE_DEPTH,
    filter_novel_plugin_artifacts,
    scan_renamed_plugin_caches,
)


def _write_cursor_plugin(directory: Path, name: str = "shadow-tool") -> None:
    manifest_dir = directory / ".cursor-plugin"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps({"name": name, "version": "1.2.3", "description": "d"})
    )
    (directory / "mcp.json").write_text(
        json.dumps({"mcpServers": {"srv": {"command": "run-srv"}}})
    )


def test_detects_renamed_cursor_cache_by_manifest_marker(tmp_path: Path):
    renamed = tmp_path / ".cursor" / "plugins" / "totally-not-a-cache" / "v9"
    _write_cursor_plugin(renamed)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.name == "shadow-tool"
    assert artifact.plugin_type == "cursor_plugin"
    assert artifact.client == "cursor"
    assert artifact.install_path == str(renamed)
    assert artifact.version == "1.2.3"
    assert artifact.has_mcp_servers is True
    assert [server.name for server in artifact.mcp_servers] == ["srv"]
    assert artifact.identifier is not None


def test_generic_mcp_marker_uses_root_client_defaults(tmp_path: Path):
    hidden = tmp_path / ".codex" / "plugins" / "innocuous-dir"
    hidden.mkdir(parents=True)
    (hidden / "mcp.json").write_text(
        json.dumps({"mcpServers": {"exfil": {"command": "exfil"}}})
    )

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.plugin_type == "codex_plugin"
    assert artifact.client == "codex"
    assert artifact.name == "innocuous-dir"


def test_opencode_package_json_marker_is_scoped_to_opencode_root(tmp_path: Path):
    opencode_plugin = tmp_path / ".config" / "opencode" / "renamed" / "hook"
    opencode_plugin.mkdir(parents=True)
    (opencode_plugin / "package.json").write_text(json.dumps({"name": "hook-pkg"}))
    # package.json outside the opencode root must not classify.
    copilot_dir = tmp_path / ".copilot" / "some-tool"
    copilot_dir.mkdir(parents=True)
    (copilot_dir / "package.json").write_text(json.dumps({"name": "not-a-plugin"}))

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.client == "opencode"
    assert artifact.plugin_type == "opencode_plugin"
    assert artifact.name == "hook-pkg"


def test_benign_directories_and_outside_roots_are_not_classified(tmp_path: Path):
    (tmp_path / ".cursor" / "plugins" / "empty-dir").mkdir(parents=True)
    (tmp_path / ".claude" / "plugins" / "notes").mkdir(parents=True)
    (tmp_path / ".claude" / "plugins" / "notes" / "README.md").write_text("hi")
    # Marker outside every allowlisted root is ignored.
    outside = tmp_path / "renamed-plugins" / "tool"
    _write_cursor_plugin(outside)
    # A marker file sitting in the client root itself is client config, not a
    # plugin install.
    (tmp_path / ".copilot").mkdir(parents=True)
    (tmp_path / ".copilot" / "mcp.json").write_text(json.dumps({"mcpServers": {}}))

    assert scan_renamed_plugin_caches(home=tmp_path) == []


def test_probe_does_not_descend_beyond_depth_cap(tmp_path: Path):
    deep = tmp_path / ".cursor" / "plugins"
    for index in range(MAX_PROBE_DEPTH + 1):
        deep = deep / f"level-{index}"
    _write_cursor_plugin(deep)

    assert scan_renamed_plugin_caches(home=tmp_path) == []


def test_probe_follows_symlinked_plugin_and_skips_ignored_directories(tmp_path: Path):
    real_plugin = tmp_path / "elsewhere" / "plugin"
    _write_cursor_plugin(real_plugin)
    root = tmp_path / ".cursor" / "plugins"
    root.mkdir(parents=True)
    (root / "linked").symlink_to(real_plugin, target_is_directory=True)
    node_modules_plugin = root / "node_modules" / "sneaky"
    _write_cursor_plugin(node_modules_plugin)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.name == "shadow-tool"
    assert artifact.install_path == str(real_plugin.resolve())


def test_probe_does_not_follow_alias_to_marker_directory(tmp_path: Path):
    root = tmp_path / ".cursor" / "plugins"
    marker_directory = root / "container" / ".claude-plugin"
    nested = marker_directory / "nested"
    nested.mkdir(parents=True)
    (nested / "mcp.json").write_text(json.dumps({"mcpServers": {}}))
    (root / "marker-alias").symlink_to(
        marker_directory,
        target_is_directory=True,
    )

    assert scan_renamed_plugin_caches(home=tmp_path) == []


def test_probe_follows_symlinked_collection_root(tmp_path: Path):
    outside_root = tmp_path / "outside-plugins"
    target = outside_root / "renamed"
    _write_cursor_plugin(target)
    cursor_root = tmp_path / ".cursor"
    cursor_root.mkdir()
    (cursor_root / "plugins").symlink_to(
        outside_root,
        target_is_directory=True,
    )

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(target.resolve())


def test_in_root_sibling_link_does_not_consume_follow_cap(monkeypatch, tmp_path: Path):
    root = tmp_path / ".cursor" / "plugins"
    first = root / "a-first"
    second = root / "b-second"
    later = root / "c-later"
    first.mkdir(parents=True)
    second.mkdir()
    later.mkdir()
    (first / "to-second").symlink_to(second, target_is_directory=True)
    outside_plugin = tmp_path / "outside-plugin"
    _write_cursor_plugin(outside_plugin)
    (later / "plugin").symlink_to(outside_plugin, target_is_directory=True)
    monkeypatch.setattr(probe_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(outside_plugin.resolve())


def test_followed_root_sibling_link_does_not_consume_follow_cap(
    monkeypatch, tmp_path: Path
):
    followed_root = tmp_path / "followed-root"
    first = followed_root / "a-first"
    second = followed_root / "b-second"
    later = followed_root / "c-later"
    first.mkdir(parents=True)
    second.mkdir()
    later.mkdir()
    (first / "to-second").symlink_to(second, target_is_directory=True)
    outside_plugin = tmp_path / "outside-plugin"
    _write_cursor_plugin(outside_plugin)
    (later / "plugin").symlink_to(outside_plugin, target_is_directory=True)
    root = tmp_path / ".cursor" / "plugins"
    root.mkdir(parents=True)
    (root / "followed").symlink_to(followed_root, target_is_directory=True)
    monkeypatch.setattr(probe_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 2)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(outside_plugin.resolve())


def test_intermediate_marker_link_consumes_shared_follow_cap(
    monkeypatch, tmp_path: Path
):
    root = tmp_path / ".cursor" / "plugins"
    marker_plugin = root / "a-marker"
    marker_plugin.mkdir(parents=True)
    marker_target = tmp_path / "marker-target"
    marker_target.mkdir()
    (marker_target / "plugin.json").write_text(json.dumps({"name": "marker"}))
    (marker_plugin / ".cursor-plugin").symlink_to(
        marker_target,
        target_is_directory=True,
    )

    later = root / "b-later"
    later.mkdir()
    outside_plugin = tmp_path / "outside-plugin"
    _write_cursor_plugin(outside_plugin, name="outside")
    (later / "plugin").symlink_to(outside_plugin, target_is_directory=True)
    monkeypatch.setattr(probe_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    artifacts = scan_renamed_plugin_caches(home=tmp_path)

    assert [(artifact.name, artifact.install_path) for artifact in artifacts] == [
        ("marker", str(marker_plugin))
    ]


def test_oversized_intermediate_marker_does_not_consume_follow_cap(
    monkeypatch, tmp_path: Path
):
    root = tmp_path / ".cursor" / "plugins"
    invalid_plugin = root / "a-invalid"
    invalid_plugin.mkdir(parents=True)
    empty_target = tmp_path / "oversized-marker-target"
    empty_target.mkdir()
    (empty_target / "plugin.json").write_bytes(
        b"x" * (probe_module.MAX_MARKER_BYTES + 1)
    )
    (invalid_plugin / ".cursor-plugin").symlink_to(
        empty_target,
        target_is_directory=True,
    )

    later = root / "b-later"
    later.mkdir()
    outside_plugin = tmp_path / "outside-plugin"
    _write_cursor_plugin(outside_plugin, name="outside")
    (later / "plugin").symlink_to(outside_plugin, target_is_directory=True)
    monkeypatch.setattr(probe_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(outside_plugin.resolve())


def test_visited_marker_target_still_classifies_alias(tmp_path: Path):
    root = tmp_path / ".cursor" / "plugins"
    shared_marker = root / "a-shared-marker"
    shared_marker.mkdir(parents=True)
    (shared_marker / "plugin.json").write_text(json.dumps({"name": "alias"}))
    alias_plugin = root / "b-alias"
    alias_plugin.mkdir()
    (alias_plugin / ".cursor-plugin").symlink_to(
        shared_marker,
        target_is_directory=True,
    )

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(alias_plugin)
    assert artifact.name == "alias"


def test_probe_resolves_covered_intermediate_before_distinct_fixed_tail(
    tmp_path: Path,
):
    shared_root = tmp_path / ".cursor"
    cursor_target = shared_root / "plugins" / "cursor-renamed"
    _write_cursor_plugin(cursor_target, name="cursor-renamed")
    opencode_target = shared_root / "opencode" / "opencode-renamed"
    opencode_target.mkdir(parents=True)
    (opencode_target / "package.json").write_text(
        json.dumps({"name": "opencode-renamed"})
    )
    (tmp_path / ".config").symlink_to(shared_root, target_is_directory=True)

    artifacts = scan_renamed_plugin_caches(home=tmp_path)

    assert {(artifact.client, artifact.install_path) for artifact in artifacts} == {
        ("cursor", str(cursor_target.resolve())),
        ("opencode", str(opencode_target.resolve())),
    }


def test_probe_refuses_links_in_windows_system_context(monkeypatch, tmp_path: Path):
    real_plugin = tmp_path / "elsewhere" / "plugin"
    _write_cursor_plugin(real_plugin)
    root = tmp_path / ".cursor" / "plugins"
    root.mkdir(parents=True)
    (root / "linked").symlink_to(real_plugin, target_is_directory=True)
    monkeypatch.setattr(
        probe_module,
        "is_windows_system_context",
        lambda: True,
    )

    assert scan_renamed_plugin_caches(home=tmp_path) == []


def test_probe_does_not_read_redirected_marker_under_windows_system(
    monkeypatch,
    tmp_path: Path,
):
    plugin_dir = tmp_path / ".cursor" / "plugins" / "redirected-marker"
    safe_manifest_dir = plugin_dir / ".cursor-plugin"
    safe_manifest_dir.mkdir(parents=True)
    (safe_manifest_dir / "plugin.json").write_text(json.dumps({"name": "safe"}))
    external_manifest_dir = tmp_path / "outside-marker"
    external_manifest_dir.mkdir()
    (external_manifest_dir / "plugin.json").write_text(
        json.dumps({"name": "redirected"})
    )
    (plugin_dir / ".codex-plugin").symlink_to(
        external_manifest_dir,
        target_is_directory=True,
    )
    monkeypatch.setattr(probe_module, "is_windows_system_context", lambda: True)

    def fail_read(*_args, **_kwargs):
        raise AssertionError("redirected marker must not reach read_bounded")

    monkeypatch.setattr(probe_module, "read_safe_relative_file", fail_read)

    assert scan_renamed_plugin_caches(home=tmp_path) == []


def test_probe_follows_in_area_target_beyond_depth_cap(tmp_path: Path):
    root = tmp_path / ".cursor" / "plugins"
    deep = root
    for index in range(MAX_PROBE_DEPTH + 1):
        deep /= f"level-{index}"
    _write_cursor_plugin(deep)
    root.mkdir(parents=True, exist_ok=True)
    (root / "shortcut").symlink_to(deep, target_is_directory=True)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(deep.resolve())


def test_probe_follows_link_into_pruned_subtree(tmp_path: Path):
    root = tmp_path / ".cursor" / "plugins"
    hidden = root / "node_modules" / "hidden-plugin"
    _write_cursor_plugin(hidden)
    (root / "shortcut").symlink_to(hidden, target_is_directory=True)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(hidden.resolve())


def test_probe_shares_follow_cap_across_homes(monkeypatch, tmp_path: Path):
    native_home = tmp_path / "native"
    extra_home = tmp_path / "extra"
    for index, current_home in enumerate((native_home, extra_home)):
        target = tmp_path / f"outside-{index}" / "plugin"
        _write_cursor_plugin(target, name=f"plugin-{index}")
        root = current_home / ".cursor" / "plugins"
        root.mkdir(parents=True)
        (root / "linked").symlink_to(target, target_is_directory=True)
    monkeypatch.setattr(probe_module, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

    artifacts = scan_renamed_plugin_caches(
        home=native_home,
        extra_home_roots=[extra_home],
    )

    assert len(artifacts) == 1


def test_probe_caps_distinct_intermediate_targets(monkeypatch, tmp_path: Path):
    cursor_target = tmp_path / "cursor-target"
    _write_cursor_plugin(cursor_target / "plugins" / "cursor-plugin")
    opencode_target = tmp_path / "opencode-target"
    opencode_plugin = opencode_target / "opencode" / "opencode-plugin"
    opencode_plugin.mkdir(parents=True)
    (opencode_plugin / "package.json").write_text(
        json.dumps({"name": "opencode-plugin"})
    )
    (tmp_path / ".cursor").symlink_to(cursor_target, target_is_directory=True)
    (tmp_path / ".config").symlink_to(opencode_target, target_is_directory=True)
    monkeypatch.setattr(probe_module, "MAX_RESOLVED_INTERMEDIATE_LINKS", 1)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.client == "cursor"


def test_probe_skips_duplicate_broken_and_looped_links(tmp_path: Path):
    target = tmp_path / "outside" / "plugin"
    _write_cursor_plugin(target)
    root = tmp_path / ".cursor" / "plugins"
    root.mkdir(parents=True)
    (root / "first").symlink_to(target, target_is_directory=True)
    (root / "duplicate").symlink_to(target, target_is_directory=True)
    (root / "broken").symlink_to(
        tmp_path / "missing",
        target_is_directory=True,
    )
    (root / "loop-a").symlink_to(root / "loop-b", target_is_directory=True)
    (root / "loop-b").symlink_to(root / "loop-a", target_is_directory=True)

    [artifact] = scan_renamed_plugin_caches(home=tmp_path)

    assert artifact.install_path == str(target.resolve())


def test_artifact_cap_truncates_probe(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(probe_module, "MAX_ARTIFACTS", 2)
    for index in range(4):
        _write_cursor_plugin(
            tmp_path / ".cursor" / "plugins" / f"renamed-{index}",
            name=f"plugin-{index}",
        )

    artifacts = scan_renamed_plugin_caches(home=tmp_path)

    assert len(artifacts) == 2


def test_directory_cap_truncates_probe(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(probe_module, "MAX_PROBE_DIRECTORIES", 3)
    for index in range(10):
        _write_cursor_plugin(
            tmp_path / ".cursor" / "plugins" / f"renamed-{index}",
            name=f"plugin-{index}",
        )

    artifacts = scan_renamed_plugin_caches(home=tmp_path)

    # Root + 2 children visited before the cap trips.
    assert len(artifacts) <= 2


def test_directory_cap_round_robins_roots_exactly(monkeypatch, tmp_path: Path):
    native_home = tmp_path / "native"
    noisy_root = native_home / ".cursor" / "plugins"
    for index in range(10):
        (noisy_root / f"noise-{index}").mkdir(parents=True)
    extra_home = tmp_path / "extra"
    _write_cursor_plugin(
        extra_home / ".cursor" / "plugins" / "later",
        name="later",
    )
    monkeypatch.setattr(probe_module, "MAX_PROBE_DIRECTORIES", 4)
    checkpoints: list[None] = []

    [artifact] = scan_renamed_plugin_caches(
        home=native_home,
        extra_home_roots=[extra_home],
        checkpoint=lambda: checkpoints.append(None),
    )

    assert artifact.name == "later"
    assert len(checkpoints) == 4


def test_scans_wsl_extra_home_roots(tmp_path: Path):
    native_home = tmp_path / "native"
    native_home.mkdir()
    wsl_home = tmp_path / "wsl-home"
    _write_cursor_plugin(wsl_home / ".cursor" / "plugins" / "renamed")

    [artifact] = scan_renamed_plugin_caches(
        home=native_home, extra_home_roots=[wsl_home]
    )

    assert artifact.install_path.startswith(str(wsl_home))


def test_checkpoint_is_invoked(tmp_path: Path):
    _write_cursor_plugin(tmp_path / ".cursor" / "plugins" / "renamed")
    calls: list[None] = []

    scan_renamed_plugin_caches(home=tmp_path, checkpoint=lambda: calls.append(None))

    assert calls


def test_filter_novel_drops_same_path_and_same_identifier(tmp_path: Path):
    normal_dir = tmp_path / ".cursor" / "plugins" / "cache" / "cursor-public" / "tool"
    _write_cursor_plugin(normal_dir, name="tool")
    renamed_copy = tmp_path / ".cursor" / "plugins" / "renamed-copy"
    _write_cursor_plugin(renamed_copy, name="tool")
    novel_dir = tmp_path / ".cursor" / "plugins" / "novel"
    _write_cursor_plugin(novel_dir, name="novel-tool")
    (novel_dir / "mcp.json").write_text(
        json.dumps({"mcpServers": {"other": {"command": "other"}}})
    )

    candidates = scan_renamed_plugin_caches(home=tmp_path)
    assert {Path(c.install_path).name for c in candidates} == {
        "tool",
        "renamed-copy",
        "novel",
    }

    existing = [c for c in candidates if c.install_path == str(normal_dir)]
    assert existing[0].identifier == compute_plugin_identifier(normal_dir)

    novel = filter_novel_plugin_artifacts(candidates, existing)

    # Same path dropped; renamed byte-identical copy dropped by identifier;
    # genuinely different plugin kept.
    assert [Path(c.install_path).name for c in novel] == ["novel"]
