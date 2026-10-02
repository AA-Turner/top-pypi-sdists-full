from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_limit_change_request_create_request_requested_limits import (
        ResourceLimitChangeRequestCreateRequestRequestedLimits,
    )


T = TypeVar("T", bound="ResourceLimitChangeRequestCreateRequest")


@_attrs_define
class ResourceLimitChangeRequestCreateRequest:
    """
    Attributes:
        resource (UUID):
        requested_limits (ResourceLimitChangeRequestCreateRequestRequestedLimits):
    """

    resource: UUID
    requested_limits: "ResourceLimitChangeRequestCreateRequestRequestedLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = str(self.resource)

        requested_limits = self.requested_limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource": resource,
                "requested_limits": requested_limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_limit_change_request_create_request_requested_limits import (
            ResourceLimitChangeRequestCreateRequestRequestedLimits,
        )

        d = dict(src_dict)
        resource = UUID(d.pop("resource"))

        requested_limits = ResourceLimitChangeRequestCreateRequestRequestedLimits.from_dict(d.pop("requested_limits"))

        resource_limit_change_request_create_request = cls(
            resource=resource,
            requested_limits=requested_limits,
        )

        resource_limit_change_request_create_request.additional_properties = d
        return resource_limit_change_request_create_request

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
