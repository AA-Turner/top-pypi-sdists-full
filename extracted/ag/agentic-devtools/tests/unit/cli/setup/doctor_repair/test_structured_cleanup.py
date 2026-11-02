"""Tests for structured_cleanup."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.doctor_repair import structured_cleanup


class TestStructuredCleanup:
    """Tests for structured_cleanup function."""

    def test_removes_directory(self, tmp_path: Path) -> None:
        d = tmp_path / "~gentic-devtools"
        d.mkdir()
        (d / "file.txt").write_text("x")
        results = structured_cleanup([d])
        assert len(results) == 1
        assert results[0].success is True
        assert results[0].path == str(d)
        assert not d.exists()

    def test_removes_file(self, tmp_path: Path) -> None:
        f = tmp_path / "_editable_impl_agentic_devtools.pth"
        f.write_text("x")
        results = structured_cleanup([f])
        assert len(results) == 1
        assert results[0].success is True
        assert not f.exists()

    def test_removes_symlink(self, tmp_path: Path) -> None:
        target = tmp_path / "target"
        target.write_text("x")
        link = tmp_path / "link"
        link.symlink_to(target)
        results = structured_cleanup([link])
        assert len(results) == 1
        assert results[0].success is True
        assert not link.exists()
        assert target.exists()  # target not removed

    def test_file_not_found_treated_as_success(self, tmp_path: Path) -> None:
        missing = tmp_path / "nonexistent"
        results = structured_cleanup([missing])
        assert len(results) == 1
        assert results[0].success is True

    def test_permission_error_recorded(self, tmp_path: Path) -> None:
        d = tmp_path / "protected"
        d.mkdir()
        with patch("shutil.rmtree", side_effect=PermissionError("denied")):
            results = structured_cleanup([d])
        assert len(results) == 1
        assert results[0].success is False
        assert "denied" in (results[0].error or "")

    def test_multiple_artifacts(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.pth"
        f1.write_text("x")
        f2 = tmp_path / "b.pth"
        f2.write_text("x")
        results = structured_cleanup([f1, f2])
        assert len(results) == 2
        assert all(r.success for r in results)

    def test_partial_failure(self, tmp_path: Path) -> None:
        f1 = tmp_path / "ok.pth"
        f1.write_text("x")
        d = tmp_path / "fail_dir"
        d.mkdir()
        with patch("shutil.rmtree", side_effect=PermissionError("nope")):
            results = structured_cleanup([f1, d])
        assert results[0].success is True
        assert results[1].success is False
