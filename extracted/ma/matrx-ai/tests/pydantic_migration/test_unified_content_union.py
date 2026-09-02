"""The UnifiedContent union must cover everything the deserializer can return.

It did not, and the failure was invisible for the worst possible reason: Python
does not enforce a return annotation, so `reconstruct_content` happily returned
`WorkbookInputContent` — for real stored `input_workbook` blocks — while
declaring a return type that did not include it. Seven of the fourteen classes
in STRUCTURED_INPUT_TYPE_MAP were missing from the union.

Nothing crashed. What broke was every consumer that TRUSTS the union, including
this campaign's own contract-closure walk, which under-counted the engine
contract at 26 dataclasses when the real figure is 33.

That is the lesson worth keeping: the campaign had already established that a
declared type in this package is a hypothesis rather than an input — and then
built a measurement tool that takes declared types as input. A wrong union does
not look like a blind spot; it looks like a complete annotation.

This test reconciles the two definitions against each other instead of trusting
either (PRINCIPLES.md: guards reconcile when they can, and diff TRUTH against
code).
"""

from __future__ import annotations

import typing

from matrx_ai.config import unified_content as uc
from matrx_ai.config.structured_input_config import STRUCTURED_INPUT_TYPE_MAP

UNION = set(typing.get_args(uc.UnifiedContent))


def test_every_structured_input_type_is_in_the_union():
    missing = set(STRUCTURED_INPUT_TYPE_MAP.values()) - UNION
    assert not missing, (
        "reconstruct_content can return these, and the union does not declare them: "
        + ", ".join(sorted(c.__name__ for c in missing))
    )


def test_the_deserializer_returns_a_declared_member_for_every_mapped_type():
    """The reconciliation that actually matters — drive the deserializer with
    each registered discriminator and require the result to be in the union."""
    for wire_type, cls in sorted(STRUCTURED_INPUT_TYPE_MAP.items()):
        got = uc.reconstruct_content({"type": wire_type})
        assert got is not None, wire_type
        assert type(got) in UNION, (
            f"reconstruct_content({wire_type!r}) returned {type(got).__name__}, "
            "which is outside its own declared return type"
        )


def test_workbook_is_the_case_that_exposed_this():
    """2 `input_workbook` blocks are stored in production. Before the fix this
    returned a class outside the declared union; the forcing function stays so
    a future narrowing of the union fails here rather than in a consumer."""
    got = uc.reconstruct_content({"type": "input_workbook", "workbook_ids": [], "editable": True})
    assert type(got).__name__ == "WorkbookInputContent"
    assert type(got) in UNION


def test_the_union_has_no_members_the_map_cannot_produce():
    """The other direction. A union member no deserializer can emit is either
    dead or a missing map entry — both worth knowing, neither silently."""
    from matrx_ai.config.structured_input_config import _StructuredInputBase

    structured_in_union = {c for c in UNION if issubclass(c, _StructuredInputBase)}
    assert structured_in_union == set(STRUCTURED_INPUT_TYPE_MAP.values())
