"""Tests for audit models."""

from agentic_devtools.cli.audit.models import (
    AuditBatch,
    BatchOutput,
    ClaimResult,
    ClosedPRInfo,
    InstructionFile,
    ReviewObservation,
)


class TestClaimResult:
    """Tests for ClaimResult enum."""

    def test_claimed_value(self) -> None:
        assert ClaimResult.CLAIMED.value == "claimed"

    def test_already_claimed_value(self) -> None:
        assert ClaimResult.ALREADY_CLAIMED.value == "already_claimed"

    def test_enum_members(self) -> None:
        assert len(ClaimResult) == 2


class TestClosedPRInfo:
    """Tests for ClosedPRInfo dataclass."""

    def test_creation(self) -> None:
        pr = ClosedPRInfo(
            number=42,
            title="feat: add feature",
            url="https://github.com/org/repo/pull/42",
            state="closed",
            closed_at="2024-01-15T10:00:00Z",
            merged=True,
        )
        assert pr.number == 42
        assert pr.title == "feat: add feature"
        assert pr.merged is True

    def test_frozen(self) -> None:
        pr = ClosedPRInfo(number=1, title="t", url="u", state="closed", closed_at="", merged=False)
        try:
            pr.number = 2  # type: ignore[misc]
            raise AssertionError("Should be frozen")
        except AttributeError:
            pass


class TestReviewObservation:
    """Tests for ReviewObservation dataclass."""

    def test_defaults(self) -> None:
        obs = ReviewObservation(
            file_path="src/main.py",
            line=10,
            body="Consider using a constant here",
            diff_hunk="@@ -10,3 +10,3 @@",
            resolved=True,
            reviewer="reviewer1",
            primary_category="naming",
        )
        assert obs.secondary_category == ""
        assert obs.is_stale is False

    def test_stale_flag(self) -> None:
        obs = ReviewObservation(
            file_path="deleted.py",
            line=5,
            body="Fix this",
            diff_hunk="",
            resolved=False,
            reviewer="bot",
            primary_category="other",
            is_stale=True,
        )
        assert obs.is_stale is True


class TestAuditBatch:
    """Tests for AuditBatch dataclass."""

    def test_defaults(self) -> None:
        batch = AuditBatch(batch_id="abc123")
        assert batch.pr_numbers == []
        assert batch.status == "preparing"
        assert batch.output_dir == ""

    def test_mutable(self) -> None:
        batch = AuditBatch(batch_id="abc123")
        batch.pr_numbers.append(42)
        batch.status = "ready"
        assert batch.pr_numbers == [42]
        assert batch.status == "ready"


class TestInstructionFile:
    """Tests for InstructionFile dataclass."""

    def test_existing_file(self) -> None:
        f = InstructionFile(path=".github/copilot-instructions.md", exists=True, content="# Rules")
        assert f.exists is True
        assert f.content == "# Rules"

    def test_nonexistent_file(self) -> None:
        f = InstructionFile(path="src/copilot-instructions.md", exists=False)
        assert f.exists is False
        assert f.content == ""


class TestBatchOutput:
    """Tests for BatchOutput dataclass."""

    def test_defaults(self) -> None:
        out = BatchOutput(batch_id="xyz")
        assert out.prs == []
        assert out.observations == []
        assert out.instruction_files == []
