from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedArrowCustomerMappingRequest")


@_attrs_define
class PatchedArrowCustomerMappingRequest:
    """
    Attributes:
        settings (Union[Unset, str]):
        arrow_reference (Union[Unset, str]): Arrow customer ID (e.g., 'XSP661245')
        arrow_company_name (Union[Unset, str]): Arrow company name
        waldur_customer (Union[Unset, str]):
        is_active (Union[Unset, bool]): Whether this mapping is active
    """

    settings: Union[Unset, str] = UNSET
    arrow_reference: Union[Unset, str] = UNSET
    arrow_company_name: Union[Unset, str] = UNSET
    waldur_customer: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings = self.settings

        arrow_reference = self.arrow_reference

        arrow_company_name = self.arrow_company_name

        waldur_customer = self.waldur_customer

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if settings is not UNSET:
            field_dict["settings"] = settings
        if arrow_reference is not UNSET:
            field_dict["arrow_reference"] = arrow_reference
        if arrow_company_name is not UNSET:
            field_dict["arrow_company_name"] = arrow_company_name
        if waldur_customer is not UNSET:
            field_dict["waldur_customer"] = waldur_customer
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        settings = d.pop("settings", UNSET)

        arrow_reference = d.pop("arrow_reference", UNSET)

        arrow_company_name = d.pop("arrow_company_name", UNSET)

        waldur_customer = d.pop("waldur_customer", UNSET)

        is_active = d.pop("is_active", UNSET)

        patched_arrow_customer_mapping_request = cls(
            settings=settings,
            arrow_reference=arrow_reference,
            arrow_company_name=arrow_company_name,
            waldur_customer=waldur_customer,
            is_active=is_active,
        )

        patched_arrow_customer_mapping_request.additional_properties = d
        return patched_arrow_customer_mapping_request

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
