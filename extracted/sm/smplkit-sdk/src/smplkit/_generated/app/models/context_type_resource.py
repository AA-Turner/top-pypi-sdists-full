from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.context_type_resource_type import check_context_type_resource_type
from ..models.context_type_resource_type import ContextTypeResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.context_type import ContextType


T = TypeVar("T", bound="ContextTypeResource")


@_attrs_define
class ContextTypeResource:
    """JSON:API resource envelope for a context type.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'attributes': {'beta_tester': {}, 'first_name': {}, 'plan': {}}, 'created_at':
                '2026-03-31T10:00:00Z', 'name': 'User', 'updated_at': '2026-03-31T10:00:00Z'}, 'id': 'user', 'type':
                'context_type'}

        Attributes:
            type_ (ContextTypeResourceType):
            attributes (ContextType): A kind of context — for example, `user`, `account`, or `device` — that
                groups together context instances sharing a common set of attributes.

                The known attribute keys for the type accumulate as instances are
                registered; each key carries an optional metadata object describing it. Example: {'attributes': {'beta_tester':
                {}, 'first_name': {}, 'plan': {}}, 'created_at': '2026-03-31T10:00:00Z', 'name': 'User', 'updated_at':
                '2026-03-31T10:00:00Z'}.
            id (None | str | Unset):
    """

    type_: ContextTypeResourceType
    attributes: ContextType
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
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
        from ..models.context_type import ContextType

        d = dict(src_dict)
        type_ = check_context_type_resource_type(d.pop("type"))

        attributes = ContextType.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        context_type_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        context_type_resource.additional_properties = d
        return context_type_resource

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
