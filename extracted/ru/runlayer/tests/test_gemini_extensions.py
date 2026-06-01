"""Tests for Gemini CLI extension scanner."""

import json
from pathlib import Path, PurePosixPath, PureWindowsPath

from runlayer_cli.scan.gemini_extensions import (
    _is_project_manifest_path,
    process_project_gemini_extensions,
    scan_gemini_extensions,
)


class TestIsProjectManifestPath:
    def test_matches_posix_path(self):
        p = PurePosixPath("/home/me/proj/.gemini/extensions/team/gemini-extension.json")
        assert _is_project_manifest_path(p) is True

    def test_matches_windows_path(self):
        """Regression: backslash-separated paths must match on Windows."""
        p = PureWindowsPath(
            r"C:\Users\me\proj\.gemini\extensions\team\gemini-extension.json"
        )
        assert _is_project_manifest_path(p) is True

    def test_rejects_wrong_filename(self):
        p = PurePosixPath("/proj/.gemini/extensions/team/other.json")
        assert _is_project_manifest_path(p) is False

    def test_rejects_wrong_structure(self):
        p = PurePosixPath("/proj/.gemini/gemini-extension.json")
        assert _is_project_manifest_path(p) is False

    def test_rejects_unrelated_path(self):
        p = PurePosixPath("/proj/.mcp.json")
        assert _is_project_manifest_path(p) is False


class TestScanGeminiExtensions:
    def test_discovers_extension_with_mcp_servers(self, tmp_path):
        ext_dir = tmp_path / "gemini-cli-security"
        ext_dir.mkdir()
        manifest = {
            "name": "gemini-cli-security",
            "version": "0.5.0",
            "mcpServers": {
                "securityServer": {
                    "command": "node",
                    "args": ["${extensionPath}/mcp-server/dist/index.js"],
                },
                "osvScanner": {
                    "command": "${extensionPath}/osv-scanner",
                    "args": ["experimental-mcp"],
                },
            },
        }
        (ext_dir / "gemini-extension.json").write_text(json.dumps(manifest))

        configs, artifacts = scan_gemini_extensions(tmp_path)
        assert len(configs) == 1
        assert configs[0].client == "gemini_cli"
        assert configs[0].config_scope == "plugin"
        assert len(configs[0].servers) == 2
        server_names = {s.name for s in configs[0].servers}
        assert server_names == {"securityServer", "osvScanner"}

        assert len(artifacts) == 1
        assert artifacts[0].name == "gemini-cli-security"
        assert artifacts[0].plugin_type == "gemini_extension"
        assert artifacts[0].has_mcp_servers is True

    def test_skips_non_directory_entries(self, tmp_path):
        """State files like extension-enablement.json must be filtered out."""
        (tmp_path / "extension-enablement.json").write_text("{}")
        configs, artifacts = scan_gemini_extensions(tmp_path)
        assert configs == []
        assert artifacts == []

    def test_extension_without_mcp_servers(self, tmp_path):
        ext_dir = tmp_path / "no-mcp-ext"
        ext_dir.mkdir()
        manifest = {"name": "no-mcp-ext", "version": "1.0.0"}
        (ext_dir / "gemini-extension.json").write_text(json.dumps(manifest))

        configs, artifacts = scan_gemini_extensions(tmp_path)
        assert configs == []
        assert len(artifacts) == 1
        assert artifacts[0].has_mcp_servers is False

    def test_empty_extensions_dir(self, tmp_path):
        configs, artifacts = scan_gemini_extensions(tmp_path)
        assert configs == []
        assert artifacts == []

    def test_missing_extensions_dir(self, tmp_path):
        nonexistent = tmp_path / "no-such-dir"
        configs, artifacts = scan_gemini_extensions(nonexistent)
        assert configs == []
        assert artifacts == []

    def test_missing_manifest(self, tmp_path):
        ext_dir = tmp_path / "no-manifest"
        ext_dir.mkdir()
        configs, artifacts = scan_gemini_extensions(tmp_path)
        assert configs == []
        assert artifacts == []


class TestProcessProjectGeminiExtensions:
    def test_discovers_project_level_extension(self, tmp_path):
        project = tmp_path / "my-project"
        ext_dir = project / ".gemini" / "extensions" / "team-ext"
        ext_dir.mkdir(parents=True)
        manifest = {
            "name": "team-ext",
            "version": "1.0.0",
            "mcpServers": {
                "teamServer": {"command": "node", "args": ["server.js"]},
            },
        }
        (ext_dir / "gemini-extension.json").write_text(json.dumps(manifest))

        configs, artifacts = process_project_gemini_extensions(
            [ext_dir / "gemini-extension.json"]
        )
        assert len(configs) == 1
        assert configs[0].config_scope == "project"
        assert configs[0].project_path == str(project)
        assert configs[0].client == "gemini_cli"
        assert len(configs[0].servers) == 1

        assert len(artifacts) == 1
        assert artifacts[0].scope == "project"

    def test_excludes_global_extensions(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "runlayer_cli.scan.gemini_extensions.Path.home", lambda: tmp_path
        )
        global_ext = tmp_path / ".gemini" / "extensions" / "global-ext"
        global_ext.mkdir(parents=True)
        manifest = {
            "name": "global-ext",
            "mcpServers": {"s": {"command": "x"}},
        }
        (global_ext / "gemini-extension.json").write_text(json.dumps(manifest))

        configs, _ = process_project_gemini_extensions(
            [global_ext / "gemini-extension.json"]
        )
        assert configs == []

    def test_ignores_non_gemini_extension_files(self):
        configs, artifacts = process_project_gemini_extensions(
            [Path("/project/.mcp.json"), Path("/project/SKILL.md")]
        )
        assert configs == []
        assert artifacts == []

    def test_deduplicates(self, tmp_path):
        project = tmp_path / "proj"
        ext_dir = project / ".gemini" / "extensions" / "dup-ext"
        ext_dir.mkdir(parents=True)
        manifest = {
            "name": "dup-ext",
            "mcpServers": {"s": {"command": "x"}},
        }
        (ext_dir / "gemini-extension.json").write_text(json.dumps(manifest))
        manifest_path = ext_dir / "gemini-extension.json"

        configs, _ = process_project_gemini_extensions([manifest_path, manifest_path])
        assert len(configs) == 1
