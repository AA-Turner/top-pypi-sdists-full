from __future__ import annotations

import pytest
from matrx_rag import sources


@pytest.mark.asyncio
async def test_org_grant_lookup_requires_active_organization_membership(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    membership_filters: list[dict[str, object]] = []

    class _PermissionQuery:
        def filter(self, *args: object, **kwargs: object) -> _PermissionQuery:
            return self

        async def exists(self) -> bool:
            return False

    class _Permissions:
        @classmethod
        def filter(cls, *args: object, **kwargs: object) -> _PermissionQuery:
            return _PermissionQuery()

    class _MembershipQuery:
        async def values_list(self, field: str, *, flat: bool) -> list[str]:
            assert field == "organization_id"
            assert flat is True
            return []

    class _Memberships:
        @classmethod
        def filter(cls, **kwargs: object) -> _MembershipQuery:
            membership_filters.append(kwargs)
            return _MembershipQuery()

    monkeypatch.setattr(
        sources,
        "get_db_model",
        lambda name: _Permissions if name == "Permissions" else _Memberships,
    )

    assert (
        await sources._has_active_grant(
            resource_id="file-1",
            resource_type="file",
            user_id="user-1",
        )
        is False
    )
    assert membership_filters == [
        {
            "user_id": "user-1",
            "container_type": "organization",
            "status": "active",
            "deleted_at__isnull": True,
        }
    ]


@pytest.mark.asyncio
async def test_file_org_access_requires_canonical_active_membership_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    membership_checks: list[dict[str, object]] = []

    class _Memberships:
        @classmethod
        async def exists(cls, **kwargs: object) -> bool:
            membership_checks.append(kwargs)
            return True

    monkeypatch.setattr(sources, "get_db_model", lambda name: _Memberships)

    row = {
        "id": "file-1",
        "created_by": None,
        "published_to_web": False,
        "organization_id": "org-1",
        "parent_folder_id": None,
    }
    assert await sources._file_row_accessible(row, user_id="user-1") is True
    assert membership_checks == [
        {
            "organization_id": "org-1",
            "user_id": "user-1",
            "container_type": "organization",
            "status": "active",
            "deleted_at__isnull": True,
        }
    ]
