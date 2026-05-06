from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectMappingResponse")


@_attrs_define
class ProjectMappingResponse:
    """
    Attributes:
        uuid (str):
        name (str):
        customer_uuid (str):
        customer_name (str):
    """

    uuid: str
    name: str
    customer_uuid: str
    customer_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        customer_uuid = self.customer_uuid

        customer_name = self.customer_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        customer_uuid = d.pop("customer_uuid")

        customer_name = d.pop("customer_name")

        project_mapping_response = cls(
            uuid=uuid,
            name=name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
        )

        project_mapping_response.additional_properties = d
        return project_mapping_response

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
