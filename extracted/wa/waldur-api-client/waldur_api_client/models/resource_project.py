import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceProject")


@_attrs_define
class ResourceProject:
    """
    Attributes:
        uuid (UUID):
        resource (UUID):
        name (str):
        backend_id (str):
        state (str):
        error_message (str):
        current_usages (Any): Dictionary mapping component types to current usage amounts. Populated by backend
            synchronization.
        resource_uuid (UUID):
        resource_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        description (Union[Unset, str]):
        limits (Union[Unset, Any]): Dictionary mapping component types to quota values. Same format as Resource.limits.
    """

    uuid: UUID
    resource: UUID
    name: str
    backend_id: str
    state: str
    error_message: str
    current_usages: Any
    resource_uuid: UUID
    resource_name: str
    created: datetime.datetime
    modified: datetime.datetime
    description: Union[Unset, str] = UNSET
    limits: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        resource = str(self.resource)

        name = self.name

        backend_id = self.backend_id

        state = self.state

        error_message = self.error_message

        current_usages = self.current_usages

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        description = self.description

        limits = self.limits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource": resource,
                "name": name,
                "backend_id": backend_id,
                "state": state,
                "error_message": error_message,
                "current_usages": current_usages,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "created": created,
                "modified": modified,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource = UUID(d.pop("resource"))

        name = d.pop("name")

        backend_id = d.pop("backend_id")

        state = d.pop("state")

        error_message = d.pop("error_message")

        current_usages = d.pop("current_usages")

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        description = d.pop("description", UNSET)

        limits = d.pop("limits", UNSET)

        resource_project = cls(
            uuid=uuid,
            resource=resource,
            name=name,
            backend_id=backend_id,
            state=state,
            error_message=error_message,
            current_usages=current_usages,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            created=created,
            modified=modified,
            description=description,
            limits=limits,
        )

        resource_project.additional_properties = d
        return resource_project

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
