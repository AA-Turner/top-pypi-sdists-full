from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_account_options import ProviderAccountOptions


T = TypeVar("T", bound="AccountOptionsVersions")


@_attrs_define
class AccountOptionsVersions:
    """
    Attributes:
        current (ProviderAccountOptions):
        proposed (ProviderAccountOptions):
    """

    current: "ProviderAccountOptions"
    proposed: "ProviderAccountOptions"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current = self.current.to_dict()

        proposed = self.proposed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current": current,
                "proposed": proposed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_account_options import ProviderAccountOptions

        d = dict(src_dict)
        current = ProviderAccountOptions.from_dict(d.pop("current"))

        proposed = ProviderAccountOptions.from_dict(d.pop("proposed"))

        account_options_versions = cls(
            current=current,
            proposed=proposed,
        )

        account_options_versions.additional_properties = d
        return account_options_versions

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
