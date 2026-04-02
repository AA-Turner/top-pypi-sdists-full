from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.arrow_billing_line import ArrowBillingLine
    from ..models.arrow_consumption_line import ArrowConsumptionLine


T = TypeVar("T", bound="FetchCustomerArrowDataResponse")


@_attrs_define
class FetchCustomerArrowDataResponse:
    """
    Attributes:
        customer_mapping_uuid (UUID):
        arrow_reference (str):
        arrow_company_name (str):
        waldur_customer_name (str):
        period (str):
        billing_available (bool):
        billing_lines (list['ArrowBillingLine']):
        billing_total_sell (Union[None, str]):
        billing_total_buy (Union[None, str]):
        consumption_lines (list['ArrowConsumptionLine']):
        consumption_total_sell (Union[None, str]):
        consumption_total_buy (Union[None, str]):
        total_customer_resources (int): Total number of resources for this customer in Waldur.
        resources_with_backend_id (int): Number of resources with backend_id set (Arrow license reference).
        matched_resources (int): Number of resources for which consumption was successfully fetched.
        error (Union[None, str]):
    """

    customer_mapping_uuid: UUID
    arrow_reference: str
    arrow_company_name: str
    waldur_customer_name: str
    period: str
    billing_available: bool
    billing_lines: list["ArrowBillingLine"]
    billing_total_sell: Union[None, str]
    billing_total_buy: Union[None, str]
    consumption_lines: list["ArrowConsumptionLine"]
    consumption_total_sell: Union[None, str]
    consumption_total_buy: Union[None, str]
    total_customer_resources: int
    resources_with_backend_id: int
    matched_resources: int
    error: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_mapping_uuid = str(self.customer_mapping_uuid)

        arrow_reference = self.arrow_reference

        arrow_company_name = self.arrow_company_name

        waldur_customer_name = self.waldur_customer_name

        period = self.period

        billing_available = self.billing_available

        billing_lines = []
        for billing_lines_item_data in self.billing_lines:
            billing_lines_item = billing_lines_item_data.to_dict()
            billing_lines.append(billing_lines_item)

        billing_total_sell: Union[None, str]
        billing_total_sell = self.billing_total_sell

        billing_total_buy: Union[None, str]
        billing_total_buy = self.billing_total_buy

        consumption_lines = []
        for consumption_lines_item_data in self.consumption_lines:
            consumption_lines_item = consumption_lines_item_data.to_dict()
            consumption_lines.append(consumption_lines_item)

        consumption_total_sell: Union[None, str]
        consumption_total_sell = self.consumption_total_sell

        consumption_total_buy: Union[None, str]
        consumption_total_buy = self.consumption_total_buy

        total_customer_resources = self.total_customer_resources

        resources_with_backend_id = self.resources_with_backend_id

        matched_resources = self.matched_resources

        error: Union[None, str]
        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_mapping_uuid": customer_mapping_uuid,
                "arrow_reference": arrow_reference,
                "arrow_company_name": arrow_company_name,
                "waldur_customer_name": waldur_customer_name,
                "period": period,
                "billing_available": billing_available,
                "billing_lines": billing_lines,
                "billing_total_sell": billing_total_sell,
                "billing_total_buy": billing_total_buy,
                "consumption_lines": consumption_lines,
                "consumption_total_sell": consumption_total_sell,
                "consumption_total_buy": consumption_total_buy,
                "total_customer_resources": total_customer_resources,
                "resources_with_backend_id": resources_with_backend_id,
                "matched_resources": matched_resources,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_billing_line import ArrowBillingLine
        from ..models.arrow_consumption_line import ArrowConsumptionLine

        d = dict(src_dict)
        customer_mapping_uuid = UUID(d.pop("customer_mapping_uuid"))

        arrow_reference = d.pop("arrow_reference")

        arrow_company_name = d.pop("arrow_company_name")

        waldur_customer_name = d.pop("waldur_customer_name")

        period = d.pop("period")

        billing_available = d.pop("billing_available")

        billing_lines = []
        _billing_lines = d.pop("billing_lines")
        for billing_lines_item_data in _billing_lines:
            billing_lines_item = ArrowBillingLine.from_dict(billing_lines_item_data)

            billing_lines.append(billing_lines_item)

        def _parse_billing_total_sell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        billing_total_sell = _parse_billing_total_sell(d.pop("billing_total_sell"))

        def _parse_billing_total_buy(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        billing_total_buy = _parse_billing_total_buy(d.pop("billing_total_buy"))

        consumption_lines = []
        _consumption_lines = d.pop("consumption_lines")
        for consumption_lines_item_data in _consumption_lines:
            consumption_lines_item = ArrowConsumptionLine.from_dict(consumption_lines_item_data)

            consumption_lines.append(consumption_lines_item)

        def _parse_consumption_total_sell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        consumption_total_sell = _parse_consumption_total_sell(d.pop("consumption_total_sell"))

        def _parse_consumption_total_buy(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        consumption_total_buy = _parse_consumption_total_buy(d.pop("consumption_total_buy"))

        total_customer_resources = d.pop("total_customer_resources")

        resources_with_backend_id = d.pop("resources_with_backend_id")

        matched_resources = d.pop("matched_resources")

        def _parse_error(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        error = _parse_error(d.pop("error"))

        fetch_customer_arrow_data_response = cls(
            customer_mapping_uuid=customer_mapping_uuid,
            arrow_reference=arrow_reference,
            arrow_company_name=arrow_company_name,
            waldur_customer_name=waldur_customer_name,
            period=period,
            billing_available=billing_available,
            billing_lines=billing_lines,
            billing_total_sell=billing_total_sell,
            billing_total_buy=billing_total_buy,
            consumption_lines=consumption_lines,
            consumption_total_sell=consumption_total_sell,
            consumption_total_buy=consumption_total_buy,
            total_customer_resources=total_customer_resources,
            resources_with_backend_id=resources_with_backend_id,
            matched_resources=matched_resources,
            error=error,
        )

        fetch_customer_arrow_data_response.additional_properties = d
        return fetch_customer_arrow_data_response

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
