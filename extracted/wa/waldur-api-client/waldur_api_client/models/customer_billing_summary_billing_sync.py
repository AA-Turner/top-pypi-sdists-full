import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CustomerBillingSummaryBillingSync")


@_attrs_define
class CustomerBillingSummaryBillingSync:
    """
    Attributes:
        uuid (UUID):
        report_period (str):
        state (str):
        sell_total (Union[None, str]):
        items_count (int):
        created (datetime.datetime):
    """

    uuid: UUID
    report_period: str
    state: str
    sell_total: Union[None, str]
    items_count: int
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        report_period = self.report_period

        state = self.state

        sell_total: Union[None, str]
        sell_total = self.sell_total

        items_count = self.items_count

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "report_period": report_period,
                "state": state,
                "sell_total": sell_total,
                "items_count": items_count,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        report_period = d.pop("report_period")

        state = d.pop("state")

        def _parse_sell_total(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sell_total = _parse_sell_total(d.pop("sell_total"))

        items_count = d.pop("items_count")

        created = isoparse(d.pop("created"))

        customer_billing_summary_billing_sync = cls(
            uuid=uuid,
            report_period=report_period,
            state=state,
            sell_total=sell_total,
            items_count=items_count,
            created=created,
        )

        customer_billing_summary_billing_sync.additional_properties = d
        return customer_billing_summary_billing_sync

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
