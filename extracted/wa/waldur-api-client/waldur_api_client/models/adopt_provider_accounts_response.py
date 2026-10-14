from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AdoptProviderAccountsResponse")


@_attrs_define
class AdoptProviderAccountsResponse:
    """
    Attributes:
        adopted (int): Provider accounts created.
        backed (int): Offering accounts now reading through a provider account.
    """

    adopted: int
    backed: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        adopted = self.adopted

        backed = self.backed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "adopted": adopted,
                "backed": backed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        adopted = d.pop("adopted")

        backed = d.pop("backed")

        adopt_provider_accounts_response = cls(
            adopted=adopted,
            backed=backed,
        )

        adopt_provider_accounts_response.additional_properties = d
        return adopt_provider_accounts_response

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
