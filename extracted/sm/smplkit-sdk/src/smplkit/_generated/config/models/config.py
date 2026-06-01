from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.config_environments_type_0 import ConfigEnvironmentsType0
    from ..models.config_items_type_0 import ConfigItemsType0


T = TypeVar("T", bound="Config")


@_attrs_define
class Config:
    """A named bag of configuration items, optionally inheriting from another config.

    Items are typed key/value pairs (`STRING`, `NUMBER`, `BOOLEAN`,
    `JSON`). Configs may declare per-environment overrides for any item
    declared on the config itself or anywhere in its inheritance chain;
    resolving a config against an environment merges the chain top-down
    and then applies the matching overrides.

        Example:
            {'created_at': '2026-05-11T12:00:00Z', 'description': 'Database connection settings.', 'environments': {'prod':
                {'host': 'db-prod.internal', 'pool_size': 20}}, 'items': {'host': {'description': 'Primary database hostname.',
                'type': 'STRING', 'value': 'db.internal'}, 'pool_size': {'description': 'Connection pool size.', 'type':
                'NUMBER', 'value': 10}}, 'name': 'Database', 'parent': 'common', 'updated_at': '2026-05-11T12:00:00Z'}

        Attributes:
            name (str): Human-readable name for the config.
            description (None | str | Unset): Optional human-readable description of what this config holds.
            parent (None | str | Unset): Key of another config to inherit items from. Inherited items appear as if declared
                on this config; locally declared items with the same key shadow them. Omit or set to `null` for a standalone
                config with no parent.
            items (ConfigItemsType0 | None | Unset): Map of item keys to item definitions declared on this config. Keys must
                be unique within the config; declared types are immutable once set and must match any type declared for the same
                key on an ancestor.
            environments (ConfigEnvironmentsType0 | None | Unset): Map of environment keys to per-environment overrides.
                Each environment maps to a flat object of item key to override value (e.g. `{"production": {"database.host":
                "db-prod.internal"}}`). Only the keys being overridden need to be present. Override values must conform to the
                item's declared `type`; `type` and `description` are always resolved from the defining configuration and are
                never redeclared on an override.
            managed (bool | None | Unset): Whether this config is admin-managed (`true`) or auto-discovered by an SDK and
                not yet claimed (`false`). Configs created through the console or `POST /api/v1/configs` are always managed.
                Configs registered via `POST /api/v1/configs/bulk` land unmanaged. Setting this field to `true` on a PUT
                promotes a discovered config to managed, which consumes a slot of the `config.managed_configurations`
                entitlement.
            created_at (datetime.datetime | None | Unset): When the config was created.
            updated_at (datetime.datetime | None | Unset): When the config was last modified.
    """

    name: str
    description: None | str | Unset = UNSET
    parent: None | str | Unset = UNSET
    items: ConfigItemsType0 | None | Unset = UNSET
    environments: ConfigEnvironmentsType0 | None | Unset = UNSET
    managed: bool | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.config_environments_type_0 import ConfigEnvironmentsType0
        from ..models.config_items_type_0 import ConfigItemsType0

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        parent: None | str | Unset
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        items: dict[str, Any] | None | Unset
        if isinstance(self.items, Unset):
            items = UNSET
        elif isinstance(self.items, ConfigItemsType0):
            items = self.items.to_dict()
        else:
            items = self.items

        environments: dict[str, Any] | None | Unset
        if isinstance(self.environments, Unset):
            environments = UNSET
        elif isinstance(self.environments, ConfigEnvironmentsType0):
            environments = self.environments.to_dict()
        else:
            environments = self.environments

        managed: bool | None | Unset
        if isinstance(self.managed, Unset):
            managed = UNSET
        else:
            managed = self.managed

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parent is not UNSET:
            field_dict["parent"] = parent
        if items is not UNSET:
            field_dict["items"] = items
        if environments is not UNSET:
            field_dict["environments"] = environments
        if managed is not UNSET:
            field_dict["managed"] = managed
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.config_environments_type_0 import ConfigEnvironmentsType0
        from ..models.config_items_type_0 import ConfigItemsType0

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_parent(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent = _parse_parent(d.pop("parent", UNSET))

        def _parse_items(data: object) -> ConfigItemsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                items_type_0 = ConfigItemsType0.from_dict(data)

                return items_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ConfigItemsType0 | None | Unset, data)

        items = _parse_items(d.pop("items", UNSET))

        def _parse_environments(data: object) -> ConfigEnvironmentsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                environments_type_0 = ConfigEnvironmentsType0.from_dict(data)

                return environments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ConfigEnvironmentsType0 | None | Unset, data)

        environments = _parse_environments(d.pop("environments", UNSET))

        def _parse_managed(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        managed = _parse_managed(d.pop("managed", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        config = cls(
            name=name,
            description=description,
            parent=parent,
            items=items,
            environments=environments,
            managed=managed,
            created_at=created_at,
            updated_at=updated_at,
        )

        config.additional_properties = d
        return config

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
