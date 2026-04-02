from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCallResourceTemplateRequest")


@_attrs_define
class PatchedCallResourceTemplateRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        attributes (Union[Unset, Any]):
        limits (Union[Unset, Any]):
        is_required (Union[Unset, bool]): If True, every proposal must include this resource type
        requested_offering (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, Any] = UNSET
    is_required: Union[Unset, bool] = UNSET
    requested_offering: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        attributes = self.attributes

        limits = self.limits

        is_required = self.is_required

        requested_offering = self.requested_offering

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if is_required is not UNSET:
            field_dict["is_required"] = is_required
        if requested_offering is not UNSET:
            field_dict["requested_offering"] = requested_offering

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        attributes = d.pop("attributes", UNSET)

        limits = d.pop("limits", UNSET)

        is_required = d.pop("is_required", UNSET)

        requested_offering = d.pop("requested_offering", UNSET)

        patched_call_resource_template_request = cls(
            name=name,
            description=description,
            attributes=attributes,
            limits=limits,
            is_required=is_required,
            requested_offering=requested_offering,
        )

        patched_call_resource_template_request.additional_properties = d
        return patched_call_resource_template_request

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
