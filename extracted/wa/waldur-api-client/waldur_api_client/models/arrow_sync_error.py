from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowSyncError")


@_attrs_define
class ArrowSyncError:
    """
    Attributes:
        error (Union[Unset, str]):
        period (Union[Unset, str]):
        subscription_id (Union[Unset, str]):
        customer_id (Union[Unset, str]):
    """

    error: Union[Unset, str] = UNSET
    period: Union[Unset, str] = UNSET
    subscription_id: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        period = self.period

        subscription_id = self.subscription_id

        customer_id = self.customer_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if period is not UNSET:
            field_dict["period"] = period
        if subscription_id is not UNSET:
            field_dict["subscription_id"] = subscription_id
        if customer_id is not UNSET:
            field_dict["customer_id"] = customer_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error", UNSET)

        period = d.pop("period", UNSET)

        subscription_id = d.pop("subscription_id", UNSET)

        customer_id = d.pop("customer_id", UNSET)

        arrow_sync_error = cls(
            error=error,
            period=period,
            subscription_id=subscription_id,
            customer_id=customer_id,
        )

        arrow_sync_error.additional_properties = d
        return arrow_sync_error

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
