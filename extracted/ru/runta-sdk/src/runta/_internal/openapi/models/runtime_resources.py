from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.runtime_resource_current import RuntimeResourceCurrent
    from ..models.runtime_resource_limits import RuntimeResourceLimits
    from ..models.runtime_resource_requests import RuntimeResourceRequests


T = TypeVar("T", bound="RuntimeResources")


@_attrs_define
class RuntimeResources:
    """Runtime resource requests and limits.

    Attributes:
        current (RuntimeResourceCurrent): Current runtime resource allocation.
        limits (RuntimeResourceLimits): Runtime resource limits.
        requests (RuntimeResourceRequests): Runtime resource requests.
    """

    current: RuntimeResourceCurrent
    limits: RuntimeResourceLimits
    requests: RuntimeResourceRequests

    def to_dict(self) -> dict[str, Any]:
        current = self.current.to_dict()

        limits = self.limits.to_dict()

        requests = self.requests.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "current": current,
                "limits": limits,
                "requests": requests,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.runtime_resource_current import RuntimeResourceCurrent
        from ..models.runtime_resource_limits import RuntimeResourceLimits
        from ..models.runtime_resource_requests import RuntimeResourceRequests

        d = dict(src_dict)
        current = RuntimeResourceCurrent.from_dict(d.pop("current"))

        limits = RuntimeResourceLimits.from_dict(d.pop("limits"))

        requests = RuntimeResourceRequests.from_dict(d.pop("requests"))

        runtime_resources = cls(
            current=current,
            limits=limits,
            requests=requests,
        )

        return runtime_resources
