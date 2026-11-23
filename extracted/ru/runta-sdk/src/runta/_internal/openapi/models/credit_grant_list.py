from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.credit_grant import CreditGrant


T = TypeVar("T", bound="CreditGrantList")


@_attrs_define
class CreditGrantList:
    """
    Attributes:
        credit_grants (list[CreditGrant]):
    """

    credit_grants: list[CreditGrant]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credit_grants = []
        for credit_grants_item_data in self.credit_grants:
            credit_grants_item = credit_grants_item_data.to_dict()
            credit_grants.append(credit_grants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "credit_grants": credit_grants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.credit_grant import CreditGrant

        d = dict(src_dict)
        credit_grants = []
        _credit_grants = d.pop("credit_grants")
        for credit_grants_item_data in _credit_grants:
            credit_grants_item = CreditGrant.from_dict(credit_grants_item_data)

            credit_grants.append(credit_grants_item)

        credit_grant_list = cls(
            credit_grants=credit_grants,
        )

        credit_grant_list.additional_properties = d
        return credit_grant_list

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
