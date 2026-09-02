"""Tests for check_instruction_file_sizes."""

import pytest

from agentic_devtools.cli.audit.instruction_size import (
    MAX_INSTRUCTION_FILE_LINES,
    InstructionFileTooLongError,
    check_instruction_file_sizes,
)


class TestCheckInstructionFileSizes:
    """Tests for the loud-failure guard used by the audit apply step."""

    def test_does_not_raise_when_all_candidates_are_within_cap(self) -> None:
        """A compliant batch passes the check silently."""
        check_instruction_file_sizes([(".github/copilot-instructions.md", "short\n")])

    def test_raises_when_a_candidate_exceeds_the_cap(self) -> None:
        """An oversized candidate fails loudly instead of being skipped."""
        content = "\n".join(["line"] * (MAX_INSTRUCTION_FILE_LINES + 1))
        with pytest.raises(InstructionFileTooLongError):
            check_instruction_file_sizes([(".github/copilot-instructions.md", content)])

    def test_error_message_names_the_file_count_cap_and_remedy(self) -> None:
        """The message must be actionable: which file, how long, and what to do."""
        content = "\n".join(["line"] * (MAX_INSTRUCTION_FILE_LINES + 5))
        with pytest.raises(InstructionFileTooLongError) as excinfo:
            check_instruction_file_sizes([("docs/copilot-instructions.md", content)])
        message = str(excinfo.value)
        assert "docs/copilot-instructions.md" in message
        assert str(MAX_INSTRUCTION_FILE_LINES + 5) in message
        assert str(MAX_INSTRUCTION_FILE_LINES) in message
        assert "do not raise the cap" in message
