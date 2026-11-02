"""The host-injected `reference` resolution seam — standalone (no matrx-orm, no host)."""

from __future__ import annotations

import asyncio

import pytest
from matrx_graph import (
    configure_reference_resolver,
    is_reference_envelope,
    is_reference_resolver_configured,
    resolve_references,
)


def _run(coro):
    return asyncio.run(coro)


def _ref(type_: str = "table", **ids) -> dict:
    return {"matrx_version": 1, "kind": "reference", "type": type_, "items": [ids]}


@pytest.fixture(autouse=True)
def _clear_resolver():
    configure_reference_resolver(None)
    yield
    configure_reference_resolver(None)


def test_detector_only_matches_reference_envelopes():
    assert is_reference_envelope(_ref(table_id="T"))
    assert not is_reference_envelope({"matrx_version": 1, "kind": "output_directive"})
    assert not is_reference_envelope({"kind": "reference"})  # no sentinel
    assert not is_reference_envelope("just text")


def test_no_resolver_is_passthrough():
    assert not is_reference_resolver_configured()
    env = _ref(table_id="T")
    payload = {"a": env, "b": [env, 1]}
    assert _run(resolve_references(payload, user_id="u")) == payload  # unchanged


def test_resolver_replaces_envelope_with_text():
    async def _resolve(obj, *, user_id):
        assert user_id == "owner"
        return f"LIVE[{obj['type']}/{obj['items'][0].get('table_id')}]"

    configure_reference_resolver(_resolve)
    payload = {"rows": [_ref(table_id="T1"), {"nested": _ref(table_id="T2")}], "n": 5}
    out = _run(resolve_references(payload, user_id="owner"))
    assert out == {
        "rows": ["LIVE[table/T1]", {"nested": "LIVE[table/T2]"}],
        "n": 5,
    }


def test_unresolvable_envelope_is_left_unchanged():
    async def _resolve(obj, *, user_id):
        return None  # not owned / unknown — fail open to the pointer

    configure_reference_resolver(_resolve)
    env = _ref(table_id="X")
    assert _run(resolve_references({"v": env}, user_id="intruder")) == {"v": env}


def test_resolver_exception_is_swallowed_and_pointer_kept():
    async def _resolve(obj, *, user_id):
        raise RuntimeError("db down")

    configure_reference_resolver(_resolve)
    env = _ref(table_id="X")
    assert _run(resolve_references(env, user_id="u")) == env


def test_payload_without_sentinel_skips_walk():
    # A resolver that would explode if called proves the fast-path never recurses.
    async def _boom(obj, *, user_id):
        raise AssertionError("resolver must not be called without a sentinel")

    configure_reference_resolver(_boom)
    payload = {"a": 1, "b": ["x", {"c": 2}]}
    assert _run(resolve_references(payload, user_id="u")) == payload
