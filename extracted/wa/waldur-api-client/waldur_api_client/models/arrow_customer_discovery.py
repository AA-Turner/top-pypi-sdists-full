from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowCustomerDiscovery")


@_attrs_define
class ArrowCustomerDiscovery:
    """
    Attributes:
        reference (str):
        company_name (str):
        email (Union[Unset, str]):
        city (Union[Unset, str]):
        country_code (Union[Unset, str]):
    """

    reference: str
    company_name: str
    email: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    country_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference = self.reference

        company_name = self.company_name

        email = self.email

        city = self.city

        country_code = self.country_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reference": reference,
                "companyName": company_name,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if city is not UNSET:
            field_dict["city"] = city
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reference = d.pop("reference")

        company_name = d.pop("companyName")

        email = d.pop("email", UNSET)

        city = d.pop("city", UNSET)

        country_code = d.pop("countryCode", UNSET)

        arrow_customer_discovery = cls(
            reference=reference,
            company_name=company_name,
            email=email,
            city=city,
            country_code=country_code,
        )

        arrow_customer_discovery.additional_properties = d
        return arrow_customer_discovery

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
