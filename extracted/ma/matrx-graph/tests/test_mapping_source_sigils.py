"""An edge mapping source that is an unsupported '$' token is REFUSED.

The measured failure (workflow ``129a4ec1-c4b3-4fdb-bdbe-0ae3b6162147``, run
``12c153a9``, 2026-09-12): a Masterwork the Conductor authored for a
non-technical user wired ``intake`` (``io.user_input``) into ``canon``
(``text.template``) with ``{"variables": "$payload"}``. Every author-time
check passed — ``workflow_plan check`` reported "no breaks" — and the user's
FIRST real run died at step 0 with
``EdgeRoutingError: ... KeyError: '$payload'``.

Why every check was quiet: the only mapping-source check compared the source
key against the upstream's DECLARED output schema, and ``io.user_input`` is
``dynamic_output`` — its keys come from ``config.fields``, so no key can be
ruled out and the check correctly stayed silent. The thing nobody encoded is
that ``$``-prefixed sources are a CLOSED vocabulary (``$FULL_PAYLOAD`` and
nothing else): no node emits a ``$``-prefixed output key, so an unknown sigil
is dead REGARDLESS of schema, dynamic or not.

These tests pin that: refused at validation (so it can never be saved or
compiled), refused at routing with a message that names the alias, and the
supported alias plus ordinary keys and dot-paths still pass untouched.
Against the pre-fix engine the first three fail — the definition validated
clean and only the run found it.
"""

from __future__ import annotations

import pytest

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.mapping_sources import WHOLE_PAYLOAD, unknown_sigil
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _the_measured_definition(source: str) -> dict:
    """The live shape, joint for joint: a dynamic-output form feeding a
    template whose ``variables`` wants the whole upstream payload."""
    return {
        "version": "1",
        "nodes": [
            {
                "id": "intake",
                "type": "io.user_input",
                "position": {"x": 0, "y": 0},
                "data": {
                    "label": "Tell Montessori what is happening",
                    "config": {
                        "fields": [
                            {
                                "key": "situation",
                                "type": "long_text",
                                "label": "What is happening?",
                                "required": True,
                            },
                            {
                                "key": "child_age",
                                "type": "text",
                                "label": "How old is the child?",
                                "required": True,
                            },
                        ]
                    },
                },
            },
            {
                "id": "canon",
                "type": "text.template",
                "position": {"x": 0, "y": 220},
                "data": {
                    "label": "The 115 approved rules",
                    "input": {"template": "THE APPROVED CANON"},
                    "config": {},
                },
            },
        ],
        "edges": [
            {
                "id": "e_intake_canon",
                "source": "intake",
                "target": "canon",
                "data": {"kind": "data", "mappings": {"variables": source}},
            }
        ],
    }


def test_the_measured_definition_is_refused_at_validation() -> None:
    """`$payload` on a DYNAMIC-output upstream — the exact live defect."""
    result = validate_definition(_the_measured_definition("$payload"), registry=_registry())
    assert not result.valid, "the definition that killed run 12c153a9 validated clean"
    offending = [
        i
        for i in result.issues
        if i.severity == "error" and i.edge_id == "e_intake_canon"
    ]
    assert offending, f"no error named the edge; got {[i.message for i in result.issues]}"
    message = offending[0].message
    # It must name the edge, the reference, and the token the author meant —
    # a refusal the author cannot act on is a different defect.
    assert "e_intake_canon" in message
    assert "$payload" in message
    assert WHOLE_PAYLOAD in message


@pytest.mark.parametrize("token", ["$payload", "$output", "$all", "$var", "$FULLPAYLOAD", "$"])
def test_every_invented_whole_output_token_is_refused(token: str) -> None:
    result = validate_definition(_the_measured_definition(token), registry=_registry())
    assert not result.valid, f"{token!r} was accepted as a mapping source"


def test_the_supported_alias_and_ordinary_sources_still_pass() -> None:
    for source in (WHOLE_PAYLOAD, "situation", "result.canon", "items.0.id"):
        result = validate_definition(_the_measured_definition(source), registry=_registry())
        assert result.valid, (
            f"{source!r} is a legitimate mapping source but was refused: "
            f"{[i.message for i in result.issues]}"
        )


def test_unknown_sigil_is_schema_free() -> None:
    """The predicate itself: only the token decides, never a schema."""
    assert unknown_sigil("$payload") == "$payload"
    assert unknown_sigil(WHOLE_PAYLOAD) is None
    assert unknown_sigil("result.canon") is None
    assert unknown_sigil("payload") is None
    assert unknown_sigil(None) is None
