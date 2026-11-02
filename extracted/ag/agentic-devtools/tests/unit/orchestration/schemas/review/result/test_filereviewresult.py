"""Tests for FileReviewResult model."""

from agentic_devtools.orchestration.schemas.review.result import FileReviewResult


class TestFileReviewResult:
    """Tests for FileReviewResult construction and serialization."""

    def test_construction(self):
        result = FileReviewResult(
            file_path="src/main.py",
            status="approved",
            summary="No issues found",
        )
        assert result.file_path == "src/main.py"
        assert result.status == "approved"
        assert result.findings == []

    def test_with_findings(self):
        result = FileReviewResult(
            file_path="src/main.py",
            status="needs-work",
            summary="Issues found",
            findings=[{"severity": "high", "description": "Bug", "diff_side": "new", "new_line": 1, "confidence": 0.9}],
        )
        assert len(result.findings) == 1
        assert result.findings[0].description == "Bug"

    def test_rejects_unknown_status(self):
        from pydantic import ValidationError

        try:
            FileReviewResult(file_path="src/main.py", status="needs_work", summary="Issues found")
        except ValidationError as exc:
            assert any(error["loc"] == ("status",) for error in exc.errors())
        else:
            raise AssertionError("Expected ValidationError for invalid status")

    def test_rejects_terminal_skipped_status(self):
        from pydantic import ValidationError

        try:
            FileReviewResult(file_path="src/main.py", status="skipped", summary="skip")
        except ValidationError as exc:
            assert any(error["loc"] == ("status",) for error in exc.errors())
        else:
            raise AssertionError("Expected ValidationError for terminal 'skipped' status")

    def test_needs_work_status_accepted(self):
        result = FileReviewResult(file_path="f.py", status="needs-work", summary="Fix it")
        assert result.status == "needs-work"

    def test_model_dump(self):
        result = FileReviewResult(
            file_path="f.py",
            status="approved",
            summary="LGTM",
        )
        data = result.model_dump()
        assert data["file_path"] == "f.py"
        assert data["findings"] == []

    def test_round_trip(self):
        original = FileReviewResult(
            file_path="f.py",
            status="approved",
            summary="OK",
        )
        raw = original.model_dump_json()
        restored = FileReviewResult.model_validate_json(raw)
        assert original == restored
