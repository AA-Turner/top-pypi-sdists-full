"""FORCING TEST — a kind definition and a kind instance carry an organization.

THE LAW (``common-docs/policies/context-is-carried-never-rebuilt.md``, rule 4):
below the boundary the organization is READ off the carried context, and an
absent one is a REFUSAL — never a row the database's ``_stamp_org_default``
backstop files in the creator's personal workspace.

Both tools used to write the key only ``if org_id:``. The create then ran
anyway, so a tool call that had lost its organization minted an org's kind (or
a person's instance) into whoever happened to own the agent — where the org's
own admins are refused the edit (the 2026-07-25 incident) and every later
org-scoped read misses the row.

The REAL tool code runs; only the ORM model it writes through is faked, and the
fake stops the call the moment it can report what it was handed.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

USER = "44444444-4444-4444-8444-444444444444"
ORG = "55555555-5555-4555-8555-555555555555"


class _Stop(Exception):
    """Raised by the fake model once it has captured the payload."""


# ---------------------------------------------------------------------------
# kind_create — the kind DEFINITION row
# ---------------------------------------------------------------------------


async def _create_kind(monkeypatch, org_id: str | None) -> tuple[dict[str, Any], Exception]:
    from matrx_ai.tools.implementations import kind_authoring

    seen: dict[str, Any] = {}

    class _KindDefinition:
        @classmethod
        async def create_item(cls, **kwargs: Any) -> Any:
            seen.update(kwargs)
            raise _Stop

    monkeypatch.setattr(kind_authoring, "get_db_model", lambda _name: _KindDefinition)
    monkeypatch.setattr(kind_authoring, "fields_from_json_schema", lambda _s: [])
    monkeypatch.setattr(kind_authoring, "schema_fingerprint", lambda _s: "fp")

    async def _no_duplicate(_fingerprint: str) -> Any:
        return None

    monkeypatch.setattr(kind_authoring, "_duplicate_shape_refusal", _no_duplicate)

    with pytest.raises(Exception) as exc:  # noqa: PT011 — either _Stop or the refusal
        await kind_authoring._create_single_kind(
            slug="demo_kind",
            label="Demo",
            wire_schema={"type": "object"},
            block_schema={"type": "object"},
            canonical_marked={"__kind": "demo_kind"},
            user_id=USER,
            org_id=org_id,
        )
    return seen, exc.value


@pytest.mark.asyncio
async def test_a_kind_definition_carries_the_calls_organization(monkeypatch):
    seen, raised = await _create_kind(monkeypatch, ORG)
    assert isinstance(raised, _Stop)
    assert seen["organization_id"] == ORG


@pytest.mark.asyncio
async def test_a_kind_definition_refuses_without_an_organization(monkeypatch):
    seen, raised = await _create_kind(monkeypatch, None)
    assert isinstance(raised, ValueError)
    assert "carries no organization" in str(raised)
    assert seen == {}, "nothing may reach the database without a tenant"


# ---------------------------------------------------------------------------
# instance_create — the kind INSTANCE row (user data)
# ---------------------------------------------------------------------------


async def _create_instance(monkeypatch, org_id: str | None) -> tuple[dict[str, Any], Any]:
    from matrx_ai.tools.implementations import kind_instance

    seen: dict[str, Any] = {}

    kd = SimpleNamespace(
        id="kind-1",
        kind="demo_kind",
        version=1,
        emitted_json_schema=None,
        title_key=None,
    )

    class _KindInstance:
        @classmethod
        async def create_item(cls, **kwargs: Any) -> Any:
            seen.update(kwargs)
            raise _Stop

    async def _resolve_kind(_ref: str, _ctx: Any) -> tuple[Any, Any]:
        return kd, None

    async def _ensure_can_view(_kd: Any, _ctx: Any) -> Any:
        return None

    monkeypatch.setattr(kind_instance, "resolve_kind", _resolve_kind)
    monkeypatch.setattr(kind_instance, "ensure_can_view_kind", _ensure_can_view)
    monkeypatch.setattr(kind_instance, "ctx_user_id", lambda _ctx: USER)
    monkeypatch.setattr(kind_instance, "ctx_org_id", lambda _ctx: org_id)
    monkeypatch.setattr(kind_instance, "kind_title_key", lambda _kd: None)
    monkeypatch.setattr(kind_instance, "get_db_model", lambda _name: _KindInstance)

    result = await kind_instance.instance_create(
        {"kind": "demo_kind", "data": {"__kind": "demo_kind", "value": 1}},
        SimpleNamespace(),
    )
    return seen, result


@pytest.mark.asyncio
async def test_an_instance_carries_the_callers_organization(monkeypatch):
    seen, _result = await _create_instance(monkeypatch, ORG)
    assert seen["organization_id"] == ORG


@pytest.mark.asyncio
async def test_an_instance_refuses_without_an_organization(monkeypatch):
    seen, result = await _create_instance(monkeypatch, None)
    assert seen == {}, "nothing may reach the database without a tenant"
    assert not result.success
    assert "carries no organization" in str(result)
