"""Test Reference dataclass (FR-001, FR-004)."""

import pytest

from agentic_devtools.cli.speckit.pass_g.models import Reference, ReferenceKind


def test_reference_fields():
    ref = Reference(
        text="my_function",
        kind=ReferenceKind.FUNCTION_NAME,
        plan_location="L42",
        context_sentence="Call `my_function` to process data",
    )
    assert ref.text == "my_function"
    assert ref.kind == ReferenceKind.FUNCTION_NAME
    assert ref.plan_location == "L42"
    assert ref.context_sentence == "Call `my_function` to process data"


def test_reference_rejects_negative_occurrence_index() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Reference(
            text="my_function",
            kind=ReferenceKind.FUNCTION_NAME,
            plan_location="L42",
            context_sentence="Call `my_function` to process data",
            occurrence_index=-1,
        )


def test_reference_rejects_non_integer_occurrence_index() -> None:
    with pytest.raises(ValueError, match="non-negative integer"):
        Reference(
            text="my_function",
            kind=ReferenceKind.FUNCTION_NAME,
            plan_location="L42",
            context_sentence="Call `my_function` to process data",
            occurrence_index=True,
        )
