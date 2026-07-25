from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.config_item_definition_type_type_0 import (
    ConfigItemDefinitionTypeType0,
    check_config_item_definition_type_type_0,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigItemDefinition")


@_attrs_define
class ConfigItemDefinition:
    """Type-declared item within a config.

    Each item carries a value plus a declared type that constrains the
    value and any per-environment overrides for the same key.

        Attributes:
            value (Any | Unset): Current value for the item. May be `null` to represent a cleared (typed but unset) slot —
                for example, after a type change where the prior value could not be coerced.
            type_ (ConfigItemDefinitionTypeType0 | None | Unset): Declared value type. Constrains the JSON shape of `value`
                and of every override of this key in the `environments` map.
            description (None | str | Unset): Optional human-readable explanation of what this item controls.
    """

    value: Any | Unset = UNSET
    type_: ConfigItemDefinitionTypeType0 | Unset | None = UNSET
    description: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        type_: str | Unset | None
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, str):
            type_ = self.type_
        else:
            type_ = self.type_

        description: str | Unset | None
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if type_ is not UNSET:
            field_dict["type"] = type_
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value", UNSET)

        def _parse_type_(data: object) -> ConfigItemDefinitionTypeType0 | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = check_config_item_definition_type_type_0(data)

                return type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ConfigItemDefinitionTypeType0 | None | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_description(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        config_item_definition = cls(
            value=value,
            type_=type_,
            description=description,
        )

        config_item_definition.additional_properties = d
        return config_item_definition

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
