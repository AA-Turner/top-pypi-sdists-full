"""Tests for _register_setup_artifacts."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup import registry as registry_module
from agentic_devtools.cli.setup.registry import load_registry


class TestRegisterSetupArtifacts:
    """Tests for _register_setup_artifacts."""

    def test_dry_run_writes_nothing_and_previews_count(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch
    ) -> None:
        """Dry-run prints a 'would register' preview and never writes the registry."""
        reg = tmp_path / "registry.json"
        monkeypatch.setattr(registry_module, "get_registry_path", lambda: reg)
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM")

        commands._register_setup_artifacts(tmp_path, cert, tmp_path / "npmrc", dry_run=True)

        out = capsys.readouterr().out
        assert "would register 2 artifact(s)" in out
        assert not reg.exists()

    def test_dry_run_counts_only_non_none_paths(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Dry-run counts only the non-None planned artifact paths."""
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM")
        commands._register_setup_artifacts(tmp_path, cert, None, dry_run=True)
        assert "would register 1 artifact(s)" in capsys.readouterr().out

    def test_real_run_registers_existing_artifacts(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch
    ) -> None:
        """A real run hashes existing files and records them for the repo context."""
        reg = tmp_path / "registry.json"
        monkeypatch.setattr(registry_module, "get_registry_path", lambda: reg)
        repo = tmp_path / "repo"
        repo.mkdir()
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM")
        npmrc = tmp_path / "npmrc"
        npmrc.write_text("registry=...")

        commands._register_setup_artifacts(repo, cert, npmrc)

        data = load_registry(reg)
        assert len(data.contexts) == 1
        assert len(data.artifacts) == 2
        assert "Registered 2 artifact(s)" in capsys.readouterr().out

    def test_real_run_skips_missing_files(self, tmp_path: Path, monkeypatch) -> None:
        """Non-existent artifact paths are skipped without error."""
        reg = tmp_path / "registry.json"
        monkeypatch.setattr(registry_module, "get_registry_path", lambda: reg)
        repo = tmp_path / "repo"
        repo.mkdir()
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM")
        missing_npmrc = tmp_path / "does-not-exist"

        commands._register_setup_artifacts(repo, cert, missing_npmrc)

        data = load_registry(reg)
        assert len(data.artifacts) == 1  # only the cert

    def test_real_run_with_no_existing_artifacts_writes_nothing(self, tmp_path: Path, monkeypatch) -> None:
        """When no artifact files exist, no registry is written and nothing prints."""
        reg = tmp_path / "registry.json"
        monkeypatch.setattr(registry_module, "get_registry_path", lambda: reg)
        repo = tmp_path / "repo"
        repo.mkdir()
        commands._register_setup_artifacts(repo, tmp_path / "missing.pem", None)
        assert not reg.exists()

    def test_registry_failure_is_swallowed(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """A registry error is caught and reported, never aborting setup."""
        repo = tmp_path / "repo"
        repo.mkdir()
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM")
        with patch.object(registry_module, "register_context", side_effect=RuntimeError("boom")):
            commands._register_setup_artifacts(repo, cert, None)
        assert "Could not update ~/.agdt/registry.json: boom" in capsys.readouterr().err
