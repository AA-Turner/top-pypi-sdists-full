from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.event_search_request_filter_type_0 import EventSearchRequestFilterType0


T = TypeVar("T", bound="EventSearchRequest")


@_attrs_define
class EventSearchRequest:
    """Request body for ``POST /api/v1/events/search``.

    Mirrors every column filter accepted by ``GET /api/v1/events`` with
    identical semantics, and adds a top-level ``filter`` field carrying
    a JSON Logic expression. When ``filter`` is present the search is
    silently capped to the last 30 days by ``occurred_at``; the
    expression is then evaluated in memory against each row that passes
    the column filters using the same ``json-logic-qubit`` evaluator
    that runs in the forwarder pipeline (so search results match what
    would be forwarded).

    Filter-combination rules match ``GET /api/v1/events`` exactly:

    - ``filter[resource_id]`` must be accompanied by
      ``filter[resource_type]`` — the index is keyed on the pair.
    - ``filter[search]`` must be accompanied by either
      ``filter[occurred_at]`` or ``filter[resource_type]`` +
      ``filter[resource_id]`` — substring matching has no index, so an
      unbounded substring scan is rejected.

        Attributes:
            filter_ (EventSearchRequestFilterType0 | None | Unset): Optional JSON Logic expression evaluated against each
                row after column filters narrow the candidate set. Null, absent, or an empty object disables JSON Logic
                filtering. When present, the search is silently capped to the last 30 days by `occurred_at` (intersected with
                any explicit `filter[occurred_at]` the caller supplied).
            filterenvironment (None | str | Unset): Comma-separated list of environment keys to scope results to (e.g.
                `production,staging`). When omitted, results are scoped to your single accessible environment; send the
                `X-Smplkit-Environment` header instead if you can access more than one. The reserved value `smplkit` selects
                platform change events that smplkit records about your own resources (flags, configuration, and so on); these
                are not tied to a deployment environment and are readable regardless of which environments you manage.
            filterevent_type (None | str | Unset): Exact match on the event's `event_type` field.
            filterresource_type (None | str | Unset): Exact match on the event's `resource_type` field.
            filterresource_id (None | str | Unset): Exact match on the event's `resource_id` field. Must be accompanied by
                `filter[resource_type]`.
            filterseverity (None | str | Unset): Exact match on the event's `severity` field. One of `TRACE`, `DEBUG`,
                `INFO`, `WARN`, `ERROR`, `FATAL`.
            filtercategory (None | str | Unset): Exact match on the event's `category` field.
            filteractor_type (None | str | Unset): Exact match on the event's `actor_type` field.
            filteractor_id (None | str | Unset): Exact match on the event's `actor_id` field.
            filteroccurred_at (None | str | Unset): Date range using interval notation, e.g.
                `[2026-04-01T00:00:00Z,2026-04-15T00:00:00Z)`. Required by `filter[search]` when the resource pair isn't
                provided. When a JSON Logic `filter` is present, the effective range is intersected with the last 30 days.
            filtersearch (None | str | Unset): Case-insensitive substring match on `resource_id` or `description`. Must be
                accompanied by either `filter[occurred_at]` or `filter[resource_type]` + `filter[resource_id]`.
            filterdo_not_forward (bool | None | Unset): When set, restrict to events whose `do_not_forward` flag matches the
                given boolean. Forwarder previews typically pass `false` to match live-pipeline semantics (events flagged
                `do_not_forward=true` are skipped by the forwarder pipeline).
            pagesize (int | Unset): Maximum events to return. Range 1..1000, default 1000 — matches every other list /
                search endpoint on the platform. Set explicitly to a smaller value when the consumer is rendering results card-
                by-card. Default: 1000.
            pageafter (None | str | Unset): Opaque cursor — pass the previous response's `links.next` cursor verbatim to
                fetch the next page. Keep the same `sort` value across paginated requests.
            sort (str | Unset): Sort field: `occurred_at` or `created_at`, optionally prefixed with `-` for descending
                order. Default `-occurred_at` (newest first). Default: '-occurred_at'.
    """

    filter_: EventSearchRequestFilterType0 | None | Unset = UNSET
    filterenvironment: None | str | Unset = UNSET
    filterevent_type: None | str | Unset = UNSET
    filterresource_type: None | str | Unset = UNSET
    filterresource_id: None | str | Unset = UNSET
    filterseverity: None | str | Unset = UNSET
    filtercategory: None | str | Unset = UNSET
    filteractor_type: None | str | Unset = UNSET
    filteractor_id: None | str | Unset = UNSET
    filteroccurred_at: None | str | Unset = UNSET
    filtersearch: None | str | Unset = UNSET
    filterdo_not_forward: bool | None | Unset = UNSET
    pagesize: int | Unset = 1000
    pageafter: None | str | Unset = UNSET
    sort: str | Unset = "-occurred_at"

    def to_dict(self) -> dict[str, Any]:
        from ..models.event_search_request_filter_type_0 import EventSearchRequestFilterType0

        filter_: dict[str, Any] | None | Unset
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, EventSearchRequestFilterType0):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        filterenvironment: None | str | Unset
        if isinstance(self.filterenvironment, Unset):
            filterenvironment = UNSET
        else:
            filterenvironment = self.filterenvironment

        filterevent_type: None | str | Unset
        if isinstance(self.filterevent_type, Unset):
            filterevent_type = UNSET
        else:
            filterevent_type = self.filterevent_type

        filterresource_type: None | str | Unset
        if isinstance(self.filterresource_type, Unset):
            filterresource_type = UNSET
        else:
            filterresource_type = self.filterresource_type

        filterresource_id: None | str | Unset
        if isinstance(self.filterresource_id, Unset):
            filterresource_id = UNSET
        else:
            filterresource_id = self.filterresource_id

        filterseverity: None | str | Unset
        if isinstance(self.filterseverity, Unset):
            filterseverity = UNSET
        else:
            filterseverity = self.filterseverity

        filtercategory: None | str | Unset
        if isinstance(self.filtercategory, Unset):
            filtercategory = UNSET
        else:
            filtercategory = self.filtercategory

        filteractor_type: None | str | Unset
        if isinstance(self.filteractor_type, Unset):
            filteractor_type = UNSET
        else:
            filteractor_type = self.filteractor_type

        filteractor_id: None | str | Unset
        if isinstance(self.filteractor_id, Unset):
            filteractor_id = UNSET
        else:
            filteractor_id = self.filteractor_id

        filteroccurred_at: None | str | Unset
        if isinstance(self.filteroccurred_at, Unset):
            filteroccurred_at = UNSET
        else:
            filteroccurred_at = self.filteroccurred_at

        filtersearch: None | str | Unset
        if isinstance(self.filtersearch, Unset):
            filtersearch = UNSET
        else:
            filtersearch = self.filtersearch

        filterdo_not_forward: bool | None | Unset
        if isinstance(self.filterdo_not_forward, Unset):
            filterdo_not_forward = UNSET
        else:
            filterdo_not_forward = self.filterdo_not_forward

        pagesize = self.pagesize

        pageafter: None | str | Unset
        if isinstance(self.pageafter, Unset):
            pageafter = UNSET
        else:
            pageafter = self.pageafter

        sort = self.sort

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if filterenvironment is not UNSET:
            field_dict["filter[environment]"] = filterenvironment
        if filterevent_type is not UNSET:
            field_dict["filter[event_type]"] = filterevent_type
        if filterresource_type is not UNSET:
            field_dict["filter[resource_type]"] = filterresource_type
        if filterresource_id is not UNSET:
            field_dict["filter[resource_id]"] = filterresource_id
        if filterseverity is not UNSET:
            field_dict["filter[severity]"] = filterseverity
        if filtercategory is not UNSET:
            field_dict["filter[category]"] = filtercategory
        if filteractor_type is not UNSET:
            field_dict["filter[actor_type]"] = filteractor_type
        if filteractor_id is not UNSET:
            field_dict["filter[actor_id]"] = filteractor_id
        if filteroccurred_at is not UNSET:
            field_dict["filter[occurred_at]"] = filteroccurred_at
        if filtersearch is not UNSET:
            field_dict["filter[search]"] = filtersearch
        if filterdo_not_forward is not UNSET:
            field_dict["filter[do_not_forward]"] = filterdo_not_forward
        if pagesize is not UNSET:
            field_dict["page[size]"] = pagesize
        if pageafter is not UNSET:
            field_dict["page[after]"] = pageafter
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_search_request_filter_type_0 import EventSearchRequestFilterType0

        d = dict(src_dict)

        def _parse_filter_(data: object) -> EventSearchRequestFilterType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = EventSearchRequestFilterType0.from_dict(data)

                return filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EventSearchRequestFilterType0 | None | Unset, data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        def _parse_filterenvironment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filterenvironment = _parse_filterenvironment(d.pop("filter[environment]", UNSET))

        def _parse_filterevent_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filterevent_type = _parse_filterevent_type(d.pop("filter[event_type]", UNSET))

        def _parse_filterresource_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filterresource_type = _parse_filterresource_type(d.pop("filter[resource_type]", UNSET))

        def _parse_filterresource_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filterresource_id = _parse_filterresource_id(d.pop("filter[resource_id]", UNSET))

        def _parse_filterseverity(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filterseverity = _parse_filterseverity(d.pop("filter[severity]", UNSET))

        def _parse_filtercategory(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filtercategory = _parse_filtercategory(d.pop("filter[category]", UNSET))

        def _parse_filteractor_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filteractor_type = _parse_filteractor_type(d.pop("filter[actor_type]", UNSET))

        def _parse_filteractor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filteractor_id = _parse_filteractor_id(d.pop("filter[actor_id]", UNSET))

        def _parse_filteroccurred_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filteroccurred_at = _parse_filteroccurred_at(d.pop("filter[occurred_at]", UNSET))

        def _parse_filtersearch(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filtersearch = _parse_filtersearch(d.pop("filter[search]", UNSET))

        def _parse_filterdo_not_forward(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        filterdo_not_forward = _parse_filterdo_not_forward(d.pop("filter[do_not_forward]", UNSET))

        pagesize = d.pop("page[size]", UNSET)

        def _parse_pageafter(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pageafter = _parse_pageafter(d.pop("page[after]", UNSET))

        sort = d.pop("sort", UNSET)

        event_search_request = cls(
            filter_=filter_,
            filterenvironment=filterenvironment,
            filterevent_type=filterevent_type,
            filterresource_type=filterresource_type,
            filterresource_id=filterresource_id,
            filterseverity=filterseverity,
            filtercategory=filtercategory,
            filteractor_type=filteractor_type,
            filteractor_id=filteractor_id,
            filteroccurred_at=filteroccurred_at,
            filtersearch=filtersearch,
            filterdo_not_forward=filterdo_not_forward,
            pagesize=pagesize,
            pageafter=pageafter,
            sort=sort,
        )

        return event_search_request
