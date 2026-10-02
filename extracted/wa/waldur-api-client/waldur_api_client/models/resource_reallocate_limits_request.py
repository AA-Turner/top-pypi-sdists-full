from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_reallocate_limits_request_limits import ResourceReallocateLimitsRequestLimits
    from ..models.resource_reallocate_target_request import ResourceReallocateTargetRequest


T = TypeVar("T", bound="ResourceReallocateLimitsRequest")


@_attrs_define
class ResourceReallocateLimitsRequest:
    """
    Attributes:
        limits (ResourceReallocateLimitsRequestLimits):
        targets (list['ResourceReallocateTargetRequest']):
    """

    limits: "ResourceReallocateLimitsRequestLimits"
    targets: list["ResourceReallocateTargetRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limits = self.limits.to_dict()

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limits": limits,
                "targets": targets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_reallocate_limits_request_limits import ResourceReallocateLimitsRequestLimits
        from ..models.resource_reallocate_target_request import ResourceReallocateTargetRequest

        d = dict(src_dict)
        limits = ResourceReallocateLimitsRequestLimits.from_dict(d.pop("limits"))

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = ResourceReallocateTargetRequest.from_dict(targets_item_data)

            targets.append(targets_item)

        resource_reallocate_limits_request = cls(
            limits=limits,
            targets=targets,
        )

        resource_reallocate_limits_request.additional_properties = d
        return resource_reallocate_limits_request

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
