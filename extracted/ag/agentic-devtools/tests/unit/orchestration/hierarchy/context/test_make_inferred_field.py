"""Unit tests for inferred context field construction."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import ContextProvenance, make_inferred_field


def test_make_inferred_field_marks_content_non_authoritative() -> None:
    """Inferred content is transformed, retained by hash, and not authoritative."""
    field = make_inferred_field(
        "siblings",
        "peer-1",
        snapshot_ref="sha256:37effc81d805811d59f99c1376b393b25529b7482c39ad866c49791b62dc44bb",
    )
    assert field.name == "siblings"
    assert field.content == "peer-1"
    assert field.provenance is ContextProvenance.INFERRED
    assert field.transformed
