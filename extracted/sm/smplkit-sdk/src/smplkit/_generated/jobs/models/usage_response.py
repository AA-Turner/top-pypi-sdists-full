from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.usage_resource import UsageResource


T = TypeVar("T", bound="UsageResponse")


@_attrs_define
class UsageResponse:
    """JSON:API single-resource response for usage.

    Attributes:
        data (UsageResource): JSON:API resource envelope for the usage report. Example: {'attributes': {'active_jobs':
            2, 'active_jobs_limit': 10, 'period': '2026-06', 'runs_included': 3000, 'runs_used': 412}, 'id': 'current',
            'type': 'usage'}.
    """

    data: UsageResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
        from ..models.usage_resource import UsageResource

        d = dict(src_dict)
        data = UsageResource.from_dict(d.pop("data"))

        usage_response = cls(
            data=data,
        )

        usage_response.additional_properties = d
        return usage_response

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
