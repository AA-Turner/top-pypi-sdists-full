from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.logger_source import LoggerSource


T = TypeVar("T", bound="LoggerSourceResource")


@_attrs_define
class LoggerSourceResource:
    """JSON:API resource envelope for a logger source observation.

    Example:
        {'attributes': {'created_at': '2026-04-01T10:00:00Z', 'environment': 'production', 'first_observed':
            '2026-04-01T10:00:00Z', 'last_seen': '2026-04-11T15:30:00Z', 'resolved_level': 'WARN', 'service': 'api-gateway',
            'updated_at': '2026-04-11T15:30:00Z'}, 'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'type': 'logger_source'}

    Attributes:
        type_ (Literal['logger_source']):
        attributes (LoggerSource): A single service / environment observation of a logger.

            A source row exists for every (service, environment) pair that has
            reported the logger via the bulk registration endpoint. The row's
            levels reflect what the SDK saw on the most recent report. Example: {'created_at': '2026-04-01T10:00:00Z',
            'environment': 'production', 'first_observed': '2026-04-01T10:00:00Z', 'last_seen': '2026-04-11T15:30:00Z',
            'resolved_level': 'WARN', 'service': 'api-gateway', 'updated_at': '2026-04-11T15:30:00Z'}.
        id (None | str | Unset):
    """

    type_: Literal["logger_source"]
    attributes: LoggerSource
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.logger_source import LoggerSource

        d = dict(src_dict)
        type_ = cast(Literal["logger_source"], d.pop("type"))
        if type_ != "logger_source":
            raise ValueError(f"type must match const 'logger_source', got '{type_}'")

        attributes = LoggerSource.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        logger_source_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        logger_source_resource.additional_properties = d
        return logger_source_resource

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
