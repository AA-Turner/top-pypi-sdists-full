import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_nested_namespace import RancherNestedNamespace


T = TypeVar("T", bound="RancherProject")


@_attrs_define
class RancherProject:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        namespaces (list['RancherNestedNamespace']):
        description (Union[Unset, str]):
        runtime_state (Union[Unset, str]):
        cluster (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    namespaces: list["RancherNestedNamespace"]
    description: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    cluster: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        namespaces = []
        for namespaces_item_data in self.namespaces:
            namespaces_item = namespaces_item_data.to_dict()
            namespaces.append(namespaces_item)

        description = self.description

        runtime_state = self.runtime_state

        cluster: Union[None, Unset, str]
        if isinstance(self.cluster, Unset):
            cluster = UNSET
        else:
            cluster = self.cluster

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "namespaces": namespaces,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if cluster is not UNSET:
            field_dict["cluster"] = cluster

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_nested_namespace import RancherNestedNamespace

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        namespaces = []
        _namespaces = d.pop("namespaces")
        for namespaces_item_data in _namespaces:
            namespaces_item = RancherNestedNamespace.from_dict(namespaces_item_data)

            namespaces.append(namespaces_item)

        description = d.pop("description", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        def _parse_cluster(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster = _parse_cluster(d.pop("cluster", UNSET))

        rancher_project = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            namespaces=namespaces,
            description=description,
            runtime_state=runtime_state,
            cluster=cluster,
        )

        rancher_project.additional_properties = d
        return rancher_project

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
