from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.event_list_links import EventListLinks
    from ..models.event_list_meta import EventListMeta
    from ..models.event_resource import EventResource


T = TypeVar("T", bound="EventListResponse")


@_attrs_define
class EventListResponse:
    """JSON:API collection response for audit events (cursor paged).

    Attributes:
        data (list[EventResource]):
        meta (EventListMeta): Cursor-pagination meta for the audit-event list endpoint.

            Audit events are append-only at high cardinality (millions of rows
            per account at production tenants), so this endpoint stays on
            cursor pagination — the documented exception in ADR-014. Every
            other read-many endpoint in the platform follows the standard
            offset convention (`page[number]` / `page[size]`).
        links (EventListLinks | None | Unset):
    """

    data: list[EventResource]
    meta: EventListMeta
    links: EventListLinks | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.event_list_links import EventListLinks

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        meta = self.meta.to_dict()

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, EventListLinks):
            links = self.links.to_dict()
        else:
            links = self.links

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "meta": meta,
            }
        )
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_list_links import EventListLinks
        from ..models.event_list_meta import EventListMeta
        from ..models.event_resource import EventResource

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = EventResource.from_dict(data_item_data)

            data.append(data_item)

        meta = EventListMeta.from_dict(d.pop("meta"))

        def _parse_links(data: object) -> EventListLinks | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = EventListLinks.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EventListLinks | None | Unset, data)

        links = _parse_links(d.pop("links", UNSET))

        event_list_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        event_list_response.additional_properties = d
        return event_list_response

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
