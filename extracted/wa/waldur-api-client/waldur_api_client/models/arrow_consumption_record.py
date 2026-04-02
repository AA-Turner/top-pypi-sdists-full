import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ArrowConsumptionRecord")


@_attrs_define
class ArrowConsumptionRecord:
    """
    Attributes:
        uuid (UUID):
        url (str):
        resource (str):
        resource_uuid (UUID):
        resource_name (str):
        project_uuid (UUID):
        project_name (str):
        customer_uuid (UUID):
        customer_name (str):
        license_reference (str): Arrow license reference (e.g., 'XSP12345')
        billing_period (datetime.date): First day of the billing month
        consumed_sell (str): Consumed sell amount from Consumption API
        consumed_buy (str): Consumed buy amount from Consumption API
        final_sell (Union[None, str]): Final sell amount from billing export
        final_buy (Union[None, str]): Final buy amount from billing export
        invoice_item_uuid (UUID):
        compensation_item_uuid (UUID):
        last_sync_at (Union[None, datetime.datetime]): When consumption was last synced from API
        finalized_at (Union[None, datetime.datetime]): When billing export data arrived
        reconciled_at (Union[None, datetime.datetime]): When reconciliation was applied
        is_finalized (bool):
        is_reconciled (bool):
        adjustment_amount (Union[None, str]):
        raw_data (Any): Raw consumption data for debugging
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    url: str
    resource: str
    resource_uuid: UUID
    resource_name: str
    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    license_reference: str
    billing_period: datetime.date
    consumed_sell: str
    consumed_buy: str
    final_sell: Union[None, str]
    final_buy: Union[None, str]
    invoice_item_uuid: UUID
    compensation_item_uuid: UUID
    last_sync_at: Union[None, datetime.datetime]
    finalized_at: Union[None, datetime.datetime]
    reconciled_at: Union[None, datetime.datetime]
    is_finalized: bool
    is_reconciled: bool
    adjustment_amount: Union[None, str]
    raw_data: Any
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        resource = self.resource

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        license_reference = self.license_reference

        billing_period = self.billing_period.isoformat()

        consumed_sell = self.consumed_sell

        consumed_buy = self.consumed_buy

        final_sell: Union[None, str]
        final_sell = self.final_sell

        final_buy: Union[None, str]
        final_buy = self.final_buy

        invoice_item_uuid = str(self.invoice_item_uuid)

        compensation_item_uuid = str(self.compensation_item_uuid)

        last_sync_at: Union[None, str]
        if isinstance(self.last_sync_at, datetime.datetime):
            last_sync_at = self.last_sync_at.isoformat()
        else:
            last_sync_at = self.last_sync_at

        finalized_at: Union[None, str]
        if isinstance(self.finalized_at, datetime.datetime):
            finalized_at = self.finalized_at.isoformat()
        else:
            finalized_at = self.finalized_at

        reconciled_at: Union[None, str]
        if isinstance(self.reconciled_at, datetime.datetime):
            reconciled_at = self.reconciled_at.isoformat()
        else:
            reconciled_at = self.reconciled_at

        is_finalized = self.is_finalized

        is_reconciled = self.is_reconciled

        adjustment_amount: Union[None, str]
        adjustment_amount = self.adjustment_amount

        raw_data = self.raw_data

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "resource": resource,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "license_reference": license_reference,
                "billing_period": billing_period,
                "consumed_sell": consumed_sell,
                "consumed_buy": consumed_buy,
                "final_sell": final_sell,
                "final_buy": final_buy,
                "invoice_item_uuid": invoice_item_uuid,
                "compensation_item_uuid": compensation_item_uuid,
                "last_sync_at": last_sync_at,
                "finalized_at": finalized_at,
                "reconciled_at": reconciled_at,
                "is_finalized": is_finalized,
                "is_reconciled": is_reconciled,
                "adjustment_amount": adjustment_amount,
                "raw_data": raw_data,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        resource = d.pop("resource")

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        license_reference = d.pop("license_reference")

        billing_period = isoparse(d.pop("billing_period")).date()

        consumed_sell = d.pop("consumed_sell")

        consumed_buy = d.pop("consumed_buy")

        def _parse_final_sell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        final_sell = _parse_final_sell(d.pop("final_sell"))

        def _parse_final_buy(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        final_buy = _parse_final_buy(d.pop("final_buy"))

        invoice_item_uuid = UUID(d.pop("invoice_item_uuid"))

        compensation_item_uuid = UUID(d.pop("compensation_item_uuid"))

        def _parse_last_sync_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sync_at_type_0 = isoparse(data)

                return last_sync_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_sync_at = _parse_last_sync_at(d.pop("last_sync_at"))

        def _parse_finalized_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finalized_at_type_0 = isoparse(data)

                return finalized_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        finalized_at = _parse_finalized_at(d.pop("finalized_at"))

        def _parse_reconciled_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reconciled_at_type_0 = isoparse(data)

                return reconciled_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reconciled_at = _parse_reconciled_at(d.pop("reconciled_at"))

        is_finalized = d.pop("is_finalized")

        is_reconciled = d.pop("is_reconciled")

        def _parse_adjustment_amount(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        adjustment_amount = _parse_adjustment_amount(d.pop("adjustment_amount"))

        raw_data = d.pop("raw_data")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        arrow_consumption_record = cls(
            uuid=uuid,
            url=url,
            resource=resource,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            license_reference=license_reference,
            billing_period=billing_period,
            consumed_sell=consumed_sell,
            consumed_buy=consumed_buy,
            final_sell=final_sell,
            final_buy=final_buy,
            invoice_item_uuid=invoice_item_uuid,
            compensation_item_uuid=compensation_item_uuid,
            last_sync_at=last_sync_at,
            finalized_at=finalized_at,
            reconciled_at=reconciled_at,
            is_finalized=is_finalized,
            is_reconciled=is_reconciled,
            adjustment_amount=adjustment_amount,
            raw_data=raw_data,
            created=created,
            modified=modified,
        )

        arrow_consumption_record.additional_properties = d
        return arrow_consumption_record

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
