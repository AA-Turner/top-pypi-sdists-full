import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.minimal_consumption_logic_enum import MinimalConsumptionLogicEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_provider_offering import NestedProviderOffering


T = TypeVar("T", bound="CustomerCredit")


@_attrs_define
class CustomerCredit:
    """
    Attributes:
        uuid (UUID):
        url (str):
        customer (str):
        customer_name (str):
        customer_uuid (UUID):
        customer_slug (str):
        offerings (list['NestedProviderOffering']):
        minimal_consumption (float):
        allocated_to_projects (float):
        consumption_last_month (float):
        value (Union[Unset, str]):
        end_date (Union[None, Unset, datetime.date]):
        expected_consumption (Union[Unset, str]):
        minimal_consumption_logic (Union[Unset, MinimalConsumptionLogicEnum]):
        grace_coefficient (Union[Unset, str]):
        apply_as_minimal_consumption (Union[Unset, bool]):
    """

    uuid: UUID
    url: str
    customer: str
    customer_name: str
    customer_uuid: UUID
    customer_slug: str
    offerings: list["NestedProviderOffering"]
    minimal_consumption: float
    allocated_to_projects: float
    consumption_last_month: float
    value: Union[Unset, str] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    expected_consumption: Union[Unset, str] = UNSET
    minimal_consumption_logic: Union[Unset, MinimalConsumptionLogicEnum] = UNSET
    grace_coefficient: Union[Unset, str] = UNSET
    apply_as_minimal_consumption: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        customer = self.customer

        customer_name = self.customer_name

        customer_uuid = str(self.customer_uuid)

        customer_slug = self.customer_slug

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        minimal_consumption = self.minimal_consumption

        allocated_to_projects = self.allocated_to_projects

        consumption_last_month = self.consumption_last_month

        value = self.value

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        expected_consumption = self.expected_consumption

        minimal_consumption_logic: Union[Unset, str] = UNSET
        if not isinstance(self.minimal_consumption_logic, Unset):
            minimal_consumption_logic = self.minimal_consumption_logic.value

        grace_coefficient = self.grace_coefficient

        apply_as_minimal_consumption = self.apply_as_minimal_consumption

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "customer": customer,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "customer_slug": customer_slug,
                "offerings": offerings,
                "minimal_consumption": minimal_consumption,
                "allocated_to_projects": allocated_to_projects,
                "consumption_last_month": consumption_last_month,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if expected_consumption is not UNSET:
            field_dict["expected_consumption"] = expected_consumption
        if minimal_consumption_logic is not UNSET:
            field_dict["minimal_consumption_logic"] = minimal_consumption_logic
        if grace_coefficient is not UNSET:
            field_dict["grace_coefficient"] = grace_coefficient
        if apply_as_minimal_consumption is not UNSET:
            field_dict["apply_as_minimal_consumption"] = apply_as_minimal_consumption

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_provider_offering import NestedProviderOffering

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        customer = d.pop("customer")

        customer_name = d.pop("customer_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_slug = d.pop("customer_slug")

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = NestedProviderOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        minimal_consumption = d.pop("minimal_consumption")

        allocated_to_projects = d.pop("allocated_to_projects")

        consumption_last_month = d.pop("consumption_last_month")

        value = d.pop("value", UNSET)

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        expected_consumption = d.pop("expected_consumption", UNSET)

        _minimal_consumption_logic = d.pop("minimal_consumption_logic", UNSET)
        minimal_consumption_logic: Union[Unset, MinimalConsumptionLogicEnum]
        if isinstance(_minimal_consumption_logic, Unset):
            minimal_consumption_logic = UNSET
        else:
            minimal_consumption_logic = MinimalConsumptionLogicEnum(_minimal_consumption_logic)

        grace_coefficient = d.pop("grace_coefficient", UNSET)

        apply_as_minimal_consumption = d.pop("apply_as_minimal_consumption", UNSET)

        customer_credit = cls(
            uuid=uuid,
            url=url,
            customer=customer,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            customer_slug=customer_slug,
            offerings=offerings,
            minimal_consumption=minimal_consumption,
            allocated_to_projects=allocated_to_projects,
            consumption_last_month=consumption_last_month,
            value=value,
            end_date=end_date,
            expected_consumption=expected_consumption,
            minimal_consumption_logic=minimal_consumption_logic,
            grace_coefficient=grace_coefficient,
            apply_as_minimal_consumption=apply_as_minimal_consumption,
        )

        customer_credit.additional_properties = d
        return customer_credit

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
