"""Tests for constants in speckit/phase0/config.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0 import config


class TestPhase0ConfigConstants:
    """Tests for the Phase 0 configuration constants."""

    def test_branch_name_template(self) -> None:
        assert config.BRANCH_NAME_TEMPLATE.format(issue_key="1799") == "speckit/1799/phase-0-normalize"

    def test_artifact_path_template(self) -> None:
        assert config.ARTIFACT_PATH_TEMPLATE.format(issue_key="1799") == ".speckit/issues/1799/issue.md"

    def test_provenance_path(self) -> None:
        assert config.PROVENANCE_PATH == ".speckit/phase0-provenance.json"

    def test_commit_type(self) -> None:
        assert config.COMMIT_TYPE == "chore"

    def test_commit_description(self) -> None:
        assert config.COMMIT_DESCRIPTION == "add normalized issue.md for Phase 0"

    def test_max_description_bytes(self) -> None:
        assert config.MAX_DESCRIPTION_BYTES == 102_400

    def test_phase_0_pr_label(self) -> None:
        assert config.PHASE_0_PR_LABEL == "speckit:phase-0"

    def test_phase_0_complete_label(self) -> None:
        assert config.PHASE_0_COMPLETE_LABEL == "speckit:phase-0-complete"
