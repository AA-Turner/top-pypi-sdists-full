from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="EventListMeta")


@_attrs_define
class EventListMeta:
    """Cursor-pagination meta for the audit-event list endpoint.

    Audit events are append-only at high cardinality (millions of rows
    per account at production tenants), so this endpoint stays on
    cursor pagination — the documented exception in ADR-014. Every
    other read-many endpoint in the platform follows the standard
    offset convention (`page[number]` / `page[size]`).

        Attributes:
            page_size (int):
    """

    page_size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page_size = self.page_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page_size": page_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page_size = d.pop("page_size")

        event_list_meta = cls(
            page_size=page_size,
        )

        event_list_meta.additional_properties = d
        return event_list_meta

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
