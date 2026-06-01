"""Stateless helpers shared between the runtime and management flag clients."""

from __future__ import annotations

from typing import Any

from smplkit._generated.flags.models.flag import Flag as GenFlag
from smplkit._generated.flags.models.flag_environment import FlagEnvironment as GenFlagEnvironment
from smplkit._generated.flags.models.flag_environments import FlagEnvironments as GenFlagEnvironments
from smplkit._generated.flags.models.flag_resource import FlagResource as ResourceFlag
from smplkit._generated.flags.models.flag_response import FlagResponse as ResponseFlag
from smplkit._generated.flags.models.flag_rule import FlagRule as GenFlagRule
from smplkit._generated.flags.models.flag_rule_logic import FlagRuleLogic as GenFlagRuleLogic
from smplkit._generated.flags.models.flag_value import FlagValue as GenFlagValue
from smplkit.flags.models import FlagEnvironment as FlagEnvironmentModel
from smplkit.flags.models import FlagRule as FlagRuleModel
from smplkit.flags.models import FlagValue as FlagValueModel


def _extract_environments(environments: Any) -> dict[str, FlagEnvironmentModel]:
    """Convert a generated ``FlagEnvironments`` object to ``dict[str, FlagEnvironment]``."""
    from smplkit._generated.flags.types import UNSET

    if environments is None or isinstance(environments, type(UNSET)):
        return {}
    if not isinstance(environments, GenFlagEnvironments):
        return {}
    result: dict[str, FlagEnvironmentModel] = {}
    for env_name, env_obj in environments.additional_properties.items():
        enabled = env_obj.enabled
        if isinstance(enabled, type(UNSET)):
            enabled = True
        default_val = env_obj.default
        if isinstance(default_val, type(UNSET)):
            default_val = None
        rules_val = env_obj.rules
        if isinstance(rules_val, type(UNSET)):
            rules_tuple: tuple[FlagRuleModel, ...] = ()
        else:
            rules_tuple = tuple(_extract_rule(r) for r in rules_val)
        result[env_name] = FlagEnvironmentModel(
            enabled=bool(enabled),
            default=default_val,
            rules=rules_tuple,
        )
    return result


def _extract_rule(rule: Any) -> FlagRuleModel:
    """Extract a generated FlagRule into the public :class:`FlagRule` model."""
    from smplkit._generated.flags.types import UNSET

    description: str | None = None
    if not isinstance(rule.description, type(UNSET)) and rule.description is not None:
        description = rule.description
    logic = dict(rule.logic.additional_properties) if hasattr(rule.logic, "additional_properties") else {}
    return FlagRuleModel(logic=logic, value=rule.value, description=description)


def _extract_values(values: Any) -> list[FlagValueModel] | None:
    """Convert a list of generated ``FlagValue`` to ``list[FlagValue]`` (or None for unconstrained)."""
    if values is None:
        return None
    return [FlagValueModel(name=v.name, value=v.value) for v in values]


def _unset_to_none(value: Any) -> Any:
    """Convert Unset sentinels to None."""
    type_name = type(value).__name__
    if type_name == "Unset":
        return None
    return value


def _build_gen_flag(
    *,
    name: str,
    type_: str,
    default: Any,
    values: list[FlagValueModel] | None,
    description: str | None = None,
    environments: dict[str, FlagEnvironmentModel] | None = None,
) -> GenFlag:
    """Build a generated Flag model from plain values."""
    gen_values: list[GenFlagValue] | None = None
    if values is not None:
        gen_values = [GenFlagValue(name=v.name, value=v.value) for v in values]

    gen_envs: GenFlagEnvironments | Any
    if environments:
        gen_envs = GenFlagEnvironments()
        env_props: dict[str, GenFlagEnvironment] = {}
        for env_name, env in environments.items():
            rules = []
            for r in env.rules:
                logic_obj = GenFlagRuleLogic()
                logic_obj.additional_properties = dict(r.logic)
                rule_obj = GenFlagRule(
                    logic=logic_obj,
                    value=r.value,
                    description=r.description,
                )
                rules.append(rule_obj)
            env_obj = GenFlagEnvironment(
                enabled=env.enabled,
                default=env.default,
                rules=rules,
            )
            env_props[env_name] = env_obj
        gen_envs.additional_properties = env_props
    else:
        from smplkit._generated.flags.types import UNSET

        gen_envs = UNSET

    return GenFlag(
        name=name,
        type_=type_,
        default=default,
        values=gen_values,
        description=description,
        environments=gen_envs,
    )


def _build_flag_request_body(flag: Any, *, flag_id: str | None = None) -> ResponseFlag:
    """Wrap a Flag model's data in the JSON:API request envelope."""
    gen_flag = _build_gen_flag(
        name=flag.name,
        type_=flag.type,
        default=flag.default,
        values=flag.values,
        description=flag.description,
        environments=flag.environments or None,
    )
    resource = ResourceFlag(attributes=gen_flag, id=flag_id, type_="flag")
    return ResponseFlag(data=resource)


def _flag_dict_from_json(data: dict[str, Any]) -> dict[str, Any]:
    """Extract flat flag attributes from a JSON:API response ``data`` block."""
    attrs = data["attributes"]
    values_raw = attrs.get("values")
    values: list[FlagValueModel] | None = None
    if values_raw is not None:
        values = [FlagValueModel(name=v["name"], value=v["value"]) for v in values_raw]
    envs: dict[str, FlagEnvironmentModel] = {}
    for env_key, env_data in (attrs.get("environments") or {}).items():
        rules_raw = env_data.get("rules") or []
        rules = [
            FlagRuleModel(
                logic=dict(r.get("logic") or {}),
                value=r.get("value"),
                description=r.get("description"),
            )
            for r in rules_raw
        ]
        envs[env_key] = FlagEnvironmentModel(
            enabled=bool(env_data.get("enabled", True)),
            default=env_data.get("default"),
            rules=rules,
        )
    return {
        "id": data.get("id", ""),
        "name": attrs["name"],
        "type": attrs["type"],
        "default": attrs["default"],
        "values": values,
        "description": attrs.get("description"),
        "environments": envs,
        "created_at": attrs.get("created_at"),
        "updated_at": attrs.get("updated_at"),
    }
