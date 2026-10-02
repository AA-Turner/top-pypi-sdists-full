import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.arrow_billing_sync_state_enum import ArrowBillingSyncStateEnum

if TYPE_CHECKING:
    from ..models.arrow_billing_sync_item import ArrowBillingSyncItem


T = TypeVar("T", bound="ArrowBillingSync")


@_attrs_define
class ArrowBillingSync:
    """
    Attributes:
        uuid (UUID):
        url (str):
        customer_mapping (str):
        customer_mapping_uuid (UUID):
        arrow_reference (str): Arrow customer ID (e.g., 'XSP661245')
        waldur_customer_name (str):
        statement_reference (str): Arrow statement ID
        report_period (str): Report period in YYYY-MM format
        arrow_state (str): Arrow billing state (pending/validated)
        state (ArrowBillingSyncStateEnum):
        state_display (str):
        buy_total (str): Total buy amount
        sell_total (str): Total sell amount
        currency (str): Currency code
        invoice_uuid (UUID):
        error_message (str): Error message if sync failed
        synced_at (Union[None, datetime.datetime]): When billing was last synced
        validated_at (Union[None, datetime.datetime]): When Arrow validated the billing
        reconciled_at (Union[None, datetime.datetime]): When reconciliation was applied
        items (list['ArrowBillingSyncItem']):
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    url: str
    customer_mapping: str
    customer_mapping_uuid: UUID
    arrow_reference: str
    waldur_customer_name: str
    statement_reference: str
    report_period: str
    arrow_state: str
    state: ArrowBillingSyncStateEnum
    state_display: str
    buy_total: str
    sell_total: str
    currency: str
    invoice_uuid: UUID
    error_message: str
    synced_at: Union[None, datetime.datetime]
    validated_at: Union[None, datetime.datetime]
    reconciled_at: Union[None, datetime.datetime]
    items: list["ArrowBillingSyncItem"]
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        customer_mapping = self.customer_mapping

        customer_mapping_uuid = str(self.customer_mapping_uuid)

        arrow_reference = self.arrow_reference

        waldur_customer_name = self.waldur_customer_name

        statement_reference = self.statement_reference

        report_period = self.report_period

        arrow_state = self.arrow_state

        state = self.state.value

        state_display = self.state_display

        buy_total = self.buy_total

        sell_total = self.sell_total

        currency = self.currency

        invoice_uuid = str(self.invoice_uuid)

        error_message = self.error_message

        synced_at: Union[None, str]
        if isinstance(self.synced_at, datetime.datetime):
            synced_at = self.synced_at.isoformat()
        else:
            synced_at = self.synced_at

        validated_at: Union[None, str]
        if isinstance(self.validated_at, datetime.datetime):
            validated_at = self.validated_at.isoformat()
        else:
            validated_at = self.validated_at

        reconciled_at: Union[None, str]
        if isinstance(self.reconciled_at, datetime.datetime):
            reconciled_at = self.reconciled_at.isoformat()
        else:
            reconciled_at = self.reconciled_at

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "customer_mapping": customer_mapping,
                "customer_mapping_uuid": customer_mapping_uuid,
                "arrow_reference": arrow_reference,
                "waldur_customer_name": waldur_customer_name,
                "statement_reference": statement_reference,
                "report_period": report_period,
                "arrow_state": arrow_state,
                "state": state,
                "state_display": state_display,
                "buy_total": buy_total,
                "sell_total": sell_total,
                "currency": currency,
                "invoice_uuid": invoice_uuid,
                "error_message": error_message,
                "synced_at": synced_at,
                "validated_at": validated_at,
                "reconciled_at": reconciled_at,
                "items": items,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_billing_sync_item import ArrowBillingSyncItem

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        customer_mapping = d.pop("customer_mapping")

        customer_mapping_uuid = UUID(d.pop("customer_mapping_uuid"))

        arrow_reference = d.pop("arrow_reference")

        waldur_customer_name = d.pop("waldur_customer_name")

        statement_reference = d.pop("statement_reference")

        report_period = d.pop("report_period")

        arrow_state = d.pop("arrow_state")

        state = ArrowBillingSyncStateEnum(d.pop("state"))

        state_display = d.pop("state_display")

        buy_total = d.pop("buy_total")

        sell_total = d.pop("sell_total")

        currency = d.pop("currency")

        invoice_uuid = UUID(d.pop("invoice_uuid"))

        error_message = d.pop("error_message")

        def _parse_synced_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synced_at_type_0 = isoparse(data)

                return synced_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        synced_at = _parse_synced_at(d.pop("synced_at"))

        def _parse_validated_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                validated_at_type_0 = isoparse(data)

                return validated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        validated_at = _parse_validated_at(d.pop("validated_at"))

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

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ArrowBillingSyncItem.from_dict(items_item_data)

            items.append(items_item)

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        arrow_billing_sync = cls(
            uuid=uuid,
            url=url,
            customer_mapping=customer_mapping,
            customer_mapping_uuid=customer_mapping_uuid,
            arrow_reference=arrow_reference,
            waldur_customer_name=waldur_customer_name,
            statement_reference=statement_reference,
            report_period=report_period,
            arrow_state=arrow_state,
            state=state,
            state_display=state_display,
            buy_total=buy_total,
            sell_total=sell_total,
            currency=currency,
            invoice_uuid=invoice_uuid,
            error_message=error_message,
            synced_at=synced_at,
            validated_at=validated_at,
            reconciled_at=reconciled_at,
            items=items,
            created=created,
            modified=modified,
        )

        arrow_billing_sync.additional_properties = d
        return arrow_billing_sync

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
