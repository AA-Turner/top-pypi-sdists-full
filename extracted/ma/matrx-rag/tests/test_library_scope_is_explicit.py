"""A library document's owner is a WORD the caller says, never a missing value.

Until 2026-09-17 ``upsert_library_doc(organization_id=None)`` meant GLOBAL: the
row was written to the system org — which ``iam.system_orgs`` marks
``global_readable`` — and published to the web. So a caller that had simply
LOST its organization (the shape THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT
exists to kill) published a tenant's reference document to every authenticated
user on the platform, with nothing on any screen saying so.

``scope`` now says it out loud, and the two failure directions are refused by
name: a global document may not also name an organization, and an organization
document may not be missing one.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_rag.library as library
from matrx_rag.ingestion import SYSTEM_ORG_ID

TENANT = "7c1f0f4e-2a1a-4f1d-9a7f-5c1f0f4e2a1a"


def _install(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    created: list[dict[str, Any]] = []

    class _LibraryDocs:
        @staticmethod
        def filter(**_kwargs: Any) -> Any:
            class _Q:
                def limit(self, _n: int) -> "_Q":
                    return self

                async def all(self) -> list[Any]:
                    return []

            return _Q()

        @staticmethod
        async def create(**kwargs: Any) -> Any:
            created.append(kwargs)
            return SimpleNamespace(id="11111111-1111-4111-8111-111111111111")

    monkeypatch.setattr(library, "get_db_model", lambda _name: _LibraryDocs)
    return created


async def test_a_global_document_is_owned_by_the_platform_and_is_public(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created = _install(monkeypatch)

    await library.upsert_library_doc(title="MTUS §9792.20", kind="guideline", scope="global")

    assert created[0]["organization_id"] == SYSTEM_ORG_ID
    assert created[0]["published_to_web"] is True


async def test_an_organization_document_keeps_its_tenant_and_stays_internal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created = _install(monkeypatch)

    await library.upsert_library_doc(
        title="Acme return-to-work policy",
        kind="policy",
        scope="organization",
        organization_id=TENANT,
    )

    assert created[0]["organization_id"] == TENANT
    assert created[0]["published_to_web"] is False, (
        "a tenant's own reference document must never be published as platform "
        "content — published_to_web on the global_readable system org is world-readable"
    )


async def test_an_organization_document_with_no_organization_refuses_and_writes_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created = _install(monkeypatch)

    with pytest.raises(ValueError, match="requires the organization"):
        await library.upsert_library_doc(
            title="Acme return-to-work policy", kind="policy", scope="organization"
        )

    assert created == [], "a lost organization must never be promoted to global content"


async def test_a_global_document_may_not_also_name_an_organization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created = _install(monkeypatch)

    with pytest.raises(ValueError, match="cannot also name organization"):
        await library.upsert_library_doc(
            title="MTUS §9792.20",
            kind="guideline",
            scope="global",
            organization_id=TENANT,
        )

    assert created == []


async def test_the_scope_must_be_one_of_the_two_words(monkeypatch: pytest.MonkeyPatch) -> None:
    created = _install(monkeypatch)

    with pytest.raises(ValueError, match="scope must be"):
        await library.upsert_library_doc(
            title="MTUS §9792.20",
            kind="guideline",
            scope="everyone",  # type: ignore[arg-type]
        )

    assert created == []
