"""Tests for repair_corrupted_artifacts."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup import doctor_repair as _dr_module
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor_repair import (
    UserDeclinedRepairError,
    repair_corrupted_artifacts,
)
from agentic_devtools.cli.setup.script_generators import required_setup as _rs_module


class TestRepairCorruptedArtifactsNoOp:
    """Healthy path: no artifacts detected."""

    def test_no_artifacts_sets_found_true(self, monkeypatch: pytest.MonkeyPatch) -> None:
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [])
        repair_corrupted_artifacts(dep)
        assert dep.found is True

    def test_no_artifacts_no_prompt(self, monkeypatch: pytest.MonkeyPatch) -> None:
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [])
        called = []
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: called.append(a))
        repair_corrupted_artifacts(dep)
        assert called == []


class TestRepairReusesCachedArtifacts:
    """Verify repair reuses artifacts from repair_details without re-scanning."""

    def test_repair_details_artifacts_used_no_rescan(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """When repair_details contains detected_artifacts (as str), detect_corrupted_artifacts is not called."""
        art = tmp_path / "~gentic-devtools"
        art.mkdir()
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        # Stored as str (JSON-serializable) — matches the real code path in commands.py.
        dep.repair_details["detected_artifacts"] = [str(art)]
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)

        scan_calls: list[int] = []

        def _no_scan() -> list[Path]:
            scan_calls.append(1)
            return []

        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", _no_scan)

        repair_corrupted_artifacts(dep)

        assert scan_calls == [], "detect_corrupted_artifacts should not be called when cached artifacts are available"
        assert dep.found is True

    def test_no_repair_details_falls_back_to_rescan(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When repair_details is empty, detect_corrupted_artifacts is called as fallback."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")

        scan_calls: list[int] = []

        def _rescan() -> list[Path]:
            scan_calls.append(1)
            return []

        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", _rescan)

        repair_corrupted_artifacts(dep)

        assert scan_calls == [1], "detect_corrupted_artifacts should be called as fallback when no cached artifacts"
        assert dep.found is True


class TestRepairCorruptedArtifactsConfirmed:
    """User confirms repair: all artifacts deleted."""

    def test_all_deleted_sets_found_true(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        art = tmp_path / "~gentic-devtools"
        art.mkdir()
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [art])
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        repair_corrupted_artifacts(dep)
        assert dep.found is True
        assert dep.repair_details["deleted_artifacts"] == [str(art)]
        assert "failed_artifacts" not in dep.repair_details

    def test_partial_failure_sets_found_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        art1 = tmp_path / "ok.pth"
        art1.write_text("x")
        art2 = tmp_path / "fail_dir"
        art2.mkdir()
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [art1, art2])
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        with patch("shutil.rmtree", side_effect=PermissionError("nope")):
            repair_corrupted_artifacts(dep)
        assert dep.found is False
        assert str(art1) in dep.repair_details["deleted_artifacts"]
        assert len(dep.repair_details["failed_artifacts"]) == 1
        assert dep.repair_details["failed_artifacts"][0]["path"] == str(art2)


class TestRepairCorruptedArtifactsDeclined:
    """User declines: no deletions."""

    def test_explicit_decline_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [Path("/sp/~gentic-devtools")])
        monkeypatch.setattr(
            _dr_module,
            "confirm_destructive_repair",
            lambda a: (_ for _ in ()).throw(UserDeclinedRepairError("User declined destructive repair")),
        )
        with pytest.raises(UserDeclinedRepairError, match="User declined"):
            repair_corrupted_artifacts(dep)
        assert dep.found is False

    def test_non_interactive_decline_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [Path("/sp/~gentic-devtools")])

        def _raise(_a):
            raise UserDeclinedRepairError("Non-interactive environment (no TTY) — cannot confirm destructive repair")

        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", _raise)
        with pytest.raises(UserDeclinedRepairError, match="Non-interactive"):
            repair_corrupted_artifacts(dep)
        assert dep.found is False


class TestRepairNeverAccessesAgdtDir:
    """Safety: repair never touches ~/.agdt/ paths."""

    def test_does_not_access_home_agdt(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        art = tmp_path / "~gentic-devtools"
        art.mkdir()
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [art])
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        repair_corrupted_artifacts(dep)
        # Only the artifact path (under tmp_path) was deleted, not ~/.agdt.
        assert dep.repair_details["deleted_artifacts"] == [str(art)]
        for path_str in dep.repair_details["deleted_artifacts"]:
            assert ".agdt" not in path_str

    def test_artifact_inside_agdt_dir_raises(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Artifacts resolved inside ~/.agdt must be refused (hard safety invariant)."""
        agdt_art = Path.home() / ".agdt" / "~gentic-devtools"
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        dep.repair_details["detected_artifacts"] = [str(agdt_art)]
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        with pytest.raises(ValueError, match=r"Refusing to delete artifact inside ~/\.agdt"):
            repair_corrupted_artifacts(dep)


class TestRepairDetectedArtifactsTypeValidation:
    """repair_details['detected_artifacts'] must be a list of str/Path."""

    def test_non_list_raises_type_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        dep.repair_details["detected_artifacts"] = "/some/path"  # str instead of list
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        with pytest.raises(TypeError, match="must be a list"):
            repair_corrupted_artifacts(dep)

    def test_list_with_invalid_entry_raises_type_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        dep.repair_details["detected_artifacts"] = [42]  # int entry
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        with pytest.raises(TypeError, match="must be str or Path"):
            repair_corrupted_artifacts(dep)


class TestRepairCrossDirectoryPartialFailure:
    """Cross-directory partial failure scenario."""

    def test_mixed_results_across_dirs(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        sp1 = tmp_path / "sp1"
        sp1.mkdir()
        sp2 = tmp_path / "sp2"
        sp2.mkdir()
        art1 = sp1 / "ok.pth"
        art1.write_text("x")
        art2 = sp2 / "fail_dir"
        art2.mkdir()
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True, category="Required")
        monkeypatch.setattr(_rs_module, "detect_corrupted_artifacts", lambda: [art1, art2])
        monkeypatch.setattr(_dr_module, "confirm_destructive_repair", lambda a: None)
        with patch("shutil.rmtree", side_effect=PermissionError("nope")):
            repair_corrupted_artifacts(dep)
        assert dep.found is False
        assert str(art1) in dep.repair_details["deleted_artifacts"]
        assert dep.repair_details["failed_artifacts"][0]["path"] == str(art2)
