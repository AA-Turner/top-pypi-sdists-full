from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.export_resource import ExportResource


T = TypeVar("T", bound="ExportResponse")


@_attrs_define
class ExportResponse:
    """JSON:API single-resource response carrying the signed URL.

    Attributes:
        data (ExportResource): JSON:API resource envelope for an export ticket.

            `id` must not be specified on create requests — the server assigns
            a fresh UUID per mint response. The UUID identifies this particular
            response envelope only; nothing is persisted behind it (the signed
            token inside `attributes.url` is the actual artifact). Example: {'attributes': {'expires_at':
            '2026-05-27T12:00:30Z', 'filter[occurred_at]': '[2026-05-01T00:00:00Z,2026-06-01T00:00:00Z)',
            'filter[resource_type]': 'order', 'format': 'CSV', 'url':
            'https://audit.smplkit.com/api/v1/exports/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.…'}, 'id':
            '11111111-2222-3333-4444-555555555555', 'type': 'export'}.
    """

    data: ExportResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export_resource import ExportResource

        d = dict(src_dict)
        data = ExportResource.from_dict(d.pop("data"))

        export_response = cls(
            data=data,
        )

        export_response.additional_properties = d
        return export_response

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
