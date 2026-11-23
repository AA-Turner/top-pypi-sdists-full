from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fresh_billing_usage import FreshBillingUsage
    from ..models.stale_billing_usage import StaleBillingUsage
    from ..models.unavailable_billing_usage import UnavailableBillingUsage


T = TypeVar("T", bound="BillingUsageResponse")


@_attrs_define
class BillingUsageResponse:
    """
    Attributes:
        data (FreshBillingUsage | StaleBillingUsage | UnavailableBillingUsage):
    """

    data: FreshBillingUsage | StaleBillingUsage | UnavailableBillingUsage
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fresh_billing_usage import FreshBillingUsage
        from ..models.stale_billing_usage import StaleBillingUsage

        data: dict[str, Any]
        if isinstance(self.data, FreshBillingUsage):
            data = self.data.to_dict()
        elif isinstance(self.data, StaleBillingUsage):
            data = self.data.to_dict()
        else:
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fresh_billing_usage import FreshBillingUsage
        from ..models.stale_billing_usage import StaleBillingUsage
        from ..models.unavailable_billing_usage import UnavailableBillingUsage

        d = dict(src_dict)

        def _parse_data(
            data: object,
        ) -> FreshBillingUsage | StaleBillingUsage | UnavailableBillingUsage:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_billing_usage_type_0 = FreshBillingUsage.from_dict(
                    data
                )

                return componentsschemas_billing_usage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_billing_usage_type_1 = StaleBillingUsage.from_dict(
                    data
                )

                return componentsschemas_billing_usage_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_billing_usage_type_2 = UnavailableBillingUsage.from_dict(
                data
            )

            return componentsschemas_billing_usage_type_2

        data = _parse_data(d.pop("data"))

        billing_usage_response = cls(
            data=data,
        )

        billing_usage_response.additional_properties = d
        return billing_usage_response

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
