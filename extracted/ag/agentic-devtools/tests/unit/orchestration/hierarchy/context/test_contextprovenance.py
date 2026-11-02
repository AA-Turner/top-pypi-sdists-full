"""Unit tests for ContextProvenance and verified/unavailable/inferred field construction."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import (
    ContextProvenance,
)


def test_context_provenance_values() -> None:
    assert {p.value for p in ContextProvenance} == {"verified", "unavailable", "inferred"}


def test_verified_provenance_is_authoritative() -> None:
    assert ContextProvenance.VERIFIED.is_authoritative
    assert not ContextProvenance.UNAVAILABLE.is_authoritative
    assert not ContextProvenance.INFERRED.is_authoritative
