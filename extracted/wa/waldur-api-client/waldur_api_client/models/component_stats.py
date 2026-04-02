from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ComponentStats")


@_attrs_define
class ComponentStats:
    """
    Attributes:
        type_ (str):
        name (str):
        description (str):
        measured_unit (str):
        billing_type (str):
        usage (int):
        limit_usage (int):
        limit (int):
        offering_name (str):
        offering_uuid (UUID):
    """

    type_: str
    name: str
    description: str
    measured_unit: str
    billing_type: str
    usage: int
    limit_usage: int
    limit: int
    offering_name: str
    offering_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        description = self.description

        measured_unit = self.measured_unit

        billing_type = self.billing_type

        usage = self.usage

        limit_usage = self.limit_usage

        limit = self.limit

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "name": name,
                "description": description,
                "measured_unit": measured_unit,
                "billing_type": billing_type,
                "usage": usage,
                "limit_usage": limit_usage,
                "limit": limit,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        name = d.pop("name")

        description = d.pop("description")

        measured_unit = d.pop("measured_unit")

        billing_type = d.pop("billing_type")

        usage = d.pop("usage")

        limit_usage = d.pop("limit_usage")

        limit = d.pop("limit")

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        component_stats = cls(
            type_=type_,
            name=name,
            description=description,
            measured_unit=measured_unit,
            billing_type=billing_type,
            usage=usage,
            limit_usage=limit_usage,
            limit=limit,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
        )

        component_stats.additional_properties = d
        return component_stats

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
