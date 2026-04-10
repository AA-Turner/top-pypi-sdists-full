from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserResidenceCountryStats")


@_attrs_define
class UserResidenceCountryStats:
    """
    Attributes:
        country_of_residence (str): Country of residence code
        count (int): Number of users
    """

    country_of_residence: str
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        country_of_residence = self.country_of_residence

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "country_of_residence": country_of_residence,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        country_of_residence = d.pop("country_of_residence")

        count = d.pop("count")

        user_residence_country_stats = cls(
            country_of_residence=country_of_residence,
            count=count,
        )

        user_residence_country_stats.additional_properties = d
        return user_residence_country_stats

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
