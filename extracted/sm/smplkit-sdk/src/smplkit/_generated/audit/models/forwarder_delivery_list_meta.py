from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="ForwarderDeliveryListMeta")


@_attrs_define
class ForwarderDeliveryListMeta:
    """Cursor-pagination meta for the forwarder-delivery log endpoint.

    Forwarder deliveries are append-only at high cardinality (one row per
    delivery attempt per event) and scroll with the same workload as
    audit events, so this endpoint stays on cursor pagination — the
    documented exception in ADR-014. The parent `/forwarders` collection
    follows the standard offset convention.

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

        forwarder_delivery_list_meta = cls(
            page_size=page_size,
        )

        forwarder_delivery_list_meta.additional_properties = d
        return forwarder_delivery_list_meta

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
