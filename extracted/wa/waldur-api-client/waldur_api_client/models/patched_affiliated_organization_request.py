from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedAffiliatedOrganizationRequest")


@_attrs_define
class PatchedAffiliatedOrganizationRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        code (Union[Unset, str]): Unique short identifier, e.g. CERN, EMBL.
        abbreviation (Union[Unset, str]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        homepage (Union[Unset, str]):
        country (Union[Unset, str]):
        address (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    abbreviation: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    homepage: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code = self.code

        abbreviation = self.abbreviation

        description = self.description

        email = self.email

        homepage = self.homepage

        country = self.country

        address = self.address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if code is not UNSET:
            field_dict["code"] = code
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if description is not UNSET:
            field_dict["description"] = description
        if email is not UNSET:
            field_dict["email"] = email
        if homepage is not UNSET:
            field_dict["homepage"] = homepage
        if country is not UNSET:
            field_dict["country"] = country
        if address is not UNSET:
            field_dict["address"] = address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        code = d.pop("code", UNSET)

        abbreviation = d.pop("abbreviation", UNSET)

        description = d.pop("description", UNSET)

        email = d.pop("email", UNSET)

        homepage = d.pop("homepage", UNSET)

        country = d.pop("country", UNSET)

        address = d.pop("address", UNSET)

        patched_affiliated_organization_request = cls(
            name=name,
            code=code,
            abbreviation=abbreviation,
            description=description,
            email=email,
            homepage=homepage,
            country=country,
            address=address,
        )

        patched_affiliated_organization_request.additional_properties = d
        return patched_affiliated_organization_request

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
