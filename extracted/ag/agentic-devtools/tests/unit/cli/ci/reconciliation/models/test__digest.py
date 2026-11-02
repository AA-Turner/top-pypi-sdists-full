"""Canonical hashing retains nested content and ignores dictionary order."""

from datetime import UTC, datetime
from types import MappingProxyType

from agentic_devtools.cli.ci.reconciliation.models import _digest


def test_nested_canonical_values(foundation):
    f = foundation()
    now = datetime(2026, 1, 1, tzinfo=UTC)
    assert _digest({"a": [now], "b": (1, 2)}) == _digest({"b": [1, 2], "a": [now.isoformat()]})
    assert _digest(MappingProxyType({"x": 1})) == _digest({"x": 1})
    assert _digest(f.state) != _digest({"repo": f.state.repo})
    assert _digest({"a": 1}) != _digest({"a": 2})
