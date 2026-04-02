from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.renewal_estimate_request_request_limits import RenewalEstimateRequestRequestLimits


T = TypeVar("T", bound="RenewalEstimateRequestRequest")


@_attrs_define
class RenewalEstimateRequestRequest:
    """
    Attributes:
        extension_months (int):
        limits (Union[Unset, RenewalEstimateRequestRequestLimits]):
    """

    extension_months: int
    limits: Union[Unset, "RenewalEstimateRequestRequestLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        extension_months = self.extension_months

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "extension_months": extension_months,
            }
        )
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.renewal_estimate_request_request_limits import RenewalEstimateRequestRequestLimits

        d = dict(src_dict)
        extension_months = d.pop("extension_months")

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, RenewalEstimateRequestRequestLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = RenewalEstimateRequestRequestLimits.from_dict(_limits)

        renewal_estimate_request_request = cls(
            extension_months=extension_months,
            limits=limits,
        )

        renewal_estimate_request_request.additional_properties = d
        return renewal_estimate_request_request

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
