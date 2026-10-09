"""Regression guard for the standalone SEO service's secrets-battery reach."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from matrx_orm import PermissionDeniedError
from matrx_orm.secrets_battery import service as battery_service

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PACKAGE_ROOT / "matrx_seo/db/grants.yaml"


class _CredentialItemQuery:
    def __init__(self, grants: dict[str, object], filters: dict[str, object]) -> None:
        self._grants = grants
        self.filters = filters

    async def values(self, *columns: str) -> list[dict[str, str]]:
        if self._grants.get("users.credential_items") != ["SELECT"]:
            raise PermissionDeniedError(
                original_error=PermissionError("permission denied for table credential_items")
            )
        assert columns == ("id",)
        return [{"id": str(self.filters["id"])}]


class _PermissionAwareCredentialItems:
    grants: dict[str, object]
    queries: list[_CredentialItemQuery]

    @classmethod
    def filter(cls, **filters: object) -> _CredentialItemQuery:
        query = _CredentialItemQuery(cls.grants, filters)
        cls.queries.append(query)
        return query


@pytest.mark.asyncio
async def test_service_grant_manifest_allows_the_real_battery_parent_lifecycle_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without this SELECT, item-bound provider fields fail before decryption."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    _PermissionAwareCredentialItems.grants = manifest["table_grants"]
    _PermissionAwareCredentialItems.queries = []
    monkeypatch.setattr(battery_service, "CredentialItem", _PermissionAwareCredentialItems)

    assert await battery_service._item_parent_is_active({"credential_item_id": "item-42"})
    assert _PermissionAwareCredentialItems.queries[0].filters == {
        "id": "item-42",
        "deleted_at__isnull": True,
        "status": "active",
    }

    del manifest["table_grants"]["users.credential_items"]
    _PermissionAwareCredentialItems.grants = manifest["table_grants"]

    with pytest.raises(PermissionDeniedError, match="credential_items"):
        await battery_service._item_parent_is_active({"credential_item_id": "item-42"})
