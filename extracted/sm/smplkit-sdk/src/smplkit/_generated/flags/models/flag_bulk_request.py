from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.flag_bulk_item import FlagBulkItem


T = TypeVar("T", bound="FlagBulkRequest")


@_attrs_define
class FlagBulkRequest:
    """Inputs to the bulk-register-flags action.

    Example:
        {'flags': [{'default': False, 'environment': 'production', 'id': 'dark-mode', 'service': 'api-gateway', 'type':
            'BOOLEAN'}, {'default': 3, 'environment': 'production', 'id': 'max-retries', 'service': 'api-gateway', 'type':
            'NUMERIC'}]}

    Attributes:
        flags (list[FlagBulkItem]): Flags reported by the SDK in this batch.
    """

    flags: list[FlagBulkItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flags = []
        for flags_item_data in self.flags:
            flags_item = flags_item_data.to_dict()
            flags.append(flags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flags": flags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag_bulk_item import FlagBulkItem

        d = dict(src_dict)
        flags = []
        _flags = d.pop("flags")
        for flags_item_data in _flags:
            flags_item = FlagBulkItem.from_dict(flags_item_data)

            flags.append(flags_item)

        flag_bulk_request = cls(
            flags=flags,
        )

        flag_bulk_request.additional_properties = d
        return flag_bulk_request

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
