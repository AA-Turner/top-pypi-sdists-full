from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.hpc_monthly_usage import HpcMonthlyUsage


T = TypeVar("T", bound="HpcUserUsage")


@_attrs_define
class HpcUserUsage:
    """
    Attributes:
        username (str):
        total (float):
        monthly (list['HpcMonthlyUsage']):
    """

    username: str
    total: float
    monthly: list["HpcMonthlyUsage"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        total = self.total

        monthly = []
        for monthly_item_data in self.monthly:
            monthly_item = monthly_item_data.to_dict()
            monthly.append(monthly_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "total": total,
                "monthly": monthly,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hpc_monthly_usage import HpcMonthlyUsage

        d = dict(src_dict)
        username = d.pop("username")

        total = d.pop("total")

        monthly = []
        _monthly = d.pop("monthly")
        for monthly_item_data in _monthly:
            monthly_item = HpcMonthlyUsage.from_dict(monthly_item_data)

            monthly.append(monthly_item)

        hpc_user_usage = cls(
            username=username,
            total=total,
            monthly=monthly,
        )

        hpc_user_usage.additional_properties = d
        return hpc_user_usage

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
