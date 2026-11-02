"""Tests for ``_reference_context_for_occurrence()``."""

from agentic_devtools.cli.speckit.verify_artifacts import _reference_context_for_occurrence


def test_returns_original_sentence_when_occurrence_is_absent() -> None:
    sentence = "Update `required.py`."

    assert _reference_context_for_occurrence(sentence, "missing.py", 0) == sentence


def test_prefers_backtick_occurrence_over_earlier_plain_text_token() -> None:
    sentence = "For example, label missing.py; then update `missing.py`."

    assert _reference_context_for_occurrence(sentence, "missing.py", 0) == "update `missing.py`."


def test_falls_back_to_non_backtick_occurrences_after_backtick_matches() -> None:
    sentence = "For example, label missing.py; then update `missing.py`; and move missing.py."

    assert _reference_context_for_occurrence(sentence, "missing.py", 1) == "For example, label missing.py"
    assert _reference_context_for_occurrence(sentence, "missing.py", 2) == "move missing.py."
    assert _reference_context_for_occurrence(sentence, "missing.py", 3) == sentence


def test_ignores_clause_delimiters_inside_the_target_path() -> None:
    sentence = "Create docs/and/file.py and update docs/missing.py."

    assert _reference_context_for_occurrence(sentence, "docs/and/file.py", 0) == "Create docs/and/file.py"


def test_conjunction_inside_parenthetical_is_not_a_clause_boundary() -> None:
    # "and" inside "(e.g. `a.py` and `b.py`)" is a list separator, not a
    # clause boundary; both references must retain the full parenthetical
    # as their context so that the illustrative-example guard can fire.
    sentence = "Create files (e.g. `a.py` and `b.py`) in the package."

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == sentence
    assert _reference_context_for_occurrence(sentence, "b.py", 0) == sentence


def test_matches_plain_path_occurrence_as_a_complete_token() -> None:
    sentence = "For example, inspect data.py; then update a.py."

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == "update a.py."


def test_matches_plain_path_occurrence_at_sentence_start() -> None:
    sentence = "a.py and b.py"

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == "a.py"


def test_returns_original_sentence_when_plain_match_is_followed_by_alphanumeric_suffix() -> None:
    sentence = "Inspect a.pyx before release."

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == sentence


def test_returns_original_sentence_when_plain_match_is_followed_by_dotted_suffix() -> None:
    sentence = "Inspect a.py.bak before release."

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == sentence


def test_matches_plain_path_occurrence_at_sentence_end() -> None:
    sentence = "Update a.py"

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == sentence


def test_accepts_plain_path_before_sentence_period_followed_by_non_token_punctuation() -> None:
    sentence = "Update a.py.)"

    assert _reference_context_for_occurrence(sentence, "a.py", 0) == sentence


def test_non_parenthetical_illustrative_list_second_item_retains_full_clause() -> None:
    # "and" in a plain (non-parenthetical) "for example" list must not split
    # the context of the second item.  "b.py" must retain the full sentence so
    # that _is_illustrative_example_reference can detect the "For example" marker.
    sentence = "For example, inspect a.py and b.py."

    assert _reference_context_for_occurrence(sentence, "b.py", 0) == sentence


def test_non_parenthetical_illustrative_list_three_items_retain_full_clause() -> None:
    # c.py (third item) must keep the full sentence so it includes the marker.
    # b.py (second item) is bounded on the right by the "and" before c.py, but
    # the context still includes the "For example" prefix, which is all that is
    # needed for illustrative-example detection.
    sentence = "For example, inspect a.py and b.py and c.py."

    assert _reference_context_for_occurrence(sentence, "b.py", 0) == "For example, inspect a.py and b.py"
    assert _reference_context_for_occurrence(sentence, "c.py", 0) == sentence


def test_and_after_semicolon_still_splits_context_outside_illustrative_clause() -> None:
    # A semicolon terminates the illustrative clause, so "b.py" must NOT
    # be treated as part of a "for example" list.
    sentence = "For example, inspect a.py; update b.py."

    assert _reference_context_for_occurrence(sentence, "b.py", 0) == "update b.py."


def test_plain_and_without_illustrative_marker_still_splits_context() -> None:
    # Without a "for example" marker, "and" should still be a clause boundary
    # for the second reference.
    sentence = "inspect a.py and b.py."

    assert _reference_context_for_occurrence(sentence, "b.py", 0) == "b.py."
