"""Manifest parsing for structured item production."""

import collections.abc as cabc
import typing as t
from typing import NamedTuple

from dreadnode.items.models import ASSET_TYPE, FINDING_TYPE

BUILTIN_ITEM_TYPES = {FINDING_TYPE, ASSET_TYPE}
BUILTIN_ITEM_ALIASES = {
    FINDING_TYPE: FINDING_TYPE,
    "findings": FINDING_TYPE,
    ASSET_TYPE: ASSET_TYPE,
    "assets": ASSET_TYPE,
}

_RESERVED_PRODUCES_KEYS = {"enabled", "types", "values", "custom"}


class ItemProducesConfig(NamedTuple):
    """Normalized structured item production config from a capability manifest."""

    enabled: bool
    builtin_types: set[str]
    registry_types: set[str]
    custom_types: dict[str, str]


def _coerce_builtin_type(value: object) -> str | None:
    if value is None:
        return None
    return BUILTIN_ITEM_ALIASES.get(str(value).strip())


def _coerce_builtin_types(value: object) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        item_type = _coerce_builtin_type(value)
        return {item_type} if item_type is not None else set()
    if isinstance(value, cabc.Iterable) and not isinstance(value, (dict, bytes)):
        selected: set[str] = set()
        for raw in value:
            item_type = _coerce_builtin_type(raw)
            if item_type is not None:
                selected.add(item_type)
        return selected
    return set()


def _coerce_registry_types(value: object) -> set[str]:
    values = [value] if isinstance(value, str) else value
    if not isinstance(values, cabc.Iterable) or isinstance(values, (dict, bytes)):
        return set()
    return {
        identifier
        for raw in values
        if (identifier := str(raw).strip()) and _coerce_builtin_type(identifier) is None
    }


def _coerce_custom_types(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    custom: dict[str, str] = {}
    for type_name, ref in value.items():
        if isinstance(ref, str) and ":" in ref:
            custom[str(type_name)] = ref
    return custom


def _legacy_builtin_types(items_cfg: object) -> set[str]:
    if not isinstance(items_cfg, dict):
        return set()
    items = t.cast("dict[str, object]", items_cfg)
    if items.get("enabled") is False:
        return set()
    raw_types = items.get("types")
    if raw_types is None:
        return set(BUILTIN_ITEM_TYPES) if items.get("enabled") is True else set()
    return _coerce_builtin_types(raw_types)


def parse_item_produces_config(manifest: object) -> ItemProducesConfig:
    """Normalize structured-item manifest config.

    New manifests use one ``outputs`` key:

    - ``outputs: true`` enables built-in ``finding`` and ``asset``
    - ``outputs: false`` disables all item tools
    - ``outputs: finding`` or ``outputs: [finding, attack_surface]`` selects registry types
    - ``outputs: {type_name: "module:Class"}`` declares custom item types
    - ``outputs: {enabled: true, values: [...], custom: {...}}`` mixes forms

    When ``outputs`` is absent, deprecated ``produces`` and legacy ``items``
    retain their combined behavior and disable semantics.
    """

    fields_set = getattr(manifest, "model_fields_set", None)
    outputs_present = (
        "outputs" in fields_set if isinstance(fields_set, set) else hasattr(manifest, "outputs")
    )
    output_cfg = (
        getattr(manifest, "outputs", None)
        if outputs_present
        else getattr(manifest, "produces", None)
    )
    items_cfg = None if outputs_present else getattr(manifest, "items", None)
    if output_cfg is False:
        return ItemProducesConfig(
            enabled=False, builtin_types=set(), registry_types=set(), custom_types={}
        )
    if (
        isinstance(items_cfg, dict)
        and t.cast("dict[str, object]", items_cfg).get("enabled") is False
    ):
        return ItemProducesConfig(
            enabled=False, builtin_types=set(), registry_types=set(), custom_types={}
        )

    builtin_types: set[str] = set()
    registry_types: set[str] = set()
    custom_types: dict[str, str] = {}

    if output_cfg is True:
        builtin_types.update(BUILTIN_ITEM_TYPES)
    elif isinstance(output_cfg, str | list):
        builtin_types.update(_coerce_builtin_types(output_cfg))
        registry_types.update(_coerce_registry_types(output_cfg))
    elif isinstance(output_cfg, dict):
        outputs = t.cast("dict[str, object]", output_cfg)
        if outputs.get("enabled") is False:
            return ItemProducesConfig(
                enabled=False,
                builtin_types=set(),
                registry_types=set(),
                custom_types={},
            )
        raw_types = outputs.get("values", outputs.get("types"))
        if raw_types is not None:
            builtin_types.update(_coerce_builtin_types(raw_types))
            registry_types.update(_coerce_registry_types(raw_types))
        elif outputs.get("enabled") is True:
            builtin_types.update(BUILTIN_ITEM_TYPES)

        custom_types.update(_coerce_custom_types(outputs.get("custom")))
        custom_types.update(
            _coerce_custom_types(
                {
                    key: value
                    for key, value in outputs.items()
                    if str(key) not in _RESERVED_PRODUCES_KEYS
                }
            )
        )

    builtin_types.update(_legacy_builtin_types(items_cfg))
    registry_types.difference_update(custom_types)
    return ItemProducesConfig(
        enabled=bool(builtin_types or registry_types or custom_types),
        builtin_types=builtin_types,
        registry_types=registry_types,
        custom_types=custom_types,
    )


def selected_builtin_item_types(manifest: object) -> set[str]:
    """Return built-in item types selected by a capability manifest."""

    config = parse_item_produces_config(manifest)
    return set(config.builtin_types) if config.enabled else set()


def custom_item_type_refs(manifest: object) -> dict[str, str]:
    """Return capability-defined item type refs selected by a manifest."""

    config = parse_item_produces_config(manifest)
    return dict(config.custom_types) if config.enabled else {}


def selected_registry_item_types(manifest: object) -> set[str]:
    """Return identifier-only specialized item types selected by a manifest."""

    config = parse_item_produces_config(manifest)
    return set(config.registry_types) if config.enabled else set()


def item_tools_enabled(manifest: object) -> bool:
    """Return whether this manifest enables any structured item tools."""

    return parse_item_produces_config(manifest).enabled
