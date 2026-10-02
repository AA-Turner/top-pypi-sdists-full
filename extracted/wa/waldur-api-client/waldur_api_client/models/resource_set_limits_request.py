from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_set_limits_request_limits import ResourceSetLimitsRequestLimits


T = TypeVar("T", bound="ResourceSetLimitsRequest")


@_attrs_define
class ResourceSetLimitsRequest:
    """
    Attributes:
        limits (ResourceSetLimitsRequestLimits): Dictionary mapping component types to their new limit values
    """

    limits: "ResourceSetLimitsRequestLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_set_limits_request_limits import ResourceSetLimitsRequestLimits

        d = dict(src_dict)
        limits = ResourceSetLimitsRequestLimits.from_dict(d.pop("limits"))

        resource_set_limits_request = cls(
            limits=limits,
        )

        resource_set_limits_request.additional_properties = d
        return resource_set_limits_request

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
