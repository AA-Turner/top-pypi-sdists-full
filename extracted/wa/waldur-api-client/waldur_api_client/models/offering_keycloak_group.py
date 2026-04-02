import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingKeycloakGroup")


@_attrs_define
class OfferingKeycloakGroup:
    """
    Attributes:
        uuid (UUID):
        url (str):
        name (str):
        backend_id (str):
        offering (str):
        offering_uuid (UUID):
        offering_name (str):
        role (str):
        role_name (str):
        role_scope_type (str): Level this role applies at, e.g. 'cluster', 'project'. Empty means offering-wide.
        resource_uuid (UUID):
        resource_name (Union[None, str]):
        created (datetime.datetime):
        modified (datetime.datetime):
        resource (Union[None, Unset, str]):
        scope_id (Union[Unset, str]): Sub-entity identifier within a resource, e.g. Rancher project ID within a cluster.
            Default: ''.
    """

    uuid: UUID
    url: str
    name: str
    backend_id: str
    offering: str
    offering_uuid: UUID
    offering_name: str
    role: str
    role_name: str
    role_scope_type: str
    resource_uuid: UUID
    resource_name: Union[None, str]
    created: datetime.datetime
    modified: datetime.datetime
    resource: Union[None, Unset, str] = UNSET
    scope_id: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        name = self.name

        backend_id = self.backend_id

        offering = self.offering

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        role = self.role

        role_name = self.role_name

        role_scope_type = self.role_scope_type

        resource_uuid = str(self.resource_uuid)

        resource_name: Union[None, str]
        resource_name = self.resource_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        else:
            resource = self.resource

        scope_id = self.scope_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "name": name,
                "backend_id": backend_id,
                "offering": offering,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "role": role,
                "role_name": role_name,
                "role_scope_type": role_scope_type,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "created": created,
                "modified": modified,
            }
        )
        if resource is not UNSET:
            field_dict["resource"] = resource
        if scope_id is not UNSET:
            field_dict["scope_id"] = scope_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        name = d.pop("name")

        backend_id = d.pop("backend_id")

        offering = d.pop("offering")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        role = d.pop("role")

        role_name = d.pop("role_name")

        role_scope_type = d.pop("role_scope_type")

        resource_uuid = UUID(d.pop("resource_uuid"))

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_resource(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource = _parse_resource(d.pop("resource", UNSET))

        scope_id = d.pop("scope_id", UNSET)

        offering_keycloak_group = cls(
            uuid=uuid,
            url=url,
            name=name,
            backend_id=backend_id,
            offering=offering,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            role=role,
            role_name=role_name,
            role_scope_type=role_scope_type,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            created=created,
            modified=modified,
            resource=resource,
            scope_id=scope_id,
        )

        offering_keycloak_group.additional_properties = d
        return offering_keycloak_group

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
