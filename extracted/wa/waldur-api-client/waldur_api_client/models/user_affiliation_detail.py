from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserAffiliationDetail")


@_attrs_define
class UserAffiliationDetail:
    """
    Attributes:
        affiliation (str): Raw affiliation URN
        organization (Union[None, str]):
        country (Union[None, str]): ISO country code
        category (str):
        identifier (Union[None, str]):
        count (int): Number of users
    """

    affiliation: str
    organization: Union[None, str]
    country: Union[None, str]
    category: str
    identifier: Union[None, str]
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        affiliation = self.affiliation

        organization: Union[None, str]
        organization = self.organization

        country: Union[None, str]
        country = self.country

        category = self.category

        identifier: Union[None, str]
        identifier = self.identifier

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "affiliation": affiliation,
                "organization": organization,
                "country": country,
                "category": category,
                "identifier": identifier,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliation = d.pop("affiliation")

        def _parse_organization(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        organization = _parse_organization(d.pop("organization"))

        def _parse_country(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        country = _parse_country(d.pop("country"))

        category = d.pop("category")

        def _parse_identifier(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        identifier = _parse_identifier(d.pop("identifier"))

        count = d.pop("count")

        user_affiliation_detail = cls(
            affiliation=affiliation,
            organization=organization,
            country=country,
            category=category,
            identifier=identifier,
            count=count,
        )

        user_affiliation_detail.additional_properties = d
        return user_affiliation_detail

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
