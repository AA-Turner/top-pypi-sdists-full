from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_terminate_request_termination_attributes import ResourceTerminateRequestTerminationAttributes


T = TypeVar("T", bound="ResourceTerminateRequest")


@_attrs_define
class ResourceTerminateRequest:
    """
    Attributes:
        attributes (Union[Unset, ResourceTerminateRequestTerminationAttributes]): Optional attributes/parameters to pass
            to the termination operation
    """

    attributes: Union[Unset, "ResourceTerminateRequestTerminationAttributes"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_terminate_request_termination_attributes import (
            ResourceTerminateRequestTerminationAttributes,
        )

        d = dict(src_dict)
        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, ResourceTerminateRequestTerminationAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ResourceTerminateRequestTerminationAttributes.from_dict(_attributes)

        resource_terminate_request = cls(
            attributes=attributes,
        )

        resource_terminate_request.additional_properties = d
        return resource_terminate_request

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
