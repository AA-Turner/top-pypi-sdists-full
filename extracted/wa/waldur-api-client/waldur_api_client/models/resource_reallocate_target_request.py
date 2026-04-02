from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_reallocate_target_request_allocated_limits import (
        ResourceReallocateTargetRequestAllocatedLimits,
    )


T = TypeVar("T", bound="ResourceReallocateTargetRequest")


@_attrs_define
class ResourceReallocateTargetRequest:
    """
    Attributes:
        resource_uuid (UUID):
        allocated_limits (ResourceReallocateTargetRequestAllocatedLimits):
    """

    resource_uuid: UUID
    allocated_limits: "ResourceReallocateTargetRequestAllocatedLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        allocated_limits = self.allocated_limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "allocated_limits": allocated_limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_reallocate_target_request_allocated_limits import (
            ResourceReallocateTargetRequestAllocatedLimits,
        )

        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        allocated_limits = ResourceReallocateTargetRequestAllocatedLimits.from_dict(d.pop("allocated_limits"))

        resource_reallocate_target_request = cls(
            resource_uuid=resource_uuid,
            allocated_limits=allocated_limits,
        )

        resource_reallocate_target_request.additional_properties = d
        return resource_reallocate_target_request

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
