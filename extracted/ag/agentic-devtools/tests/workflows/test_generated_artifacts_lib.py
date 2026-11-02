"""Behavioral tests for generated-artifacts.sh helper functions."""

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "lib" / "generated-artifacts.sh"


HAS_BASH = shutil.which("bash") is not None


def _run_library_command(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        ["/usr/bin/env", "bash", "-c", script],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.mark.skipif(not HAS_BASH, reason="bash is required for generated-artifacts shell library tests")
class TestGeneratedArtifactsLibrary:
    """Validate migration and resolver behavior with temporary spec directories."""

    def test_migrate_moves_legacy_file_when_generated_copy_is_missing(self, tmp_path: Path) -> None:
        spec_dir = tmp_path / "specs" / "1234-feature"
        spec_dir.mkdir(parents=True)
        legacy = spec_dir / "analysis-report.md"
        legacy.write_text("legacy-report", encoding="utf-8")

        _run_library_command(
            f'source "{SCRIPT_PATH}"; migrate_legacy_generated_artifacts "{spec_dir}" "analysis-report.md"'
        )

        current = spec_dir / "generated" / "analysis-report.md"
        assert current.read_text(encoding="utf-8") == "legacy-report"
        assert not legacy.exists()

    def test_migrate_removes_legacy_file_when_generated_copy_already_exists(self, tmp_path: Path) -> None:
        spec_dir = tmp_path / "specs" / "1234-feature"
        generated = spec_dir / "generated"
        generated.mkdir(parents=True)
        current = generated / "analysis-report.md"
        current.write_text("current-report", encoding="utf-8")
        legacy = spec_dir / "analysis-report.md"
        legacy.write_text("legacy-report", encoding="utf-8")

        _run_library_command(
            f'source "{SCRIPT_PATH}"; migrate_legacy_generated_artifacts "{spec_dir}" "analysis-report.md"'
        )

        assert current.read_text(encoding="utf-8") == "current-report"
        assert not legacy.exists()

    def test_resolve_prefers_generated_path_when_both_copies_exist(self, tmp_path: Path) -> None:
        spec_dir = tmp_path / "specs" / "1234-feature"
        generated = spec_dir / "generated"
        generated.mkdir(parents=True)
        current = generated / "analysis-report.md"
        current.write_text("current-report", encoding="utf-8")
        legacy = spec_dir / "analysis-report.md"
        legacy.write_text("legacy-report", encoding="utf-8")

        result = _run_library_command(
            f'source "{SCRIPT_PATH}"; resolve_generated_artifact "{spec_dir}" "analysis-report.md"'
        )

        assert result.stdout.strip() == str(current)

    def test_resolve_falls_back_to_legacy_path_when_generated_copy_is_missing(self, tmp_path: Path) -> None:
        spec_dir = tmp_path / "specs" / "1234-feature"
        spec_dir.mkdir(parents=True)
        legacy = spec_dir / "analysis-report.md"
        legacy.write_text("legacy-report", encoding="utf-8")

        result = _run_library_command(
            f'source "{SCRIPT_PATH}"; resolve_generated_artifact "{spec_dir}" "analysis-report.md"'
        )

        assert result.stdout.strip() == str(legacy)
