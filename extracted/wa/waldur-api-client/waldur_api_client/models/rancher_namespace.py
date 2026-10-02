import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherNamespace")


@_attrs_define
class RancherNamespace:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        runtime_state (Union[Unset, str]):
        project (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    runtime_state: Union[Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        runtime_state = self.runtime_state

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
            }
        )
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        runtime_state = d.pop("runtime_state", UNSET)

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        rancher_namespace = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            runtime_state=runtime_state,
            project=project,
        )

        rancher_namespace.additional_properties = d
        return rancher_namespace

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
