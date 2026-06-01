from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="RemoveReferencesRequest")


@_attrs_define
class RemoveReferencesRequest:
    """Inputs to the remove-references action.

    Exactly one of `context` or `context_type` must be provided.

        Attributes:
            context (None | str | Unset): Identifier of the context instance to remove references to, formatted as
                `{type}:{key}` (e.g. `customer:c-123`).
            context_type (None | str | Unset): Context type to remove all references to (any attribute of this type).
    """

    context: None | str | Unset = UNSET
    context_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context: None | str | Unset
        if isinstance(self.context, Unset):
            context = UNSET
        else:
            context = self.context

        context_type: None | str | Unset
        if isinstance(self.context_type, Unset):
            context_type = UNSET
        else:
            context_type = self.context_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if context is not UNSET:
            field_dict["context"] = context
        if context_type is not UNSET:
            field_dict["context_type"] = context_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_context(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context = _parse_context(d.pop("context", UNSET))

        def _parse_context_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context_type = _parse_context_type(d.pop("context_type", UNSET))

        remove_references_request = cls(
            context=context,
            context_type=context_type,
        )

        remove_references_request.additional_properties = d
        return remove_references_request

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
