"""Tests for the InstructionFileTooLongError exception class."""

from agentic_devtools.cli.audit.instruction_size import InstructionFileTooLongError


class TestInstructionFileTooLongError:
    """Tests for InstructionFileTooLongError."""

    def test_is_a_runtime_error(self) -> None:
        """Callers may catch it as a RuntimeError."""
        assert issubclass(InstructionFileTooLongError, RuntimeError)

    def test_preserves_its_message(self) -> None:
        """The remediation message survives round-tripping through str()."""
        assert str(InstructionFileTooLongError("too long")) == "too long"
