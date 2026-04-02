from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackendResourceRequest")


@_attrs_define
class BackendResourceRequest:
    """
    Attributes:
        name (str):
        project (UUID):
        offering (UUID):
        backend_id (Union[Unset, str]):
        backend_metadata (Union[Unset, Any]):
    """

    name: str
    project: UUID
    offering: UUID
    backend_id: Union[Unset, str] = UNSET
    backend_metadata: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project = str(self.project)

        offering = str(self.offering)

        backend_id = self.backend_id

        backend_metadata = self.backend_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "project": project,
                "offering": offering,
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
        name = d.pop("name")

        project = UUID(d.pop("project"))

        offering = UUID(d.pop("offering"))

        backend_id = d.pop("backend_id", UNSET)

        backend_metadata = d.pop("backend_metadata", UNSET)

        backend_resource_request = cls(
            name=name,
            project=project,
            offering=offering,
            backend_id=backend_id,
            backend_metadata=backend_metadata,
        )

        backend_resource_request.additional_properties = d
        return backend_resource_request

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
