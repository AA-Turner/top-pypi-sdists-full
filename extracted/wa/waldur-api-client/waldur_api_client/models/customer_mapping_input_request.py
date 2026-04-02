from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerMappingInputRequest")


@_attrs_define
class CustomerMappingInputRequest:
    """
    Attributes:
        arrow_reference (str):
        waldur_customer_uuid (UUID):
    """

    arrow_reference: str
    waldur_customer_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        arrow_reference = self.arrow_reference

        waldur_customer_uuid = str(self.waldur_customer_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "arrow_reference": arrow_reference,
                "waldur_customer_uuid": waldur_customer_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        arrow_reference = d.pop("arrow_reference")

        waldur_customer_uuid = UUID(d.pop("waldur_customer_uuid"))

        customer_mapping_input_request = cls(
            arrow_reference=arrow_reference,
            waldur_customer_uuid=waldur_customer_uuid,
        )

        customer_mapping_input_request.additional_properties = d
        return customer_mapping_input_request

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
