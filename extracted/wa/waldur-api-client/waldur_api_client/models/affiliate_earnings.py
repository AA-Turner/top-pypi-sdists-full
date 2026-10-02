from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.affiliate_earnings_month import AffiliateEarningsMonth


T = TypeVar("T", bound="AffiliateEarnings")


@_attrs_define
class AffiliateEarnings:
    """
    Attributes:
        total_earned (str):
        withdrawable_balance (str):
        per_month (list['AffiliateEarningsMonth']):
    """

    total_earned: str
    withdrawable_balance: str
    per_month: list["AffiliateEarningsMonth"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_earned = self.total_earned

        withdrawable_balance = self.withdrawable_balance

        per_month = []
        for per_month_item_data in self.per_month:
            per_month_item = per_month_item_data.to_dict()
            per_month.append(per_month_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_earned": total_earned,
                "withdrawable_balance": withdrawable_balance,
                "per_month": per_month,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.affiliate_earnings_month import AffiliateEarningsMonth

        d = dict(src_dict)
        total_earned = d.pop("total_earned")

        withdrawable_balance = d.pop("withdrawable_balance")

        per_month = []
        _per_month = d.pop("per_month")
        for per_month_item_data in _per_month:
            per_month_item = AffiliateEarningsMonth.from_dict(per_month_item_data)

            per_month.append(per_month_item)

        affiliate_earnings = cls(
            total_earned=total_earned,
            withdrawable_balance=withdrawable_balance,
            per_month=per_month,
        )

        affiliate_earnings.additional_properties = d
        return affiliate_earnings

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
