from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestedResourceRequest")


@_attrs_define
class RequestedResourceRequest:
    """
    Attributes:
        attributes (Union[Unset, Any]):
        limits (Union[Unset, Any]):
        description (Union[Unset, str]):
        requested_offering_uuid (Union[Unset, UUID]):
        call_resource_template_uuid (Union[Unset, UUID]):
    """

    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, Any] = UNSET
    description: Union[Unset, str] = UNSET
    requested_offering_uuid: Union[Unset, UUID] = UNSET
    call_resource_template_uuid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes

        limits = self.limits

        description = self.description

        requested_offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.requested_offering_uuid, Unset):
            requested_offering_uuid = str(self.requested_offering_uuid)

        call_resource_template_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.call_resource_template_uuid, Unset):
            call_resource_template_uuid = str(self.call_resource_template_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if description is not UNSET:
            field_dict["description"] = description
        if requested_offering_uuid is not UNSET:
            field_dict["requested_offering_uuid"] = requested_offering_uuid
        if call_resource_template_uuid is not UNSET:
            field_dict["call_resource_template_uuid"] = call_resource_template_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attributes = d.pop("attributes", UNSET)

        limits = d.pop("limits", UNSET)

        description = d.pop("description", UNSET)

        _requested_offering_uuid = d.pop("requested_offering_uuid", UNSET)
        requested_offering_uuid: Union[Unset, UUID]
        if isinstance(_requested_offering_uuid, Unset):
            requested_offering_uuid = UNSET
        else:
            requested_offering_uuid = UUID(_requested_offering_uuid)

        _call_resource_template_uuid = d.pop("call_resource_template_uuid", UNSET)
        call_resource_template_uuid: Union[Unset, UUID]
        if isinstance(_call_resource_template_uuid, Unset):
            call_resource_template_uuid = UNSET
        else:
            call_resource_template_uuid = UUID(_call_resource_template_uuid)

        requested_resource_request = cls(
            attributes=attributes,
            limits=limits,
            description=description,
            requested_offering_uuid=requested_offering_uuid,
            call_resource_template_uuid=call_resource_template_uuid,
        )

        requested_resource_request.additional_properties = d
        return requested_resource_request

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
