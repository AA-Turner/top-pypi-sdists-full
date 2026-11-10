from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        upcoming (Union['AffiliateEarningsMonth', None]): Fee the current month is expected to earn from the referred
            customer's open invoice, on the base an accrual uses: the net price after estimated volume discounts and credit
            compensation, plus what paid credit covers. Null when the month will earn nothing on this link. Not yet accrued:
            the amount changes until month close.
    """

    total_earned: str
    withdrawable_balance: str
    per_month: list["AffiliateEarningsMonth"]
    upcoming: Union["AffiliateEarningsMonth", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.affiliate_earnings_month import AffiliateEarningsMonth

        total_earned = self.total_earned

        withdrawable_balance = self.withdrawable_balance

        per_month = []
        for per_month_item_data in self.per_month:
            per_month_item = per_month_item_data.to_dict()
            per_month.append(per_month_item)

        upcoming: Union[None, dict[str, Any]]
        if isinstance(self.upcoming, AffiliateEarningsMonth):
            upcoming = self.upcoming.to_dict()
        else:
            upcoming = self.upcoming

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_earned": total_earned,
                "withdrawable_balance": withdrawable_balance,
                "per_month": per_month,
                "upcoming": upcoming,
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

        def _parse_upcoming(data: object) -> Union["AffiliateEarningsMonth", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                upcoming_type_1 = AffiliateEarningsMonth.from_dict(data)

                return upcoming_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AffiliateEarningsMonth", None], data)

        upcoming = _parse_upcoming(d.pop("upcoming"))

        affiliate_earnings = cls(
            total_earned=total_earned,
            withdrawable_balance=withdrawable_balance,
            per_month=per_month,
            upcoming=upcoming,
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
