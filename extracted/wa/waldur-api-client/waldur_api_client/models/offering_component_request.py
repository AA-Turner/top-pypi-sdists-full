from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_type_enum import BillingTypeEnum
from ..models.blank_enum import BlankEnum
from ..models.limit_period_enum import LimitPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingComponentRequest")


@_attrs_define
class OfferingComponentRequest:
    """
    Attributes:
        billing_type (BillingTypeEnum):
        type_ (str): Unique internal name of the measured unit, for example floating_ip.
        name (str): Display name for the measured unit, for example, Floating IP.
        description (Union[Unset, str]):
        measured_unit (Union[Unset, str]): Unit of measurement, for example, GB.
        unit_factor (Union[Unset, int]): The conversion factor from backend units to measured_unit
        limit_period (Union[BlankEnum, LimitPeriodEnum, None, Unset]):
        limit_amount (Union[None, Unset, int]):
        article_code (Union[Unset, str]):
        max_value (Union[None, Unset, int]):
        min_value (Union[None, Unset, int]):
        max_available_limit (Union[None, Unset, int]):
        is_boolean (Union[Unset, bool]):
        default_limit (Union[None, Unset, int]):
        is_prepaid (Union[Unset, bool]):
        overage_component (Union[None, UUID, Unset]):
        min_prepaid_duration (Union[None, Unset, int]):
        max_prepaid_duration (Union[None, Unset, int]):
    """

    billing_type: BillingTypeEnum
    type_: str
    name: str
    description: Union[Unset, str] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    unit_factor: Union[Unset, int] = UNSET
    limit_period: Union[BlankEnum, LimitPeriodEnum, None, Unset] = UNSET
    limit_amount: Union[None, Unset, int] = UNSET
    article_code: Union[Unset, str] = UNSET
    max_value: Union[None, Unset, int] = UNSET
    min_value: Union[None, Unset, int] = UNSET
    max_available_limit: Union[None, Unset, int] = UNSET
    is_boolean: Union[Unset, bool] = UNSET
    default_limit: Union[None, Unset, int] = UNSET
    is_prepaid: Union[Unset, bool] = UNSET
    overage_component: Union[None, UUID, Unset] = UNSET
    min_prepaid_duration: Union[None, Unset, int] = UNSET
    max_prepaid_duration: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_type = self.billing_type.value

        type_ = self.type_

        name = self.name

        description = self.description

        measured_unit = self.measured_unit

        unit_factor = self.unit_factor

        limit_period: Union[None, Unset, str]
        if isinstance(self.limit_period, Unset):
            limit_period = UNSET
        elif isinstance(self.limit_period, LimitPeriodEnum):
            limit_period = self.limit_period.value
        elif isinstance(self.limit_period, BlankEnum):
            limit_period = self.limit_period.value
        else:
            limit_period = self.limit_period

        limit_amount: Union[None, Unset, int]
        if isinstance(self.limit_amount, Unset):
            limit_amount = UNSET
        else:
            limit_amount = self.limit_amount

        article_code = self.article_code

        max_value: Union[None, Unset, int]
        if isinstance(self.max_value, Unset):
            max_value = UNSET
        else:
            max_value = self.max_value

        min_value: Union[None, Unset, int]
        if isinstance(self.min_value, Unset):
            min_value = UNSET
        else:
            min_value = self.min_value

        max_available_limit: Union[None, Unset, int]
        if isinstance(self.max_available_limit, Unset):
            max_available_limit = UNSET
        else:
            max_available_limit = self.max_available_limit

        is_boolean = self.is_boolean

        default_limit: Union[None, Unset, int]
        if isinstance(self.default_limit, Unset):
            default_limit = UNSET
        else:
            default_limit = self.default_limit

        is_prepaid = self.is_prepaid

        overage_component: Union[None, Unset, str]
        if isinstance(self.overage_component, Unset):
            overage_component = UNSET
        elif isinstance(self.overage_component, UUID):
            overage_component = str(self.overage_component)
        else:
            overage_component = self.overage_component

        min_prepaid_duration: Union[None, Unset, int]
        if isinstance(self.min_prepaid_duration, Unset):
            min_prepaid_duration = UNSET
        else:
            min_prepaid_duration = self.min_prepaid_duration

        max_prepaid_duration: Union[None, Unset, int]
        if isinstance(self.max_prepaid_duration, Unset):
            max_prepaid_duration = UNSET
        else:
            max_prepaid_duration = self.max_prepaid_duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "billing_type": billing_type,
                "type": type_,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if unit_factor is not UNSET:
            field_dict["unit_factor"] = unit_factor
        if limit_period is not UNSET:
            field_dict["limit_period"] = limit_period
        if limit_amount is not UNSET:
            field_dict["limit_amount"] = limit_amount
        if article_code is not UNSET:
            field_dict["article_code"] = article_code
        if max_value is not UNSET:
            field_dict["max_value"] = max_value
        if min_value is not UNSET:
            field_dict["min_value"] = min_value
        if max_available_limit is not UNSET:
            field_dict["max_available_limit"] = max_available_limit
        if is_boolean is not UNSET:
            field_dict["is_boolean"] = is_boolean
        if default_limit is not UNSET:
            field_dict["default_limit"] = default_limit
        if is_prepaid is not UNSET:
            field_dict["is_prepaid"] = is_prepaid
        if overage_component is not UNSET:
            field_dict["overage_component"] = overage_component
        if min_prepaid_duration is not UNSET:
            field_dict["min_prepaid_duration"] = min_prepaid_duration
        if max_prepaid_duration is not UNSET:
            field_dict["max_prepaid_duration"] = max_prepaid_duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_type = BillingTypeEnum(d.pop("billing_type"))

        type_ = d.pop("type")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        unit_factor = d.pop("unit_factor", UNSET)

        def _parse_limit_period(data: object) -> Union[BlankEnum, LimitPeriodEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                limit_period_type_0 = LimitPeriodEnum(data)

                return limit_period_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                limit_period_type_1 = BlankEnum(data)

                return limit_period_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, LimitPeriodEnum, None, Unset], data)

        limit_period = _parse_limit_period(d.pop("limit_period", UNSET))

        def _parse_limit_amount(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        limit_amount = _parse_limit_amount(d.pop("limit_amount", UNSET))

        article_code = d.pop("article_code", UNSET)

        def _parse_max_value(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_value = _parse_max_value(d.pop("max_value", UNSET))

        def _parse_min_value(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_value = _parse_min_value(d.pop("min_value", UNSET))

        def _parse_max_available_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_available_limit = _parse_max_available_limit(d.pop("max_available_limit", UNSET))

        is_boolean = d.pop("is_boolean", UNSET)

        def _parse_default_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_limit = _parse_default_limit(d.pop("default_limit", UNSET))

        is_prepaid = d.pop("is_prepaid", UNSET)

        def _parse_overage_component(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                overage_component_type_0 = UUID(data)

                return overage_component_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        overage_component = _parse_overage_component(d.pop("overage_component", UNSET))

        def _parse_min_prepaid_duration(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_prepaid_duration = _parse_min_prepaid_duration(d.pop("min_prepaid_duration", UNSET))

        def _parse_max_prepaid_duration(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_prepaid_duration = _parse_max_prepaid_duration(d.pop("max_prepaid_duration", UNSET))

        offering_component_request = cls(
            billing_type=billing_type,
            type_=type_,
            name=name,
            description=description,
            measured_unit=measured_unit,
            unit_factor=unit_factor,
            limit_period=limit_period,
            limit_amount=limit_amount,
            article_code=article_code,
            max_value=max_value,
            min_value=min_value,
            max_available_limit=max_available_limit,
            is_boolean=is_boolean,
            default_limit=default_limit,
            is_prepaid=is_prepaid,
            overage_component=overage_component,
            min_prepaid_duration=min_prepaid_duration,
            max_prepaid_duration=max_prepaid_duration,
        )

        offering_component_request.additional_properties = d
        return offering_component_request

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
