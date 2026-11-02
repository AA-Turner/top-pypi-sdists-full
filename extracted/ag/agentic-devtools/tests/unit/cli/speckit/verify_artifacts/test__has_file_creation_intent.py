"""Tests for ``_has_file_creation_intent()`` in ``verify_artifacts``."""

import pytest

from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind
from agentic_devtools.cli.speckit.verify_artifacts import _has_file_creation_intent


def _make_ref(context: str, text: str = "pkg/handler.py", occurrence_index: int = 0) -> Reference:
    return Reference(
        text=text,
        kind=ReferenceKind.FILE_PATH,
        context_sentence=context,
        plan_location="plan.md:1",
        occurrence_index=occurrence_index,
    )


class TestHasFileCreationIntentStrict:
    """Gate uses a strict verb set — only unambiguous file-creation verbs qualify."""

    @pytest.mark.parametrize(
        "verb",
        [
            "create",
            "Introduce",
            "Define",
            "Scaffold",
            "Generate",
            "Set up",
        ],
    )
    def test_returns_true_for_unambiguous_creation_verbs(self, verb: str) -> None:
        ref = _make_ref(f"{verb} `pkg/handler.py` for the webhook.")
        assert _has_file_creation_intent(ref) is True

    @pytest.mark.parametrize(
        "verb",
        [
            "add",
            "implement",
            "write",
            "build",
            "register",
            "wire up",
        ],
    )
    def test_returns_false_for_ambiguous_task_verbs(self, verb: str) -> None:
        """Ambiguous verbs describe work done in a file, not the file's creation."""
        ref = _make_ref(f"{verb} FR-001 in `pkg/handler.py`.")
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_for_context_without_any_marker(self) -> None:
        ref = _make_ref("Update `pkg/handler.py` to fix the bug.")
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_reference_normalizes_to_empty_text(self) -> None:
        ref = _make_ref("Create `pkg/handler.py`.", text="#L1")
        assert _has_file_creation_intent(ref) is False

    def test_word_boundary_prevents_substring_match(self) -> None:
        """'recreate' must not match 'create' at a non-word boundary."""
        ref = _make_ref("Recreate `pkg/handler.py` from scratch.")
        assert _has_file_creation_intent(ref) is False

    def test_case_insensitive_match(self) -> None:
        ref = _make_ref("SCAFFOLD `pkg/handler.py` via the generator.")
        assert _has_file_creation_intent(ref) is True

    def test_does_not_treat_creation_of_other_path_as_creation_intent(self) -> None:
        ref = _make_ref(
            "Create `pkg/new.py` and update `pkg/missing.py`.",
            text="pkg/missing.py",
        )
        assert _has_file_creation_intent(ref) is False

    def test_detects_creation_intent_for_first_clause_reference(self) -> None:
        ref = _make_ref(
            "Create `pkg/new.py` and update `pkg/missing.py`.",
            text="pkg/new.py",
        )
        assert _has_file_creation_intent(ref) is True

    def test_returns_false_for_later_occurrence_of_same_path(self) -> None:
        ref = _make_ref(
            "For example, create `pkg/missing.py` and update `pkg/missing.py`.",
            text="pkg/missing.py",
            occurrence_index=1,
        )
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_reference_is_absent_from_context(self) -> None:
        ref = _make_ref("Create `pkg/new.py` now.", text="pkg/missing.py")
        assert _has_file_creation_intent(ref) is False

    def test_ignores_boundary_keyword_inside_reference_text(self) -> None:
        ref = _make_ref("Update `and/file.py` now.", text="and/file.py")
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_creation_verb_does_not_govern_the_reference(self) -> None:
        ref = _make_ref("Update `pkg/typo.py` to generate a coverage report.", text="pkg/typo.py")
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_creation_verb_governs_different_object_via_relative_clause(
        self,
    ) -> None:
        """'create' governs 'service', not the file — relative clause signals this."""
        ref = _make_ref(
            "Create a service that updates `pkg/missing.py`.",
            text="pkg/missing.py",
        )
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_which_clause_separates_verb_from_reference(self) -> None:
        ref = _make_ref(
            "Define a module which exposes `pkg/api.py`.",
            text="pkg/api.py",
        )
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_verb_governs_a_noun_phrase_without_relative_pronoun(
        self,
    ) -> None:
        """'create' governs 'service'; the path only names where it lives."""
        ref = _make_ref("Create a service in `pkg/misspelled.py`.", text="pkg/misspelled.py")
        assert _has_file_creation_intent(ref) is False

    def test_returns_false_when_path_is_connected_with_non_naming_preposition(self) -> None:
        ref = _make_ref("Create tests with `pkg/existing.py`.", text="pkg/existing.py")
        assert _has_file_creation_intent(ref) is False

    @pytest.mark.parametrize(
        "context",
        [
            "Create a new file at `pkg/api.py`.",
            "Create the file `pkg/api.py`.",
            "Scaffold an empty module named `pkg/api.py`.",
            "Generate a new script called `pkg/api.py`.",
        ],
    )
    def test_returns_true_when_reference_is_the_created_object(self, context: str) -> None:
        ref = _make_ref(context, text="pkg/api.py")
        assert _has_file_creation_intent(ref) is True

    def test_second_occurrence_in_new_sentence_not_treated_as_creation(self) -> None:
        """Sentence boundary isolates creation verb from the second occurrence."""
        context = "Create `pkg/handler.py`. Update `pkg/handler.py` with the new method."
        ref = _make_ref(context, text="pkg/handler.py", occurrence_index=1)
        assert _has_file_creation_intent(ref) is False

    def test_first_occurrence_in_creation_sentence_still_detected(self) -> None:
        """First occurrence is still in the creation clause after splitting."""
        context = "Create `pkg/handler.py`. Update `pkg/handler.py` with the new method."
        ref = _make_ref(context, text="pkg/handler.py", occurrence_index=0)
        assert _has_file_creation_intent(ref) is True
