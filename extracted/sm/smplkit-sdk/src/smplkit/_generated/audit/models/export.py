from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.export_format import check_export_format
from ..models.export_format import ExportFormat
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="Export")


@_attrs_define
class Export:
    """A request for a short-lived signed download URL.

    The customer chooses a `format` and supplies the same filter set
    the events list endpoint accepts. The server mints an HMAC-signed
    URL (valid for 30 seconds) that the browser navigates to for a
    native streaming download — no `Authorization` header required at
    download time.

    The download honors the **same filter-combination rules** as
    `GET /api/v1/events`:

    - `filter[resource_id]` must be accompanied by `filter[resource_type]`.
    - `filter[search]` must be accompanied by either `filter[occurred_at]`
      or `filter[resource_type]` + `filter[resource_id]`.

    A request that violates these rules is rejected at mint time with
    `400 Bad Request`.

        Attributes:
            format_ (ExportFormat): Output format for the download. `CSV` writes one row per event with the event payload
                (`data`) serialized as a JSON-encoded cell. `JSONL` writes one JSON object per line with `data` preserved as a
                nested object.
            environment (None | str | Unset): The single environment the export is scoped to. Omit it and a single-
                environment credential implies it (a multi-environment credential must name it), and a named environment must be
                one the caller may access. An export always covers exactly one environment.
            filteroccurred_at (None | str | Unset): Date range using interval notation, e.g.
                `[2026-04-01T00:00:00Z,2026-04-15T00:00:00Z)`.
            filteractor_type (None | str | Unset): Exact match on the event's `actor_type` field.
            filteractor_id (None | str | Unset): Exact match on the event's `actor_id` field.
            filterevent_type (None | str | Unset): Exact match on the event's `event_type` field.
            filterresource_type (None | str | Unset): Exact match on the event's `resource_type` field.
            filterresource_id (None | str | Unset): Exact match on the event's `resource_id` field. Must be accompanied by
                `filter[resource_type]`.
            filtersearch (None | str | Unset): Case-insensitive substring match against `resource_id` or `description`. Must
                be accompanied by either `filter[occurred_at]` or `filter[resource_type]` + `filter[resource_id]`.
            filterdo_not_forward (bool | None | Unset): When set, restrict to events whose `do_not_forward` flag matches the
                given boolean.
            url (None | str | Unset): Absolute, signed download URL. Open in a browser to stream the export to disk. Expires
                shortly after mint — see `expires_at`.
            expires_at (datetime.datetime | None | Unset): When the signed URL stops being valid (ISO-8601 UTC). Open the
                URL well before this time — the signed token is stateless, so a single mint cannot be 'refreshed'; mint a new
                export if the URL has expired.
    """

    format_: ExportFormat
    environment: None | str | Unset = UNSET
    filteroccurred_at: None | str | Unset = UNSET
    filteractor_type: None | str | Unset = UNSET
    filteractor_id: None | str | Unset = UNSET
    filterevent_type: None | str | Unset = UNSET
    filterresource_type: None | str | Unset = UNSET
    filterresource_id: None | str | Unset = UNSET
    filtersearch: None | str | Unset = UNSET
    filterdo_not_forward: bool | None | Unset = UNSET
    url: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        format_: str = self.format_

        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        filteroccurred_at: None | str | Unset
        if isinstance(self.filteroccurred_at, Unset):
            filteroccurred_at = UNSET
        else:
            filteroccurred_at = self.filteroccurred_at

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

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "format": format_,
            }
        )
        if environment is not UNSET:
            field_dict["environment"] = environment
        if filteroccurred_at is not UNSET:
            field_dict["filter[occurred_at]"] = filteroccurred_at
        if filteractor_type is not UNSET:
            field_dict["filter[actor_type]"] = filteractor_type
        if filteractor_id is not UNSET:
            field_dict["filter[actor_id]"] = filteractor_id
        if filterevent_type is not UNSET:
            field_dict["filter[event_type]"] = filterevent_type
        if filterresource_type is not UNSET:
            field_dict["filter[resource_type]"] = filterresource_type
        if filterresource_id is not UNSET:
            field_dict["filter[resource_id]"] = filterresource_id
        if filtersearch is not UNSET:
            field_dict["filter[search]"] = filtersearch
        if filterdo_not_forward is not UNSET:
            field_dict["filter[do_not_forward]"] = filterdo_not_forward
        if url is not UNSET:
            field_dict["url"] = url
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        format_ = check_export_format(d.pop("format"))

        def _parse_environment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        def _parse_filteroccurred_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filteroccurred_at = _parse_filteroccurred_at(d.pop("filter[occurred_at]", UNSET))

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

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        export = cls(
            format_=format_,
            environment=environment,
            filteroccurred_at=filteroccurred_at,
            filteractor_type=filteractor_type,
            filteractor_id=filteractor_id,
            filterevent_type=filterevent_type,
            filterresource_type=filterresource_type,
            filterresource_id=filterresource_id,
            filtersearch=filtersearch,
            filterdo_not_forward=filterdo_not_forward,
            url=url,
            expires_at=expires_at,
        )

        export.additional_properties = d
        return export

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
