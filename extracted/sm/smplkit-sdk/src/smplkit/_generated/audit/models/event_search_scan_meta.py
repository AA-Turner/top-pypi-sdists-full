from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="EventSearchScanMeta")


@_attrs_define
class EventSearchScanMeta:
    """Scan statistics for a search response.

    Exposed so a selective JSON Logic filter doesn't silently look like
    "0 matches" when the truth is "the scan ceiling was reached before
    the filter had a chance to find page[size] matches."

        Attributes:
            scanned (int): Rows scanned after column filters narrowed the candidate set, before the JSON Logic expression
                was applied.
            matched (int): Rows the JSON Logic expression matched. Equal to `len(data)` for the page being returned plus any
                matches found beyond the page size.
            exhausted (bool): `true` if the server hit the per-request scan ceiling before finding `page[size]` matches.
                When true, paginate again with the returned `links.next` cursor to continue scanning past the ceiling.
    """

    scanned: int
    matched: int
    exhausted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scanned = self.scanned

        matched = self.matched

        exhausted = self.exhausted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scanned": scanned,
                "matched": matched,
                "exhausted": exhausted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scanned = d.pop("scanned")

        matched = d.pop("matched")

        exhausted = d.pop("exhausted")

        event_search_scan_meta = cls(
            scanned=scanned,
            matched=matched,
            exhausted=exhausted,
        )

        event_search_scan_meta.additional_properties = d
        return event_search_scan_meta

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
