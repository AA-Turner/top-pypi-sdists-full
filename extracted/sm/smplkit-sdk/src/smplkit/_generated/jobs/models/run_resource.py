from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


if TYPE_CHECKING:
    from ..models.run import Run


T = TypeVar("T", bound="RunResource")


@_attrs_define
class RunResource:
    """JSON:API resource envelope for a run (server-assigned UUID id).

    Example:
        {'attributes': {'created_at': '2026-06-05T02:00:00Z', 'finished_at': '2026-06-05T02:00:00.430Z', 'job':
            'nightly-cache-warm', 'job_version': 3, 'pending_duration_ms': 120, 'request': {'body': '{"scope":"all"}',
            'headers': [{'name': 'Authorization', 'value': '<redacted>'}], 'method': 'POST', 'url':
            'https://api.example.com/cache/warm'}, 'result': {'body': '{"ok":true}', 'body_bytes': 11, 'body_truncated':
            False, 'headers': {'content-type': 'application/json'}, 'status': 200}, 'run_duration_ms': 310, 'scheduled_for':
            '2026-06-05T02:00:00Z', 'started_at': '2026-06-05T02:00:00.120Z', 'status': 'SUCCEEDED', 'total_duration_ms':
            430, 'trigger': 'SCHEDULE'}, 'id': '8f2b1c4a-0000-4a1b-9c3d-1e2f3a4b5c6d', 'type': 'run'}

    Attributes:
        id (str):
        attributes (Run): One occurrence of a job executing.
        type_ (str | Unset):  Default: 'run'.
    """

    id: str
    attributes: Run
    type_: str | Unset = "run"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        attributes = self.attributes.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "attributes": attributes,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run import Run

        d = dict(src_dict)
        id = d.pop("id")

        attributes = Run.from_dict(d.pop("attributes"))

        type_ = d.pop("type", UNSET)

        run_resource = cls(
            id=id,
            attributes=attributes,
            type_=type_,
        )

        run_resource.additional_properties = d
        return run_resource

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
