import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CustomerBillingSummaryConsumptionRecord")


@_attrs_define
class CustomerBillingSummaryConsumptionRecord:
    """
    Attributes:
        uuid (UUID):
        license_reference (str):
        resource_name (Union[None, str]):
        billing_period (datetime.date):
        consumed_sell (str):
        final_sell (Union[None, str]):
        is_finalized (bool):
        is_reconciled (bool):
    """

    uuid: UUID
    license_reference: str
    resource_name: Union[None, str]
    billing_period: datetime.date
    consumed_sell: str
    final_sell: Union[None, str]
    is_finalized: bool
    is_reconciled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        license_reference = self.license_reference

        resource_name: Union[None, str]
        resource_name = self.resource_name

        billing_period = self.billing_period.isoformat()

        consumed_sell = self.consumed_sell

        final_sell: Union[None, str]
        final_sell = self.final_sell

        is_finalized = self.is_finalized

        is_reconciled = self.is_reconciled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "license_reference": license_reference,
                "resource_name": resource_name,
                "billing_period": billing_period,
                "consumed_sell": consumed_sell,
                "final_sell": final_sell,
                "is_finalized": is_finalized,
                "is_reconciled": is_reconciled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        license_reference = d.pop("license_reference")

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        billing_period = isoparse(d.pop("billing_period")).date()

        consumed_sell = d.pop("consumed_sell")

        def _parse_final_sell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        final_sell = _parse_final_sell(d.pop("final_sell"))

        is_finalized = d.pop("is_finalized")

        is_reconciled = d.pop("is_reconciled")

        customer_billing_summary_consumption_record = cls(
            uuid=uuid,
            license_reference=license_reference,
            resource_name=resource_name,
            billing_period=billing_period,
            consumed_sell=consumed_sell,
            final_sell=final_sell,
            is_finalized=is_finalized,
            is_reconciled=is_reconciled,
        )

        customer_billing_summary_consumption_record.additional_properties = d
        return customer_billing_summary_consumption_record

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
