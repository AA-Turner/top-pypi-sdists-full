"""A refused INPUT told in prose is INVALID/MISSING_INPUT with its field, never NOT_AUTHORIZED.

The person's own value rides in the reason ("forbidden", "permission", "403"); the prose ladder read
those as a permission refusal and the run screen said "belongs to a different account" (2026-11-14).
"""
import pytest

from matrx_graph.failure import Cause, failure_from_text


@pytest.mark.parametrize(
    ("text", "field", "cause"),
    [
        ("Input validation failed for 'audience': 'forbidden' is not one of ['kids']", "audience", Cause.INVALID_INPUT),
        ("Input 'rule_text' is invalid: permission to publish must be yes or no", "rule_text", Cause.INVALID_INPUT),
        ("Input 'topic' is required", "topic", Cause.MISSING_INPUT),
    ],
)
def test_named_input_refusal_keeps_field_and_cause(text, field, cause):
    failure = failure_from_text(text)
    assert failure.cause == cause
    assert failure.field == field


def test_a_real_permission_refusal_is_still_not_authorized():
    assert failure_from_text("permission denied for table x").cause == Cause.NOT_AUTHORIZED
