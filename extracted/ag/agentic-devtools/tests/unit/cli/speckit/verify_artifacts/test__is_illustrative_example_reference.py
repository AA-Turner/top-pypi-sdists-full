"""Tests for ``_is_illustrative_example_reference()``."""

from agentic_devtools.cli.speckit.verify_artifacts import (
    Reference,
    ReferenceKind,
    _is_illustrative_example_reference,
)


class TestIsIllustrativeExampleReference:
    """Detecting when references are illustrative examples."""

    def test_returns_false_for_empty_context_sentence(self) -> None:
        reference = Reference(text="test_a.py", kind=ReferenceKind.FILE_PATH, plan_location="L1", context_sentence="")

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_false_when_reference_normalizes_to_empty_text(self) -> None:
        reference = Reference(text="?", kind=ReferenceKind.FILE_PATH, plan_location="L1", context_sentence="(e.g. ?)")

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_false_when_reference_text_is_absent_from_sentence(self) -> None:
        reference = Reference(
            text="test_missing.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Create files (e.g. `test_a.py`).",
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_true_for_e_g_prefix_before_reference(self) -> None:
        reference = Reference(
            text="test_a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Create files (e.g. `test_a.py`, `test_b.py`).",
        )

        assert _is_illustrative_example_reference(reference) is True

    def test_returns_true_for_plain_reference_after_e_g_prefix(self) -> None:
        reference = Reference(
            text="test_a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Create files (e.g. test_a.py) in the package.",
        )

        assert _is_illustrative_example_reference(reference) is True

    def test_returns_false_for_reference_after_example_clause(self) -> None:
        reference = Reference(
            text="required.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect `old.py`; update `required.py`.",
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_false_for_for_example_generation_phrase(self) -> None:
        reference = Reference(
            text="required.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Use for example generation, then update `required.py`.",
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_false_for_for_example_prose_without_file_example(self) -> None:
        reference = Reference(
            text="auth.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Token docs include prose, for example the bearer token stored in auth.py.",
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_second_reference_in_parenthetical_list_is_illustrative(self) -> None:
        reference = Reference(
            text="test_b.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Create files (e.g. `test_a.py` and `test_b.py`) in the package.",
        )

        assert _is_illustrative_example_reference(reference) is True

    def test_second_plain_reference_in_parenthetical_list_is_illustrative(self) -> None:
        reference = Reference(
            text="test_b.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="Create files (e.g. test_a.py and test_b.py) in the package.",
        )

        assert _is_illustrative_example_reference(reference) is True

    def test_second_plain_reference_in_non_parenthetical_list_is_illustrative(self) -> None:
        # Regression: "For example, inspect a.py and b.py." — b.py loses its
        # illustrative marker when "and" splits the context at the clause level.
        reference = Reference(
            text="b.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect a.py and b.py.",
        )

        assert _is_illustrative_example_reference(reference) is True

    def test_third_plain_reference_in_non_parenthetical_list_is_illustrative(self) -> None:
        reference = Reference(
            text="c.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect a.py and b.py and c.py.",
        )

        assert _is_illustrative_example_reference(reference) is True

    def test_and_followed_by_verb_is_not_a_list_separator(self) -> None:
        # "and update" is an action boundary, not a list separator.
        reference = Reference(
            text="b.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect a.py and update b.py.",
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_same_path_second_occurrence_after_action_verb_is_not_illustrative(self) -> None:
        # Regression: when the same path appears twice in an and-separated
        # illustrative sentence ("For example, inspect a.py and update a.py."),
        # _reference_context_for_occurrence returns the full sentence for both
        # occurrences because "and" inside an illustrative clause is a list
        # separator.  Without occurrence_index, find() always picks the first
        # position and both get classified as illustrative — suppressing the
        # required "update a.py" action.
        first = Reference(
            text="a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect a.py and update a.py.",
            occurrence_index=0,
        )
        second = Reference(
            text="a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect a.py and update a.py.",
            occurrence_index=1,
        )

        assert _is_illustrative_example_reference(first) is True
        assert _is_illustrative_example_reference(second) is False

    def test_suffix_collision_inside_other_filename_is_not_selected_as_reference_start(self) -> None:
        # Regression: "a.py" should not match the suffix inside "data.py".
        reference = Reference(
            text="a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect data.py and update a.py.",
            occurrence_index=0,
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_false_when_occurrence_index_exceeds_token_bounded_match_count(self) -> None:
        # A Reference can be constructed with an occurrence_index that is
        # higher than the number of token-bounded matches in the sentence
        # (e.g. if the path only appears once but index 1 is requested).
        # The function should return False rather than raising an IndexError.
        reference = Reference(
            text="a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect a.py.",
            occurrence_index=1,
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_false_when_reference_is_in_a_new_sentence_after_for_example(
        self,
    ) -> None:
        """A sentence boundary breaks the illustrative scope from a prior sentence."""
        reference = Reference(
            text="b.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect `a.py`. Update `b.py` with the result.",
            occurrence_index=0,
        )

        assert _is_illustrative_example_reference(reference) is False

    def test_returns_true_when_reference_is_in_same_sentence_as_for_example(
        self,
    ) -> None:
        """A reference in the same sentence as the for-example marker is illustrative."""
        reference = Reference(
            text="a.py",
            kind=ReferenceKind.FILE_PATH,
            plan_location="L1",
            context_sentence="For example, inspect `a.py`. Update `b.py` with the result.",
            occurrence_index=0,
        )

        assert _is_illustrative_example_reference(reference) is True
