"""Evidence references cannot cross kind or PR ownership."""

import pytest

from agentic_devtools.cli.ci.reconciliation.models import _evidence_ref


def test_typed_reference(foundation):
    f = foundation()
    identity = f.state.pr_envelopes[42].observation_id
    assert _evidence_ref(f.state, identity, 42, {"observation"}) == f.state.evidence[identity]
    with pytest.raises(ValueError, match="missing evidence"):
        _evidence_ref(f.state, None, 42, {"observation"})
    with pytest.raises(ValueError, match="foreign or wrong-kind"):
        _evidence_ref(f.state, identity, 43, {"observation"})
