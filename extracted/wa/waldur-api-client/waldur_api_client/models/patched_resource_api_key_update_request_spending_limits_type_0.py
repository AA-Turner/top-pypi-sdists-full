from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.patched_resource_api_key_update_request_spending_limits_type_0_additional_property_type_0 import (
        PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0,
    )


T = TypeVar("T", bound="PatchedResourceApiKeyUpdateRequestSpendingLimitsType0")


@_attrs_define
class PatchedResourceApiKeyUpdateRequestSpendingLimitsType0:
    """Limits per component type and period, replacing the key's limits; a null amount clears that period's limit. Only
    where the offering's api_key_limits is not off. A period other than month must be offered on the component and needs
    the offering's api_key_daily_usage. A limit may not exceed the resource's spending limit for the same period.

    """

    additional_properties: dict[
        str, Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0", None]
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.patched_resource_api_key_update_request_spending_limits_type_0_additional_property_type_0 import (
            PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_resource_api_key_update_request_spending_limits_type_0_additional_property_type_0 import (
            PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0,
        )

        d = dict(src_dict)
        patched_resource_api_key_update_request_spending_limits_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0", None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = (
                        PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0.from_dict(data)
                    )

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                return cast(
                    Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0", None], data
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        patched_resource_api_key_update_request_spending_limits_type_0.additional_properties = additional_properties
        return patched_resource_api_key_update_request_spending_limits_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0", None]:
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0AdditionalPropertyType0", None],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
