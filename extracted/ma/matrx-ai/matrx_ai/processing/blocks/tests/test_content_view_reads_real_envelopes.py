"""THE §6 CONTENT CHANNEL MUST NAME WHAT THE PRODUCER ACTUALLY STAMPED.

`_envelope_value` read `envelope["kind"]`. The envelope `envelope_for_block`
builds puts the kind on `envelope["root"]["kind"]`, so that read was ALWAYS
None: every stamped, schema-validated block an agent ever produced — was folded into markdown prose and
reached the reader as raw JSON (Arman's run a268ba41, 2026-08-22).

Every existing test in `test_content_view.py` passed throughout, because they
all build their `__ir` by hand. This one refuses to: the envelope under test
comes from the REAL producer, so the reader is pinned to the shape actually
shipped and the two cannot drift apart again.
"""

from __future__ import annotations

import pytest

from matrx_ai.processing.blocks import envelope as envelope_module
from matrx_ai.processing.blocks.content_view import content_from_text
from matrx_ai.processing.blocks.stream_processor import process_complete_to_blocks

# LEGACY-5: the pre-kind quiz root key no longer types a block; the reader is pinned
# with a family the server engine still stamps (```mermaid -> mermaid_diagram).
ANSWER = "Here is your diagram.\n\n```mermaid\ngraph TD\n    A[Light] --> B[Glucose]\n```\n"

# The kind's registered schema. Injected into the sync snapshot through the
# seam the module documents for exactly this ("sync context (tests) — caller
# injects the snapshot"), so the test needs no database while every other
# link — parser, adapter, partition, validation, assembly, reader — is the
# production implementation.
MERMAID_SCHEMA = {
    "type": "object",
    "properties": {"code": {"type": "string"}},
    "required": ["code"],
}


@pytest.fixture
def warm_catalog():
    envelope_module._schema_snapshot["mermaid_diagram"] = MERMAID_SCHEMA
    yield
    envelope_module.reset_kind_catalog_snapshot()


def test_the_producer_really_does_stamp_this_block(warm_catalog):
    """Guard on the guard: if nothing stamps, the test below proves nothing."""
    stamped = [
        b for b in process_complete_to_blocks(ANSWER)
        if (b.get("metadata") or {}).get("__ir")
    ]
    assert stamped, "no block was stamped — this suite would pass vacuously"
    envelope = stamped[0]["metadata"]["__ir"]
    assert envelope["root"]["kind"] == "mermaid_diagram", (
        "the kind moved off `root` — every reader of this envelope must move with it"
    )


def test_a_stamped_block_reaches_content_as_its_KIND_not_as_prose(warm_catalog):
    content = content_from_text(ANSWER)
    kinds = [instance["__kind"] for instance in content]
    assert "mermaid_diagram" in kinds, (
        "the validated diagram was folded into prose — the reader gets raw "
        f"source where a diagram component belongs (got {kinds})"
    )
    diagram = next(i for i in content if i["__kind"] == "mermaid_diagram")
    assert "A[Light]" in diagram["code"]
    # …and the prose around it is still its own instance, in order.
    assert kinds == ["markdown", "mermaid_diagram"]


def test_an_unstamped_block_still_folds_to_prose():
    """The fallback is unchanged: no envelope, no name, no invention."""
    kinds = [i["__kind"] for i in content_from_text(ANSWER)]
    assert kinds == ["markdown"]
