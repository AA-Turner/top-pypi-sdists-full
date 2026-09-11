from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.invite_status import InviteStatus
from ..models.organization_membership_role import OrganizationMembershipRole
from ..models.workspace_membership_role import WorkspaceMembershipRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="InviteResponse")


@_attrs_define
class InviteResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        email (str): The invited email
        id (UUID): The unique ID of the entity
        invited_by (UUID): The user who created the invite
        org_role (OrganizationMembershipRole): The role to assign to the user
        organization_id (UUID): The organization the invite grants access to
        status (InviteStatus): The current status of the invite
        accepted_at (datetime.datetime | None | Unset): When the invite was accepted, if accepted
        accepted_by (None | Unset | UUID): The user who accepted the invite, if accepted
        workspace_id (None | Unset | UUID): The workspace the invite grants access to; null for org-only invites
        workspace_role (None | Unset | WorkspaceMembershipRole): The workspace role granted on accept; null for org-only
            invites
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    email: str
    id: UUID
    invited_by: UUID
    org_role: OrganizationMembershipRole
    organization_id: UUID
    status: InviteStatus
    accepted_at: datetime.datetime | None | Unset = UNSET
    accepted_by: None | Unset | UUID = UNSET
    workspace_id: None | Unset | UUID = UNSET
    workspace_role: None | Unset | WorkspaceMembershipRole = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        email = self.email

        id = str(self.id)

        invited_by = str(self.invited_by)

        org_role = self.org_role.value

        organization_id = str(self.organization_id)

        status = self.status.value

        accepted_at: None | str | Unset
        if isinstance(self.accepted_at, Unset):
            accepted_at = UNSET
        elif isinstance(self.accepted_at, datetime.datetime):
            accepted_at = self.accepted_at.isoformat()
        else:
            accepted_at = self.accepted_at

        accepted_by: None | str | Unset
        if isinstance(self.accepted_by, Unset):
            accepted_by = UNSET
        elif isinstance(self.accepted_by, UUID):
            accepted_by = str(self.accepted_by)
        else:
            accepted_by = self.accepted_by

        workspace_id: None | str | Unset
        if isinstance(self.workspace_id, Unset):
            workspace_id = UNSET
        elif isinstance(self.workspace_id, UUID):
            workspace_id = str(self.workspace_id)
        else:
            workspace_id = self.workspace_id

        workspace_role: None | str | Unset
        if isinstance(self.workspace_role, Unset):
            workspace_role = UNSET
        elif isinstance(self.workspace_role, WorkspaceMembershipRole):
            workspace_role = self.workspace_role.value
        else:
            workspace_role = self.workspace_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "email": email,
                "id": id,
                "invited_by": invited_by,
                "org_role": org_role,
                "organization_id": organization_id,
                "status": status,
            }
        )
        if accepted_at is not UNSET:
            field_dict["accepted_at"] = accepted_at
        if accepted_by is not UNSET:
            field_dict["accepted_by"] = accepted_by
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if workspace_role is not UNSET:
            field_dict["workspace_role"] = workspace_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        email = d.pop("email")

        id = UUID(d.pop("id"))

        invited_by = UUID(d.pop("invited_by"))

        org_role = OrganizationMembershipRole(d.pop("org_role"))

        organization_id = UUID(d.pop("organization_id"))

        status = InviteStatus(d.pop("status"))

        def _parse_accepted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                accepted_at_type_0 = isoparse(data)

                return accepted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        accepted_at = _parse_accepted_at(d.pop("accepted_at", UNSET))

        def _parse_accepted_by(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                accepted_by_type_0 = UUID(data)

                return accepted_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        accepted_by = _parse_accepted_by(d.pop("accepted_by", UNSET))

        def _parse_workspace_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                workspace_id_type_0 = UUID(data)

                return workspace_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        workspace_id = _parse_workspace_id(d.pop("workspace_id", UNSET))

        def _parse_workspace_role(
            data: object,
        ) -> None | Unset | WorkspaceMembershipRole:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                workspace_role_type_0 = WorkspaceMembershipRole(data)

                return workspace_role_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WorkspaceMembershipRole, data)

        workspace_role = _parse_workspace_role(d.pop("workspace_role", UNSET))

        invite_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            email=email,
            id=id,
            invited_by=invited_by,
            org_role=org_role,
            organization_id=organization_id,
            status=status,
            accepted_at=accepted_at,
            accepted_by=accepted_by,
            workspace_id=workspace_id,
            workspace_role=workspace_role,
        )

        invite_response.additional_properties = d
        return invite_response

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
