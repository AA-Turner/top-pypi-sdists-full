"""Tests for find_oversized_instruction_files."""

from agentic_devtools.cli.audit.instruction_size import (
    MAX_INSTRUCTION_FILE_LINES,
    find_oversized_instruction_files,
)


class TestFindOversizedInstructionFiles:
    """Tests for the instruction-file line cap detector."""

    def test_returns_empty_for_files_within_cap(self) -> None:
        """A file exactly at the cap is not a violation."""
        content = "\n".join(["line"] * MAX_INSTRUCTION_FILE_LINES)
        assert find_oversized_instruction_files([(".github/copilot-instructions.md", content)]) == []

    def test_trailing_newline_does_not_add_a_line(self) -> None:
        """A newline-terminated file at the cap is still within the cap."""
        content = "\n".join(["line"] * MAX_INSTRUCTION_FILE_LINES) + "\n"
        assert find_oversized_instruction_files([(".github/copilot-instructions.md", content)]) == []

    def test_reports_path_and_line_count_over_cap(self) -> None:
        """A file one line over the cap is reported with its line count."""
        content = "\n".join(["line"] * (MAX_INSTRUCTION_FILE_LINES + 1))
        violations = find_oversized_instruction_files([("docs/copilot-instructions.md", content)])
        assert violations == [("docs/copilot-instructions.md", MAX_INSTRUCTION_FILE_LINES + 1)]

    def test_reports_every_violation_in_input_order(self) -> None:
        """All oversized candidates are reported, in the order supplied."""
        oversized = "\n".join(["line"] * (MAX_INSTRUCTION_FILE_LINES + 2))
        violations = find_oversized_instruction_files(
            [
                ("a/copilot-instructions.md", oversized),
                ("b/copilot-instructions.md", "short"),
                ("c/copilot-instructions.md", oversized),
            ]
        )
        assert [path for path, _ in violations] == [
            "a/copilot-instructions.md",
            "c/copilot-instructions.md",
        ]

    def test_returns_empty_for_no_candidates(self) -> None:
        """No candidates means no violations."""
        assert find_oversized_instruction_files([]) == []
