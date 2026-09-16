"""Legacy CAS bookkeeping does not change the bound source payload."""

from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.models import _legacy_digest


def test_content_binding(foundation):
    f = foundation()
    assert _legacy_digest(f.state) == _legacy_digest(replace(f.state, revision=100, last_updated_at=f.now))
    assert _legacy_digest(f.state) != _legacy_digest(replace(f.state, inventory_invalidated=False))
