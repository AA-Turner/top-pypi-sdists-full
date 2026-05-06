from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedResourceProjectRequest")


@_attrs_define
class PatchedResourceProjectRequest:
    """
    Attributes:
        resource (Union[Unset, UUID]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        limits (Union[Unset, Any]): Dictionary mapping component types to quota values. Same format as Resource.limits.
    """

    resource: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    limits: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource: Union[Unset, str] = UNSET
        if not isinstance(self.resource, Unset):
            resource = str(self.resource)

        name = self.name

        description = self.description

        limits = self.limits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource is not UNSET:
            field_dict["resource"] = resource
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, UUID]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = UUID(_resource)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        limits = d.pop("limits", UNSET)

        patched_resource_project_request = cls(
            resource=resource,
            name=name,
            description=description,
            limits=limits,
        )

        patched_resource_project_request.additional_properties = d
        return patched_resource_project_request

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
