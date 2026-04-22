from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cancelled_run_info import CancelledRunInfo


T = TypeVar("T", bound="BulkCancelResponse")


@_attrs_define
class BulkCancelResponse:
    """
    Attributes:
        cancelled (list['CancelledRunInfo']): Runs that were cancelled (or would be in dry-run mode).
        not_running (list[str]): Job refs that had no active run to cancel.
    """

    cancelled: list["CancelledRunInfo"]
    not_running: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cancelled = []
        for cancelled_item_data in self.cancelled:
            cancelled_item = cancelled_item_data.to_dict()
            cancelled.append(cancelled_item)

        not_running = self.not_running

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cancelled": cancelled,
                "not_running": not_running,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cancelled_run_info import CancelledRunInfo

        d = dict(src_dict)
        cancelled = []
        _cancelled = d.pop("cancelled")
        for cancelled_item_data in _cancelled:
            cancelled_item = CancelledRunInfo.from_dict(cancelled_item_data)

            cancelled.append(cancelled_item)

        not_running = cast(list[str], d.pop("not_running"))

        bulk_cancel_response = cls(
            cancelled=cancelled,
            not_running=not_running,
        )

        bulk_cancel_response.additional_properties = d
        return bulk_cancel_response

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
