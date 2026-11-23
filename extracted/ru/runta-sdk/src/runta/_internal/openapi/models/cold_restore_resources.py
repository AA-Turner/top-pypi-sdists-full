from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cold_restore_resource_requests import ColdRestoreResourceRequests
    from ..models.runtime_resource_limits import RuntimeResourceLimits


T = TypeVar("T", bound="ColdRestoreResources")


@_attrs_define
class ColdRestoreResources:
    """Legacy resource override type. Checkpoint restore rejects this object and keeps the recorded CPU and memory requests
    and limits.

        Attributes:
            requests (ColdRestoreResourceRequests): Legacy resource override type. Checkpoint restore rejects resource
                overrides.
            limits (RuntimeResourceLimits | Unset): Runtime resource limits.
    """

    requests: ColdRestoreResourceRequests
    limits: RuntimeResourceLimits | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        requests = self.requests.to_dict()

        limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "requests": requests,
            }
        )
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cold_restore_resource_requests import ColdRestoreResourceRequests
        from ..models.runtime_resource_limits import RuntimeResourceLimits

        d = dict(src_dict)
        requests = ColdRestoreResourceRequests.from_dict(d.pop("requests"))

        _limits = d.pop("limits", UNSET)
        limits: RuntimeResourceLimits | Unset
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = RuntimeResourceLimits.from_dict(_limits)

        cold_restore_resources = cls(
            requests=requests,
            limits=limits,
        )

        return cold_restore_resources
