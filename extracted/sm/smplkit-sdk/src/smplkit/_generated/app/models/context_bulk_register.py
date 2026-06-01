from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.context_bulk_item import ContextBulkItem


T = TypeVar("T", bound="ContextBulkRegister")


@_attrs_define
class ContextBulkRegister:
    """Bulk registration request body for the contexts endpoint.

    Attributes:
        contexts (list[ContextBulkItem]): One context instance per entry.
    """

    contexts: list[ContextBulkItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        contexts = []
        for contexts_item_data in self.contexts:
            contexts_item = contexts_item_data.to_dict()
            contexts.append(contexts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contexts": contexts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.context_bulk_item import ContextBulkItem

        d = dict(src_dict)
        contexts = []
        _contexts = d.pop("contexts")
        for contexts_item_data in _contexts:
            contexts_item = ContextBulkItem.from_dict(contexts_item_data)

            contexts.append(contexts_item)

        context_bulk_register = cls(
            contexts=contexts,
        )

        context_bulk_register.additional_properties = d
        return context_bulk_register

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
