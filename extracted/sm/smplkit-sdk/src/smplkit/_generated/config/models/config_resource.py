from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.config import Config


T = TypeVar("T", bound="ConfigResource")


@_attrs_define
class ConfigResource:
    """JSON:API resource envelope for a config.

    `id` is the human-readable key for the config and must be supplied
    by the caller on create. It is unique within the account.

        Example:
            {'attributes': {'created_at': '2026-05-11T12:00:00Z', 'description': 'Database connection settings.',
                'environments': {'prod': {'host': 'db-prod.internal'}}, 'items': {'host': {'description': 'Primary database
                hostname.', 'type': 'STRING', 'value': 'db.internal'}}, 'name': 'Database', 'parent': 'common', 'updated_at':
                '2026-05-11T12:00:00Z'}, 'id': 'database', 'type': 'config'}

        Attributes:
            type_ (Literal['config']):
            attributes (Config): A named bag of configuration items, optionally inheriting from another config.

                Items are typed key/value pairs (`STRING`, `NUMBER`, `BOOLEAN`,
                `JSON`). Configs may declare per-environment overrides for any item
                declared on the config itself or anywhere in its inheritance chain;
                resolving a config against an environment merges the chain top-down
                and then applies the matching overrides. Example: {'created_at': '2026-05-11T12:00:00Z', 'description':
                'Database connection settings.', 'environments': {'prod': {'host': 'db-prod.internal', 'pool_size': 20}},
                'items': {'host': {'description': 'Primary database hostname.', 'type': 'STRING', 'value': 'db.internal'},
                'pool_size': {'description': 'Connection pool size.', 'type': 'NUMBER', 'value': 10}}, 'name': 'Database',
                'parent': 'common', 'updated_at': '2026-05-11T12:00:00Z'}.
            id (None | str | Unset):
    """

    type_: Literal["config"]
    attributes: Config
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
        from ..models.config import Config

        d = dict(src_dict)
        type_ = cast(Literal["config"], d.pop("type"))
        if type_ != "config":
            raise ValueError(f"type must match const 'config', got '{type_}'")

        attributes = Config.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        config_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        config_resource.additional_properties = d
        return config_resource

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
