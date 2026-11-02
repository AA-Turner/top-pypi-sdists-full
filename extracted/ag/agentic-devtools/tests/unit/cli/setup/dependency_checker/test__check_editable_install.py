"""Tests for the report-only editable installation diagnostic."""

import json
import ntpath
import os
from importlib.metadata import PackageNotFoundError, PathDistribution
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.setup import dependency_checker as checker


@pytest.fixture
def project(tmp_path, monkeypatch):
    """Invoke from a nested directory in a project with spaces in its path."""
    root = tmp_path / "current worktree"
    child = root / "nested"
    child.mkdir(parents=True)
    (root / "pyproject.toml").touch()
    monkeypatch.chdir(child)
    return root


@pytest.fixture
def metadata(monkeypatch):
    """Isolate installed distribution metadata from the host environment."""
    dist = Mock(spec=["read_text"])
    monkeypatch.setattr(checker, "distribution", Mock(return_value=dist))
    return dist


class TestCheckEditableInstall:
    @pytest.mark.parametrize("raw", [None, "{}", '{"dir_info": {}}', '{"dir_info": {"editable": false}}'])
    def test_non_editable_or_absent_direct_url(self, project, metadata, raw):
        metadata.read_text.return_value = raw
        status = checker._check_editable_install()
        assert status.name == "editable-install"
        assert status.found is True
        assert status.required is False
        metadata.read_text.assert_called_once_with("direct_url.json")
        checker.distribution.assert_called_once_with("agentic-devtools")

    def test_distribution_not_installed(self, project, metadata):
        checker.distribution.side_effect = PackageNotFoundError
        assert checker._check_editable_install().found is True

    @pytest.mark.parametrize("editable", [None, False, True])
    def test_path_distribution_absent_or_healthy_direct_url(self, project, tmp_path, monkeypatch, editable):
        metadata_path = tmp_path / "site-packages" / "agentic_devtools-1.0.dist-info"
        metadata_path.mkdir(parents=True)
        if editable is not None:
            (metadata_path / "direct_url.json").write_text(
                json.dumps({"dir_info": {"editable": editable}, "url": project.as_uri()}), encoding="utf-8"
            )
        monkeypatch.setattr(checker, "distribution", Mock(return_value=PathDistribution(metadata_path)))
        assert checker._check_editable_install().found is True

    def test_path_distribution_with_unreadable_direct_url_warns(self, project, tmp_path, monkeypatch):
        metadata_path = tmp_path / "site-packages" / "agentic_devtools-1.0.dist-info"
        metadata_path.mkdir(parents=True)
        direct_url_path = metadata_path / "direct_url.json"
        direct_url_path.write_text("{}", encoding="utf-8")
        monkeypatch.setattr(checker, "distribution", Mock(return_value=PathDistribution(metadata_path)))
        original_read_text = Path.read_text

        def read_text(path, *args, **kwargs):
            if path == direct_url_path:
                raise PermissionError("permission denied")
            return original_read_text(path, *args, **kwargs)

        with patch.object(Path, "read_text", read_text):
            status = checker._check_editable_install()

        assert status.found is False
        assert status.required is False
        assert status.category == "Warning"

    @pytest.mark.parametrize("source_kind", ["missing", "foreign", "file"])
    def test_stale_source_warning(self, project, metadata, tmp_path, source_kind):
        source = tmp_path / "other"
        if source_kind == "foreign":
            source.mkdir()
        elif source_kind == "file":
            source.touch()
        metadata.read_text.return_value = json.dumps({"dir_info": {"editable": True}, "url": source.as_uri()})
        status = checker._check_editable_install()
        assert status.name == "editable-install"
        assert status.found is False
        assert status.required is False
        assert status.category == "Warning"
        assert str(project) in status.install_hint
        assert status.install_hint.startswith("pip install -e ")
        assert status.repair_details == {}
        assert source.exists() is (source_kind != "missing")

    @pytest.mark.parametrize("suffix", ["", "/nested/.."])
    def test_matching_normalized_source(self, project, metadata, suffix):
        metadata.read_text.return_value = json.dumps({"dir_info": {"editable": True}, "url": project.as_uri() + suffix})
        assert checker._check_editable_install().found is True

    def test_symlink_source(self, project, metadata, tmp_path):
        link = tmp_path / "link"
        link.symlink_to(project, target_is_directory=True)
        metadata.read_text.return_value = json.dumps({"dir_info": {"editable": True}, "url": link.as_uri()})
        assert checker._check_editable_install().found is True

    def test_nearest_project_root(self, project, metadata, monkeypatch):
        nested = project / "nested"
        (nested / "pyproject.toml").touch()
        metadata.read_text.return_value = json.dumps({"dir_info": {"editable": True}, "url": nested.as_uri()})
        assert checker._check_editable_install().found is True

    @pytest.mark.parametrize("exists", [True, False])
    def test_no_project_root_still_checks_source(self, tmp_path, metadata, monkeypatch, exists):
        monkeypatch.chdir(tmp_path)
        source = tmp_path / "source"
        if exists:
            source.mkdir()
        metadata.read_text.return_value = json.dumps({"dir_info": {"editable": True}, "url": source.as_uri()})
        status = checker._check_editable_install()
        assert status.found is exists
        assert status.required is False
        if not exists:
            assert "<current-worktree-root>" in status.install_hint

    @pytest.mark.parametrize("platform", ["linux", "win32"])
    def test_windows_case_insensitive_comparison(self, project, metadata, monkeypatch, platform):
        metadata.read_text.return_value = json.dumps(
            {"dir_info": {"editable": True}, "url": project.as_uri().upper().replace("FILE:", "file:")}
        )
        with (
            patch.object(checker.sys, "platform", platform),
            patch.object(checker.os.path, "normcase", side_effect=ntpath.normcase),
            patch.object(Path, "is_dir", return_value=True),
        ):
            assert checker._check_editable_install().found is True

    @pytest.mark.parametrize("path_component", ["R&D", "path with spaces", "O'Brien", "$cash", "`tick", "(build)"])
    def test_windows_hint_uses_power_shell_literal_quoting(self, tmp_path, metadata, monkeypatch, path_component):
        root = tmp_path / path_component
        child = root / "nested"
        child.mkdir(parents=True)
        (root / "pyproject.toml").touch()
        monkeypatch.chdir(child)
        metadata.read_text.return_value = json.dumps(
            {"dir_info": {"editable": True}, "url": (tmp_path / "other").as_uri()}
        )

        with patch.object(checker.sys, "platform", "win32"):
            status = checker._check_editable_install()

        quoted_root = str(root).replace("'", "''")
        assert status.install_hint == f"pip install -e '{quoted_root}'"

    @pytest.mark.parametrize(
        "raw",
        [
            "",
            "{",
            "null",
            "[]",
            "42",
            '{"dir_info": null}',
            '{"dir_info": []}',
            '{"dir_info": {"editable": "true"}}',
            '{"dir_info": {"editable": true}}',
            '{"dir_info": {"editable": true}, "url": null}',
            '{"dir_info": {"editable": true}, "url": 42}',
            '{"dir_info": {"editable": true}, "url": true}',
            '{"dir_info": {"editable": true}, "url": []}',
            '{"dir_info": {"editable": true}, "url": {}}',
            '{"dir_info": {"editable": true}, "url": "https://example.com/source"}',
            '{"dir_info": {"editable": true}, "url": "file:relative"}',
            '{"dir_info": {"editable": true}, "url": "file:///tmp/source?query"}',
            '{"dir_info": {"editable": true}, "url": "file:///tmp/source#fragment"}',
            '{"dir_info": {"editable": true}, "url": "file:///tmp/%00"}',
        ],
    )
    def test_malformed_metadata_warns(self, project, metadata, raw):
        metadata.read_text.return_value = raw
        status = checker._check_editable_install()
        assert status.found is False
        assert status.required is False
        assert status.category == "Warning"
        assert str(project) in status.install_hint

    @pytest.mark.parametrize("error", [OSError("unreadable"), UnicodeError("invalid encoding")])
    def test_unreadable_metadata_warns(self, project, metadata, error):
        metadata.read_text.side_effect = error
        assert checker._check_editable_install().found is False

    def test_distribution_lookup_error_warns(self, project, metadata):
        checker.distribution.side_effect = OSError("unreadable")
        assert checker._check_editable_install().found is False

    @pytest.mark.parametrize("error", [OSError("deleted cwd"), FileNotFoundError("deleted cwd")])
    def test_unavailable_cwd_warns(self, metadata, error):
        with patch.object(Path, "cwd", side_effect=error):
            status = checker._check_editable_install()
        assert status.found is False
        assert "<current-worktree-root>" in status.install_hint

    def test_filesystem_error_warns(self, project, metadata):
        metadata.read_text.return_value = json.dumps({"dir_info": {"editable": True}, "url": project.as_uri()})
        with patch.object(Path, "resolve", side_effect=RuntimeError("symlink loop")):
            assert checker._check_editable_install().found is False

    def test_remote_file_url_warns_on_posix(self, project, metadata):
        metadata.read_text.return_value = '{"dir_info": {"editable": true}, "url": "file://server/share/source"}'
        status = checker._check_editable_install()
        assert status.found is False

    def test_does_not_mutate_environment(self, project, metadata):
        metadata.read_text.return_value = '{"dir_info": {"editable": true}, "url": "file:///missing"}'
        with patch.dict(os.environ):
            before = dict(os.environ)
            checker._check_editable_install()
            assert dict(os.environ) == before
