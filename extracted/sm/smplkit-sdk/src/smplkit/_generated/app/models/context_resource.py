from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.context_resource_type import ContextResourceType, check_context_resource_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.context import Context


T = TypeVar("T", bound="ContextResource")


@_attrs_define
class ContextResource:
    """JSON:API resource envelope for a context instance.

    `id` is the composite identifier `context_type:key` (e.g. `user:alice-123`).

        Example:
            {'attributes': {'attributes': {'first_name': 'Alice', 'plan': 'enterprise'}, 'context_type': 'user',
                'created_at': '2026-03-31T10:00:00Z', 'key': 'alice-123', 'name': 'Alice Smith', 'updated_at':
                '2026-03-31T10:00:00Z'}, 'id': 'user:alice-123', 'type': 'context'}

        Attributes:
            type_ (ContextResourceType):
            attributes (Context): A specific instance of a context type — for example, a particular
                user, account, or device — together with the attributes observed on it.

                Context instances are addressed by a composite identifier of the form
                `context_type:key` (e.g. `user:alice-123`). Example: {'attributes': {'first_name': 'Alice', 'plan':
                'enterprise'}, 'context_type': 'user', 'created_at': '2026-03-31T10:00:00Z', 'key': 'alice-123', 'name': 'Alice
                Smith', 'updated_at': '2026-03-31T10:00:00Z'}.
            id (None | str | Unset):
    """

    type_: ContextResourceType
    attributes: Context
    id: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: str | Unset | None
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.context import Context

        d = dict(src_dict)
        type_ = check_context_resource_type(d.pop("type"))

        attributes = Context.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        context_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        context_resource.additional_properties = d
        return context_resource

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
