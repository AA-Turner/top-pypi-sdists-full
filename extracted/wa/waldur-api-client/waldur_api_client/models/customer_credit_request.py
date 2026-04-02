import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.minimal_consumption_logic_enum import MinimalConsumptionLogicEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerCreditRequest")


@_attrs_define
class CustomerCreditRequest:
    """
    Attributes:
        customer (str):
        value (Union[Unset, str]):
        end_date (Union[None, Unset, datetime.date]):
        expected_consumption (Union[Unset, str]):
        minimal_consumption_logic (Union[Unset, MinimalConsumptionLogicEnum]):
        grace_coefficient (Union[Unset, str]):
        apply_as_minimal_consumption (Union[Unset, bool]):
    """

    customer: str
    value: Union[Unset, str] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    expected_consumption: Union[Unset, str] = UNSET
    minimal_consumption_logic: Union[Unset, MinimalConsumptionLogicEnum] = UNSET
    grace_coefficient: Union[Unset, str] = UNSET
    apply_as_minimal_consumption: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer = self.customer

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
                "customer": customer,
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
        d = dict(src_dict)
        customer = d.pop("customer")

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

        customer_credit_request = cls(
            customer=customer,
            value=value,
            end_date=end_date,
            expected_consumption=expected_consumption,
            minimal_consumption_logic=minimal_consumption_logic,
            grace_coefficient=grace_coefficient,
            apply_as_minimal_consumption=apply_as_minimal_consumption,
        )

        customer_credit_request.additional_properties = d
        return customer_credit_request

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
