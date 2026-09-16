"""Historical ledger digest changes when retained authority changes."""

from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.models import _history_digest


def test_history_not_revision(foundation):
    f = foundation()
    assert _history_digest(f.state) == _history_digest(replace(f.state, revision=11))
    assert _history_digest(f.state) != _history_digest(replace(f.state, attempts={}))
