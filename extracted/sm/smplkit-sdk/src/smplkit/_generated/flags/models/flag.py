from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.flag_type import check_flag_type
from ..models.flag_type import FlagType
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.flag_environments import FlagEnvironments
    from ..models.flag_source import FlagSource
    from ..models.flag_value import FlagValue


T = TypeVar("T", bound="Flag")


@_attrs_define
class Flag:
    """A feature flag whose value is resolved at runtime from environment
    rules and a default.

    A flag has a value type (`BOOLEAN`, `STRING`, `NUMERIC`, or `JSON`)
    and either a fixed set of allowed values (constrained) or accepts
    any value matching the type (unconstrained). Each environment can
    enable or disable the flag, set its own default, and define
    targeting rules that override the default for specific evaluation
    contexts.

        Example:
            {'created_at': '2026-03-27T10:00:00Z', 'default': False, 'description': 'Enable dark mode for the application
                UI', 'environments': {'production': {'default': False, 'enabled': True, 'rules': [{'description': 'Beta users
                get dark mode', 'logic': {'==': [{'var': 'customer.beta'}, True]}, 'value': True}]}, 'staging': {'default':
                True, 'enabled': True, 'rules': []}}, 'managed': True, 'name': 'Dark Mode', 'type': 'BOOLEAN', 'updated_at':
                '2026-03-27T10:00:00Z', 'values': [{'name': 'on', 'value': True}, {'name': 'off', 'value': False}]}

        Attributes:
            name (str): Human-readable display name for the flag. Cannot be empty or whitespace-only.
            type_ (FlagType): Value type of the flag. Accepted case-insensitively. Changing the type cascades to `values`,
                `default`, and every environment's rules and default.
            default (Any): Default value returned when no environment rule fires and the environment has no `default`. For
                constrained flags (non-null `values`), must equal one of the entries in the `values` array. For unconstrained
                flags, must match `type`.
            description (None | str | Unset): Human-readable description of the flag's purpose.
            values (list[FlagValue] | None | Unset): Ordered set of allowed values for a constrained flag, or `null` for an
                unconstrained flag. `BOOLEAN` flags, if constrained, must declare exactly two values.
            environments (FlagEnvironments | Unset): Per-environment configuration keyed by environment name (`production`,
                `staging`, etc.). Environments not listed fall back to the flag's global `default`.
            managed (bool | None | Unset): `true` when the flag was created through the API, `false` when it was auto-
                discovered from a bulk-register call. Auto-discovered flags can be edited and converted to managed by setting
                this to `true`.
            sources (list[FlagSource] | None | Unset): SDK-reported observations of this flag, grouped by service and
                environment. Populated automatically by the bulk-register endpoint.
            created_at (datetime.datetime | None | Unset): When the flag was created.
            updated_at (datetime.datetime | None | Unset): When the flag was last modified.
    """

    name: str
    type_: FlagType
    default: Any
    description: None | str | Unset = UNSET
    values: list[FlagValue] | None | Unset = UNSET
    environments: FlagEnvironments | Unset = UNSET
    managed: bool | None | Unset = UNSET
    sources: list[FlagSource] | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_: str = self.type_

        default = self.default

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        values: list[dict[str, Any]] | None | Unset
        if isinstance(self.values, Unset):
            values = UNSET
        elif isinstance(self.values, list):
            values = []
            for values_type_0_item_data in self.values:
                values_type_0_item = values_type_0_item_data.to_dict()
                values.append(values_type_0_item)

        else:
            values = self.values

        environments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environments, Unset):
            environments = self.environments.to_dict()

        managed: bool | None | Unset
        if isinstance(self.managed, Unset):
            managed = UNSET
        else:
            managed = self.managed

        sources: list[dict[str, Any]] | None | Unset
        if isinstance(self.sources, Unset):
            sources = UNSET
        elif isinstance(self.sources, list):
            sources = []
            for sources_type_0_item_data in self.sources:
                sources_type_0_item = sources_type_0_item_data.to_dict()
                sources.append(sources_type_0_item)

        else:
            sources = self.sources

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
                "type": type_,
                "default": default,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if values is not UNSET:
            field_dict["values"] = values
        if environments is not UNSET:
            field_dict["environments"] = environments
        if managed is not UNSET:
            field_dict["managed"] = managed
        if sources is not UNSET:
            field_dict["sources"] = sources
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag_environments import FlagEnvironments
        from ..models.flag_source import FlagSource
        from ..models.flag_value import FlagValue

        d = dict(src_dict)
        name = d.pop("name")

        type_ = check_flag_type(d.pop("type"))

        default = d.pop("default")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_values(data: object) -> list[FlagValue] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                values_type_0 = []
                _values_type_0 = data
                for values_type_0_item_data in _values_type_0:
                    values_type_0_item = FlagValue.from_dict(values_type_0_item_data)

                    values_type_0.append(values_type_0_item)

                return values_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[FlagValue] | None | Unset, data)

        values = _parse_values(d.pop("values", UNSET))

        _environments = d.pop("environments", UNSET)
        environments: FlagEnvironments | Unset
        if isinstance(_environments, Unset):
            environments = UNSET
        else:
            environments = FlagEnvironments.from_dict(_environments)

        def _parse_managed(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        managed = _parse_managed(d.pop("managed", UNSET))

        def _parse_sources(data: object) -> list[FlagSource] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sources_type_0 = []
                _sources_type_0 = data
                for sources_type_0_item_data in _sources_type_0:
                    sources_type_0_item = FlagSource.from_dict(sources_type_0_item_data)

                    sources_type_0.append(sources_type_0_item)

                return sources_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[FlagSource] | None | Unset, data)

        sources = _parse_sources(d.pop("sources", UNSET))

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

        flag = cls(
            name=name,
            type_=type_,
            default=default,
            description=description,
            values=values,
            environments=environments,
            managed=managed,
            sources=sources,
            created_at=created_at,
            updated_at=updated_at,
        )

        flag.additional_properties = d
        return flag

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
