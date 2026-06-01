"""Tests for skill discovery in scan (SKILL.md directories only)."""

from pathlib import Path
from unittest import mock

import httpx

from runlayer_cli.scan import file_collector
from runlayer_cli.scan.file_collector import MAX_SINGLE_FILE_BYTES
from runlayer_cli.scan.skill_scanner import (
    ARTIFACT_SKILL_MD,
    DiscoveredSkillArtifact,
    SkillFile,
    _collect_files_safe,
    _infer_home_client_tool,
    _infer_project_root,
    _is_dependency_path,
    _parse_frontmatter,
    _scan_skill_md_dir,
    process_skill_paths,
    scan_global_skills,
)
from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact, PluginFile
from runlayer_cli.scan.service import (
    submit_discovered_plugins,
    submit_discovered_skills,
)


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = "---\nname: my-skill\ndescription: Does stuff\n---\n# Body"
        fm = _parse_frontmatter(content)
        assert fm["name"] == "my-skill"
        assert fm["description"] == "Does stuff"

    def test_no_frontmatter(self):
        assert _parse_frontmatter("# Just markdown") == {}

    def test_invalid_yaml(self):
        assert _parse_frontmatter("---\n: :\n---\n") == {}

    def test_unclosed_frontmatter(self):
        assert _parse_frontmatter("---\nname: x\n# no close") == {}


class TestIsDependencyPath:
    def test_node_modules(self):
        assert _is_dependency_path(Path("/project/node_modules/pkg/skills/x"))

    def test_venv(self):
        assert _is_dependency_path(Path("/project/.venv/lib/skill"))

    def test_user_path(self):
        assert not _is_dependency_path(Path("/home/user/project/skills/my-skill"))


class TestCollectFilesSafe:
    def test_collects_supported_files(self, tmp_path):
        (tmp_path / "SKILL.md").write_text("# skill")
        (tmp_path / "helper.py").write_text("print('hi')")
        (tmp_path / "image.png").write_bytes(b"\x89PNG")

        files, symlinks, oversized = _collect_files_safe(tmp_path)
        titles = {f.title for f in files}
        assert "SKILL.md" in titles
        assert "helper.py" in titles
        assert "image.png" not in titles
        assert not oversized
        assert symlinks == []

    def test_skips_external_symlink(self, tmp_path):
        external = tmp_path / "external"
        external.mkdir()
        secret = external / "secret.py"
        secret.write_text("SECRET_KEY='abc'")

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# skill")
        link = skill_dir / "steal.py"
        link.symlink_to(secret)

        files, symlinks, oversized = _collect_files_safe(skill_dir)
        titles = {f.title for f in files}
        assert "steal.py" not in titles
        assert str(link) in symlinks

    def test_follows_internal_symlink(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        real_file = skill_dir / "real.py"
        real_file.write_text("print('real')")
        link = skill_dir / "alias.py"
        link.symlink_to(real_file)
        (skill_dir / "SKILL.md").write_text("# skill")

        files, symlinks, oversized = _collect_files_safe(skill_dir)
        titles = {f.title for f in files}
        assert "alias.py" in titles
        assert symlinks == []

    def test_oversized_file_flagged(self, tmp_path):
        (tmp_path / "big.py").write_text("x" * (MAX_SINGLE_FILE_BYTES + 1))
        (tmp_path / "small.md").write_text("ok")

        files, _, oversized = _collect_files_safe(tmp_path)
        assert oversized
        titles = {f.title for f in files}
        assert "big.py" not in titles
        assert "small.md" in titles

    def test_oversized_file_does_not_stop_subdirectory_traversal(self, tmp_path):
        """A single >1 MB file should not prevent collecting files in subdirs."""
        (tmp_path / "SKILL.md").write_text("---\nname: s\n---\n# ok")
        (tmp_path / "big.py").write_text("x" * (MAX_SINGLE_FILE_BYTES + 1))

        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "helper.py").write_text("print('hi')")

        files, _, oversized = _collect_files_safe(tmp_path)
        assert oversized
        titles = {f.title for f in files}
        assert "big.py" not in titles
        assert "SKILL.md" in titles
        assert "sub/helper.py" in titles

    def test_total_budget_stops_across_subdirectories(self, tmp_path, monkeypatch):
        """After hitting MAX_TOTAL_BYTES, files in subdirs must NOT be collected."""
        monkeypatch.setattr(file_collector, "MAX_TOTAL_BYTES", 100)

        (tmp_path / "root.md").write_text("A" * 60)
        (tmp_path / "trigger.md").write_text("B" * 60)

        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "extra.md").write_text("C" * 10)

        files, _, oversized = _collect_files_safe(tmp_path)
        assert oversized
        titles = {f.title for f in files}
        assert "root.md" in titles
        assert "trigger.md" not in titles
        assert "sub/extra.md" not in titles


class TestScanSkillMdDir:
    def test_valid_skill(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A test skill\n---\n# Instructions"
        )
        (skill_dir / "helper.py").write_text("print('hello')")

        artifact = _scan_skill_md_dir(skill_dir, scope="global", tool="claude_code")
        assert artifact is not None
        assert artifact.name == "my-skill"
        assert artifact.description == "A test skill"
        assert artifact.artifact_type == ARTIFACT_SKILL_MD
        assert artifact.scope == "global"
        assert artifact.identifier is not None
        assert artifact.file_count == 2

    def test_missing_name_uses_folder_name(self, tmp_path):
        skill_dir = tmp_path / "bad-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\ndescription: no name\n---\n")

        artifact = _scan_skill_md_dir(skill_dir, scope="global", tool="multi")
        assert artifact is not None
        assert artifact.name == "bad-skill"

    def test_has_scripts_detected(self, tmp_path):
        skill_dir = tmp_path / "scripted"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: scripted\n---\n")
        scripts = skill_dir / "scripts"
        scripts.mkdir()
        (scripts / "run.sh").write_text("#!/bin/bash")

        artifact = _scan_skill_md_dir(skill_dir, scope="project", tool="multi")
        assert artifact is not None
        assert artifact.has_scripts is True


class TestInferProjectRoot:
    def test_skill_md_in_dot_tool_skills_dir(self):
        p = Path("/project/.cursor/skills/deploy/SKILL.md")
        assert _infer_project_root(p) == "/project"

    def test_skill_md_in_dot_agents_skills_dir(self):
        p = Path("/project/.agents/skills/deploy/SKILL.md")
        assert _infer_project_root(p) == "/project"

    def test_skill_md_in_plain_skills_dir(self):
        p = Path("/project/skills/deploy/SKILL.md")
        assert _infer_project_root(p) == "/project"

    def test_skill_md_without_skills_container(self):
        p = Path("/project/deploy-tool/SKILL.md")
        assert _infer_project_root(p) == "/project"


class TestProcessSkillPaths:
    def test_skill_md_discovered(self, tmp_path):
        skill_dir = tmp_path / "project" / ".agents" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: deploy\ndescription: Deploy helper\n---\n")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].artifact_type == ARTIFACT_SKILL_MD
        assert results[0].name == "deploy"
        assert results[0].project_path == str(tmp_path / "project")

    def test_non_skill_files_ignored(self, tmp_path):
        """AGENTS.md, CLAUDE.md, .cursorrules etc. are no longer treated as skills."""
        project = tmp_path / "project"
        project.mkdir()
        for name in [
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".cursorrules",
            ".windsurfrules",
        ]:
            f = project / name
            f.write_text(f"# {name}")

        gh = project / ".github"
        gh.mkdir()
        (gh / "copilot-instructions.md").write_text("# Copilot")

        results = process_skill_paths(
            [
                project / n
                for n in [
                    "AGENTS.md",
                    "CLAUDE.md",
                    "GEMINI.md",
                    ".cursorrules",
                    ".windsurfrules",
                ]
            ]
            + [gh / "copilot-instructions.md"]
        )
        assert results == []

    def test_deduplicates_skill_dirs(self, tmp_path):
        skill_dir = tmp_path / "skill"
        skill_dir.mkdir()
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: dup\n---\n")

        results = process_skill_paths([marker, marker])
        assert len(results) == 1

    def test_unknown_filename_ignored(self, tmp_path):
        f = tmp_path / "random.txt"
        f.write_text("nope")
        assert process_skill_paths([f]) == []


class TestScanGlobalSkills:
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_skills_in_global_dirs(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".claude" / "skills" / "my-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: test\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        assert any(r.name == "my-skill" for r in results)
        assert all(r.scope == "global" for r in results)

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_copilot_global_skills(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".copilot" / "skills" / "pr-reviewer"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: pr-reviewer\ndescription: Review PRs\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        pr = [r for r in results if r.name == "pr-reviewer"]
        assert len(pr) == 1
        assert pr[0].tool == "github_copilot_cli"
        assert pr[0].scope == "global"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_cline_global_skills(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".cline" / "skills" / "cline-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: cline-skill\ndescription: Cline skill\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        cs = [r for r in results if r.name == "cline-skill"]
        assert len(cs) == 1
        assert cs[0].tool == "cline"
        assert cs[0].scope == "global"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_opencode_global_skills(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".config" / "opencode" / "skills" / "oc-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: oc-skill\ndescription: OpenCode skill\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        oc = [r for r in results if r.name == "oc-skill"]
        assert len(oc) == 1
        assert oc[0].tool == "opencode"
        assert oc[0].scope == "global"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_empty_home(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        assert scan_global_skills() == []


class TestSubmitDiscoveredSkills:
    def test_calls_fingerprint_then_submit(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}

        skill = DiscoveredSkillArtifact(
            name="test",
            path="/test",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# test")],
        )

        submitted = submit_discovered_skills(client, [skill])

        assert submitted == "success"
        client.submit_skill_fingerprint.assert_called_once_with(
            "abc123", ARTIFACT_SKILL_MD, oversized=False
        )
        client.submit_skill.assert_called_once()

    def test_submit_includes_device_context(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}

        skill = DiscoveredSkillArtifact(
            name="test",
            path="/test",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# test")],
        )

        scan_result = mock.MagicMock()
        scan_result.device_id = "dev-123"
        scan_result.hostname = "my-host"
        scan_result.os = "darwin"
        scan_result.os_version = "14.0"
        scan_result.username = "alice"
        scan_result.org_device_id = None

        submit_discovered_skills(client, [skill], scan_result)
        payload = client.submit_skill.call_args[0][0]
        assert payload["device_id"] == "dev-123"
        assert payload["hostname"] == "my-host"
        assert payload["os"] == "darwin"
        assert payload["username"] == "alice"

    def test_submits_empty_files_when_known(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": True}

        skill = DiscoveredSkillArtifact(
            name="known",
            path="/known",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# known")],
        )

        submit_discovered_skills(client, [skill])
        client.submit_skill.assert_called_once()
        payload = client.submit_skill.call_args[0][0]
        assert payload["files"] == []

    def test_submits_empty_files_when_oversized(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}

        skill = DiscoveredSkillArtifact(
            name="big-skill",
            path="/big",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="hash-oversized",
            oversized=True,
        )

        submit_discovered_skills(client, [skill])
        client.submit_skill_fingerprint.assert_called_once_with(
            "hash-oversized", ARTIFACT_SKILL_MD, oversized=True
        )
        client.submit_skill.assert_called_once()
        payload = client.submit_skill.call_args[0][0]
        assert payload["files"] == []

    def test_known_artifact_still_sends_device_context(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": True}

        skill = DiscoveredSkillArtifact(
            name="known",
            path="/known",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# known")],
        )

        scan_result = mock.MagicMock()
        scan_result.device_id = "dev-456"
        scan_result.hostname = "box2"
        scan_result.os = "linux"
        scan_result.os_version = "6.1"
        scan_result.username = "bob"
        scan_result.org_device_id = None

        submit_discovered_skills(client, [skill], scan_result)
        client.submit_skill.assert_called_once()
        payload = client.submit_skill.call_args[0][0]
        assert payload["files"] == []
        assert payload["device_id"] == "dev-456"
        assert payload["hostname"] == "box2"
        assert payload["os"] == "linux"
        assert payload["username"] == "bob"

    def test_skips_skill_without_identifier(self):
        client = mock.MagicMock()

        skill = DiscoveredSkillArtifact(
            name="no-id",
            path="/no-id",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier=None,
        )

        submit_discovered_skills(client, [skill])
        client.submit_skill_fingerprint.assert_not_called()

    def test_handles_not_implemented_gracefully(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.side_effect = NotImplementedError("stub")

        skill = DiscoveredSkillArtifact(
            name="stub",
            path="/stub",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
        )

        submit_discovered_skills(client, [skill])

    def test_handles_api_error_gracefully(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.side_effect = RuntimeError("network")

        skill = DiscoveredSkillArtifact(
            name="err",
            path="/err",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submit_discovered_skills(client, [skill])

        warning_mock.assert_called_once_with(
            "skill_submission_failed",
            skill="err",
            error="network",
            error_type="RuntimeError",
        )

    def test_returns_unsupported_when_skill_endpoint_unsupported(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"unsupported": True}

        skill = DiscoveredSkillArtifact(
            name="unsupported",
            path="/unsupported",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
        )

        submitted = submit_discovered_skills(client, [skill])

        assert submitted == "unsupported"
        client.submit_skill.assert_not_called()

    def test_stops_after_skill_transport_error(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_skill_fingerprint.side_effect = httpx.ConnectError(
            "network", request=request
        )

        skills = [
            DiscoveredSkillArtifact(
                name="err",
                path="/err",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="abc123",
            ),
            DiscoveredSkillArtifact(
                name="skipped",
                path="/skipped",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="def456",
            ),
        ]

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submitted = submit_discovered_skills(client, skills)

        assert submitted == "failed"
        assert client.submit_skill_fingerprint.call_count == 1
        warning_mock.assert_called_once_with(
            "skill_submission_failed",
            skill="err",
            error="network",
            error_type="ConnectError",
        )


class TestSubmitDiscoveredPlugins:
    def test_handles_api_error_without_traceback(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.side_effect = RuntimeError("network")

        plugin = DiscoveredPluginArtifact(
            name="err-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/plugin",
            identifier="abc123",
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submit_discovered_plugins(client, [plugin])

        warning_mock.assert_called_once_with(
            "plugin_submission_failed",
            plugin="err-plugin",
            error="network",
            error_type="RuntimeError",
        )

    def test_returns_unsupported_when_plugin_endpoint_unsupported(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"unsupported": True}

        plugin = DiscoveredPluginArtifact(
            name="unsupported-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/plugin",
            identifier="abc123",
        )

        submitted = submit_discovered_plugins(client, [plugin])

        assert submitted == "unsupported"
        client.submit_plugin.assert_not_called()

    def test_stops_after_plugin_transport_error(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_plugin_fingerprint.side_effect = httpx.ConnectError(
            "network", request=request
        )

        plugins = [
            DiscoveredPluginArtifact(
                name="err-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/plugin",
                identifier="abc123",
            ),
            DiscoveredPluginArtifact(
                name="skipped-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/skipped-plugin",
                identifier="def456",
            ),
        ]

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submitted = submit_discovered_plugins(client, plugins)

        assert submitted == "failed"
        assert client.submit_plugin_fingerprint.call_count == 1
        warning_mock.assert_called_once_with(
            "plugin_submission_failed",
            plugin="err-plugin",
            error="network",
            error_type="ConnectError",
        )


class TestGlobalSkillDeduplication:
    """Global skills must not appear as both 'project' and 'global' scope."""

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_process_skill_paths_excludes_global_skill_dirs(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / ".claude" / "skills" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# Instructions")

        results = process_skill_paths([marker])
        assert len(results) == 0, (
            "SKILL.md under a global skill dir should be excluded from project results"
        )

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_project_skill_not_excluded(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / "projects" / "my-app" / ".cursor" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: deploy\n---\n# Deploy")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].scope == "project"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_no_duplicates_between_phases(self, mock_home, tmp_path):
        """Simulate Phase 2 + Phase 6 and verify no duplicates."""
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / ".claude" / "skills" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# test")

        project_skills = process_skill_paths([marker])
        global_skills = scan_global_skills()

        all_skills = project_skills + global_skills
        paths = [s.path for s in all_skills]
        assert len(paths) == len(set(paths)), f"Duplicate skill paths found: {paths}"


class TestInferHomeClientTool:
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_cursor_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".cursor" / "skills-cursor" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "cursor"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_codex_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".codex" / "skills" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "codex"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_copilot_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".copilot" / "skills" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "github_copilot_cli"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_cline_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".cline" / "skills" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "cline"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_not_under_home(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = Path("/other/path/SKILL.md")
        assert _infer_home_client_tool(fpath) is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_unknown_client_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".unknown-tool" / "skills" / "SKILL.md"
        assert _infer_home_client_tool(fpath) is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_nested_in_project_not_matched(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / "projects" / "app" / ".cursor" / "skills" / "s" / "SKILL.md"
        assert _infer_home_client_tool(fpath) is None


class TestProcessSkillPathsUserScope:
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_home_client_skill_gets_user_scope(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / ".cursor" / "skills-cursor" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# Instructions")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].scope == "user"
        assert results[0].tool == "cursor"
        assert results[0].project_path is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_project_skill_keeps_project_scope(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / "projects" / "app" / ".cursor" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: deploy\n---\n# Deploy")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].scope == "project"
        assert results[0].tool == "multi"
        assert results[0].project_path is not None


class TestDiscoveredSkillArtifactPayload:
    def test_to_api_payload(self):
        artifact = DiscoveredSkillArtifact(
            name="test-skill",
            path="/path/to/skill",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="claude_code",
            project_path="/path/to",
            identifier="hash123",
            description="Test",
            has_scripts=True,
            file_count=2,
            files=[
                SkillFile(title="SKILL.md", content="# Skill"),
                SkillFile(title="scripts/run.sh", content="#!/bin/bash"),
            ],
            oversized=False,
            symlinks_found=["/path/to/link"],
            git_remote_url="https://github.com/org/repo.git",
            is_dependency=False,
            source_type="user",
        )

        payload = artifact.to_api_payload()
        assert payload["identifier"] == "hash123"
        assert payload["name"] == "test-skill"
        assert payload["artifact_type"] == ARTIFACT_SKILL_MD
        assert payload["has_scripts"] is True
        assert payload["oversized"] is False
        assert payload["git_remote_url"] == "https://github.com/org/repo.git"
        assert payload["source_type"] == "user"
        assert len(payload["files"]) == 2
        assert payload["symlinks_found"] == ["/path/to/link"]

    def test_source_plugin_identifier_in_payload(self):
        artifact = DiscoveredSkillArtifact(
            name="plugin-skill",
            path="/home/user/.claude/plugins/my-plugin/skills/deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
            source_plugin_identifier="abc123",
        )
        payload = artifact.to_api_payload()
        assert payload["source_plugin_identifier"] == "abc123"

    def test_source_plugin_identifier_absent_when_none(self):
        artifact = DiscoveredSkillArtifact(
            name="standalone-skill",
            path="/home/user/skills/test",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
        )
        payload = artifact.to_api_payload()
        assert "source_plugin_identifier" not in payload


class TestTagSkillsWithPlugins:
    def test_tag_skills_prefix_match(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import tag_skills_with_plugins

        plugin_dir = tmp_path / "plugins" / "my-plugin"
        plugin_dir.mkdir(parents=True)
        skill_dir = plugin_dir / "skills" / "deploy"
        skill_dir.mkdir(parents=True)

        skill = DiscoveredSkillArtifact(
            name="deploy",
            path=str(skill_dir.resolve()),
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
        )
        plugin_path_map = {plugin_dir.resolve(): "plugin-hash-123"}
        tag_skills_with_plugins([skill], plugin_path_map)
        assert skill.source_plugin_identifier == "plugin-hash-123"

    def test_tag_skills_no_match(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import tag_skills_with_plugins

        plugin_dir = tmp_path / "plugins" / "other-plugin"
        plugin_dir.mkdir(parents=True)
        unrelated = tmp_path / "skills" / "standalone"
        unrelated.mkdir(parents=True)

        skill = DiscoveredSkillArtifact(
            name="standalone",
            path=str(unrelated.resolve()),
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
        )
        plugin_path_map = {plugin_dir.resolve(): "other-hash"}
        tag_skills_with_plugins([skill], plugin_path_map)
        assert skill.source_plugin_identifier is None

    def test_tag_skills_longest_prefix_wins(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import tag_skills_with_plugins

        parent = tmp_path / "plugins" / "outer"
        parent.mkdir(parents=True)
        child = parent / "inner"
        child.mkdir(parents=True)
        skill_dir = child / "skills" / "test"
        skill_dir.mkdir(parents=True)

        skill = DiscoveredSkillArtifact(
            name="test",
            path=str(skill_dir.resolve()),
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
        )
        plugin_path_map = {
            parent.resolve(): "outer-hash",
            child.resolve(): "inner-hash",
        }
        tag_skills_with_plugins([skill], plugin_path_map)
        assert skill.source_plugin_identifier == "inner-hash"


class TestSubmitDiscoveredPluginsFileStripping:
    def test_calls_fingerprint_then_submit(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}

        plugin = DiscoveredPluginArtifact(
            name="test-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/test",
            identifier="plug-abc",
            files=[PluginFile(title="package.json", content="{}")],
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin_fingerprint.assert_called_once_with("plug-abc")
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == [{"title": "package.json", "content": "{}"}]

    def test_submits_empty_files_when_known(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": True}

        plugin = DiscoveredPluginArtifact(
            name="known-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/known",
            identifier="plug-known",
            files=[PluginFile(title="package.json", content="{}")],
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == []

    def test_submits_empty_files_when_oversized(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}

        plugin = DiscoveredPluginArtifact(
            name="big-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/big",
            identifier="plug-big",
            oversized=True,
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin_fingerprint.assert_called_once_with("plug-big")
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == []

    def test_known_artifact_still_sends_device_context(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": True}

        plugin = DiscoveredPluginArtifact(
            name="known-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/known",
            identifier="plug-known",
            files=[PluginFile(title="package.json", content="{}")],
        )

        scan_result = mock.MagicMock()
        scan_result.device_id = "dev-789"
        scan_result.hostname = "box3"
        scan_result.os = "windows"
        scan_result.os_version = "11"
        scan_result.username = "charlie"
        scan_result.org_device_id = None

        submit_discovered_plugins(client, [plugin], scan_result)
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == []
        assert payload["device_id"] == "dev-789"
        assert payload["hostname"] == "box3"
        assert payload["os"] == "windows"
        assert payload["username"] == "charlie"

    def test_skips_plugin_without_identifier(self):
        client = mock.MagicMock()

        plugin = DiscoveredPluginArtifact(
            name="no-id",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/noid",
            identifier=None,
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin_fingerprint.assert_not_called()
