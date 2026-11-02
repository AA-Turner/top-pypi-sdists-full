"""Stability contract for creative-format asset aliases.

`adcp.types.aliases` pins semantic names onto ``AssetsNN`` generated classes
so downstream consumers never import the numbered form. datamodel-codegen
renumbers these whenever the upstream ``$defs`` ordering shifts, which
silently breaks consumers that pinned to ``Assets5`` or ``Assets14``.

These tests assert each semantic alias still resolves to a class whose
``asset_type`` (or ``item_type`` for the group container) discriminator
default matches the expected literal. If a test here fails after a schema
regeneration, the generator renumbered something and the corresponding
alias in ``src/adcp/types/aliases.py`` needs its numbered import updated.

The contract is intentionally loud: add/remove aliases here in lockstep
with ``aliases.py`` so the public API remains stable across generator runs.
"""

from __future__ import annotations

from typing import Literal

import pytest

from adcp import types as adcp_types

INDIVIDUAL_ASSET_EXPECTATIONS: dict[str, str] = {
    "ImageFormatAsset": "image",
    "VideoFormatAsset": "video",
    "AudioFormatAsset": "audio",
    "TextFormatAsset": "text",
    "MarkdownFormatAsset": "markdown",
    "HtmlFormatAsset": "html",
    "CssFormatAsset": "css",
    "JavascriptFormatAsset": "javascript",
    "VastFormatAsset": "vast",
    "DaastFormatAsset": "daast",
    "UrlFormatAsset": "url",
    "WebhookFormatAsset": "webhook",
    "BriefFormatAsset": "brief",
    "CatalogFormatAsset": "catalog",
}

GROUP_ASSET_EXPECTATIONS: dict[str, str] = {
    "ImageFormatGroupAsset": "image",
    "VideoFormatGroupAsset": "video",
    "AudioFormatGroupAsset": "audio",
    "TextFormatGroupAsset": "text",
    "MarkdownFormatGroupAsset": "markdown",
    "HtmlFormatGroupAsset": "html",
    "CssFormatGroupAsset": "css",
    "JavascriptFormatGroupAsset": "javascript",
    "VastFormatGroupAsset": "vast",
    "DaastFormatGroupAsset": "daast",
    "UrlFormatGroupAsset": "url",
    "WebhookFormatGroupAsset": "webhook",
}


def _literal_value(cls, field_name: str) -> str | None:
    """Return the single literal value on a Pydantic discriminator field.

    Parses the field's ``annotation`` (the ``Literal[...]`` type) rather
    than reading ``FieldInfo.default`` — several generated discriminator
    fields declare the literal as the annotation without also setting a
    default, which would make ``FieldInfo.default`` return
    ``PydanticUndefined`` and any equality comparison vacuously pass.
    Reading the annotation catches renumbering even when defaults aren't
    populated on the field.
    """
    from typing import get_args, get_origin

    field = cls.model_fields[field_name]
    annotation = field.annotation
    if get_origin(annotation) is Literal:
        args = get_args(annotation)
        if len(args) == 1 and isinstance(args[0], str):
            return args[0]
    # Fall back to FieldInfo.default when the annotation isn't a bare
    # Literal (Annotated[Literal[...], Field(default=...)] shape).
    default = field.default
    if isinstance(default, str):
        return default
    return None


@pytest.mark.parametrize(
    ("alias_name", "expected_asset_type"),
    list(INDIVIDUAL_ASSET_EXPECTATIONS.items()),
)
def test_individual_asset_alias_resolves_to_expected_discriminator(
    alias_name: str, expected_asset_type: str
) -> None:
    cls = getattr(adcp_types, alias_name)
    asset_type = _literal_value(cls, "asset_type")
    assert asset_type == expected_asset_type, (
        f"{alias_name} resolved to class with asset_type={asset_type!r}; "
        f"expected {expected_asset_type!r}. The generator likely renumbered "
        "AssetsNN — update the numbered import in src/adcp/types/aliases.py "
        "to point at the class matching this asset_type."
    )
    item_type = _literal_value(cls, "item_type")
    assert item_type == "individual", (
        f"{alias_name} resolved to class with item_type={item_type!r}; " "expected 'individual'."
    )


@pytest.mark.parametrize(
    ("alias_name", "expected_asset_type"),
    list(GROUP_ASSET_EXPECTATIONS.items()),
)
def test_group_asset_alias_resolves_to_expected_discriminator(
    alias_name: str, expected_asset_type: str
) -> None:
    cls = getattr(adcp_types, alias_name)
    asset_type = _literal_value(cls, "asset_type")
    assert asset_type == expected_asset_type, (
        f"{alias_name} resolved to class with asset_type={asset_type!r}; "
        f"expected {expected_asset_type!r}. The generator likely renumbered "
        "AssetsNN — update the numbered import in src/adcp/types/aliases.py "
        "to point at the class matching this asset_type."
    )


def test_repeatable_asset_group_discriminator_is_stable() -> None:
    cls = adcp_types.RepeatableAssetGroup
    item_type = _literal_value(cls, "item_type")
    assert item_type == "repeatable_group", (
        f"RepeatableAssetGroup.item_type={item_type!r}; " "expected 'repeatable_group'."
    )


def test_format_category_module_raises_migration_pointer() -> None:
    # MIGRATION_v3_to_v4: `FormatCategory` was removed from the generated
    # schemas in AdCP 3.0. Importing the old module path now raises a
    # guided ImportError instead of ModuleNotFoundError.
    with pytest.raises(ImportError, match="MIGRATION_v3_to_v4"):
        from adcp.types.domains.enums.format_category import (  # noqa: F401
            FormatCategory,
        )


def test_all_aliases_exported_from_adcp_types() -> None:
    # `adcp.types` is the canonical public surface per CLAUDE.md.
    # Top-level ``adcp`` re-exports a curated subset; these format-asset
    # aliases are specifically reachable via ``from adcp.types import X``.
    missing = [
        name
        for name in (
            *INDIVIDUAL_ASSET_EXPECTATIONS,
            *GROUP_ASSET_EXPECTATIONS,
            "RepeatableAssetGroup",
        )
        if not hasattr(adcp_types, name)
    ]
    assert not missing, f"Asset aliases missing from adcp.types: {missing}"


# Asset-content types: `<Type>Content` is the public name for the
# payload-describing types (issue #221). The pre-4.0 `<Type>Asset` names
# collided against `<Type>FormatAsset` (slot-describing) and were removed
# from the public surface in 4.0.
#
# These classes describe an actual asset payload (codec, duration, URL,
# dimensions) rather than a slot inside a format definition, so they
# carry no `asset_type` discriminator — just payload fields like `url`.
CONTENT_TYPE_EXPECTATIONS: dict[str, str] = {
    "AudioContent": "audio_asset",
    "CssContent": "css_asset",
    "HtmlContent": "html_asset",
    "ImageContent": "image_asset",
    "JavascriptContent": "javascript_asset",
    "TextContent": "text_asset",
    "UrlContent": "url_asset",
    "VideoContent": "video_asset",
    "WebhookContent": "webhook_asset",
}


@pytest.mark.parametrize(
    ("content_name", "expected_module_suffix"),
    list(CONTENT_TYPE_EXPECTATIONS.items()),
)
def test_content_type_resolves_to_generated_payload_class(
    content_name: str, expected_module_suffix: str
) -> None:
    # Each public `<Type>Content` must resolve to the corresponding
    # generated payload class under ``domains/core/assets/*``.
    cls = getattr(adcp_types, content_name)
    expected_module = f"adcp.types.domains.core.assets.{expected_module_suffix}"
    assert cls.__module__ == expected_module, (
        f"{content_name} resolved to {cls.__module__}.{cls.__name__}; "
        f"expected a class from {expected_module}."
    )


def test_content_types_do_not_collide_with_format_assets() -> None:
    # Guardrail for the naming split: `<Type>Content` payload types must not
    # resolve to the same class as `<Type>FormatAsset` slot types.
    collisions = []
    for content_name in CONTENT_TYPE_EXPECTATIONS:
        stem = content_name[: -len("Content")]
        format_name = f"{stem}FormatAsset"
        if not hasattr(adcp_types, format_name):
            continue
        if getattr(adcp_types, content_name) is getattr(adcp_types, format_name):
            collisions.append((content_name, format_name))
    assert not collisions, f"Content/FormatAsset collisions: {collisions}"


@pytest.mark.parametrize(
    "legacy_name",
    [
        "AudioAsset",
        "CssAsset",
        "HtmlAsset",
        "ImageAsset",
        "JavascriptAsset",
        "TextAsset",
        "UrlAsset",
        "VideoAsset",
        "WebhookAsset",
    ],
)
def test_legacy_asset_names_not_on_public_surface(legacy_name: str) -> None:
    # Pre-4.0 names for asset-content types. Removed in 4.0 in favor of
    # `<Type>Content`. Guard against both `__all__` membership (star import)
    # and attribute access (`from adcp.types import AudioAsset`), which
    # resolves against module attributes regardless of `__all__`.
    replacement = legacy_name.replace("Asset", "Content")
    assert legacy_name not in adcp_types.__all__, (
        f"{legacy_name} is still in adcp.types.__all__; it was renamed to "
        f"{replacement} in 4.0 per MIGRATION_v3_to_v4.md."
    )
    assert not hasattr(adcp_types, legacy_name), (
        f"{legacy_name} is still an attribute of adcp.types — likely a raw "
        f"`from adcp.types._generated import {legacy_name}` in __init__.py "
        f"missing an `as {replacement}` clause."
    )
