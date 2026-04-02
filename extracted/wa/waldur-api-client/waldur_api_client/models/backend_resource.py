import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackendResource")


@_attrs_define
class BackendResource:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        project (UUID):
        project_name (str):
        project_url (str):
        offering (UUID):
        offering_name (str):
        offering_url (str):
        backend_id (Union[Unset, str]):
        backend_metadata (Union[Unset, Any]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    project: UUID
    project_name: str
    project_url: str
    offering: UUID
    offering_name: str
    offering_url: str
    backend_id: Union[Unset, str] = UNSET
    backend_metadata: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        project = str(self.project)

        project_name = self.project_name

        project_url = self.project_url

        offering = str(self.offering)

        offering_name = self.offering_name

        offering_url = self.offering_url

        backend_id = self.backend_id

        backend_metadata = self.backend_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "project": project,
                "project_name": project_name,
                "project_url": project_url,
                "offering": offering,
                "offering_name": offering_name,
                "offering_url": offering_url,
            }
        )
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if backend_metadata is not UNSET:
            field_dict["backend_metadata"] = backend_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        project = UUID(d.pop("project"))

        project_name = d.pop("project_name")

        project_url = d.pop("project_url")

        offering = UUID(d.pop("offering"))

        offering_name = d.pop("offering_name")

        offering_url = d.pop("offering_url")

        backend_id = d.pop("backend_id", UNSET)

        backend_metadata = d.pop("backend_metadata", UNSET)

        backend_resource = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            project=project,
            project_name=project_name,
            project_url=project_url,
            offering=offering,
            offering_name=offering_name,
            offering_url=offering_url,
            backend_id=backend_id,
            backend_metadata=backend_metadata,
        )

        backend_resource.additional_properties = d
        return backend_resource

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
