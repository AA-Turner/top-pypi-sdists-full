"""Tests for check_corrupted_artifacts_status."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.commands import check_corrupted_artifacts_status


class TestCheckCorruptedArtifactsStatus:
    """Tests for check_corrupted_artifacts_status helper."""

    def test_healthy_returns_found_true(self) -> None:
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
            return_value=[],
        ):
            status, artifacts = check_corrupted_artifacts_status()
        assert status.found is True
        assert status.name == "corrupted-install-artifacts"
        assert status.required is True
        assert status.category == "Required"
        assert artifacts == []

    def test_corrupted_returns_found_false(self) -> None:
        fake_artifacts = [Path("/sp/~gentic-devtools")]
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
            return_value=fake_artifacts,
        ):
            status, artifacts = check_corrupted_artifacts_status()
        assert status.found is False
        assert status.name == "corrupted-install-artifacts"
        assert artifacts == fake_artifacts

    def test_corrupted_stores_artifacts_in_repair_details(self) -> None:
        fake_artifacts = [Path("/sp/~gentic-devtools")]
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
            return_value=fake_artifacts,
        ):
            status, _artifacts = check_corrupted_artifacts_status()
        # Stored as str so repair_details stays JSON-serializable.
        assert status.repair_details.get("detected_artifacts") == [str(p) for p in fake_artifacts]

    def test_healthy_repair_details_empty(self) -> None:
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
            return_value=[],
        ):
            status, _artifacts = check_corrupted_artifacts_status()
        assert "detected_artifacts" not in status.repair_details

    def test_oserror_treated_as_healthy(self) -> None:
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
            side_effect=OSError("scan failed"),
        ):
            status, artifacts = check_corrupted_artifacts_status()
        assert status.found is True
        assert artifacts == []

    def test_permission_error_treated_as_healthy(self) -> None:
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
            side_effect=PermissionError("denied"),
        ):
            status, artifacts = check_corrupted_artifacts_status()
        assert status.found is True
        assert artifacts == []
