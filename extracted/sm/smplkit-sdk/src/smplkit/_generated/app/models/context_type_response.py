from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.context_type_resource import ContextTypeResource


T = TypeVar("T", bound="ContextTypeResponse")


@_attrs_define
class ContextTypeResponse:
    """JSON:API single-resource response envelope for a context type.

    Attributes:
        data (ContextTypeResource): JSON:API resource envelope for a context type.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'attributes':
            {'beta_tester': {}, 'first_name': {}, 'plan': {}}, 'created_at': '2026-03-31T10:00:00Z', 'name': 'User',
            'updated_at': '2026-03-31T10:00:00Z'}, 'id': 'user', 'type': 'context_type'}.
    """

    data: ContextTypeResource
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
        from ..models.context_type_resource import ContextTypeResource

        d = dict(src_dict)
        data = ContextTypeResource.from_dict(d.pop("data"))

        context_type_response = cls(
            data=data,
        )

        context_type_response.additional_properties = d
        return context_type_response

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
