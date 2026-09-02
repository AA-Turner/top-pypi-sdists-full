"""Tests for bounded project-artifact discovery across WSL homes."""

from __future__ import annotations

import os
import posixpath
import subprocess
from pathlib import Path, PureWindowsPath

import pytest

from runlayer_cli.scan.agent_definition_scanner import AGENT_DEFINITION_PATTERNS
from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    ProjectConfigPattern,
    get_all_clients,
)
from runlayer_cli.scan.project_tree_match import (
    MAX_PROJECT_TREE_DEPTH,
    _project_agent_definition_match,
    _project_candidates_for_path,
    _project_config_specs,
    _project_skill_file_match,
)
from runlayer_cli.scan.skill_scanner import (
    SUPPORTED_EXTENSIONS as SKILL_SUPPORTED_EXTENSIONS,
)
from runlayer_cli.scan import wsl_projects as wsl_projects_module
from runlayer_cli.scan.wsl_projects import scan_wsl_projects


def _client() -> MCPClientDefinition:
    return MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[],
        project_config=ProjectConfigPattern(
            relative_path=".cursor/mcp.json",
            servers_key="mcpServers",
        ),
    )


def _config_content(command: str = "server") -> bytes:
    return ('{"mcpServers":{"example":{"command":"' + command + '"}}}').encode()


def _write_config(project: Path, content: bytes | None = None) -> Path:
    config = project / ".cursor" / "mcp.json"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_bytes(content if content is not None else _config_content())
    return config


def test_scan_wsl_projects_collects_configs_skills_and_agent_definitions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    project = home / "code" / "demo"
    config_path = _write_config(project)
    skill_path = project / ".agents" / "skills" / "deploy"
    skill_path.mkdir(parents=True)
    (skill_path / "SKILL.md").write_text("# Deploy")
    (skill_path / "notes.md").write_text("notes")
    agent_path = project / ".cursor" / "agents" / "reviewer.md"
    agent_path.parent.mkdir(parents=True)
    agent_path.write_text(
        "---\nname: reviewer\ndescription: Reviews code\n---\nReview changes."
    )

    def fail_subprocess(*args, **kwargs):
        del args, kwargs
        raise AssertionError("WSL project scanning must not execute subprocesses")

    monkeypatch.setattr(subprocess, "run", fail_subprocess)
    monkeypatch.setattr(subprocess, "Popen", fail_subprocess)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert len(result.configurations) == 1
    configuration = result.configurations[0]
    assert configuration.client == "cursor"
    assert configuration.config_scope == "project"
    assert configuration.config_path == str(config_path)
    assert configuration.project_path == str(project)
    assert configuration.servers[0].project_name == str(project)
    assert [skill.name for skill in result.skills] == ["deploy"]
    assert result.skills[0].path == str(skill_path)
    assert {file.title for file in result.skills[0].files} == {
        "SKILL.md",
        "notes.md",
    }
    assert [definition.name for definition in result.agent_definitions] == ["reviewer"]
    assert result.agent_definitions[0].path == str(agent_path)
    assert result.agent_definitions[0].project_path == str(project)


def test_scan_wsl_projects_follows_external_file_and_directory_symlinks(
    tmp_path: Path,
) -> None:
    home = tmp_path / "wsl-home"
    file_target = tmp_path / "external-config.json"
    file_target.write_bytes(_config_content("external-file"))
    file_link = home / "a" / ".cursor" / "mcp.json"
    file_link.parent.mkdir(parents=True)
    directory_target = tmp_path / "external-project"
    directory_config = _write_config(
        directory_target,
        _config_content("external-directory"),
    )
    directory_link = home / "b"
    try:
        file_link.symlink_to(file_target)
        directory_link.symlink_to(directory_target, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(file_link),
        str(directory_link / directory_config.relative_to(directory_target)),
    ]


def test_scan_wsl_projects_reads_followed_file_via_resolved_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    target = tmp_path / "external-config.json"
    target.write_bytes(_config_content())
    link = home / "project" / ".cursor" / "mcp.json"
    link.parent.mkdir(parents=True)
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")
    read_paths = []
    real_read_bounded = wsl_projects_module.read_bounded

    def track_read(path, *, max_bytes):
        read_paths.append(path)
        return real_read_bounded(path, max_bytes=max_bytes)

    monkeypatch.setattr(wsl_projects_module, "read_bounded", track_read)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [str(link)]
    assert read_paths == [target.resolve()]


def test_scan_wsl_projects_skips_entry_when_link_probe_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    blocked = _write_config(home / "project")
    real_lstat = Path.lstat

    def deny_blocked_lstat(path, *args, **kwargs):
        if path == blocked:
            raise PermissionError("denied")
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", deny_blocked_lstat)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert result.configurations == []


def test_scan_wsl_projects_skips_in_area_alias_and_follows_beyond_depth_targets(
    tmp_path: Path,
) -> None:
    home = tmp_path / "wsl-home"
    normal = _write_config(home / "real", _config_content("normal"))
    in_area_alias = home / "alias" / ".cursor" / "mcp.json"
    in_area_alias.parent.mkdir(parents=True)

    file_target_project = home / "physical-file" / "one" / "two" / "three" / "four"
    file_target = _write_config(
        file_target_project,
        _config_content("beyond-file"),
    )
    file_link = home / "linked-file" / ".cursor" / "mcp.json"
    file_link.parent.mkdir(parents=True)

    directory_target = home / "physical-directory" / "one" / "two" / "three" / "four"
    directory_config = _write_config(
        directory_target,
        _config_content("beyond-directory"),
    )
    directory_link = home / "linked-directory"
    try:
        in_area_alias.symlink_to(normal)
        file_link.symlink_to(file_target)
        directory_link.symlink_to(directory_target, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert {config.config_path for config in result.configurations} == {
        str(normal),
        str(file_link),
        str(directory_link / directory_config.relative_to(directory_target)),
    }


def test_scan_wsl_projects_depth_boundary_covers_file_but_not_deeper_directory(
    tmp_path: Path,
) -> None:
    home = tmp_path / "wsl-home"
    max_depth_project = home.joinpath(
        *(f"file-{index}" for index in range(MAX_PROJECT_TREE_DEPTH))
    )
    max_depth_config = _write_config(
        max_depth_project,
        _config_content("boundary-file"),
    )
    beyond_depth_project = home.joinpath(
        *(f"directory-{index}" for index in range(MAX_PROJECT_TREE_DEPTH + 1))
    )
    beyond_depth_config = _write_config(
        beyond_depth_project,
        _config_content("beyond-directory"),
    )
    file_alias = home / "file-alias" / ".cursor" / "mcp.json"
    file_alias.parent.mkdir(parents=True)
    directory_alias = home / "directory-alias"
    try:
        file_alias.symlink_to(max_depth_config)
        directory_alias.symlink_to(
            beyond_depth_project,
            target_is_directory=True,
        )
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert {config.config_path for config in result.configurations} == {
        str(max_depth_config),
        str(directory_alias / beyond_depth_config.relative_to(beyond_depth_project)),
    }


def test_scan_wsl_projects_skips_broken_ancestor_and_looping_links(
    tmp_path: Path,
) -> None:
    home = tmp_path / "wsl-home"
    home.mkdir()
    first_target = tmp_path / "first-target"
    second_target = tmp_path / "second-target"
    first_config = _write_config(first_target, _config_content("first"))
    second_config = _write_config(second_target, _config_content("second"))
    entry = home / "a-entry"
    broken = home / "b-broken" / ".cursor" / "mcp.json"
    broken.parent.mkdir(parents=True)
    try:
        entry.symlink_to(first_target, target_is_directory=True)
        broken.symlink_to(tmp_path / "missing.json")
        (home / "c-ancestor").symlink_to(home.parent, target_is_directory=True)
        (first_target / "to-second").symlink_to(
            second_target,
            target_is_directory=True,
        )
        (second_target / "to-first").symlink_to(
            first_target,
            target_is_directory=True,
        )
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(entry / first_config.relative_to(first_target)),
        str(entry / "to-second" / second_config.relative_to(second_target)),
    ]


def test_scan_wsl_projects_caps_followed_targets_at_64(tmp_path: Path) -> None:
    home = tmp_path / "wsl-home"
    external = tmp_path / "external"
    external.mkdir()
    links = []
    try:
        for index in range(65):
            target = external / f"target-{index:03}.json"
            target.write_bytes(_config_content(str(index)))
            link = home / f"project-{index:03}" / ".cursor" / "mcp.json"
            link.parent.mkdir(parents=True)
            link.symlink_to(target)
            links.append(link)
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(link) for link in links[:64]
    ]


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unavailable")
def test_scan_wsl_projects_non_file_link_does_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    special_target = tmp_path / "special"
    os.mkfifo(special_target)
    special_link = home / "a" / ".cursor" / "mcp.json"
    special_link.parent.mkdir(parents=True)
    special_link.symlink_to(special_target)
    valid_target = tmp_path / "valid.json"
    valid_target.write_bytes(_config_content("valid"))
    valid_link = home / "b" / ".cursor" / "mcp.json"
    valid_link.parent.mkdir(parents=True)
    valid_link.symlink_to(valid_target)
    monkeypatch.setattr(wsl_projects_module, "MAX_FOLLOWED_WSL_PROJECT_TARGETS", 1)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [str(valid_link)]


def test_scan_wsl_projects_unreadable_link_does_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    unreadable_target = tmp_path / "unreadable.json"
    unreadable_target.write_bytes(_config_content("unreadable"))
    unreadable_link = home / "a" / ".cursor" / "mcp.json"
    unreadable_link.parent.mkdir(parents=True)
    unreadable_link.symlink_to(unreadable_target)
    valid_target = tmp_path / "valid.json"
    valid_target.write_bytes(_config_content("valid"))
    valid_link = home / "b" / ".cursor" / "mcp.json"
    valid_link.parent.mkdir(parents=True)
    valid_link.symlink_to(valid_target)
    real_read = wsl_projects_module._read_bounded_file

    def reject_first(path, *, byte_budget):
        if path == unreadable_target.resolve():
            return None
        return real_read(path, byte_budget=byte_budget)

    monkeypatch.setattr(wsl_projects_module, "_read_bounded_file", reject_first)
    monkeypatch.setattr(wsl_projects_module, "MAX_FOLLOWED_WSL_PROJECT_TARGETS", 1)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [str(valid_link)]


def test_scan_wsl_projects_uses_one_follow_policy_across_homes(
    tmp_path: Path,
) -> None:
    first_home = tmp_path / "first-home"
    second_home = tmp_path / "second-home"
    first_link = first_home / "project" / ".cursor" / "mcp.json"
    second_link = second_home / "project" / ".cursor" / "mcp.json"
    target = tmp_path / "external.json"
    target.write_bytes(_config_content())
    first_link.parent.mkdir(parents=True)
    second_link.parent.mkdir(parents=True)
    try:
        first_link.symlink_to(target)
        second_link.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[first_home, second_home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [str(first_link)]


def test_scan_wsl_projects_follows_linked_home_and_preserves_logical_path(
    tmp_path: Path,
) -> None:
    home = tmp_path / "wsl-home"
    external = tmp_path / "external-home"
    config = _write_config(external / "project")
    try:
        home.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [item.config_path for item in result.configurations] == [
        str(home / config.relative_to(external))
    ]


def test_scan_wsl_projects_linked_homes_count_toward_follow_cap(
    tmp_path: Path,
) -> None:
    homes = []
    expected_paths = []
    try:
        for index in range(65):
            target = tmp_path / f"target-{index:03}"
            config = _write_config(target / "project", _config_content(str(index)))
            home = tmp_path / f"home-{index:03}"
            home.symlink_to(target, target_is_directory=True)
            homes.append(home)
            expected_paths.append(str(home / config.relative_to(target)))
    except OSError:
        pytest.skip("directory symlinks unavailable")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=homes,
        time_budget=30,
    )

    assert [item.config_path for item in result.configurations] == expected_paths[:64]


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unavailable")
def test_scan_wsl_projects_non_directory_home_link_does_not_consume_follow_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    special_target = tmp_path / "special"
    os.mkfifo(special_target)
    special_home = tmp_path / "a-home"
    special_home.symlink_to(special_target)
    valid_target = tmp_path / "valid-home"
    valid_config = _write_config(valid_target / "project")
    valid_home = tmp_path / "b-home"
    valid_home.symlink_to(valid_target, target_is_directory=True)
    monkeypatch.setattr(wsl_projects_module, "MAX_FOLLOWED_WSL_PROJECT_TARGETS", 1)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[special_home, valid_home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(valid_home / valid_config.relative_to(valid_target))
    ]


def test_scan_wsl_projects_system_context_skips_all_links(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    normal = _write_config(home / "a", _config_content("normal"))
    file_target = tmp_path / "external-file.json"
    file_target.write_bytes(_config_content("file"))
    file_link = home / "b" / ".cursor" / "mcp.json"
    file_link.parent.mkdir(parents=True)
    directory_target = tmp_path / "external-directory"
    _write_config(directory_target, _config_content("directory"))
    directory_link = home / "c"
    try:
        file_link.symlink_to(file_target)
        directory_link.symlink_to(directory_target, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(
        wsl_projects_module,
        "is_windows_system_context",
        lambda: True,
    )

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [str(normal)]


def test_scan_wsl_projects_system_context_rejects_linked_home(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    external = tmp_path / "external-home"
    _write_config(external / "project")
    try:
        home.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    monkeypatch.setattr(
        wsl_projects_module,
        "is_windows_system_context",
        lambda: True,
    )

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert result.configurations == []


def test_scan_wsl_projects_system_rejects_linked_home_component_before_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outside_parent = tmp_path / "outside-parent"
    target_home = outside_parent / "alice"
    _write_config(target_home / "project")
    linked_parent = tmp_path / "linked-parent"
    try:
        linked_parent.symlink_to(outside_parent, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    home = linked_parent / "alice"
    monkeypatch.setattr(
        wsl_projects_module,
        "is_windows_system_context",
        lambda: True,
    )
    real_stat = Path.stat
    target_stats = []
    target_scandirs = []

    def track_target_stat(path, *args, **kwargs):
        if path in {home, target_home}:
            target_stats.append(path)
        return real_stat(path, *args, **kwargs)

    real_scandir = wsl_projects_module.os.scandir

    def track_target_scandir(path):
        if Path(path) in {home, target_home}:
            target_scandirs.append(Path(path))
        return real_scandir(path)

    monkeypatch.setattr(Path, "stat", track_target_stat)
    monkeypatch.setattr(wsl_projects_module.os, "scandir", track_target_scandir)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert result.configurations == []
    assert target_stats == []
    assert target_scandirs == []


def test_native_path_preserves_wsl_unc_root() -> None:
    home = PureWindowsPath(r"\\wsl.localhost\Ubuntu\home\alice")

    native = wsl_projects_module._native_path(home, "/code/demo/.mcp.json")

    assert native == PureWindowsPath(
        r"\\wsl.localhost\Ubuntu\home\alice\code\demo\.mcp.json"
    )


def test_scan_wsl_projects_excludes_home_root_artifacts(tmp_path: Path) -> None:
    home = tmp_path / "wsl-home"
    valid_project = home / "code" / "demo"
    valid_config = _write_config(valid_project)
    _write_config(home)
    global_skill = home / ".agents" / "skills" / "global"
    global_skill.mkdir(parents=True)
    (global_skill / "SKILL.md").write_text("# Global")
    user_agent = home / ".cursor" / "agents" / "global.md"
    user_agent.parent.mkdir(parents=True)
    user_agent.write_text("# Global")

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(valid_config)
    ]
    assert result.skills == []
    assert result.agent_definitions == []


def test_scan_wsl_projects_skips_known_state_dot_dirs_but_descends_unknown(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Known client/tool/OS state dot-dirs (.claude, .local, ...) are pure noise
    on slow 9P mounts: alphabetical DFS explores them before real projects and
    burns the time budget, and they can't produce results anyway (their direct
    artifacts are user-scope, excluded). So the walk must not scandir into them.
    An unknown dot-dir (a versioned ~/.dotfiles repo) is a real project checkout,
    so it is descended and its nested config is discovered."""
    home = tmp_path / "wsl-home"
    session_noise = home / ".claude" / "projects" / "session" / "chunks"
    session_noise.mkdir(parents=True)
    share_noise = home / ".local" / "share" / "app" / "data"
    share_noise.mkdir(parents=True)
    dotfiles_config = _write_config(home / ".dotfiles" / "nested")
    project_config = _write_config(home / "code" / "demo")

    visited: list[str] = []
    original_scandir = os.scandir

    def recording_scandir(path):
        visited.append(str(path))
        return original_scandir(path)

    monkeypatch.setattr(wsl_projects_module.os, "scandir", recording_scandir)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert sorted(config.config_path for config in result.configurations) == sorted(
        [str(dotfiles_config), str(project_config)]
    )
    home_prefix = str(home) + os.sep

    def _top_segment(path: str) -> str:
        return path[len(home_prefix) :].split(os.sep)[0]

    home_visits = {
        _top_segment(path) for path in visited if path.startswith(home_prefix)
    }
    # Known state dot-dirs are never scandir'd; the unknown project dot-dir is.
    assert ".claude" not in home_visits
    assert ".local" not in home_visits
    assert ".dotfiles" in home_visits


def test_scan_wsl_projects_discovers_nested_projects_in_unknown_dot_directory(
    tmp_path: Path,
) -> None:
    """A user's own project checkout kept inside a home-root dot directory
    (e.g. a versioned ``~/.dotfiles`` repo) is not tool state: its nested
    project configs/skills/agents must still be discovered. Only known
    client/tool state dot-dirs are skipped, not every dot-dir."""
    home = tmp_path / "wsl-home"
    nested_config = _write_config(home / ".dotfiles" / "nested")
    nested_skill = home / ".dotfiles" / "nested" / ".agents" / "skills" / "deploy"
    nested_skill.mkdir(parents=True)
    (nested_skill / "SKILL.md").write_text("# Deploy")
    nested_agent = home / ".dotfiles" / "nested" / ".cursor" / "agents" / "reviewer.md"
    nested_agent.parent.mkdir(parents=True)
    nested_agent.write_text(
        "---\nname: reviewer\ndescription: Reviews code\n---\nReview changes."
    )

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(nested_config)
    ]
    assert [skill.name for skill in result.skills] == ["deploy"]
    assert [definition.name for definition in result.agent_definitions] == ["reviewer"]


def test_scan_wsl_projects_caps_project_depth_at_four(tmp_path: Path) -> None:
    home = tmp_path / "wsl-home"
    at_limit = home / "one" / "two" / "three" / "four"
    beyond_limit = at_limit / "five"
    at_limit_config = _write_config(at_limit, _config_content("at-limit"))
    _write_config(beyond_limit, _config_content("beyond-limit"))

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(at_limit_config)
    ]


@pytest.mark.parametrize(
    ("relative_parts", "expected"),
    [
        # Ancestors of / the marker directory itself stay reachable.
        (("one", "two", "three", "four", ".cursor"), True),
        (("one", "two", "three", "four", ".cursor", "agents"), True),
        # Skill trees nest arbitrarily deep by design.
        (("one", "two", "three", "four", ".agents", "skills", "a", "b"), True),
        # Recursive agent patterns (opencode) nest below the marker.
        (("one", "two", "three", "four", ".opencode", "agents", "sub"), True),
        # Inside a config marker dir there is nothing left to find.
        (("one", "two", "three", "four", ".cursor", "extensions"), False),
        (("one", "two", "three", "four", ".cursor", "extensions", "vendor"), False),
        # Non-recursive agent markers hold files directly, not subtrees.
        (("one", "two", "three", "four", ".cursor", "agents", "sub"), False),
    ],
)
def test_can_descend_project_tree_bounds_marker_subtrees(
    relative_parts: tuple[str, ...],
    expected: bool,
) -> None:
    specs = _project_config_specs([_client()])

    assert (
        wsl_projects_module._can_descend_project_tree(relative_parts, specs) is expected
    )


def test_scan_wsl_projects_does_not_walk_inside_config_marker_dirs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    project = home / "one" / "two" / "three" / "four"
    config_path = _write_config(project)
    irrelevant = project / ".cursor" / "extensions" / "vendor" / "assets"
    irrelevant.mkdir(parents=True)
    (irrelevant / "blob.json").write_bytes(_config_content("noise"))

    visited: list[str] = []
    original_scandir = os.scandir

    def recording_scandir(path):
        visited.append(str(path))
        return original_scandir(path)

    monkeypatch.setattr(wsl_projects_module.os, "scandir", recording_scandir)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(config_path)
    ]
    assert not any("extensions" in path for path in visited)


def test_scan_wsl_projects_caps_matched_files_per_home(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    first = _write_config(home / "a", _config_content("a"))
    second = _write_config(home / "b", _config_content("b"))
    _write_config(home / "c", _config_content("c"))
    monkeypatch.setattr(wsl_projects_module, "MAX_WSL_PROJECT_MATCHED_FILES", 2)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(first),
        str(second),
    ]


def test_scan_wsl_projects_followed_matches_share_file_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    link_target = tmp_path / "outside-target.json"
    link_target.write_bytes(_config_content("outside"))
    link_config = home / "a" / ".cursor" / "mcp.json"
    link_config.parent.mkdir(parents=True)
    link_config.symlink_to(link_target)
    second = _write_config(home / "b", _config_content("b"))
    _write_config(home / "c", _config_content("c"))
    monkeypatch.setattr(wsl_projects_module, "MAX_WSL_PROJECT_MATCHED_FILES", 2)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(link_config),
        str(second),
    ]


def test_scan_wsl_projects_broken_matches_do_not_consume_file_cap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    broken = home / "a" / ".cursor" / "mcp.json"
    broken.parent.mkdir(parents=True)
    try:
        broken.symlink_to(tmp_path / "missing.json")
    except OSError:
        pytest.skip("symlinks unavailable")
    second = _write_config(home / "b", _config_content("b"))
    third = _write_config(home / "c", _config_content("c"))
    monkeypatch.setattr(wsl_projects_module, "MAX_WSL_PROJECT_MATCHED_FILES", 2)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [
        str(second),
        str(third),
    ]


def test_scan_wsl_projects_skips_oversized_single_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    _write_config(home / "project")
    monkeypatch.setattr(wsl_projects_module, "MAX_SINGLE_FILE_BYTES", 8)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert result.configurations == []


def test_scan_wsl_projects_returns_partial_results_at_aggregate_byte_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    content = _config_content()
    first = _write_config(home / "a", content)
    external = tmp_path / "external"
    _write_config(external, content)
    try:
        (home / "b").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    monkeypatch.setattr(wsl_projects_module, "MAX_TOTAL_BYTES", len(content) + 1)

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=10,
    )

    assert [config.config_path for config in result.configurations] == [str(first)]


def test_scan_wsl_projects_returns_partial_results_at_time_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "wsl-home"
    first = _write_config(home / "a", _config_content("a"))
    _write_config(home / "b", _config_content("b"))
    clock = {"now": 0.0}
    original_read = wsl_projects_module._read_bounded_file

    def read_and_advance(*args, **kwargs):
        content = original_read(*args, **kwargs)
        clock["now"] = 2.0
        return content

    monkeypatch.setattr(wsl_projects_module.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(
        wsl_projects_module,
        "_read_bounded_file",
        read_and_advance,
    )

    result = scan_wsl_projects(
        clients=[_client()],
        wsl_homes=[home],
        time_budget=1,
    )

    assert [config.config_path for config in result.configurations] == [str(first)]


def test_scaled_wsl_scan_budget_is_bounded() -> None:
    assert wsl_projects_module._scaled_wsl_scan_time_budget(0) == 30
    assert wsl_projects_module._scaled_wsl_scan_time_budget(2) == 50
    assert wsl_projects_module._scaled_wsl_scan_time_budget(100) == 300


def test_scan_wsl_projects_is_non_fatal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        wsl_projects_module,
        "_scan_wsl_projects",
        lambda **kwargs: (_ for _ in ()).throw(OSError("denied")),
    )

    result = scan_wsl_projects(clients=[_client()], wsl_homes=[])

    assert result.configurations == []
    assert result.skills == []
    assert result.agent_definitions == []


# ---------------------------------------------------------------------------
# Descent gate superset invariant
#
# ``_can_descend_project_tree`` hand-re-encodes the matchers' structural rules
# in a different module. The samples below are derived from the live matcher
# definitions so a shape change (new config marker, new agent marker, recursion
# flip, deeper skill nesting) automatically produces new accepted paths the gate
# must still admit — turning silent drift into a red CI run.
# ---------------------------------------------------------------------------

_DESCENT_SPECS = _project_config_specs(get_all_clients())
# Deepest allowed project (the binding case): only here do marker / skills dirs
# sit beyond the depth short circuit and exercise the re-encoded rules.
_PROJECT_PREFIX = tuple(f"p{index}" for index in range(MAX_PROJECT_TREE_DEPTH))
_ROOT = "/"


def _logical(parts: tuple[str, ...]) -> str:
    return posixpath.join(_ROOT, *parts)


def _matcher_accepted_sample_paths() -> list[tuple[str, str, tuple[str, ...]]]:
    """Sample ``(label, kind, parts)`` file paths each matcher accepts."""
    samples: list[tuple[str, str, tuple[str, ...]]] = []

    for spec in _DESCENT_SPECS:
        label = f"config:{spec.client.name}:{'/'.join(spec.relative_parts)}"
        samples.append((label, "config", _PROJECT_PREFIX + spec.relative_parts))

    for pattern in AGENT_DEFINITION_PATTERNS:
        filename = f"definition{pattern.filename_suffix}"
        for marker in pattern.project_markers:
            marker_label = "/".join(marker)
            samples.append(
                (
                    f"agent:{pattern.client}:{marker_label}",
                    "agent",
                    _PROJECT_PREFIX + marker + (filename,),
                )
            )
            # Recursive patterns place files arbitrarily deep below the marker.
            if pattern.project_recursive:
                samples.append(
                    (
                        f"agent-nested:{pattern.client}:{marker_label}",
                        "agent",
                        _PROJECT_PREFIX + marker + ("sub", "deep", filename),
                    )
                )

    # Skills have no per-client metadata to enumerate: the matcher hard-codes a
    # ``skills`` directory with at most one leading dot-directory folded out of
    # the project path, plus arbitrarily deep files beneath the skill dir. Pin
    # every known accepted shape at the deepest project so a depth or dot-prefix
    # change in the matcher or the gate breaks this test.
    skill_file = "SKILL.md"
    assert posixpath.splitext(skill_file)[1].lower() in SKILL_SUPPORTED_EXTENSIONS
    samples.extend(
        [
            ("skill:bare", "skill", _PROJECT_PREFIX + ("skills", "deploy", skill_file)),
            (
                "skill:bare-nested",
                "skill",
                _PROJECT_PREFIX + ("skills", "deploy", "sub", "deep", skill_file),
            ),
            (
                "skill:dot-prefixed",
                "skill",
                _PROJECT_PREFIX + (".agents", "skills", "deploy", skill_file),
            ),
            (
                "skill:dot-prefixed-nested",
                "skill",
                _PROJECT_PREFIX
                + (".agents", "skills", "deploy", "sub", "deep", skill_file),
            ),
        ]
    )

    # Dedupe on parts (clients can share a relative config path) so parametrize
    # ids stay unique and each descent path is checked once.
    deduped: dict[tuple[str, ...], tuple[str, str, tuple[str, ...]]] = {}
    for label, kind, parts in samples:
        deduped.setdefault(parts, (label, kind, parts))
    return list(deduped.values())


_MATCHER_ACCEPTED_SAMPLE_PATHS = _matcher_accepted_sample_paths()


def _matcher_accepts(kind: str, parts: tuple[str, ...]) -> bool:
    logical = _logical(parts)
    if kind == "config":
        return bool(
            _project_candidates_for_path(logical, root_path=_ROOT, specs=_DESCENT_SPECS)
        )
    if kind == "agent":
        return _project_agent_definition_match(logical, root_path=_ROOT) is not None
    if kind == "skill":
        return _project_skill_file_match(logical, root_path=_ROOT) is not None
    raise AssertionError(f"unknown matcher kind {kind!r}")


def test_descent_gate_covers_all_three_matchers() -> None:
    """The samples must exercise every matcher, or a matcher could drift
    unguarded because nothing derives paths from it."""
    kinds = {kind for _, kind, _ in _MATCHER_ACCEPTED_SAMPLE_PATHS}
    assert kinds == {"config", "agent", "skill"}


@pytest.mark.parametrize(
    ("label", "kind", "parts"),
    _MATCHER_ACCEPTED_SAMPLE_PATHS,
    ids=[label for label, _, _ in _MATCHER_ACCEPTED_SAMPLE_PATHS],
)
def test_descent_gate_is_superset_of_every_matcher_accepted_path(
    label: str,
    kind: str,
    parts: tuple[str, ...],
) -> None:
    """Every directory on the path to a matcher-accepted file must be
    descendable, or the budgeted walk silently drops the artifact.

    ``_can_descend_project_tree`` re-encodes the depth / config-marker /
    dot-dir-before-skills / agent-marker+recursion rules from
    ``project_tree_match`` in a separate module. This guards that re-encoding:
    the sample paths come from the live matcher definitions, so if a matcher
    shape drifts and the gate is not widened to match, an ancestor it no longer
    admits fails here instead of silently under-collecting in production.
    """
    # Guard against a vacuous test: the sample must really be matcher-accepted.
    assert _matcher_accepts(kind, parts), (
        f"sample {label!r} is no longer accepted by the {kind} matcher; "
        "regenerate the sample paths from the current matcher definitions"
    )

    for depth in range(1, len(parts)):
        ancestor = parts[:depth]
        assert (
            wsl_projects_module._can_descend_project_tree(ancestor, _DESCENT_SPECS)
            is True
        ), (
            f"{label}: descent gate prunes ancestor {'/'.join(ancestor)!r} that "
            "leads to a matcher-accepted file — artifacts under it would be "
            "silently dropped"
        )
