from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_spending_limits_spending_limits_additional_property_type_0 import (
        ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0,
    )


T = TypeVar("T", bound="ResourceSpendingLimitsSpendingLimits")


@_attrs_define
class ResourceSpendingLimitsSpendingLimits:
    """The resource's spending limits, replacing the current ones: {component_type: {period: amount}}. A missing or null
    period clears that limit; an empty object clears them all.

    """

    additional_properties: dict[str, Union["ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0", None]] = (
        _attrs_field(init=False, factory=dict)
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_spending_limits_spending_limits_additional_property_type_0 import (
            ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_spending_limits_spending_limits_additional_property_type_0 import (
            ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0,
        )

        d = dict(src_dict)
        resource_spending_limits_spending_limits = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0", None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0.from_dict(
                        data
                    )

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                return cast(Union["ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0", None], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        resource_spending_limits_spending_limits.additional_properties = additional_properties
        return resource_spending_limits_spending_limits

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0", None]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union["ResourceSpendingLimitsSpendingLimitsAdditionalPropertyType0", None]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
