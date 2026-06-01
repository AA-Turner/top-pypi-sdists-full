from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.config import Config


T = TypeVar("T", bound="ConfigCreateResource")


@_attrs_define
class ConfigCreateResource:
    """JSON:API resource envelope for creating a config (id required).

    Example:
        {'attributes': {'description': 'Settings for the user service.', 'environments': {'prod': {'host': 'db-
            prod.internal'}}, 'items': {'host': {'description': 'Database host.', 'type': 'STRING', 'value':
            'db.internal'}}, 'name': 'User Service', 'parent': 'common'}, 'id': 'user-service', 'type': 'config'}

    Attributes:
        id (str): Client-supplied resource id.
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
    """

    id: str
    type_: Literal["config"]
    attributes: Config
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.config import Config

        d = dict(src_dict)
        id = d.pop("id")

        type_ = cast(Literal["config"], d.pop("type"))
        if type_ != "config":
            raise ValueError(f"type must match const 'config', got '{type_}'")

        attributes = Config.from_dict(d.pop("attributes"))

        config_create_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        config_create_resource.additional_properties = d
        return config_create_resource

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
