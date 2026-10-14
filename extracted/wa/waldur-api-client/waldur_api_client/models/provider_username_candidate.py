from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProviderUsernameCandidate")


@_attrs_define
class ProviderUsernameCandidate:
    """
    Attributes:
        username (str):
        offering_count (int):
        offering_uuids (list[str]):
        has_active_resources (bool):
        home_directories (list[str]):
    """

    username: str
    offering_count: int
    offering_uuids: list[str]
    has_active_resources: bool
    home_directories: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        offering_count = self.offering_count

        offering_uuids = self.offering_uuids

        has_active_resources = self.has_active_resources

        home_directories = self.home_directories

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "offering_count": offering_count,
                "offering_uuids": offering_uuids,
                "has_active_resources": has_active_resources,
                "home_directories": home_directories,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        offering_count = d.pop("offering_count")

        offering_uuids = cast(list[str], d.pop("offering_uuids"))

        has_active_resources = d.pop("has_active_resources")

        home_directories = cast(list[str], d.pop("home_directories"))

        provider_username_candidate = cls(
            username=username,
            offering_count=offering_count,
            offering_uuids=offering_uuids,
            has_active_resources=has_active_resources,
            home_directories=home_directories,
        )

        provider_username_candidate.additional_properties = d
        return provider_username_candidate

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
