"""Tests for ``_is_negated_artifact_reference()``."""

from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind
from agentic_devtools.cli.speckit.verify_artifacts import _is_negated_artifact_reference


class TestIsNegatedArtifactReference:
    """Explicitly negative artifact statements should not count as promises."""

    def test_detects_no_separate_artifact_statement(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="No separate `research.md` artifact is committed for this plan.",
        )

        assert _is_negated_artifact_reference(reference) is True

    def test_detects_negated_artifact_list_entry(self) -> None:
        reference = Reference(
            text="quickstart.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="No separate `research.md` or `quickstart.md` artifact is committed for this plan.",
        )

        assert _is_negated_artifact_reference(reference) is True

    def test_returns_false_for_positive_artifact_reference(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="See `research.md` for the analysis details.",
        )

        assert _is_negated_artifact_reference(reference) is False

    def test_returns_false_when_negated_statement_targets_a_different_artifact(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence=(
                "No separate `quickstart.md` artifact is committed for this plan; "
                "see `research.md` for the inlined notes."
            ),
        )

        assert _is_negated_artifact_reference(reference) is False

    def test_returns_false_when_context_sentence_is_empty(self) -> None:
        reference = Reference(
            text="research.md",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="",
        )

        assert _is_negated_artifact_reference(reference) is False
