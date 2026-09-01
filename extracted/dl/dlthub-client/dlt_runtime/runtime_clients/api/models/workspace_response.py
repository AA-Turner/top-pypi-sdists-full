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
    from ..models.workspace_response_predefined_profiles import (
        WorkspaceResponsePredefinedProfiles,
    )


T = TypeVar("T", bound="WorkspaceResponse")


@_attrs_define
class WorkspaceResponse:
    """
    Attributes:
        dataplane_id (str): Identifier of the data plane that holds this workspace's user data. Matches the subdomain of
            the plane's public entrypoint.
        dataplane_url (str): Public base URL of the data plane that holds this workspace's user data (e.g.
            ``https://<dataplane_id>.dlthub.com``). Clients attach a DataplaneUserJwt (minted via GET
            /api/v1/workspaces/{id}/dataplane-access-token) when calling data-plane services (telemetry, logs) at this host.
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        description (None | str): The description of the workspace
        id (UUID): The unique ID of the entity
        name (str): The name of the workspace
        organization_id (UUID): The ID of the parent organization
        archived_at (datetime.datetime | None | Unset): Timestamp when the workspace was archived; null when live.
            Archived workspaces reject all mutations except unarchive.
        is_playground (bool | Unset): Whether this is the user's auto-created personal playground workspace. Playgrounds
            are single-member and cannot be renamed or deleted. Default: False.
        predefined_profiles (WorkspaceResponsePredefinedProfiles | Unset): Predefined profile names keyed by access
            level name, e.g. {'DATA_WRITE': 'prod', 'DATA_READ': 'access'}
    """

    dataplane_id: str
    dataplane_url: str
    date_added: datetime.datetime
    date_updated: datetime.datetime
    description: None | str
    id: UUID
    name: str
    organization_id: UUID
    archived_at: datetime.datetime | None | Unset = UNSET
    is_playground: bool | Unset = False
    predefined_profiles: WorkspaceResponsePredefinedProfiles | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataplane_id = self.dataplane_id

        dataplane_url = self.dataplane_url

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        description: None | str
        description = self.description

        id = str(self.id)

        name = self.name

        organization_id = str(self.organization_id)

        archived_at: None | str | Unset
        if isinstance(self.archived_at, Unset):
            archived_at = UNSET
        elif isinstance(self.archived_at, datetime.datetime):
            archived_at = self.archived_at.isoformat()
        else:
            archived_at = self.archived_at

        is_playground = self.is_playground

        predefined_profiles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.predefined_profiles, Unset):
            predefined_profiles = self.predefined_profiles.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataplane_id": dataplane_id,
                "dataplane_url": dataplane_url,
                "date_added": date_added,
                "date_updated": date_updated,
                "description": description,
                "id": id,
                "name": name,
                "organization_id": organization_id,
            }
        )
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at
        if is_playground is not UNSET:
            field_dict["is_playground"] = is_playground
        if predefined_profiles is not UNSET:
            field_dict["predefined_profiles"] = predefined_profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_response_predefined_profiles import (
            WorkspaceResponsePredefinedProfiles,
        )

        d = dict(src_dict)
        dataplane_id = d.pop("dataplane_id")

        dataplane_url = d.pop("dataplane_url")

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        id = UUID(d.pop("id"))

        name = d.pop("name")

        organization_id = UUID(d.pop("organization_id"))

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

        is_playground = d.pop("is_playground", UNSET)

        _predefined_profiles = d.pop("predefined_profiles", UNSET)
        predefined_profiles: WorkspaceResponsePredefinedProfiles | Unset
        if isinstance(_predefined_profiles, Unset):
            predefined_profiles = UNSET
        else:
            predefined_profiles = WorkspaceResponsePredefinedProfiles.from_dict(
                _predefined_profiles
            )

        workspace_response = cls(
            dataplane_id=dataplane_id,
            dataplane_url=dataplane_url,
            date_added=date_added,
            date_updated=date_updated,
            description=description,
            id=id,
            name=name,
            organization_id=organization_id,
            archived_at=archived_at,
            is_playground=is_playground,
            predefined_profiles=predefined_profiles,
        )

        workspace_response.additional_properties = d
        return workspace_response

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
