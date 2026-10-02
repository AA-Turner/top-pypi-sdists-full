from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerDetails")


@_attrs_define
class CustomerDetails:
    """
    Attributes:
        name (Union[Unset, str]):
        address (Union[Unset, str]):
        country (Union[Unset, str]):
        country_name (Union[None, Unset, str]):
        email (Union[Unset, str]):
        postal (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        bank_name (Union[Unset, str]):
        bank_account (Union[Unset, str]):
        vat_code (Union[Unset, str]): VAT number
    """

    name: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    country_name: Union[None, Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    postal: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    bank_name: Union[Unset, str] = UNSET
    bank_account: Union[Unset, str] = UNSET
    vat_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        address = self.address

        country = self.country

        country_name: Union[None, Unset, str]
        if isinstance(self.country_name, Unset):
            country_name = UNSET
        else:
            country_name = self.country_name

        email = self.email

        postal = self.postal

        phone_number = self.phone_number

        bank_name = self.bank_name

        bank_account = self.bank_account

        vat_code = self.vat_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if address is not UNSET:
            field_dict["address"] = address
        if country is not UNSET:
            field_dict["country"] = country
        if country_name is not UNSET:
            field_dict["country_name"] = country_name
        if email is not UNSET:
            field_dict["email"] = email
        if postal is not UNSET:
            field_dict["postal"] = postal
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if bank_name is not UNSET:
            field_dict["bank_name"] = bank_name
        if bank_account is not UNSET:
            field_dict["bank_account"] = bank_account
        if vat_code is not UNSET:
            field_dict["vat_code"] = vat_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        address = d.pop("address", UNSET)

        country = d.pop("country", UNSET)

        def _parse_country_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        country_name = _parse_country_name(d.pop("country_name", UNSET))

        email = d.pop("email", UNSET)

        postal = d.pop("postal", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        bank_name = d.pop("bank_name", UNSET)

        bank_account = d.pop("bank_account", UNSET)

        vat_code = d.pop("vat_code", UNSET)

        customer_details = cls(
            name=name,
            address=address,
            country=country,
            country_name=country_name,
            email=email,
            postal=postal,
            phone_number=phone_number,
            bank_name=bank_name,
            bank_account=bank_account,
            vat_code=vat_code,
        )

        customer_details.additional_properties = d
        return customer_details

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
