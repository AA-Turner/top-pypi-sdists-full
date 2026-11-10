from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.booking_resource_spending_limits_additional_property_type_0 import (
        BookingResourceSpendingLimitsAdditionalPropertyType0,
    )


T = TypeVar("T", bound="BookingResourceSpendingLimits")


@_attrs_define
class BookingResourceSpendingLimits:
    """Spending limits on usage-based components, per period. Changed with the set_spending_limits action."""

    additional_properties: dict[str, Union["BookingResourceSpendingLimitsAdditionalPropertyType0", None]] = (
        _attrs_field(init=False, factory=dict)
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.booking_resource_spending_limits_additional_property_type_0 import (
            BookingResourceSpendingLimitsAdditionalPropertyType0,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, BookingResourceSpendingLimitsAdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.booking_resource_spending_limits_additional_property_type_0 import (
            BookingResourceSpendingLimitsAdditionalPropertyType0,
        )

        d = dict(src_dict)
        booking_resource_spending_limits = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["BookingResourceSpendingLimitsAdditionalPropertyType0", None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = BookingResourceSpendingLimitsAdditionalPropertyType0.from_dict(data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                return cast(Union["BookingResourceSpendingLimitsAdditionalPropertyType0", None], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        booking_resource_spending_limits.additional_properties = additional_properties
        return booking_resource_spending_limits

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["BookingResourceSpendingLimitsAdditionalPropertyType0", None]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union["BookingResourceSpendingLimitsAdditionalPropertyType0", None]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
