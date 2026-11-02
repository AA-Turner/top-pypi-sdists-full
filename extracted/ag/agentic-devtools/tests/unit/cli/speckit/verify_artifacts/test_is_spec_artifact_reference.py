"""Tests for ``is_spec_artifact_reference()``."""

import pytest

from agentic_devtools.cli.speckit.verify_artifacts import is_spec_artifact_reference


class TestIsSpecArtifactReference:
    """Distinguishing spec-directory artifacts from repository files."""

    @pytest.mark.parametrize(
        "text",
        ["spec.md", "plan.md", "tasks.md", "research.md", "data-model.md", "quickstart.md", "analysis-report.md"],
    )
    def test_accepts_known_artifact_filenames(self, text: str) -> None:
        assert is_spec_artifact_reference(text) is True

    @pytest.mark.parametrize(
        "text",
        ["contracts/api.md", "contracts/openapi.yaml", "checklists/requirements.md"],
    )
    def test_accepts_artifact_subdirectory_paths(self, text: str) -> None:
        assert is_spec_artifact_reference(text) is True

    @pytest.mark.parametrize(
        "text",
        [
            "generated/analysis-report.md",
            "generated/fr-coverage.json",
            "generated/test-coverage.json",
        ],
    )
    def test_accepts_canonical_generated_diagnostic_paths(self, text: str) -> None:
        assert is_spec_artifact_reference(text) is True

    def test_rejects_non_relocated_file_under_generated(self) -> None:
        # Only RELOCATED_GENERATED_ARTIFACT_FILENAMES qualify; other generated/
        # paths are not spec artifacts.
        assert is_spec_artifact_reference("generated/spec.md") is False

    def test_rejects_repository_paths(self) -> None:
        assert is_spec_artifact_reference("agentic_devtools/cli/runner.py") is False

    def test_rejects_readme_at_repository_root(self) -> None:
        assert is_spec_artifact_reference("README.md") is False
