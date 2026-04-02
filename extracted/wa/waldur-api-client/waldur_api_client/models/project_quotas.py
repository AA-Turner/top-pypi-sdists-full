from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectQuotas")


@_attrs_define
class ProjectQuotas:
    """
    Attributes:
        project_name (str):
        customer_name (str):
        customer_abbreviation (str):
        value (int):
    """

    project_name: str
    customer_name: str
    customer_abbreviation: str
    value: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_name = self.project_name

        customer_name = self.customer_name

        customer_abbreviation = self.customer_abbreviation

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_name": project_name,
                "customer_name": customer_name,
                "customer_abbreviation": customer_abbreviation,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_name = d.pop("project_name")

        customer_name = d.pop("customer_name")

        customer_abbreviation = d.pop("customer_abbreviation")

        value = d.pop("value")

        project_quotas = cls(
            project_name=project_name,
            customer_name=customer_name,
            customer_abbreviation=customer_abbreviation,
            value=value,
        )

        project_quotas.additional_properties = d
        return project_quotas

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
