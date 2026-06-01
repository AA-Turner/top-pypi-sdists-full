from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.export import Export


T = TypeVar("T", bound="ExportResource")


@_attrs_define
class ExportResource:
    """JSON:API resource envelope for an export ticket.

    `id` must not be specified on create requests — the server assigns
    a fresh UUID per mint response. The UUID identifies this particular
    response envelope only; nothing is persisted behind it (the signed
    token inside `attributes.url` is the actual artifact).

        Example:
            {'attributes': {'expires_at': '2026-05-27T12:00:30Z', 'filter[occurred_at]':
                '[2026-05-01T00:00:00Z,2026-06-01T00:00:00Z)', 'filter[resource_type]': 'order', 'format': 'CSV', 'url':
                'https://audit.smplkit.com/api/v1/exports/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.…'}, 'id':
                '11111111-2222-3333-4444-555555555555', 'type': 'export'}

        Attributes:
            attributes (Export): A request for a short-lived signed download URL.

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
            id (None | str | Unset):
            type_ (str | Unset):  Default: 'export'.
    """

    attributes: Export
    id: None | str | Unset = UNSET
    type_: str | Unset = "export"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export import Export

        d = dict(src_dict)
        attributes = Export.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        type_ = d.pop("type", UNSET)

        export_resource = cls(
            attributes=attributes,
            id=id,
            type_=type_,
        )

        export_resource.additional_properties = d
        return export_resource

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
