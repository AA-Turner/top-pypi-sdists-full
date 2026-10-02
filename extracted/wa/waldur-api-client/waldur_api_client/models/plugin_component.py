from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_type_enum import BillingTypeEnum

T = TypeVar("T", bound="PluginComponent")


@_attrs_define
class PluginComponent:
    """
    Attributes:
        type_ (str): Type identifier of the component
        name (str): Display name of the component
        measured_unit (str): Unit of measurement for the component
        billing_type (BillingTypeEnum):
    """

    type_: str
    name: str
    measured_unit: str
    billing_type: BillingTypeEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        measured_unit = self.measured_unit

        billing_type = self.billing_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "name": name,
                "measured_unit": measured_unit,
                "billing_type": billing_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        name = d.pop("name")

        measured_unit = d.pop("measured_unit")

        billing_type = BillingTypeEnum(d.pop("billing_type"))

        plugin_component = cls(
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            billing_type=billing_type,
        )

        plugin_component.additional_properties = d
        return plugin_component

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
