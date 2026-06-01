from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.event_search_scan_meta import EventSearchScanMeta


T = TypeVar("T", bound="EventSearchListMeta")


@_attrs_define
class EventSearchListMeta:
    """Cursor-pagination + scan meta for the search response.

    Mirrors `EventListMeta` (cursor pagination — `page_size` is the
    only pagination field) and adds the `scan` block above.

        Attributes:
            page_size (int):
            scan (EventSearchScanMeta): Scan statistics for a search response.

                Exposed so a selective JSON Logic filter doesn't silently look like
                "0 matches" when the truth is "the scan ceiling was reached before
                the filter had a chance to find page[size] matches."
    """

    page_size: int
    scan: EventSearchScanMeta
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page_size = self.page_size

        scan = self.scan.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page_size": page_size,
                "scan": scan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_search_scan_meta import EventSearchScanMeta

        d = dict(src_dict)
        page_size = d.pop("page_size")

        scan = EventSearchScanMeta.from_dict(d.pop("scan"))

        event_search_list_meta = cls(
            page_size=page_size,
            scan=scan,
        )

        event_search_list_meta.additional_properties = d
        return event_search_list_meta

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
