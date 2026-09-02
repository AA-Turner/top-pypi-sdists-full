"""Tests for write_batch_output() verifying Markdown structure."""

from pathlib import Path

from agentic_devtools.cli.audit.models import (
    BatchOutput,
    ClosedPRInfo,
    InstructionFile,
    ReviewObservation,
)
from agentic_devtools.cli.audit.output_format import write_batch_output


class TestWriteBatchOutput:
    """Tests for write_batch_output() verifying output file generation."""

    def _make_batch_output(self) -> BatchOutput:
        return BatchOutput(
            batch_id="test-batch-123",
            prs=[
                ClosedPRInfo(
                    number=42,
                    title="feat: add feature",
                    url="https://github.com/org/repo/pull/42",
                    state="closed",
                    closed_at="2024-01-15T10:00:00Z",
                    merged=True,
                ),
            ],
            observations=[
                ReviewObservation(
                    file_path="src/main.py",
                    line=10,
                    body="Missing validation for input",
                    diff_hunk="@@ -10,3 +10,3 @@\n-old\n+new",
                    resolved=True,
                    reviewer="reviewer1",
                    primary_category="input_validation",
                    secondary_category="error_handling",
                    pr_number=42,
                ),
            ],
            instruction_files=[
                InstructionFile(
                    path=".github/copilot-instructions.md",
                    exists=True,
                    content="# Root instructions\nExisting content.",
                ),
            ],
        )

    def test_creates_output_directory(self, tmp_path: Path) -> None:
        output_dir = tmp_path / "output"
        batch_output = self._make_batch_output()
        write_batch_output(batch_output, str(output_dir))
        assert output_dir.is_dir()

    def test_writes_batch_summary(self, tmp_path: Path) -> None:
        batch_output = self._make_batch_output()
        write_batch_output(batch_output, str(tmp_path))
        summary = (tmp_path / "batch-summary.md").read_text()
        assert "test-batch-123" in summary
        assert "#42" in summary
        assert "input_validation" in summary

    def test_writes_batch_data(self, tmp_path: Path) -> None:
        batch_output = self._make_batch_output()
        write_batch_output(batch_output, str(tmp_path))
        data = (tmp_path / "batch-data.md").read_text()
        assert "PR #42" in data
        assert "src/main.py" in data
        assert "Missing validation" in data
        assert "diff hunk" in data.lower() or "@@ -10,3 +10,3 @@" in data

    def test_writes_instruction_files(self, tmp_path: Path) -> None:
        batch_output = self._make_batch_output()
        write_batch_output(batch_output, str(tmp_path))
        instructions = (tmp_path / "instruction-files.md").read_text()
        assert ".github/copilot-instructions.md" in instructions
        assert "Root instructions" in instructions
        assert "exists (update allowed)" in instructions

    def test_empty_batch(self, tmp_path: Path) -> None:
        batch_output = BatchOutput(batch_id="empty-batch")
        write_batch_output(batch_output, str(tmp_path))
        assert (tmp_path / "batch-summary.md").is_file()
        assert (tmp_path / "batch-data.md").is_file()
        assert (tmp_path / "instruction-files.md").is_file()

    def test_pr_with_no_observations(self, tmp_path: Path) -> None:
        batch_output = BatchOutput(
            batch_id="no-observations",
            prs=[
                ClosedPRInfo(
                    number=99,
                    title="Empty PR",
                    url="https://github.com/org/repo/pull/99",
                    state="closed",
                    closed_at="2024-01-15T10:00:00Z",
                    merged=False,
                ),
            ],
            observations=[],
        )

        write_batch_output(batch_output, str(tmp_path))

        data = (tmp_path / "batch-data.md").read_text()
        assert "No review observations for this PR" in data

    def test_instruction_file_exists_but_empty_content(self, tmp_path: Path) -> None:
        batch_output = BatchOutput(
            batch_id="empty-instructions",
            instruction_files=[
                InstructionFile(
                    path="src/copilot-instructions.md",
                    exists=True,
                    content="",
                ),
            ],
        )

        write_batch_output(batch_output, str(tmp_path))

        instructions = (tmp_path / "instruction-files.md").read_text()
        assert "src/copilot-instructions.md" in instructions
        assert "exists (update allowed)" in instructions
        assert "```markdown" not in instructions

    def test_legacy_instruction_file_marked_read_only(self, tmp_path: Path) -> None:
        """Read-only migration context is rendered distinctly from updateable files."""
        batch_output = BatchOutput(
            batch_id="legacy-instructions",
            instruction_files=[
                InstructionFile(
                    path="src/copilot-instructions.md",
                    exists=True,
                    can_update=False,
                    content="# Legacy instructions",
                ),
            ],
        )

        write_batch_output(batch_output, str(tmp_path))

        instructions = (tmp_path / "instruction-files.md").read_text()
        assert "src/copilot-instructions.md" in instructions
        assert "exists (read-only migration context)" in instructions

    def test_missing_read_only_instruction_file_not_marked_creatable(self, tmp_path: Path) -> None:
        """Missing read-only entries are not mislabeled as creation targets."""
        batch_output = BatchOutput(
            batch_id="missing-legacy-instructions",
            instruction_files=[
                InstructionFile(
                    path="src/copilot-instructions.md",
                    exists=False,
                    can_update=False,
                    content="",
                ),
            ],
        )

        write_batch_output(batch_output, str(tmp_path))

        instructions = (tmp_path / "instruction-files.md").read_text()
        assert "src/copilot-instructions.md" in instructions
        assert "does not exist (read-only migration context)" in instructions

    def test_stale_observations_marked(self, tmp_path: Path) -> None:
        batch_output = BatchOutput(
            batch_id="stale-test",
            prs=[
                ClosedPRInfo(number=1, title="t", url="u", state="closed", closed_at="", merged=True),
            ],
            observations=[
                ReviewObservation(
                    file_path="deleted.py",
                    line=5,
                    body="Fix this",
                    diff_hunk="",
                    resolved=False,
                    reviewer="bot",
                    primary_category="other",
                    is_stale=True,
                    pr_number=1,
                ),
            ],
        )
        write_batch_output(batch_output, str(tmp_path))
        data = (tmp_path / "batch-data.md").read_text()
        assert "STALE" in data

    def test_empty_diff_hunk_emits_placeholder_section(self, tmp_path: Path) -> None:
        """Diff hunk section is always emitted; placeholder used when hunk is absent."""
        batch_output = BatchOutput(
            batch_id="empty-hunk-test",
            prs=[
                ClosedPRInfo(number=5, title="PR", url="u", state="closed", closed_at="", merged=True),
            ],
            observations=[
                ReviewObservation(
                    file_path="src/foo.py",
                    line=1,
                    body="PR-level comment with no diff hunk",
                    diff_hunk="",
                    resolved=False,
                    reviewer="bot",
                    primary_category="other",
                    pr_number=5,
                ),
            ],
        )
        write_batch_output(batch_output, str(tmp_path))
        data = (tmp_path / "batch-data.md").read_text()
        assert "**Diff hunk:**" in data
        assert "*(no diff hunk available)*" in data

    def test_multiline_body_and_backticks_are_fenced(self, tmp_path: Path) -> None:
        """Bodies and hunks use safe fences so embedded Markdown cannot break structure."""
        body = "First line\n```python\nprint('hi')\n```"
        diff_hunk = "@@ -1 +1 @@\n-```old\n+```new"
        batch_output = BatchOutput(
            batch_id="fenced-observation",
            prs=[
                ClosedPRInfo(number=7, title="PR", url="u", state="closed", closed_at="", merged=True),
            ],
            observations=[
                ReviewObservation(
                    file_path="src/foo.py",
                    line=3,
                    body=body,
                    diff_hunk=diff_hunk,
                    resolved=False,
                    reviewer="bot",
                    primary_category="other",
                    pr_number=7,
                ),
            ],
        )

        write_batch_output(batch_output, str(tmp_path))

        data = (tmp_path / "batch-data.md").read_text()
        assert "- **Body:** First line" not in data
        assert "````text" in data
        assert "````diff" in data
        assert body in data
        assert diff_hunk in data

    def test_instruction_file_with_triple_backtick_uses_longer_fence(self, tmp_path: Path) -> None:
        """Instruction file content containing ``` is wrapped in a longer fence to avoid corruption."""
        content_with_fence = "# Instructions\n\n```python\nprint('hi')\n```\n"
        batch_output = BatchOutput(
            batch_id="fence-test",
            instruction_files=[
                InstructionFile(
                    path=".github/copilot-instructions.md",
                    exists=True,
                    content=content_with_fence,
                ),
            ],
        )

        write_batch_output(batch_output, str(tmp_path))

        instructions = (tmp_path / "instruction-files.md").read_text()
        # Content is present
        assert "print('hi')" in instructions
        # Must be wrapped in a fence longer than triple-backtick
        assert "````markdown" in instructions
        # The outer fence must not be prematurely terminated
        outer_fence = "````"
        open_pos = instructions.index(f"{outer_fence}markdown")
        close_pos = instructions.index(outer_fence, open_pos + len(f"{outer_fence}markdown"))
        # The inner ``` must appear between the outer fence delimiters
        inner_fence_pos = instructions.index("```python", open_pos)
        assert open_pos < inner_fence_pos < close_pos
