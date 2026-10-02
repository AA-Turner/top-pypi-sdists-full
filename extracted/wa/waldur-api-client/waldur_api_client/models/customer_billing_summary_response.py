from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.customer_billing_summary_billing_sync import CustomerBillingSummaryBillingSync
    from ..models.customer_billing_summary_consumption_record import CustomerBillingSummaryConsumptionRecord


T = TypeVar("T", bound="CustomerBillingSummaryResponse")


@_attrs_define
class CustomerBillingSummaryResponse:
    """
    Attributes:
        customer_mapping_uuid (UUID):
        arrow_reference (str):
        arrow_company_name (str):
        waldur_customer_uuid (UUID):
        waldur_customer_name (str):
        total_consumption_records (int):
        total_consumed_sell (str):
        total_final_sell (Union[None, str]):
        pending_records (int):
        finalized_records (int):
        reconciled_records (int):
        total_billing_syncs (int):
        total_billing_sell (Union[None, str]):
        recent_consumption_records (list['CustomerBillingSummaryConsumptionRecord']):
        recent_billing_syncs (list['CustomerBillingSummaryBillingSync']):
    """

    customer_mapping_uuid: UUID
    arrow_reference: str
    arrow_company_name: str
    waldur_customer_uuid: UUID
    waldur_customer_name: str
    total_consumption_records: int
    total_consumed_sell: str
    total_final_sell: Union[None, str]
    pending_records: int
    finalized_records: int
    reconciled_records: int
    total_billing_syncs: int
    total_billing_sell: Union[None, str]
    recent_consumption_records: list["CustomerBillingSummaryConsumptionRecord"]
    recent_billing_syncs: list["CustomerBillingSummaryBillingSync"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_mapping_uuid = str(self.customer_mapping_uuid)

        arrow_reference = self.arrow_reference

        arrow_company_name = self.arrow_company_name

        waldur_customer_uuid = str(self.waldur_customer_uuid)

        waldur_customer_name = self.waldur_customer_name

        total_consumption_records = self.total_consumption_records

        total_consumed_sell = self.total_consumed_sell

        total_final_sell: Union[None, str]
        total_final_sell = self.total_final_sell

        pending_records = self.pending_records

        finalized_records = self.finalized_records

        reconciled_records = self.reconciled_records

        total_billing_syncs = self.total_billing_syncs

        total_billing_sell: Union[None, str]
        total_billing_sell = self.total_billing_sell

        recent_consumption_records = []
        for recent_consumption_records_item_data in self.recent_consumption_records:
            recent_consumption_records_item = recent_consumption_records_item_data.to_dict()
            recent_consumption_records.append(recent_consumption_records_item)

        recent_billing_syncs = []
        for recent_billing_syncs_item_data in self.recent_billing_syncs:
            recent_billing_syncs_item = recent_billing_syncs_item_data.to_dict()
            recent_billing_syncs.append(recent_billing_syncs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_mapping_uuid": customer_mapping_uuid,
                "arrow_reference": arrow_reference,
                "arrow_company_name": arrow_company_name,
                "waldur_customer_uuid": waldur_customer_uuid,
                "waldur_customer_name": waldur_customer_name,
                "total_consumption_records": total_consumption_records,
                "total_consumed_sell": total_consumed_sell,
                "total_final_sell": total_final_sell,
                "pending_records": pending_records,
                "finalized_records": finalized_records,
                "reconciled_records": reconciled_records,
                "total_billing_syncs": total_billing_syncs,
                "total_billing_sell": total_billing_sell,
                "recent_consumption_records": recent_consumption_records,
                "recent_billing_syncs": recent_billing_syncs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_billing_summary_billing_sync import CustomerBillingSummaryBillingSync
        from ..models.customer_billing_summary_consumption_record import CustomerBillingSummaryConsumptionRecord

        d = dict(src_dict)
        customer_mapping_uuid = UUID(d.pop("customer_mapping_uuid"))

        arrow_reference = d.pop("arrow_reference")

        arrow_company_name = d.pop("arrow_company_name")

        waldur_customer_uuid = UUID(d.pop("waldur_customer_uuid"))

        waldur_customer_name = d.pop("waldur_customer_name")

        total_consumption_records = d.pop("total_consumption_records")

        total_consumed_sell = d.pop("total_consumed_sell")

        def _parse_total_final_sell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        total_final_sell = _parse_total_final_sell(d.pop("total_final_sell"))

        pending_records = d.pop("pending_records")

        finalized_records = d.pop("finalized_records")

        reconciled_records = d.pop("reconciled_records")

        total_billing_syncs = d.pop("total_billing_syncs")

        def _parse_total_billing_sell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        total_billing_sell = _parse_total_billing_sell(d.pop("total_billing_sell"))

        recent_consumption_records = []
        _recent_consumption_records = d.pop("recent_consumption_records")
        for recent_consumption_records_item_data in _recent_consumption_records:
            recent_consumption_records_item = CustomerBillingSummaryConsumptionRecord.from_dict(
                recent_consumption_records_item_data
            )

            recent_consumption_records.append(recent_consumption_records_item)

        recent_billing_syncs = []
        _recent_billing_syncs = d.pop("recent_billing_syncs")
        for recent_billing_syncs_item_data in _recent_billing_syncs:
            recent_billing_syncs_item = CustomerBillingSummaryBillingSync.from_dict(recent_billing_syncs_item_data)

            recent_billing_syncs.append(recent_billing_syncs_item)

        customer_billing_summary_response = cls(
            customer_mapping_uuid=customer_mapping_uuid,
            arrow_reference=arrow_reference,
            arrow_company_name=arrow_company_name,
            waldur_customer_uuid=waldur_customer_uuid,
            waldur_customer_name=waldur_customer_name,
            total_consumption_records=total_consumption_records,
            total_consumed_sell=total_consumed_sell,
            total_final_sell=total_final_sell,
            pending_records=pending_records,
            finalized_records=finalized_records,
            reconciled_records=reconciled_records,
            total_billing_syncs=total_billing_syncs,
            total_billing_sell=total_billing_sell,
            recent_consumption_records=recent_consumption_records,
            recent_billing_syncs=recent_billing_syncs,
        )

        customer_billing_summary_response.additional_properties = d
        return customer_billing_summary_response

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
