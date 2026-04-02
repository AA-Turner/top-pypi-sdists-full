from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CallResourceTemplateRequest")


@_attrs_define
class CallResourceTemplateRequest:
    """
    Attributes:
        name (str):
        requested_offering (str):
        description (Union[Unset, str]):
        attributes (Union[Unset, Any]):
        limits (Union[Unset, Any]):
        is_required (Union[Unset, bool]): If True, every proposal must include this resource type
    """

    name: str
    requested_offering: str
    description: Union[Unset, str] = UNSET
    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, Any] = UNSET
    is_required: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        requested_offering = self.requested_offering

        description = self.description

        attributes = self.attributes

        limits = self.limits

        is_required = self.is_required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "requested_offering": requested_offering,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if is_required is not UNSET:
            field_dict["is_required"] = is_required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        requested_offering = d.pop("requested_offering")

        description = d.pop("description", UNSET)

        attributes = d.pop("attributes", UNSET)

        limits = d.pop("limits", UNSET)

        is_required = d.pop("is_required", UNSET)

        call_resource_template_request = cls(
            name=name,
            requested_offering=requested_offering,
            description=description,
            attributes=attributes,
            limits=limits,
            is_required=is_required,
        )

        call_resource_template_request.additional_properties = d
        return call_resource_template_request

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
