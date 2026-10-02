from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowCustomerMappingRequest")


@_attrs_define
class ArrowCustomerMappingRequest:
    """
    Attributes:
        settings (str):
        arrow_reference (str): Arrow customer ID (e.g., 'XSP661245')
        waldur_customer (str):
        arrow_company_name (Union[Unset, str]): Arrow company name
        is_active (Union[Unset, bool]): Whether this mapping is active
    """

    settings: str
    arrow_reference: str
    waldur_customer: str
    arrow_company_name: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings = self.settings

        arrow_reference = self.arrow_reference

        waldur_customer = self.waldur_customer

        arrow_company_name = self.arrow_company_name

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
                "arrow_reference": arrow_reference,
                "waldur_customer": waldur_customer,
            }
        )
        if arrow_company_name is not UNSET:
            field_dict["arrow_company_name"] = arrow_company_name
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        settings = d.pop("settings")

        arrow_reference = d.pop("arrow_reference")

        waldur_customer = d.pop("waldur_customer")

        arrow_company_name = d.pop("arrow_company_name", UNSET)

        is_active = d.pop("is_active", UNSET)

        arrow_customer_mapping_request = cls(
            settings=settings,
            arrow_reference=arrow_reference,
            waldur_customer=waldur_customer,
            arrow_company_name=arrow_company_name,
            is_active=is_active,
        )

        arrow_customer_mapping_request.additional_properties = d
        return arrow_customer_mapping_request

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
