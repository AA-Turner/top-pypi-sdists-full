from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.flag_source import FlagSource


T = TypeVar("T", bound="FlagSourceResource")


@_attrs_define
class FlagSourceResource:
    """JSON:API resource envelope for a flag source.

    `id` is the source record's UUID. Sources are not created or
    modified directly — the flags service registers and refreshes them
    in response to SDK bulk-register requests.

        Example:
            {'attributes': {'created_at': '2026-04-17T10:00:00Z', 'declared_default': True, 'declared_type': 'BOOLEAN',
                'environment': 'production', 'first_observed': '2026-04-17T10:00:00Z', 'last_seen': '2026-04-17T15:30:00Z',
                'service': 'api-gateway', 'updated_at': '2026-04-17T15:30:00Z'}, 'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
                'type': 'flag_source'}

        Attributes:
            type_ (Literal['flag_source']):
            attributes (FlagSource): A record of an SDK observing a feature flag from a particular
                service and environment.

                The flags service auto-registers a source the first time an SDK
                reports a flag from a given service/environment pair and refreshes
                `last_seen` on every subsequent report. Each source captures the
                value type and default value the SDK declared in source code at
                that location, which makes it possible to detect when service code
                has drifted from the flag's authoritative configuration.
            id (None | str | Unset):
    """

    type_: Literal["flag_source"]
    attributes: FlagSource
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
        from ..models.flag_source import FlagSource

        d = dict(src_dict)
        type_ = cast(Literal["flag_source"], d.pop("type"))
        if type_ != "flag_source":
            raise ValueError(f"type must match const 'flag_source', got '{type_}'")

        attributes = FlagSource.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        flag_source_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        flag_source_resource.additional_properties = d
        return flag_source_resource

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
