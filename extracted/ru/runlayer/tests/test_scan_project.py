"""Tests for project-level config scanning using find command."""

import os
import time
from pathlib import Path
from unittest import mock

import pytest
import structlog

from runlayer_cli.scan import project_scanner
from runlayer_cli.scan.clients import (
    ConfigPath,
    MCPClientDefinition,
    ProjectConfigPattern,
    get_client_by_name,
)
from runlayer_cli.scan.project_scanner import (
    EXCLUDED_DIRECTORIES,
    MAX_DISCOVERED_NODE_MODULES,
    MAX_PROJECT_DEPTH,
    MAX_PROJECT_TIMEOUT,
    _PathBudget,
    _clamp_scan_bound,
    _escape_powershell_string,
    _get_project_root,
    _is_within_root,
    _search_unix,
    _search_windows,
    _stream_crawl,
    find_files_and_node_modules_under_home,
    find_files_under_home,
    scan_for_project_configs,
)
from runlayer_cli.scan.resource_governor import (
    ScanResourceLimitExceeded,
    build_governor,
)
from runlayer_cli.scan.scanner_primitives import SymlinkFollowPolicy
from runlayer_cli.scan.symlink_follow import (
    _crawl_followed_symlink_targets,
    _matches_requested_path,
)


class TestGetProjectRoot:
    """Tests for determining project root from config path."""

    def test_mcp_json_at_root(self, tmp_path):
        """For .mcp.json, project root is parent directory."""
        config_path = tmp_path / "my-project" / ".mcp.json"
        project_root = _get_project_root(config_path, path_contains=None)
        assert project_root == tmp_path / "my-project"

    def test_vscode_mcp_json(self, tmp_path):
        """For .vscode/mcp.json, project root is grandparent directory."""
        config_path = tmp_path / "my-project" / ".vscode" / "mcp.json"
        project_root = _get_project_root(config_path, path_contains=".vscode")
        assert project_root == tmp_path / "my-project"

    def test_windsurf_config(self, tmp_path):
        """For .windsurf/mcp_config.json, project root is grandparent."""
        config_path = tmp_path / "my-project" / ".windsurf" / "mcp_config.json"
        project_root = _get_project_root(config_path, path_contains=".windsurf")
        assert project_root == tmp_path / "my-project"

    def test_junie_nested_mcp_json(self, tmp_path):
        """For .junie/mcp/mcp.json, strip both config directories."""
        config_path = tmp_path / "my-project" / ".junie" / "mcp" / "mcp.json"
        project_root = _get_project_root(config_path, path_contains=".junie/mcp")
        assert project_root == tmp_path / "my-project"


class TestScanForProjectConfigs:
    """Integration tests for the main scanning function."""

    @pytest.fixture(autouse=True)
    def _single_top_level_shard(self, monkeypatch):
        monkeypatch.setattr(
            project_scanner, "_crawlable_home_subdirs", lambda *_a, **_k: []
        )

    def test_returns_empty_for_no_clients(self):
        """Returns empty list when no clients have project configs."""
        client = MCPClientDefinition(
            name="cursor",
            display_name="Cursor",
            paths=[],
            project_config=None,  # No project config
        )
        results = scan_for_project_configs([client])
        assert results == []

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_uses_find_on_macos(self, mock_system, mock_search, tmp_path):
        """Uses find command for searching on macOS."""
        # Setup mock to return a found path
        config_path = tmp_path / "project" / ".mcp.json"
        config_path.parent.mkdir(parents=True)
        config_path.touch()
        mock_search.return_value = [config_path]

        client = MCPClientDefinition(
            name="claude_code",
            display_name="Claude Code",
            paths=[],
            project_config=ProjectConfigPattern(
                relative_path=".mcp.json",
                servers_key="mcpServers",
            ),
        )

        results = scan_for_project_configs([client])

        mock_search.assert_called_once()
        assert len(results) == 1
        assert results[0].client_name == "claude_code"

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_matches_vscode_path_pattern(self, mock_system, mock_search, tmp_path):
        """Correctly matches VS Code configs in .vscode directories."""
        # VS Code config in .vscode/
        vscode_config = tmp_path / "project" / ".vscode" / "mcp.json"
        vscode_config.parent.mkdir(parents=True)
        vscode_config.touch()

        # Another mcp.json NOT in .vscode (should not match)
        other_config = tmp_path / "other" / "mcp.json"
        other_config.parent.mkdir(parents=True)
        other_config.touch()

        mock_search.return_value = [vscode_config, other_config]

        client = MCPClientDefinition(
            name="vscode",
            display_name="VS Code",
            paths=[],
            project_config=ProjectConfigPattern(
                relative_path=".vscode/mcp.json",
                servers_key="servers",
            ),
        )

        results = scan_for_project_configs([client])

        # Should only find the one in .vscode/
        assert len(results) == 1
        assert results[0].config_path == vscode_config
        assert results[0].project_path == tmp_path / "project"

    def test_matches_multi_segment_junie_path_pattern(self, tmp_path):
        """Match the full .junie/mcp suffix and attribute it to the repo root."""
        junie_config = tmp_path / "project" / ".junie" / "mcp" / "mcp.json"
        junie_config.parent.mkdir(parents=True)
        junie_config.touch()

        wrong_config = tmp_path / "other" / ".not-junie" / "mcp" / "mcp.json"
        wrong_config.parent.mkdir(parents=True)
        wrong_config.touch()

        client = MCPClientDefinition(
            name="junie",
            display_name="JetBrains Junie",
            paths=[],
            project_config=ProjectConfigPattern(
                relative_path=".junie/mcp/mcp.json",
                servers_key="mcpServers",
            ),
        )

        results = scan_for_project_configs(
            [client],
            precomputed_paths=[junie_config, wrong_config],
        )

        assert len(results) == 1
        assert results[0].config_path == junie_config
        assert results[0].project_path == tmp_path / "project"

    def test_matches_kilo_root_config_with_modern_server_key(self, tmp_path):
        """Kilo reads project-level kilo.jsonc directly from the repo root."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        kilo_config = project_root / "kilo.jsonc"
        kilo_config.touch()

        client = get_client_by_name("kilo_code")
        results = scan_for_project_configs(
            [client],
            precomputed_paths=[kilo_config],
        )

        assert len(results) == 1
        assert results[0].config_path == kilo_config
        assert results[0].project_path == project_root
        assert results[0].servers_key == "mcp"

    def test_nested_kilo_config_uses_only_specific_project_pattern(self, tmp_path):
        """A nested Kilo config must not also match its root-level basename."""
        project_root = tmp_path / "project"
        kilo_config = project_root / ".kilo" / "kilo.jsonc"
        kilo_config.parent.mkdir(parents=True)
        kilo_config.touch()

        client = get_client_by_name("kilo_code")
        results = scan_for_project_configs(
            [client],
            precomputed_paths=[kilo_config],
        )

        assert len(results) == 1
        assert results[0].config_path == kilo_config
        assert results[0].project_path == project_root
        assert results[0].servers_key == "mcp"

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_excludes_global_config_from_project_results(
        self, mock_system, mock_search, tmp_path
    ):
        """Global config at ~/.cursor/mcp.json must not be reported as a project config.

        Regression: Cursor's global path (~/.cursor/mcp.json) and project pattern
        (.cursor/mcp.json) share the same structure. The find command picks up the
        global config, its parent ".cursor" matches path_contains, and _get_project_root
        resolves to $HOME — causing a duplicate scan.
        """
        home = tmp_path / "home"
        global_config = home / ".cursor" / "mcp.json"
        global_config.parent.mkdir(parents=True)
        global_config.touch()

        project_config = home / "projects" / "myapp" / ".cursor" / "mcp.json"
        project_config.parent.mkdir(parents=True)
        project_config.touch()

        mock_search.return_value = [global_config, project_config]

        client = MCPClientDefinition(
            name="cursor",
            display_name="Cursor",
            paths=[ConfigPath(str(home / ".cursor/mcp.json"), platform="all")],
            servers_key="mcpServers",
            project_config=ProjectConfigPattern(
                relative_path=".cursor/mcp.json",
                servers_key="mcpServers",
            ),
        )

        results = scan_for_project_configs([client])

        assert len(results) == 1
        assert results[0].config_path == project_config
        assert results[0].project_path == home / "projects" / "myapp"

    def test_excludes_plugin_bundled_config_from_project_results(self, tmp_path):
        """Plugin-bundled .mcp.json must not be re-detected as a project config.

        Regression (ENG-3528): a Copilot plugin's .mcp.json lives at
        ~/.copilot/installed-plugins/<market>/<plugin>/.mcp.json and is already
        reported with config_scope="plugin" by scan_copilot_plugins. The shared
        home crawl also surfaces it, where it would be double-counted under
        github_copilot_cli (duplicate) and claude_code (wrong client) which both
        match .mcp.json. Paths under installed-plugins must be skipped.
        """
        plugin_config = (
            tmp_path
            / ".copilot"
            / "installed-plugins"
            / "my-market"
            / "my-plugin"
            / ".mcp.json"
        )
        plugin_config.parent.mkdir(parents=True)
        plugin_config.touch()

        real_project_config = tmp_path / "projects" / "myapp" / ".mcp.json"
        real_project_config.parent.mkdir(parents=True)
        real_project_config.touch()

        client = MCPClientDefinition(
            name="github_copilot_cli",
            display_name="GitHub Copilot CLI",
            paths=[],
            project_config=ProjectConfigPattern(
                relative_path=".mcp.json",
                servers_key="mcpServers",
            ),
        )

        results = scan_for_project_configs(
            [client],
            precomputed_paths=[plugin_config, real_project_config],
        )

        assert len(results) == 1
        assert results[0].config_path == real_project_config

    @pytest.mark.parametrize(
        "plugin_relative_path",
        [
            ".claude/plugins/marketplaces/official/discord/.mcp.json",
            ".claude/plugins/marketplaces/official/external_plugins/linear/.mcp.json",
            ".cursor/plugins/cache/cursor-public/box/version/.mcp.json",
            ".codex/plugins/cache/example/.mcp.json",
        ],
    )
    def test_excludes_client_plugin_config_from_project_results(
        self,
        tmp_path: Path,
        plugin_relative_path: str,
    ):
        """Client plugin configs must not be re-detected as project configs."""
        plugin_config = tmp_path / plugin_relative_path
        plugin_config.parent.mkdir(parents=True)
        plugin_config.touch()

        real_project_config = tmp_path / "projects" / "myapp" / ".mcp.json"
        real_project_config.parent.mkdir(parents=True)
        real_project_config.touch()

        client = MCPClientDefinition(
            name="github_copilot_cli",
            display_name="GitHub Copilot CLI",
            paths=[],
            project_config=ProjectConfigPattern(
                relative_path=".mcp.json",
                servers_key="mcpServers",
            ),
        )

        results = scan_for_project_configs(
            [client],
            precomputed_paths=[plugin_config, real_project_config],
        )

        assert [result.config_path for result in results] == [real_project_config]

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_does_not_match_similar_directory_names(
        self, mock_system, mock_search, tmp_path
    ):
        """Does not match paths where expected parent is a substring of actual parent.

        Regression test: .vscode_backup/mcp.json should NOT match when looking for
        .vscode/mcp.json, even though '.vscode' is a substring of '.vscode_backup'.
        """
        # Valid VS Code config in .vscode/
        valid_config = tmp_path / "project1" / ".vscode" / "mcp.json"
        valid_config.parent.mkdir(parents=True)
        valid_config.touch()

        # Invalid: .vscode_backup should NOT match (substring of expected parent)
        backup_config = tmp_path / "project2" / ".vscode_backup" / "mcp.json"
        backup_config.parent.mkdir(parents=True)
        backup_config.touch()

        # Invalid: .vscode_old should NOT match
        old_config = tmp_path / "project3" / ".vscode_old" / "mcp.json"
        old_config.parent.mkdir(parents=True)
        old_config.touch()

        mock_search.return_value = [valid_config, backup_config, old_config]

        client = MCPClientDefinition(
            name="vscode",
            display_name="VS Code",
            paths=[],
            project_config=ProjectConfigPattern(
                relative_path=".vscode/mcp.json",
                servers_key="servers",
            ),
        )

        results = scan_for_project_configs([client])

        # Should only find the one in exact .vscode/ directory
        assert len(results) == 1
        assert results[0].config_path == valid_config
        assert results[0].project_path == tmp_path / "project1"


class TestSearchUnix:
    """Tests for the Unix find command search."""

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_surfaces_symlinks_without_following_them(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        (external / ".mcp.json").write_text("{}")
        link = home / "projects"
        link.symlink_to(external, target_is_directory=True)
        symlink_paths = []

        results = _search_unix(
            [".mcp.json"],
            timeout=30,
            max_depth=3,
            roots=[home],
            symlink_paths=symlink_paths,
        )

        assert results == []
        assert symlink_paths == [link]

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_builds_correct_find_command(self, mock_run, tmp_path):
        """Builds correct find command with exclusions."""
        mock_run.return_value = mock.Mock(
            stdout="",
            returncode=0,
        )
        roots = [tmp_path / "first", tmp_path / "second"]

        _search_unix(
            [".mcp.json", "mcp.json"],
            timeout=30,
            max_depth=5,
            roots=roots,
        )

        # Verify find was called
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]

        # Check command structure
        assert cmd[:3] == ["find", *(str(root) for root in roots)]
        assert "-maxdepth" in cmd
        assert "5" in cmd
        assert "-type" in cmd
        assert "f" in cmd
        assert ".mcp.json" in cmd
        assert "mcp.json" in cmd
        # Check exclusions
        assert "*/node_modules/*" in cmd or "node_modules" in str(cmd)

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_prints_node_modules_before_pruning(self, mock_run, tmp_path):
        config = tmp_path / ".mcp.json"
        config.write_text("{}")
        node_modules = tmp_path / "renamed-prefix" / "lib" / "node_modules"
        node_modules.mkdir(parents=True)
        mock_run.return_value = mock.Mock(
            stdout=f"{node_modules}\n{config}\n",
            returncode=0,
        )

        results = _search_unix(
            [".mcp.json"],
            timeout=30,
            max_depth=7,
            roots=[tmp_path],
            discover_node_modules=True,
        )

        assert set(results) == {config, node_modules}
        command = mock_run.call_args[0][0]
        node_index = command.index("node_modules")
        assert command[node_index - 1 : node_index + 4] == [
            "-name",
            "node_modules",
            "-print",
            "-prune",
            ")",
        ]

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_handles_timeout(self, mock_run):
        """Handles subprocess timeout gracefully."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="find", timeout=30)

        # Should not raise, just return empty list
        results = _search_unix([".mcp.json"], timeout=30, max_depth=5)
        assert results == []


class TestClampScanBound:
    """Unit tests for the shared scan-bound clamp helper."""

    def test_clamps_above_maximum(self):
        assert _clamp_scan_bound(50, default=5, maximum=MAX_PROJECT_DEPTH) == 20

    def test_passes_through_in_range(self):
        assert _clamp_scan_bound(12, default=5, maximum=MAX_PROJECT_DEPTH) == 12

    def test_clamps_below_one_to_one(self):
        assert _clamp_scan_bound(0, default=5, maximum=MAX_PROJECT_DEPTH) == 1
        assert _clamp_scan_bound(-3, default=5, maximum=MAX_PROJECT_DEPTH) == 1

    def test_non_int_falls_back_to_default(self):
        assert _clamp_scan_bound("7", default=5, maximum=MAX_PROJECT_DEPTH) == 5
        assert _clamp_scan_bound(None, default=5, maximum=MAX_PROJECT_DEPTH) == 5

    def test_bool_falls_back_to_default(self):
        # isinstance(True, int) is True, so bool must be rejected explicitly.
        assert _clamp_scan_bound(True, default=5, maximum=MAX_PROJECT_DEPTH) == 5


@pytest.mark.parametrize(
    ("path", "pattern", "windows", "expected"),
    [
        (Path("/home/project/skill.md"), "SKILL.md", False, True),
        (Path("/home/project/app.csproj"), "*.csproj", False, True),
        (
            Path("/home/project/.cursor/agents/fix.md"),
            ".cursor/agents/*.md",
            False,
            True,
        ),
        (Path("/home/project/.MCP.JSON"), ".mcp.json", False, False),
        (Path("C:/Users/alex/project/.MCP.JSON"), ".mcp.json", True, True),
        (
            Path("C:/Users/alex/project/.CURSOR/AGENTS/fix.MD"),
            ".cursor/agents/*.md",
            True,
            True,
        ),
    ],
)
def test_symlink_path_matching_semantics(path, pattern, windows, expected):
    assert _matches_requested_path(path, [pattern], windows=windows) is expected


@pytest.mark.skipif(os.name == "nt", reason="Unix symlink behavior")
def test_failed_path_reservation_does_not_consume_follow_capacity(tmp_path):
    file_target = tmp_path / "opaque"
    file_target.write_text("{}")
    file_link = tmp_path / ".mcp.json"
    file_link.symlink_to(file_target)
    directory_target = tmp_path / "project"
    directory_target.mkdir()
    directory_link = tmp_path / "z-project"
    directory_link.symlink_to(directory_target, target_is_directory=True)
    searched_roots: list[Path] = []

    def fake_search(_filenames, _timeout, _max_depth, **kwargs):
        searched_roots.extend(kwargs["roots"])
        return []

    _crawl_followed_symlink_targets(
        [".mcp.json"],
        [directory_link, file_link],
        deadline=time.monotonic() + 10,
        policy=SymlinkFollowPolicy(scan_areas=(), max_followed=1),
        system="Darwin",
        governor=None,
        path_budget=_PathBudget(0),
        discover_node_modules=False,
        max_workers=1,
        follow_depth=2,
        search_unix=fake_search,
        search_windows=fake_search,
    )

    assert searched_roots == [directory_target.resolve()]


class TestFindFilesUnderHomeClamp:
    """find_files_under_home clamps depth/timeout into the supported range
    before crawling — backstop for non-typer programmatic callers."""

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_clamps_depth_above_max(self, mock_system, mock_search, monkeypatch):
        mock_search.return_value = []
        monkeypatch.setattr(
            project_scanner,
            "_crawlable_home_subdirs",
            lambda *_a, **_k: [Path("/home/user/project")],
        )
        find_files_under_home([".mcp.json"], timeout=60, max_depth=50)
        depths = [call.args[2] for call in mock_search.call_args_list]
        assert depths == [1, MAX_PROJECT_DEPTH - 1]

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_clamps_timeout_above_max(self, mock_system, mock_search):
        mock_search.return_value = []
        find_files_under_home([".mcp.json"], timeout=999, max_depth=5)
        remaining = mock_search.call_args[0][1]
        assert 0 < remaining <= MAX_PROJECT_TIMEOUT

    @mock.patch("runlayer_cli.scan.project_scanner._search_unix")
    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system", return_value="Darwin"
    )
    def test_passes_in_range_values_through(
        self, mock_system, mock_search, monkeypatch
    ):
        mock_search.return_value = []
        monkeypatch.setattr(
            project_scanner,
            "_crawlable_home_subdirs",
            lambda *_a, **_k: [Path("/home/user/project")],
        )
        find_files_under_home([".mcp.json"], timeout=120, max_depth=15)
        assert all(0 < call.args[1] <= 120 for call in mock_search.call_args_list)
        assert [call.args[2] for call in mock_search.call_args_list] == [1, 14]


class TestFindFilesUnderProjectRoots:
    def test_dedupes_nested_roots_and_applies_bounds(self, monkeypatch, tmp_path):
        project = tmp_path / "code" / "project"
        nested_project = project / "packages" / "nested"
        nested_skill = nested_project / ".claude" / "skills" / "deep" / "SKILL.md"
        nested_project.mkdir(parents=True)
        calls = []

        def fake_search(filenames, timeout, max_depth, **kwargs):
            calls.append(
                {
                    "filenames": filenames,
                    "timeout": timeout,
                    "max_depth": max_depth,
                    **kwargs,
                }
            )
            return [nested_skill]

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(project_scanner, "_search_unix", fake_search)

        results = project_scanner.find_files_under_project_roots(
            ["SKILL.md", ".cursor/agents/*.md"],
            [nested_project, project, project],
            timeout=12,
            max_depth=8,
            max_paths=25,
        )

        assert results == [nested_skill]
        assert len(calls) == 1
        assert calls[0]["roots"] == [project]
        assert calls[0]["max_depth"] == 8
        assert 0 < calls[0]["timeout"] <= 12

    def test_scans_roots_outside_home(self, monkeypatch, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        hit = outside / "SKILL.md"
        search = mock.Mock(return_value=[hit])
        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(project_scanner, "_search_unix", search)

        results = project_scanner.find_files_under_project_roots(
            ["SKILL.md"],
            [outside],
        )

        assert results == [hit]
        assert search.call_args.kwargs["roots"] == [outside.resolve()]

    def test_combined_helper_keeps_logical_home_and_canonical_external_roots(
        self,
        monkeypatch,
        tmp_path,
    ):
        home = tmp_path / "home"
        home_project = home / "project"
        home_project.mkdir(parents=True)
        external_project = tmp_path / "external"
        external_project.mkdir()
        nested_skill = external_project / ".claude" / "skills" / "deep" / "SKILL.md"
        calls = []

        def fake_search(filenames, timeout, max_depth, **kwargs):
            calls.append(kwargs["roots"])
            return [nested_skill]

        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(project_scanner, "scan_worker_count", lambda _governor: 1)
        monkeypatch.setattr(project_scanner, "_search_unix", fake_search)

        results = project_scanner.find_files_under_project_roots(
            ["SKILL.md"],
            [home_project, external_project],
        )

        assert results == [nested_skill]
        assert calls == [[home_project, external_project.resolve()]]

    def test_combined_helper_shares_budget_across_root_scopes(
        self,
        monkeypatch,
        tmp_path,
    ):
        home = tmp_path / "home"
        home_project = home / "project"
        home_project.mkdir(parents=True)
        external_project = tmp_path / "external"
        external_project.mkdir()
        calls = []

        def fake_search(filenames, timeout, max_depth, **kwargs):
            calls.append(kwargs)
            return []

        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(project_scanner, "scan_worker_count", lambda _governor: 2)
        monkeypatch.setattr(project_scanner, "_search_unix", fake_search)

        project_scanner.find_files_under_project_roots(
            ["SKILL.md"],
            [home_project, external_project],
            max_paths=25,
        )

        assert {root for call in calls for root in call["roots"]} == {
            home_project,
            external_project.resolve(),
        }
        assert len({id(call["path_budget"]) for call in calls}) == 1

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_in_home_helper_iteratively_follows_symlinks(
        self,
        monkeypatch,
        tmp_path,
    ):
        home = tmp_path / "home"
        project = home / "project"
        project.mkdir(parents=True)
        first_target = tmp_path / "first-target"
        first_target.mkdir()
        second_target = tmp_path / "second-target"
        second_target.mkdir()
        skill = second_target / "SKILL.md"
        skill.write_text("# skill")
        (project / "linked-first").symlink_to(
            first_target,
            target_is_directory=True,
        )
        (first_target / "linked-second").symlink_to(
            second_target,
            target_is_directory=True,
        )
        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")

        results = project_scanner.find_files_under_project_roots(
            ["SKILL.md"],
            [project],
        )

        assert results == [skill.resolve()]

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_external_helper_iteratively_follows_symlinks(
        self,
        monkeypatch,
        tmp_path,
    ):
        home = tmp_path / "home"
        home.mkdir()
        project = tmp_path / "external-project"
        project.mkdir()
        first_target = tmp_path / "first-target"
        first_target.mkdir()
        second_target = tmp_path / "second-target"
        second_target.mkdir()
        skill = second_target / "SKILL.md"
        skill.write_text("# skill")
        (project / "linked-first").symlink_to(
            first_target,
            target_is_directory=True,
        )
        (first_target / "linked-second").symlink_to(
            second_target,
            target_is_directory=True,
        )
        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")

        results = project_scanner.find_files_under_project_roots(
            ["SKILL.md"],
            [project],
        )

        assert results == [skill.resolve()]

    def test_windows_search_stays_inside_home(self, monkeypatch, tmp_path):
        home = tmp_path / "home"
        project = home / "project"
        project.mkdir(parents=True)
        calls = []

        def fake_search(filenames, timeout, max_depth, **kwargs):
            calls.append(
                {
                    "max_depth": max_depth,
                    "containment_root": kwargs["containment_root"],
                    "roots": kwargs["roots"],
                }
            )
            return []

        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Windows")
        monkeypatch.setattr(project_scanner, "_search_windows", fake_search)

        project_scanner.find_files_under_project_roots(
            ["SKILL.md"],
            [project],
            max_depth=8,
        )

        assert calls == [
            {
                "max_depth": 7,
                "containment_root": home,
                "roots": [project],
            }
        ]


class TestFindFilesUnderHomeUnixSharding:
    @pytest.mark.parametrize("configured_depth", [3, 12])
    @pytest.mark.skipif(os.name == "nt", reason="Unix symlink behavior")
    def test_followed_roots_use_configured_home_depth(
        self,
        configured_depth,
        tmp_path,
    ):
        home = tmp_path / "home"
        home.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        link = home / "project"
        link.symlink_to(external, target_is_directory=True)
        followed_depths: list[int] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            if kwargs["roots"] == [home]:
                kwargs["symlink_paths"].append(link)
            else:
                followed_depths.append(max_depth)
            return []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
            mock.patch.object(
                project_scanner,
                "_crawlable_home_subdirs",
                return_value=[],
            ),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
        ):
            find_files_under_home([".mcp.json"], max_depth=configured_depth)

        assert followed_depths == [configured_depth]

    @pytest.mark.skipif(os.name == "nt", reason="Unix symlink behavior")
    def test_depth_one_sharding_surfaces_links_and_keeps_excludes(self, tmp_path):
        home = tmp_path / "home"
        real_root = home / "project"
        real_root.mkdir(parents=True)
        external = tmp_path / "external"
        external.mkdir()
        link = home / "linked"
        link.symlink_to(external, target_is_directory=True)
        excluded_link = home / ".cache"
        excluded_link.symlink_to(external, target_is_directory=True)
        symlink_paths: list[Path] = []

        roots = project_scanner._crawlable_home_subdirs(
            home,
            windows=False,
            symlink_paths=symlink_paths,
        )

        assert roots == [real_root]
        assert symlink_paths == [link]

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_follows_external_symlink_root(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        config = external / ".mcp.json"
        config.write_text("{}")
        (home / "projects").symlink_to(external, target_is_directory=True)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=2,
            )

        assert results == [config.resolve()]

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_skips_link_to_excluded_target_directory(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        excluded_target = tmp_path / "external" / ".venv"
        excluded_target.mkdir(parents=True)
        (excluded_target / ".mcp.json").write_text("{}")
        (home / "a-excluded").symlink_to(
            excluded_target,
            target_is_directory=True,
        )
        wanted_target = tmp_path / "wanted"
        wanted_target.mkdir()
        wanted_config = wanted_target / ".mcp.json"
        wanted_config.write_text("{}")
        (home / "z-wanted").symlink_to(
            wanted_target,
            target_is_directory=True,
        )

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
            mock.patch.object(
                project_scanner,
                "MAX_FOLLOWED_SYMLINK_TARGETS",
                1,
            ),
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=2,
            )

        assert results == [wanted_config.resolve()]

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_drains_links_found_in_followed_roots(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        first = tmp_path / "first"
        first.mkdir()
        second = tmp_path / "second"
        second.mkdir()
        config = second / ".mcp.json"
        config.write_text("{}")
        (home / "projects").symlink_to(first, target_is_directory=True)
        (first / "next").symlink_to(second, target_is_directory=True)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=2,
            )

        assert results == [config.resolve()]

    @pytest.mark.skipif(os.name == "nt", reason="Unix symlink behavior")
    def test_scans_each_external_realpath_once_across_aliases_and_cycles(
        self,
        tmp_path,
    ):
        home = tmp_path / "home"
        home.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        config = external / ".mcp.json"
        config.write_text("{}")
        first_link = home / "first"
        first_link.symlink_to(external, target_is_directory=True)
        second_link = home / "second"
        second_link.symlink_to(external, target_is_directory=True)
        back_link = external / "back"
        back_link.symlink_to(external, target_is_directory=True)
        external_scans = 0

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            nonlocal external_scans
            if kwargs["roots"] == [external.resolve()]:
                external_scans += 1
                kwargs["symlink_paths"].append(back_link)
                return [config]
            return []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
        ):
            results = find_files_under_home([".mcp.json"], max_depth=2)

        assert results == [config]
        assert external_scans == 1

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_includes_matching_external_symlinked_file(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        target = tmp_path / "external" / "opaque"
        target.parent.mkdir()
        target.write_text("{}")
        link = home / ".mcp.json"
        link.symlink_to(target)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
        ):
            results = find_files_under_home([".mcp.json"], max_depth=2)

        assert results == [target.resolve()]

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_skips_external_symlinked_file_with_unmatched_link_name(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        target = tmp_path / "external" / ".mcp.json"
        target.parent.mkdir()
        target.write_text("{}")
        (home / "not-requested.json").symlink_to(target)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
        ):
            results = find_files_under_home([".mcp.json"], max_depth=2)

        assert results == []

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_unmatched_file_links_do_not_consume_follow_cap(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        noise_root = tmp_path / "noise"
        noise_root.mkdir()
        for index in range(64):
            target = noise_root / f"noise-{index:03}"
            target.write_text("noise")
            (home / f"a-noise-{index:03}").symlink_to(target)
        project = tmp_path / "wanted-project"
        project.mkdir()
        config = project / ".mcp.json"
        config.write_text("{}")
        (home / "z-project").symlink_to(project, target_is_directory=True)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
        ):
            results = find_files_under_home([".mcp.json"], max_depth=2)

        assert results == [config.resolve()]

    @pytest.mark.skipif(os.name == "nt", reason="Unix find and symlink behavior")
    def test_symlinked_node_modules_is_discovered_without_descent(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        target = tmp_path / "external-packages" / "vendor"
        target.mkdir(parents=True)
        hidden_config = target / ".mcp.json"
        hidden_config.write_text("{}")
        (home / "node_modules").symlink_to(target, target_is_directory=True)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
        ):
            result = find_files_and_node_modules_under_home(
                [".mcp.json"],
                max_depth=2,
            )

        assert result.found_paths == []
        assert result.node_modules_paths == [target.resolve()]

    def test_partitions_dedupes_and_caps_node_modules(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        config = home / ".mcp.json"
        node_modules = [
            home / f"renamed-{index:03}" / "node_modules"
            for index in range(MAX_DISCOVERED_NODE_MODULES + 10)
        ]

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
            mock.patch.object(
                project_scanner,
                "_search_unix",
                return_value=[config, *node_modules, node_modules[0]],
            ),
        ):
            result = find_files_and_node_modules_under_home(
                [".mcp.json"],
                max_depth=1,
            )

        assert result.found_paths == [config]
        assert (
            result.node_modules_paths
            == sorted(node_modules)[:MAX_DISCOVERED_NODE_MODULES]
        )

    def test_shards_consume_one_aggregate_deadline(self, tmp_path):
        home = tmp_path / "home"
        project = home / "project"
        project.mkdir(parents=True)

        budgets: list[tuple[int, float]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            budgets.append((max_depth, timeout))
            return []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform, "system", return_value="Darwin"
            ),
            mock.patch.object(project_scanner, "scan_worker_count", return_value=1),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
            mock.patch(
                "runlayer_cli.scan.project_scanner.time.monotonic",
                side_effect=[100.0, 100.0, 110.0],
            ),
        ):
            find_files_under_home([".mcp.json"], timeout=30, max_depth=7)

        assert budgets == [(1, 30.0), (6, 20.0)]

    def test_parallel_shards_collect_symlinks_in_local_lists(self, tmp_path):
        home = tmp_path / "home"
        for name in ("first", "second"):
            (home / name).mkdir(parents=True)
        symlink_list_ids: list[int] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            symlink_list_ids.append(id(kwargs["symlink_paths"]))
            return []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
            mock.patch.object(project_scanner, "scan_worker_count", return_value=2),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
        ):
            find_files_under_home([".mcp.json"], timeout=30, max_depth=7)

        assert len(symlink_list_ids) > 1
        assert len(set(symlink_list_ids)) == len(symlink_list_ids)

    @pytest.mark.skipif(os.name == "nt", reason="Unix symlink behavior")
    def test_followed_roots_reuse_deadline_and_path_budget(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        config = external / ".mcp.json"
        config.write_text("{}")
        (home / "project").symlink_to(external, target_is_directory=True)
        calls: list[tuple[list[Path], float, int]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            calls.append((kwargs["roots"], timeout, id(kwargs["path_budget"])))
            return [config] if kwargs["roots"] == [external.resolve()] else []

        governor = build_governor(max_paths=100)
        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Darwin",
            ),
            mock.patch.object(project_scanner, "scan_worker_count", return_value=1),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
            mock.patch(
                "runlayer_cli.scan.project_scanner.time.monotonic",
                side_effect=[100.0, 100.0, 105.0, 110.0],
            ),
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=2,
                governor=governor,
            )

        assert results == [config]
        assert [(roots, timeout) for roots, timeout, _ in calls] == [
            ([home], 30.0),
            ([external.resolve()], 20.0),
        ]
        assert len({budget_id for _, _, budget_id in calls}) == 1

    def test_skips_shard_started_after_deadline_and_keeps_results(self, tmp_path):
        home = tmp_path / "home"
        project = home / "project"
        project.mkdir(parents=True)
        top_hit = home / ".mcp.json"

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform, "system", return_value="Darwin"
            ),
            mock.patch.object(project_scanner, "scan_worker_count", return_value=1),
            mock.patch.object(
                project_scanner,
                "_search_unix",
                return_value=[top_hit],
            ) as mock_search,
            mock.patch(
                "runlayer_cli.scan.project_scanner.time.monotonic",
                side_effect=[100.0, 100.0, 131.0],
            ),
            structlog.testing.capture_logs() as logs,
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=7,
            )

        assert results == [top_hit]
        mock_search.assert_called_once()
        skipped = [
            log for log in logs if log["event"] == "crawl_shard_skipped_deadline"
        ]
        assert len(skipped) == 1
        assert skipped[0]["roots"] == [str(project)]

    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system",
        return_value="Darwin",
    )
    def test_groups_recursive_roots_into_at_most_worker_count(
        self, mock_system, tmp_path
    ):
        home = tmp_path / "home"
        roots = [home / f"project-{index}" for index in range(7)]
        for root in roots:
            root.mkdir(parents=True)

        calls: list[tuple[list[Path], int]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            calls.append((kwargs["roots"], max_depth))
            return []

        governor = build_governor(cpu_cores=2, max_cpu_percent=100)
        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
        ):
            find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=7,
                governor=governor,
            )

        top_calls = [call for call in calls if call[1] == 1]
        assert top_calls == [([home], 1)]
        recursive_calls = [call for call in calls if call[1] == 6]
        assert len(recursive_calls) == 2
        assert sorted(root for group, _ in recursive_calls for root in group) == roots

    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system",
        return_value="Darwin",
    )
    def test_shards_depth_one_roots_and_keeps_top_level_files(
        self, mock_system, tmp_path
    ):
        home = tmp_path / "home"
        home.mkdir()
        project = home / "project"
        project.mkdir()
        docs = home / "docs"
        docs.mkdir()
        excluded = home / ".cache"
        excluded.mkdir()

        top_hit = home / ".mcp.json"
        project_hit = project / ".mcp.json"
        docs_hit = docs / "SKILL.md"
        root_hits = {
            home: top_hit,
            project: project_hit,
            docs: docs_hit,
        }
        calls: list[tuple[list[Path], int]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            roots = kwargs["roots"]
            calls.append((roots, max_depth))
            return [root_hits[root] for root in roots]

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
        ):
            results = find_files_under_home(
                [".mcp.json", "SKILL.md"],
                timeout=30,
                max_depth=7,
            )

        assert results == sorted([top_hit, project_hit, docs_hit])
        top_calls = [call for call in calls if call[1] == 1]
        assert top_calls == [([home], 1)]
        recursive_roots = [
            root for roots, depth in calls if depth == 6 for root in roots
        ]
        assert sorted(recursive_roots) == sorted([project, docs])

    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system",
        return_value="Darwin",
    )
    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_one_timed_out_shard_keeps_other_results(
        self, mock_run, mock_system, tmp_path
    ):
        import subprocess

        home = tmp_path / "home"
        fast = home / "fast"
        slow = home / "slow"
        fast.mkdir(parents=True)
        slow.mkdir()
        fast_hit = fast / ".mcp.json"
        fast_hit.touch()

        def run_find(command, **kwargs):
            root = Path(command[1])
            if root == slow:
                raise subprocess.TimeoutExpired(command, timeout=30)
            stdout = f"{fast_hit}\n" if root == fast else ""
            return mock.Mock(stdout=stdout, returncode=0)

        mock_run.side_effect = run_find
        with mock.patch.object(Path, "home", return_value=home):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=7,
            )

        assert results == [fast_hit]

    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system",
        return_value="Darwin",
    )
    def test_shards_share_one_aggregate_path_budget(self, mock_system, tmp_path):
        home = tmp_path / "home"
        roots = [home / name for name in ("alpha", "bravo", "charlie")]
        for root in roots:
            root.mkdir(parents=True)

        budget_ids: set[int] = set()

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            budget = kwargs["path_budget"]
            budget_ids.add(id(budget))
            hits = []
            for root in kwargs["roots"]:
                if not budget.reserve():
                    break
                hits.append(root / ".mcp.json")
            return hits

        governor = build_governor(
            cpu_cores=4,
            max_cpu_percent=100,
            max_paths=2,
        )
        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(project_scanner, "_search_unix", side_effect=fake_search),
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=7,
                governor=governor,
            )

        assert len(results) == 2
        assert len(budget_ids) == 1


class TestFindFilesUnderHomeWindowsSharding:
    def test_user_context_follows_external_reparse_root(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        external = tmp_path / "external"
        external.mkdir()
        config = external / ".mcp.json"
        config.write_text("{}")
        (home / "project").symlink_to(external, target_is_directory=True)
        calls: list[dict[str, object]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            calls.append({"max_depth": max_depth, **kwargs})
            return [config] if kwargs["roots"] == [external.resolve()] else []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform,
                "system",
                return_value="Windows",
            ),
            mock.patch.object(
                project_scanner,
                "is_windows_system_context",
                return_value=False,
            ),
            mock.patch.object(
                project_scanner,
                "_search_windows",
                side_effect=fake_search,
            ),
        ):
            results = find_files_under_home([".mcp.json"], max_depth=2)

        assert results == [config]
        external_calls = [
            call for call in calls if call["roots"] == [external.resolve()]
        ]
        assert len(external_calls) == 1
        assert external_calls[0]["containment_root"] == external.resolve()

    def test_shards_consume_one_aggregate_deadline(self, tmp_path):
        home = tmp_path / "home"
        project = home / "project"
        project.mkdir(parents=True)

        budgets: list[tuple[bool, float]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            budgets.append((kwargs.get("recursive", True), timeout))
            return []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner.platform, "system", return_value="Windows"
            ),
            mock.patch.object(project_scanner, "scan_worker_count", return_value=1),
            mock.patch.object(
                project_scanner,
                "_search_windows",
                side_effect=fake_search,
            ),
            mock.patch(
                "runlayer_cli.scan.project_scanner.time.monotonic",
                side_effect=[100.0, 100.0, 110.0],
            ),
        ):
            find_files_under_home([".mcp.json"], timeout=30, max_depth=7)

        assert budgets == [(False, 30.0), (True, 20.0)]

    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system",
        return_value="Windows",
    )
    def test_groups_safe_roots_and_keeps_top_level_files(self, mock_system, tmp_path):
        home = tmp_path / "home"
        roots = [home / name for name in ("alpha", "bravo", "charlie")]
        for root in roots:
            root.mkdir(parents=True)
        (home / "AppData").mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (home / "junction").symlink_to(outside, target_is_directory=True)

        top_hit = home / ".mcp.json"
        root_hits = {root: root / ".mcp.json" for root in roots}
        calls: list[dict[str, object]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            calls.append({"max_depth": max_depth, **kwargs})
            search_roots = kwargs["roots"]
            if not kwargs.get("recursive", True):
                return [top_hit]
            return [root_hits[root] for root in search_roots]

        governor = build_governor(cpu_cores=2, max_cpu_percent=100)
        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner,
                "is_windows_system_context",
                return_value=True,
            ),
            mock.patch.object(
                project_scanner,
                "_search_windows",
                side_effect=fake_search,
            ),
        ):
            results = find_files_under_home(
                [".mcp.json"],
                timeout=30,
                max_depth=7,
                governor=governor,
            )

        assert results == sorted([top_hit, *root_hits.values()])
        top_calls = [call for call in calls if not call.get("recursive", True)]
        assert len(top_calls) == 1
        assert top_calls[0]["roots"] == [home]
        recursive_calls = [call for call in calls if call.get("recursive", True)]
        assert len(recursive_calls) == 2
        assert all(call["max_depth"] == 6 for call in recursive_calls)
        grouped_roots = [root for call in recursive_calls for root in call["roots"]]
        assert sorted(grouped_roots) == roots

    @mock.patch(
        "runlayer_cli.scan.project_scanner.platform.system",
        return_value="Windows",
    )
    def test_depth_one_still_covers_second_level(self, mock_system, tmp_path):
        # Pre-shard crawl was `Get-ChildItem home -Recurse -Depth 1`, which
        # returns TWO levels below home (-Depth 0 == immediate children). The
        # sharded crawl must keep that coverage via -Depth 0 subdir shards.
        home = tmp_path / "home"
        roots = [home / name for name in ("alpha", "bravo")]
        for root in roots:
            root.mkdir(parents=True)

        calls: list[dict[str, object]] = []

        def fake_search(filenames, timeout, max_depth, governor=None, **kwargs):
            calls.append({"max_depth": max_depth, **kwargs})
            return []

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(
                project_scanner,
                "_search_windows",
                side_effect=fake_search,
            ),
        ):
            find_files_under_home([".mcp.json"], timeout=30, max_depth=1)

        recursive_calls = [call for call in calls if call.get("recursive", True)]
        assert recursive_calls, "depth-1 crawl must still shard home subdirs"
        assert all(call["max_depth"] == 0 for call in recursive_calls)
        grouped_roots = [root for call in recursive_calls for root in call["roots"]]
        assert sorted(grouped_roots) == roots


class TestSearchWindows:
    """Tests for the Windows PowerShell search."""

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_surfaces_reparse_paths_in_user_context(self, mock_run, tmp_path):
        reparse = Path("C:/Users/alex/project-link")
        prefix = project_scanner._WINDOWS_REPARSE_PREFIX
        mock_run.return_value = mock.Mock(
            stdout=f"{prefix}{reparse}\n",
            returncode=0,
        )
        symlink_paths: list[Path] = []

        results = _search_windows(
            [".mcp.json"],
            timeout=30,
            max_depth=5,
            roots=[tmp_path],
            containment_root=tmp_path,
            symlink_paths=symlink_paths,
            windows_system_context=False,
        )

        assert results == []
        assert symlink_paths == [reparse]
        command = mock_run.call_args[0][0][-1]
        assert "$emitReparse = $true" in command
        assert f"$reparsePrefix = '{prefix}'" in command

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_system_context_keeps_reparse_paths_hidden(self, mock_run, tmp_path):
        reparse = Path("C:/Users/alex/project-link")
        prefix = project_scanner._WINDOWS_REPARSE_PREFIX
        mock_run.return_value = mock.Mock(
            stdout=f"{prefix}{reparse}\n",
            returncode=0,
        )
        symlink_paths: list[Path] = []

        results = _search_windows(
            [".mcp.json"],
            timeout=30,
            max_depth=5,
            roots=[tmp_path],
            containment_root=tmp_path,
            symlink_paths=symlink_paths,
            windows_system_context=True,
        )

        assert results == []
        assert symlink_paths == []
        command = mock_run.call_args[0][0][-1]
        assert "$emitReparse = $false" in command

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    @mock.patch("runlayer_cli.scan.project_scanner.Path.home")
    def test_escapes_home_path_with_special_characters(
        self, mock_home, mock_run, tmp_path
    ):
        """Escapes home paths containing PowerShell special characters."""
        # Simulate a home path with special characters
        mock_home.return_value = tmp_path / "User's $HOME `test"
        mock_run.return_value = mock.Mock(stdout="", returncode=0)

        _search_windows([".mcp.json"], timeout=30, max_depth=5)

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0][-1]  # The PowerShell command string

        # Single quotes should be doubled
        assert "User''s" in cmd
        # Path should use single quotes (not double) to prevent variable expansion
        assert "Get-ChildItem -Path '" in cmd
        # The $ and ` should be preserved literally (single quotes prevent expansion)
        assert "$HOME" in cmd
        assert "`test" in cmd

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    @mock.patch("runlayer_cli.scan.project_scanner.Path.home")
    def test_uses_single_quotes_for_path(self, mock_home, mock_run, tmp_path):
        """Uses single quotes around path to prevent PowerShell injection."""
        mock_home.return_value = tmp_path / "normal_home"
        mock_run.return_value = mock.Mock(stdout="", returncode=0)

        _search_windows([".mcp.json"], timeout=30, max_depth=5)

        cmd = mock_run.call_args[0][0][-1]
        # Should use single quotes, not double quotes
        assert f"Get-ChildItem -Path '{tmp_path / 'normal_home'}'" in cmd

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_accepts_grouped_path_array(self, mock_run, tmp_path):
        home = tmp_path / "home"
        first = home / "first"
        second = home / "second"
        mock_run.return_value = mock.Mock(stdout="", returncode=0)

        _search_windows(
            [".mcp.json"],
            timeout=30,
            max_depth=6,
            roots=[first, second],
            containment_root=home,
        )

        command = mock_run.call_args[0][0][-1]
        assert f"Get-ChildItem -Path '{first}', '{second}'" in command
        assert "$maxDepth = 6" in command
        assert "$recursive = $true" in command

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_treats_question_mark_filename_as_glob(self, mock_run, tmp_path):
        mock_run.return_value = mock.Mock(stdout="", returncode=0)

        _search_windows(
            ["config?.json"],
            timeout=30,
            max_depth=6,
            roots=[tmp_path],
            containment_root=tmp_path,
        )

        command = mock_run.call_args[0][0][-1]
        assert "$item.Name -like 'config?.json'" in command
        assert "$item.Name -in @('config?.json')" not in command

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    @mock.patch("runlayer_cli.scan.project_scanner.Path.home")
    def test_honors_depth_up_to_max(self, mock_home, mock_run, tmp_path):
        """Depth between the old cap (10) and the new max (20) is honored, not reset.

        Regression: the old code reset anything above 10 back to 5, silently
        capping a configured ProjectDepth on Windows.
        """
        mock_home.return_value = tmp_path / "home"
        mock_run.return_value = mock.Mock(stdout="", returncode=0)

        _search_windows([".mcp.json"], timeout=30, max_depth=15)

        cmd = mock_run.call_args[0][0][-1]
        assert "$maxDepth = 15" in cmd

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    @mock.patch("runlayer_cli.scan.project_scanner.Path.home")
    def test_resets_depth_above_max(self, mock_home, mock_run, tmp_path):
        """Depth above the new max (20) falls back to the safe default of 7."""
        mock_home.return_value = tmp_path / "home"
        mock_run.return_value = mock.Mock(stdout="", returncode=0)

        _search_windows([".mcp.json"], timeout=30, max_depth=25)

        cmd = mock_run.call_args[0][0][-1]
        assert "$maxDepth = 7" in cmd

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_records_node_modules_and_prunes_descent(self, mock_run, tmp_path):
        home = tmp_path / "home"
        config = home / "project" / ".mcp.json"
        config.parent.mkdir(parents=True)
        config.write_text("{}")
        node_modules = home / "renamed-prefix" / "node_modules"
        node_modules.mkdir(parents=True)
        mock_run.return_value = mock.Mock(
            stdout=f"{node_modules}\n{config}\n",
            returncode=0,
        )

        results = _search_windows(
            [".mcp.json"],
            timeout=30,
            max_depth=7,
            roots=[home],
            containment_root=home,
            discover_node_modules=True,
        )

        assert set(results) == {config, node_modules}
        command = mock_run.call_args[0][0][-1]
        assert "$item.Name -ieq 'node_modules'" in command
        assert "$discoverNodeModules = $true" in command

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_handles_timeout(self, mock_run):
        """Handles subprocess timeout gracefully."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="powershell", timeout=30)

        # Should not raise, just return empty list
        results = _search_windows([".mcp.json"], timeout=30, max_depth=5)
        assert results == []


class TestIsWithinRoot:
    """Containment check used to reject reparse-point escapes (CWE-59/61)."""

    def test_same_path_is_within(self):
        assert _is_within_root("/home/bob", "/home/bob")

    def test_child_is_within(self):
        assert _is_within_root("/home/bob", "/home/bob/.cursor/mcp.json")

    def test_outside_is_rejected(self):
        assert not _is_within_root("/home/bob", "/etc/passwd")

    def test_sibling_prefix_is_rejected(self):
        # "/home/bobby" shares the "/home/bob" string prefix but is NOT under it.
        assert not _is_within_root("/home/bob", "/home/bobby/secret")


class TestSearchWindowsReparseHardening:
    """Regression (CWE-59/61): a SYSTEM all-users scan reads user-controlled home
    trees, so a non-admin can plant a junction/symlink to redirect SYSTEM's read
    outside the profile. _search_windows must drop reparse-point entries and any
    result whose canonical path escapes the home root."""

    def test_command_excludes_reparse_points(self, tmp_path):
        with (
            mock.patch("runlayer_cli.scan.project_scanner.subprocess.run") as mock_run,
            mock.patch(
                "runlayer_cli.scan.project_scanner.Path.home",
                return_value=tmp_path / "home",
            ),
        ):
            mock_run.return_value = mock.Mock(stdout="", returncode=0)
            _search_windows([".mcp.json"], timeout=30, max_depth=5)

        cmd = mock_run.call_args[0][0][-1]
        assert "[System.IO.FileAttributes]::ReparsePoint" in cmd

    def test_keeps_real_file_inside_home(self, tmp_path):
        home = tmp_path / "home"
        config = home / ".cursor" / "mcp.json"
        config.parent.mkdir(parents=True)
        config.write_text("{}")

        with (
            mock.patch("runlayer_cli.scan.project_scanner.subprocess.run") as mock_run,
            mock.patch(
                "runlayer_cli.scan.project_scanner.Path.home", return_value=home
            ),
        ):
            mock_run.return_value = mock.Mock(stdout=str(config), returncode=0)
            results = _search_windows([".mcp.json"], timeout=30, max_depth=5)

        assert results == [config]

    def test_drops_symlinked_file(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir(parents=True)
        outside = tmp_path / "outside" / "real.json"
        outside.parent.mkdir(parents=True)
        outside.write_text("{}")
        link = home / ".cursor"
        link.mkdir()
        symlinked = link / "mcp.json"
        symlinked.symlink_to(outside)

        with (
            mock.patch("runlayer_cli.scan.project_scanner.subprocess.run") as mock_run,
            mock.patch(
                "runlayer_cli.scan.project_scanner.Path.home", return_value=home
            ),
        ):
            mock_run.return_value = mock.Mock(stdout=str(symlinked), returncode=0)
            results = _search_windows([".mcp.json"], timeout=30, max_depth=5)

        assert results == []

    def test_drops_file_under_escaping_junction(self, tmp_path):
        # A directory symlink/junction inside home that points OUTSIDE it: a
        # result reached "through" it canonicalizes outside the home root.
        home = tmp_path / "home"
        home.mkdir(parents=True)
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()
        (outside_dir / "mcp.json").write_text("{}")
        (home / "evil").symlink_to(outside_dir, target_is_directory=True)
        escaped = home / "evil" / "mcp.json"

        with (
            mock.patch("runlayer_cli.scan.project_scanner.subprocess.run") as mock_run,
            mock.patch(
                "runlayer_cli.scan.project_scanner.Path.home", return_value=home
            ),
        ):
            mock_run.return_value = mock.Mock(stdout=str(escaped), returncode=0)
            results = _search_windows([".mcp.json"], timeout=30, max_depth=5)

        assert results == []

    def test_keeps_only_inhome_results_when_mixed(self, tmp_path):
        home = tmp_path / "home"
        good = home / "proj" / ".mcp.json"
        good.parent.mkdir(parents=True)
        good.write_text("{}")
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()
        (outside_dir / ".mcp.json").write_text("{}")
        (home / "evil").symlink_to(outside_dir, target_is_directory=True)
        escaped = home / "evil" / ".mcp.json"

        with (
            mock.patch("runlayer_cli.scan.project_scanner.subprocess.run") as mock_run,
            mock.patch(
                "runlayer_cli.scan.project_scanner.Path.home", return_value=home
            ),
        ):
            mock_run.return_value = mock.Mock(stdout=f"{good}\n{escaped}", returncode=0)
            results = _search_windows([".mcp.json"], timeout=30, max_depth=5)

        assert results == [good]


class TestEscapePowerShellString:
    """Tests for PowerShell string escaping."""

    def test_escapes_single_quotes(self):
        """Single quotes are doubled for PowerShell single-quoted strings."""
        assert _escape_powershell_string("it's") == "it''s"
        assert _escape_powershell_string("'quoted'") == "''quoted''"

    def test_preserves_other_characters(self):
        """Other special characters are preserved (single quotes handle them)."""
        # These are special in PowerShell but safe in single-quoted strings
        assert _escape_powershell_string("$HOME") == "$HOME"
        assert _escape_powershell_string("`n") == "`n"
        assert _escape_powershell_string('"double"') == '"double"'
        assert _escape_powershell_string("path\\to\\file") == "path\\to\\file"

    def test_empty_string(self):
        """Handles empty string."""
        assert _escape_powershell_string("") == ""

    def test_multiple_single_quotes(self):
        """Handles multiple single quotes."""
        assert _escape_powershell_string("it's John's") == "it''s John''s"


class TestExcludedDirectories:
    """Tests for the exclusion directories list."""

    def test_contains_common_exclusions(self):
        """EXCLUDED_DIRECTORIES contains expected directories."""
        assert "node_modules" in EXCLUDED_DIRECTORIES
        assert ".git" in EXCLUDED_DIRECTORIES
        assert "venv" in EXCLUDED_DIRECTORIES
        assert "AppData" in EXCLUDED_DIRECTORIES
        assert "Library/Application Support" in EXCLUDED_DIRECTORIES
        assert "__pycache__" in EXCLUDED_DIRECTORIES
        assert "dist" in EXCLUDED_DIRECTORIES
        assert "build" in EXCLUDED_DIRECTORIES

    def test_excludes_installed_plugins(self):
        """installed-plugins is excluded so plugin-bundled configs aren't re-crawled."""
        assert "installed-plugins" in EXCLUDED_DIRECTORIES


class _FakeStdout:
    """Iterable stdout stand-in that tracks exhaustion + close (for FakePopen)."""

    def __init__(self, lines: list[str]) -> None:
        self._it = iter(lines)
        self.exhausted = False
        self.closed = False

    def __iter__(self):
        return self

    def __next__(self) -> str:
        try:
            return next(self._it)
        except StopIteration:
            self.exhausted = True
            raise

    def close(self) -> None:
        self.closed = True


class FakePopen:
    """subprocess.Popen stand-in whose stdout yields canned crawl lines."""

    def __init__(self, lines: list[str], pid: int = 424242) -> None:
        self.stdout = _FakeStdout(lines)
        self.pid = pid
        self.killed = False
        self._waited = False

    def poll(self):
        # Model a child that exits once its stdout is drained; still "running"
        # if we bailed early (max-paths break / abort) so the finally kills it.
        if self.killed or self._waited or self.stdout.exhausted:
            return 0
        return None

    def wait(self, timeout=None):
        self._waited = True
        return 0

    def kill(self) -> None:
        self.killed = True


class FakeGovernor:
    """Governor test double: deterministic max_paths + abort, records children."""

    def __init__(self, *, max_paths: int = 1_000_000, abort_after: int | None = None):
        self.max_paths = max_paths
        self._abort_after = abort_after
        self.checkpoints = 0
        self.registered: list[object] = []
        self.unregistered: list[object] = []

    def checkpoint(self) -> None:
        self.checkpoints += 1
        if self._abort_after is not None and self.checkpoints >= self._abort_after:
            raise ScanResourceLimitExceeded("tripped")

    def register_child(self, proc) -> None:
        self.registered.append(proc)

    def unregister_child(self, proc) -> None:
        self.unregistered.append(proc)


class TestStreamCrawl:
    """Governed streaming crawl: per-line accept, checkpoints, path budget,
    child registration, and abort/timeout kill."""

    @pytest.mark.skipif(project_scanner.os.name != "posix", reason="POSIX only")
    def test_deprioritizes_posix_child_after_spawn(self, monkeypatch):
        fake = FakePopen([])
        popen_kwargs: dict[str, object] = {}

        def popen(*_args, **kwargs):
            popen_kwargs.update(kwargs)
            return fake

        monkeypatch.setattr(project_scanner.subprocess, "Popen", popen)
        setpriority = mock.Mock()
        monkeypatch.setattr(project_scanner.os, "setpriority", setpriority)

        _stream_crawl(["find"], 30, lambda _line: None, FakeGovernor(), label="find")

        assert popen_kwargs["start_new_session"] is True
        assert "preexec_fn" not in popen_kwargs
        setpriority.assert_called_once_with(
            project_scanner.os.PRIO_PROCESS,
            fake.pid,
            10,
        )

    def test_uses_below_normal_priority_at_windows_spawn(self, monkeypatch):
        fake = FakePopen([])
        popen_kwargs: dict[str, object] = {}

        def popen(*_args, **kwargs):
            popen_kwargs.update(kwargs)
            return fake

        monkeypatch.setattr(project_scanner.subprocess, "Popen", popen)
        monkeypatch.setattr(project_scanner.os, "name", "nt")
        priority_flag = 0x00004000
        monkeypatch.setattr(
            project_scanner.subprocess,
            "BELOW_NORMAL_PRIORITY_CLASS",
            priority_flag,
            raising=False,
        )

        _stream_crawl(
            ["powershell"],
            30,
            lambda _line: None,
            FakeGovernor(),
            label="powershell",
        )

        assert popen_kwargs["start_new_session"] is False
        assert popen_kwargs["creationflags"] == priority_flag
        assert "preexec_fn" not in popen_kwargs

    def test_streams_and_accepts_lines(self, monkeypatch):
        fake = FakePopen(["/a/.mcp.json\n", "\n", "/b/.mcp.json\n"])
        monkeypatch.setattr(project_scanner.subprocess, "Popen", lambda *a, **k: fake)
        gov = FakeGovernor()

        results = _stream_crawl(
            ["find"], 30, lambda line: Path(line), gov, label="find"
        )

        # Blank line is skipped; the two real lines are accepted in order.
        assert results == [Path("/a/.mcp.json"), Path("/b/.mcp.json")]

    def test_registers_and_unregisters_child(self, monkeypatch):
        fake = FakePopen(["/a/.mcp.json\n"])
        monkeypatch.setattr(project_scanner.subprocess, "Popen", lambda *a, **k: fake)
        gov = FakeGovernor()

        _stream_crawl(["find"], 30, lambda line: Path(line), gov, label="find")

        assert gov.registered == [fake]
        assert gov.unregistered == [fake]

    def test_path_budget_stops_and_kills_child(self, monkeypatch):
        lines = [f"/p/{i}/.mcp.json\n" for i in range(10)]
        fake = FakePopen(lines)
        monkeypatch.setattr(project_scanner.subprocess, "Popen", lambda *a, **k: fake)
        killed: list[object] = []
        monkeypatch.setattr(
            project_scanner,
            "terminate_process",
            lambda proc: killed.append(proc),
        )
        gov = FakeGovernor(max_paths=3)

        results = _stream_crawl(
            ["find"], 30, lambda line: Path(line), gov, label="find"
        )

        assert len(results) == 3  # stops at the budget
        assert killed == [fake]  # child killed since it was still running

    def test_abort_midstream_raises_and_kills_child(self, monkeypatch):
        # 300 lines forces a checkpoint at line 256 before stdout is drained;
        # abort_after=1 raises there, so the child is still running at cleanup.
        lines = [f"/p/{i}/.mcp.json\n" for i in range(300)]
        fake = FakePopen(lines)
        monkeypatch.setattr(project_scanner.subprocess, "Popen", lambda *a, **k: fake)
        killed: list[object] = []
        monkeypatch.setattr(
            project_scanner,
            "terminate_process",
            lambda proc: killed.append(proc),
        )
        gov = FakeGovernor(abort_after=1)

        with pytest.raises(ScanResourceLimitExceeded):
            _stream_crawl(["find"], 30, lambda line: Path(line), gov, label="find")

        assert gov.unregistered == [fake]
        assert killed == [fake]

    def test_missing_command_returns_empty(self, monkeypatch):
        def _raise(*a, **k):
            raise FileNotFoundError

        monkeypatch.setattr(project_scanner.subprocess, "Popen", _raise)
        gov = FakeGovernor()

        results = _stream_crawl(
            ["find"], 30, lambda line: Path(line), gov, label="find"
        )
        assert results == []


class TestFindFilesUnderHomeGovernor:
    """find_files_under_home routes to the streaming crawl when a governor is
    supplied, and yields the same results as the blocking path."""

    def test_streams_real_files_with_governor(self, monkeypatch, tmp_path):
        f1 = tmp_path / "a" / ".mcp.json"
        f1.parent.mkdir(parents=True)
        f1.write_text("{}")
        f2 = tmp_path / "b" / ".mcp.json"
        f2.parent.mkdir(parents=True)
        f2.write_text("{}")

        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")
        fake = FakePopen([f"{f1}\n", f"{f2}\n"])
        monkeypatch.setattr(project_scanner.subprocess, "Popen", lambda *a, **k: fake)

        gov = build_governor(memory_limit_mb=8192)
        results = find_files_under_home([".mcp.json"], governor=gov)

        assert set(results) == {f1, f2}

    def test_generous_governor_matches_blocking_path(self, monkeypatch, tmp_path):
        f1 = tmp_path / "proj" / ".mcp.json"
        f1.parent.mkdir(parents=True)
        f1.write_text("{}")
        monkeypatch.setattr(project_scanner.platform, "system", lambda: "Darwin")

        # Blocking path (governor=None) via subprocess.run.
        with mock.patch.object(project_scanner.subprocess, "run") as mock_run:
            mock_run.return_value = mock.Mock(stdout=f"{f1}\n", returncode=0)
            blocking = find_files_under_home([".mcp.json"])

        # Streaming path (generous governor) via Popen; identical results.
        fake = FakePopen([f"{f1}\n"])
        monkeypatch.setattr(project_scanner.subprocess, "Popen", lambda *a, **k: fake)
        streamed = find_files_under_home(
            [".mcp.json"], governor=build_governor(memory_limit_mb=8192)
        )

        assert blocking == streamed == [f1]
