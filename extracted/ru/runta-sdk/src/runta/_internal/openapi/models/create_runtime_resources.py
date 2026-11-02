from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_runtime_resource_requests import CreateRuntimeResourceRequests
    from ..models.runtime_resource_limits import RuntimeResourceLimits


T = TypeVar("T", bound="CreateRuntimeResources")


@_attrs_define
class CreateRuntimeResources:
    """Resource requests and limits for runtime creation.

    Attributes:
        limits (RuntimeResourceLimits | Unset): Runtime resource limits.
        requests (CreateRuntimeResourceRequests | Unset): Resource requests for runtime creation.
    """

    limits: RuntimeResourceLimits | Unset = UNSET
    requests: CreateRuntimeResourceRequests | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        requests: dict[str, Any] | Unset = UNSET
        if not isinstance(self.requests, Unset):
            requests = self.requests.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if limits is not UNSET:
            field_dict["limits"] = limits
        if requests is not UNSET:
            field_dict["requests"] = requests

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_runtime_resource_requests import (
            CreateRuntimeResourceRequests,
        )
        from ..models.runtime_resource_limits import RuntimeResourceLimits

        d = dict(src_dict)
        _limits = d.pop("limits", UNSET)
        limits: RuntimeResourceLimits | Unset
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = RuntimeResourceLimits.from_dict(_limits)

        _requests = d.pop("requests", UNSET)
        requests: CreateRuntimeResourceRequests | Unset
        if isinstance(_requests, Unset):
            requests = UNSET
        else:
            requests = CreateRuntimeResourceRequests.from_dict(_requests)

        create_runtime_resources = cls(
            limits=limits,
            requests=requests,
        )

        return create_runtime_resources
