from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.context_resource import ContextResource


T = TypeVar("T", bound="ContextRequest")


@_attrs_define
class ContextRequest:
    """JSON:API request envelope for creating or updating a context instance.

    Attributes:
        data (ContextResource): JSON:API resource envelope for a context instance.

            `id` is the composite identifier `context_type:key` (e.g. `user:alice-123`). Example: {'attributes':
            {'attributes': {'first_name': 'Alice', 'plan': 'enterprise'}, 'context_type': 'user', 'created_at':
            '2026-03-31T10:00:00Z', 'key': 'alice-123', 'name': 'Alice Smith', 'updated_at': '2026-03-31T10:00:00Z'}, 'id':
            'user:alice-123', 'type': 'context'}.
    """

    data: ContextResource
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
        from ..models.context_resource import ContextResource

        d = dict(src_dict)
        data = ContextResource.from_dict(d.pop("data"))

        context_request = cls(
            data=data,
        )

        context_request.additional_properties = d
        return context_request

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
