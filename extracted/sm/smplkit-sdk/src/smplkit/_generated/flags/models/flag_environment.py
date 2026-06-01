from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.flag_rule import FlagRule


T = TypeVar("T", bound="FlagEnvironment")


@_attrs_define
class FlagEnvironment:
    """Per-environment evaluation configuration for a flag.

    Attributes:
        enabled (bool | Unset): Whether the flag is active in this environment. When `false`, evaluation skips rules and
            returns the flag's global `default`. Default: True.
        default (Any | None | Unset): Environment-level default returned when no rule fires. If `null`, evaluation falls
            back to the flag's global `default`.
        rules (list[FlagRule] | Unset): Targeting rules evaluated top-down. The first rule whose logic returns truthy
            provides the result.
    """

    enabled: bool | Unset = True
    default: Any | None | Unset = UNSET
    rules: list[FlagRule] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        default: Any | None | Unset
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if default is not UNSET:
            field_dict["default"] = default
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag_rule import FlagRule

        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        def _parse_default(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        default = _parse_default(d.pop("default", UNSET))

        _rules = d.pop("rules", UNSET)
        rules: list[FlagRule] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = FlagRule.from_dict(rules_item_data)

                rules.append(rules_item)

        flag_environment = cls(
            enabled=enabled,
            default=default,
            rules=rules,
        )

        flag_environment.additional_properties = d
        return flag_environment

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
