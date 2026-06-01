from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="EnvironmentUsage")


@_attrs_define
class EnvironmentUsage:
    """Counts of references to an environment held by other resources.

    Returned by `GET /environments/{id}/usage` so the console can warn
    the user about per-environment configuration that would survive a
    bare environment-row deletion. Each count is the number of distinct
    referencing resources, not the number of rule entries within them.

        Example:
            {'config_overrides': 5, 'flag_env_defaults': 2, 'flag_rules': 3, 'logger_overrides': 1}

        Attributes:
            flag_rules (int): Number of feature-flag targeting rules scoped to this environment. Each flag may contribute
                multiple rules.
            flag_env_defaults (int): Number of feature flags that declare an environment-level default value for this
                environment.
            config_overrides (int): Number of config-item overrides keyed to this environment, summed across all configs.
            logger_overrides (int): Number of loggers with an environment-level level override for this environment.
    """

    flag_rules: int
    flag_env_defaults: int
    config_overrides: int
    logger_overrides: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flag_rules = self.flag_rules

        flag_env_defaults = self.flag_env_defaults

        config_overrides = self.config_overrides

        logger_overrides = self.logger_overrides

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flag_rules": flag_rules,
                "flag_env_defaults": flag_env_defaults,
                "config_overrides": config_overrides,
                "logger_overrides": logger_overrides,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        flag_rules = d.pop("flag_rules")

        flag_env_defaults = d.pop("flag_env_defaults")

        config_overrides = d.pop("config_overrides")

        logger_overrides = d.pop("logger_overrides")

        environment_usage = cls(
            flag_rules=flag_rules,
            flag_env_defaults=flag_env_defaults,
            config_overrides=config_overrides,
            logger_overrides=logger_overrides,
        )

        environment_usage.additional_properties = d
        return environment_usage

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
