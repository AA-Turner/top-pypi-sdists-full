"""Tests for ``resolve_generated_artifact()``."""

from pathlib import Path

from agentic_devtools.cli.speckit.verify_artifacts import (
    GENERATED_ARTIFACT_SUBDIR,
    resolve_generated_artifact,
)


class TestResolveGeneratedArtifact:
    """Diagnostics resolve from ``generated/`` with a legacy-root fallback."""

    def test_prefers_the_generated_subdirectory(self, tmp_path: Path) -> None:
        generated = tmp_path / GENERATED_ARTIFACT_SUBDIR
        generated.mkdir()
        (generated / "test-coverage.json").write_text("{}", encoding="utf-8")
        (tmp_path / "test-coverage.json").write_text("{}", encoding="utf-8")

        resolved = resolve_generated_artifact(tmp_path, "test-coverage.json")

        assert resolved == generated / "test-coverage.json"

    def test_falls_back_to_the_legacy_spec_directory_root(self, tmp_path: Path) -> None:
        legacy = tmp_path / "test-coverage.json"
        legacy.write_text("{}", encoding="utf-8")

        assert resolve_generated_artifact(tmp_path, "test-coverage.json") == legacy

    def test_returns_the_generated_path_when_the_file_is_absent(self, tmp_path: Path) -> None:
        resolved = resolve_generated_artifact(tmp_path, "analysis-report.md")

        assert resolved == tmp_path / GENERATED_ARTIFACT_SUBDIR / "analysis-report.md"
