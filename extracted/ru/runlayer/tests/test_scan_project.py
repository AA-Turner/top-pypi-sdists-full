"""Tests for project-level config scanning using find command."""

from unittest import mock


from runlayer_cli.scan.clients import (
    ConfigPath,
    MCPClientDefinition,
    ProjectConfigPattern,
)
from runlayer_cli.scan.project_scanner import (
    EXCLUDED_DIRECTORIES,
    _escape_powershell_string,
    _get_project_root,
    _search_unix,
    _search_windows,
    scan_for_project_configs,
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


class TestScanForProjectConfigs:
    """Integration tests for the main scanning function."""

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

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_builds_correct_find_command(self, mock_run, tmp_path):
        """Builds correct find command with exclusions."""
        mock_run.return_value = mock.Mock(
            stdout="",
            returncode=0,
        )

        _search_unix([".mcp.json", "mcp.json"], timeout=30, max_depth=5)

        # Verify find was called
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]

        # Check command structure
        assert cmd[0] == "find"
        assert "-maxdepth" in cmd
        assert "5" in cmd
        assert "-type" in cmd
        assert "f" in cmd
        assert ".mcp.json" in cmd
        assert "mcp.json" in cmd
        # Check exclusions
        assert "*/node_modules/*" in cmd or "node_modules" in str(cmd)

    @mock.patch("runlayer_cli.scan.project_scanner.subprocess.run")
    def test_handles_timeout(self, mock_run):
        """Handles subprocess timeout gracefully."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="find", timeout=30)

        # Should not raise, just return empty list
        results = _search_unix([".mcp.json"], timeout=30, max_depth=5)
        assert results == []


class TestSearchWindows:
    """Tests for the Windows PowerShell search."""

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
    def test_handles_timeout(self, mock_run):
        """Handles subprocess timeout gracefully."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="powershell", timeout=30)

        # Should not raise, just return empty list
        results = _search_windows([".mcp.json"], timeout=30, max_depth=5)
        assert results == []


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
