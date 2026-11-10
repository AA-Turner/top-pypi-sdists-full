import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.compensate_in_enum import CompensateInEnum
from ..models.minimal_consumption_logic_enum import MinimalConsumptionLogicEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectCreditRequest")


@_attrs_define
class ProjectCreditRequest:
    """
    Attributes:
        project (str):
        value (Union[Unset, str]):
        end_date (Union[None, Unset, datetime.date]):
        expected_consumption (Union[Unset, str]):
        minimal_consumption_logic (Union[Unset, MinimalConsumptionLogicEnum]):
        grace_coefficient (Union[Unset, str]):
        apply_as_minimal_consumption (Union[Unset, bool]):
        mark_unused_credit_as_spent_on_project_termination (Union[Unset, bool]):
        pay_earlier_invoices (Union[Unset, bool]): Also pay the cost of earlier, closed invoices of the project that no
            credit covered. Staff only.
        earlier_invoices_from (Union[None, Unset, datetime.date]): First month of earlier invoices to pay, as its first
            day. Empty: from the first invoice.
        earlier_invoices_until (Union[None, Unset, datetime.date]): Last month of earlier invoices to pay, as its first
            day. Empty: up to the last closed invoice.
        earlier_invoices_compensate_in (Union[Unset, CompensateInEnum]):
    """

    project: str
    value: Union[Unset, str] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    expected_consumption: Union[Unset, str] = UNSET
    minimal_consumption_logic: Union[Unset, MinimalConsumptionLogicEnum] = UNSET
    grace_coefficient: Union[Unset, str] = UNSET
    apply_as_minimal_consumption: Union[Unset, bool] = UNSET
    mark_unused_credit_as_spent_on_project_termination: Union[Unset, bool] = UNSET
    pay_earlier_invoices: Union[Unset, bool] = UNSET
    earlier_invoices_from: Union[None, Unset, datetime.date] = UNSET
    earlier_invoices_until: Union[None, Unset, datetime.date] = UNSET
    earlier_invoices_compensate_in: Union[Unset, CompensateInEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

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

        mark_unused_credit_as_spent_on_project_termination = self.mark_unused_credit_as_spent_on_project_termination

        pay_earlier_invoices = self.pay_earlier_invoices

        earlier_invoices_from: Union[None, Unset, str]
        if isinstance(self.earlier_invoices_from, Unset):
            earlier_invoices_from = UNSET
        elif isinstance(self.earlier_invoices_from, datetime.date):
            earlier_invoices_from = self.earlier_invoices_from.isoformat()
        else:
            earlier_invoices_from = self.earlier_invoices_from

        earlier_invoices_until: Union[None, Unset, str]
        if isinstance(self.earlier_invoices_until, Unset):
            earlier_invoices_until = UNSET
        elif isinstance(self.earlier_invoices_until, datetime.date):
            earlier_invoices_until = self.earlier_invoices_until.isoformat()
        else:
            earlier_invoices_until = self.earlier_invoices_until

        earlier_invoices_compensate_in: Union[Unset, str] = UNSET
        if not isinstance(self.earlier_invoices_compensate_in, Unset):
            earlier_invoices_compensate_in = self.earlier_invoices_compensate_in.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
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
        if mark_unused_credit_as_spent_on_project_termination is not UNSET:
            field_dict["mark_unused_credit_as_spent_on_project_termination"] = (
                mark_unused_credit_as_spent_on_project_termination
            )
        if pay_earlier_invoices is not UNSET:
            field_dict["pay_earlier_invoices"] = pay_earlier_invoices
        if earlier_invoices_from is not UNSET:
            field_dict["earlier_invoices_from"] = earlier_invoices_from
        if earlier_invoices_until is not UNSET:
            field_dict["earlier_invoices_until"] = earlier_invoices_until
        if earlier_invoices_compensate_in is not UNSET:
            field_dict["earlier_invoices_compensate_in"] = earlier_invoices_compensate_in

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project")

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

        mark_unused_credit_as_spent_on_project_termination = d.pop(
            "mark_unused_credit_as_spent_on_project_termination", UNSET
        )

        pay_earlier_invoices = d.pop("pay_earlier_invoices", UNSET)

        def _parse_earlier_invoices_from(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                earlier_invoices_from_type_0 = isoparse(data).date()

                return earlier_invoices_from_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        earlier_invoices_from = _parse_earlier_invoices_from(d.pop("earlier_invoices_from", UNSET))

        def _parse_earlier_invoices_until(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                earlier_invoices_until_type_0 = isoparse(data).date()

                return earlier_invoices_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        earlier_invoices_until = _parse_earlier_invoices_until(d.pop("earlier_invoices_until", UNSET))

        _earlier_invoices_compensate_in = d.pop("earlier_invoices_compensate_in", UNSET)
        earlier_invoices_compensate_in: Union[Unset, CompensateInEnum]
        if isinstance(_earlier_invoices_compensate_in, Unset):
            earlier_invoices_compensate_in = UNSET
        else:
            earlier_invoices_compensate_in = CompensateInEnum(_earlier_invoices_compensate_in)

        project_credit_request = cls(
            project=project,
            value=value,
            end_date=end_date,
            expected_consumption=expected_consumption,
            minimal_consumption_logic=minimal_consumption_logic,
            grace_coefficient=grace_coefficient,
            apply_as_minimal_consumption=apply_as_minimal_consumption,
            mark_unused_credit_as_spent_on_project_termination=mark_unused_credit_as_spent_on_project_termination,
            pay_earlier_invoices=pay_earlier_invoices,
            earlier_invoices_from=earlier_invoices_from,
            earlier_invoices_until=earlier_invoices_until,
            earlier_invoices_compensate_in=earlier_invoices_compensate_in,
        )

        project_credit_request.additional_properties = d
        return project_credit_request

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
