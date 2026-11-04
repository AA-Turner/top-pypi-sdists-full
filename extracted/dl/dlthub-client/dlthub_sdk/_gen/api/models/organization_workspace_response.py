from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_workspace_response_predefined_profiles import (
        OrganizationWorkspaceResponsePredefinedProfiles,
    )
    from ..models.workspace_member_response import WorkspaceMemberResponse


T = TypeVar("T", bound="OrganizationWorkspaceResponse")


@_attrs_define
class OrganizationWorkspaceResponse:
    """
    Attributes:
        created_at (datetime.datetime): When it was created.
        dataplane_id (str): Identifier of the data plane that holds this workspace's user data. Matches the subdomain of
            the plane's public entrypoint.
        dataplane_url (str): Base URL of the workspace's data plane, `https://<dataplane_id>.dlthub.com`, where the
            Dataplane, Logs and Telemetry APIs are served. Call them with a token from `POST
            /api/v1/workspaces/{workspace_id}/-issue-dataplane-token`.
        description (None | str): Free-text description of the workspace; `null` when none is set.
        id (UUID): Unique ID (a UUID).
        member_count (int): Number of active human members in the workspace.
        name (str): The name of the workspace
        organization_id (UUID): The ID of the parent organization
        owner_members (list[WorkspaceMemberResponse]): The workspace's active human owners, in the order they joined.
        updated_at (datetime.datetime): When it was last changed.
        archived_at (datetime.datetime | None | Unset): When the workspace was archived; `null` when live. An archived
            workspace rejects all changes except unarchiving, though owners can still manage its workspace variables.
        credit_threshold (int | None | Unset): Monthly credit consumption threshold that triggers an email alert; null
            when disabled.
        is_playground (bool | Unset): Whether this is the user's auto-created personal playground workspace. A
            playground has a single member and cannot be updated, archived, shared, or given API keys. Default: False.
        predefined_profiles (OrganizationWorkspaceResponsePredefinedProfiles | Unset): Built-in profiles by data access:
            `DATA_WRITE` → `prod` (runs need developer or owner), `DATA_READ` → `access` (viewers may run).
    """

    created_at: datetime.datetime
    dataplane_id: str
    dataplane_url: str
    description: None | str
    id: UUID
    member_count: int
    name: str
    organization_id: UUID
    owner_members: list[WorkspaceMemberResponse]
    updated_at: datetime.datetime
    archived_at: datetime.datetime | None | Unset = UNSET
    credit_threshold: int | None | Unset = UNSET
    is_playground: bool | Unset = False
    predefined_profiles: OrganizationWorkspaceResponsePredefinedProfiles | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        dataplane_id = self.dataplane_id

        dataplane_url = self.dataplane_url

        description: None | str
        description = self.description

        id = str(self.id)

        member_count = self.member_count

        name = self.name

        organization_id = str(self.organization_id)

        owner_members = []
        for owner_members_item_data in self.owner_members:
            owner_members_item = owner_members_item_data.to_dict()
            owner_members.append(owner_members_item)

        updated_at = self.updated_at.isoformat()

        archived_at: None | str | Unset
        if isinstance(self.archived_at, Unset):
            archived_at = UNSET
        elif isinstance(self.archived_at, datetime.datetime):
            archived_at = self.archived_at.isoformat()
        else:
            archived_at = self.archived_at

        credit_threshold: int | None | Unset
        if isinstance(self.credit_threshold, Unset):
            credit_threshold = UNSET
        else:
            credit_threshold = self.credit_threshold

        is_playground = self.is_playground

        predefined_profiles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.predefined_profiles, Unset):
            predefined_profiles = self.predefined_profiles.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "dataplane_id": dataplane_id,
                "dataplane_url": dataplane_url,
                "description": description,
                "id": id,
                "member_count": member_count,
                "name": name,
                "organization_id": organization_id,
                "owner_members": owner_members,
                "updated_at": updated_at,
            }
        )
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at
        if credit_threshold is not UNSET:
            field_dict["credit_threshold"] = credit_threshold
        if is_playground is not UNSET:
            field_dict["is_playground"] = is_playground
        if predefined_profiles is not UNSET:
            field_dict["predefined_profiles"] = predefined_profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_workspace_response_predefined_profiles import (
            OrganizationWorkspaceResponsePredefinedProfiles,
        )
        from ..models.workspace_member_response import WorkspaceMemberResponse

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        dataplane_id = d.pop("dataplane_id")

        dataplane_url = d.pop("dataplane_url")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        id = UUID(d.pop("id"))

        member_count = d.pop("member_count")

        name = d.pop("name")

        organization_id = UUID(d.pop("organization_id"))

        owner_members = []
        _owner_members = d.pop("owner_members")
        for owner_members_item_data in _owner_members:
            owner_members_item = WorkspaceMemberResponse.from_dict(
                owner_members_item_data
            )

            owner_members.append(owner_members_item)

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_archived_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                archived_at_type_0 = isoparse(data)

                return archived_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        archived_at = _parse_archived_at(d.pop("archived_at", UNSET))

        def _parse_credit_threshold(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        credit_threshold = _parse_credit_threshold(d.pop("credit_threshold", UNSET))

        is_playground = d.pop("is_playground", UNSET)

        _predefined_profiles = d.pop("predefined_profiles", UNSET)
        predefined_profiles: OrganizationWorkspaceResponsePredefinedProfiles | Unset
        if isinstance(_predefined_profiles, Unset):
            predefined_profiles = UNSET
        else:
            predefined_profiles = (
                OrganizationWorkspaceResponsePredefinedProfiles.from_dict(
                    _predefined_profiles
                )
            )

        organization_workspace_response = cls(
            created_at=created_at,
            dataplane_id=dataplane_id,
            dataplane_url=dataplane_url,
            description=description,
            id=id,
            member_count=member_count,
            name=name,
            organization_id=organization_id,
            owner_members=owner_members,
            updated_at=updated_at,
            archived_at=archived_at,
            credit_threshold=credit_threshold,
            is_playground=is_playground,
            predefined_profiles=predefined_profiles,
        )

        organization_workspace_response.additional_properties = d
        return organization_workspace_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
