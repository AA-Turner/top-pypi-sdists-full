from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.event_resource import EventResource
    from ..models.event_search_list_links import EventSearchListLinks
    from ..models.event_search_list_meta import EventSearchListMeta


T = TypeVar("T", bound="EventSearchResponse")


@_attrs_define
class EventSearchResponse:
    """JSON:API list envelope returned by the search endpoint.

    Structurally identical to ``EventListResponse`` from the list
    endpoint — the only difference is the extra `scan` block inside
    `meta` (`EventSearchListMeta` vs `EventListMeta`).

        Attributes:
            data (list[EventResource]):
            meta (EventSearchListMeta): Cursor-pagination + scan meta for the search response.

                Mirrors `EventListMeta` (cursor pagination — `page_size` is the
                only pagination field) and adds the `scan` block above.
            links (EventSearchListLinks | None | Unset):
    """

    data: list[EventResource]
    meta: EventSearchListMeta
    links: EventSearchListLinks | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.event_search_list_links import EventSearchListLinks

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        meta = self.meta.to_dict()

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, EventSearchListLinks):
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
        from ..models.event_resource import EventResource
        from ..models.event_search_list_links import EventSearchListLinks
        from ..models.event_search_list_meta import EventSearchListMeta

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = EventResource.from_dict(data_item_data)

            data.append(data_item)

        meta = EventSearchListMeta.from_dict(d.pop("meta"))

        def _parse_links(data: object) -> EventSearchListLinks | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = EventSearchListLinks.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EventSearchListLinks | None | Unset, data)

        links = _parse_links(d.pop("links", UNSET))

        event_search_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        event_search_response.additional_properties = d
        return event_search_response

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
