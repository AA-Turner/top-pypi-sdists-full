"""Tests for ``is_variable_interpolation()``."""

from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind
from agentic_devtools.cli.speckit.verify_artifacts import is_variable_interpolation


def _reference(text: str, context: str, occurrence_index: int = 0) -> Reference:
    return Reference(
        text=text,
        kind=ReferenceKind.FILE_PATH,
        plan_location="L1",
        context_sentence=context,
        occurrence_index=occurrence_index,
    )


class TestIsVariableInterpolation:
    """Detecting runtime-expanded paths that must not be checked on disk."""

    def test_detects_shell_variable_prefix(self) -> None:
        reference = _reference("SPEC_DIR/spec.md", 'SPEC_FILE="$SPEC_DIR/spec.md"')

        assert is_variable_interpolation(reference) is True

    def test_detects_brace_prefix(self) -> None:
        reference = _reference("SPEC_DIR/spec.md", "path = {SPEC_DIR/spec.md}")

        assert is_variable_interpolation(reference) is True

    def test_detects_percent_prefix(self) -> None:
        reference = _reference("SPEC_DIR/spec.md", "set path=%SPEC_DIR/spec.md%")

        assert is_variable_interpolation(reference) is True

    def test_returns_false_for_plain_reference(self) -> None:
        reference = _reference("cli/runner.py", "Update cli/runner.py accordingly.")

        assert is_variable_interpolation(reference) is False

    def test_returns_false_when_reference_starts_the_sentence(self) -> None:
        reference = _reference("cli/runner.py", "cli/runner.py is updated.")

        assert is_variable_interpolation(reference) is False

    def test_returns_false_when_text_absent_from_context(self) -> None:
        reference = _reference("cli/runner.py", "Unrelated sentence.")

        assert is_variable_interpolation(reference) is False

    def test_returns_false_when_reference_normalizes_to_empty_text(self) -> None:
        reference = _reference("#L1", "$SPEC_DIR/spec.md")

        assert is_variable_interpolation(reference) is False

    def test_returns_false_for_plain_selected_occurrence_when_later_one_is_interpolated(self) -> None:
        reference = _reference("SPEC_DIR/spec.md", "SPEC_DIR/spec.md becomes $SPEC_DIR/spec.md")

        assert is_variable_interpolation(reference) is False

    def test_detects_interpolation_on_the_selected_later_occurrence(self) -> None:
        reference = _reference(
            "SPEC_DIR/spec.md",
            "SPEC_DIR/spec.md becomes $SPEC_DIR/spec.md",
            occurrence_index=1,
        )

        assert is_variable_interpolation(reference) is True
