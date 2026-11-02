"""Tests for ``_is_conditional_artifact_reference()``."""

from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind
from agentic_devtools.cli.speckit.verify_artifacts import _is_conditional_artifact_reference


class TestIsConditionalArtifactReference:
    """Artifacts annotated as 'optional' in their context must not be treated as promises."""

    def test_detects_optional_annotation_in_tree_comment(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="├── research.md          # Optional — only when there are unresolved technical unknowns",
        )

        assert _is_conditional_artifact_reference(reference) is True

    def test_detects_optional_annotation_case_insensitive(self) -> None:
        reference = Reference(
            text="data-model.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="├── data-model.md        # OPTIONAL — only when the feature introduces data entities",
        )

        assert _is_conditional_artifact_reference(reference) is True

    def test_returns_false_for_unconditional_reference(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="See `research.md` for the analysis details.",
        )

        assert _is_conditional_artifact_reference(reference) is False

    def test_returns_false_for_optional_word_without_tree_annotation(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="See research.md for optional deployment guidance.",
        )

        assert _is_conditional_artifact_reference(reference) is False

    def test_returns_false_when_context_sentence_is_empty(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="",
        )

        assert _is_conditional_artifact_reference(reference) is False
