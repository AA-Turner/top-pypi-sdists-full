from __future__ import annotations

from typing import Any, Dict, Optional, Union, cast


AppliedVariants = Optional[Dict[str, Any]]
TagValue = Union[str, Dict[str, str]]


def _get_parent_variantised_path(applied_variants: Dict[str, Any], meta_key: str) -> str:
    """
    Port of JS getParentVariantisedPath().
    Finds the longest variantised field path that is a prefix of meta_key.
    """
    try:
        if not meta_key:
            return ""
        variantised_field_paths = sorted(applied_variants.keys(), key=len, reverse=True)
        child_fragments = meta_key.split(".")
        if not child_fragments or not variantised_field_paths:
            return ""
        for path in variantised_field_paths:
            parent_fragments = str(path).split(".")
            if len(parent_fragments) > len(child_fragments):
                continue
            if all(child_fragments[i] == parent_fragments[i] for i in range(len(parent_fragments))):
                return str(path)
        return ""
    except Exception:
        return ""


def _apply_variant_to_data_value(data_value: str, applied_variants: AppliedVariants, meta_key: str, should_apply_variant: bool) -> str:
    """
    Port of JS applyVariantToDataValue().

    If the current field (or its parent field path) is variantised, prefixes with
    'v2:' and appends `_{variant}` to the entry uid segment of the dot-path.
    """
    if not should_apply_variant or not applied_variants or not meta_key or not isinstance(applied_variants, dict):
        return data_value

    variant: Optional[str] = None
    if meta_key in applied_variants:
        variant = str(applied_variants[meta_key])
    else:
        parent_path = _get_parent_variantised_path(applied_variants, meta_key)
        if parent_path:
            variant = str(applied_variants.get(parent_path))

    if not variant:
        return data_value

    parts = ("v2:" + data_value).split(".")
    if len(parts) >= 2:
        parts[1] = parts[1] + "_" + variant
    return ".".join(parts)


def _tags_value(data_value: str, tags_as_object: bool, applied_variants: AppliedVariants, meta_key: str, should_apply_variant: bool) -> TagValue:
    resolved = _apply_variant_to_data_value(data_value, applied_variants, meta_key, should_apply_variant)
    if tags_as_object:
        return {"data-cslp": resolved}
    return f"data-cslp={resolved}"


def _parent_tags_value(data_value: str, tags_as_object: bool) -> TagValue:
    if tags_as_object:
        return {"data-cslp-parent-field": data_value}
    return f"data-cslp-parent-field={data_value}"


def getTag(  # pylint: disable=invalid-name
    content: Any,
    prefix: str,
    tags_as_object: bool,
    locale: str,
    applied_variants: AppliedVariants,
    should_apply_variant: bool,
    meta_key: str = "",
) -> Dict[str, Any]:
    """
    Port of JS getTag() from `src/entry-editable.ts`.

    Returns a dict mapping field keys to CSLP tag values, and mutates nested objects/refs
    by attaching their own `$` tag maps.
    """
    if content is None or not isinstance(content, dict):
        return {}

    tags: Dict[str, Any] = {}
    for key, value in content.items():
        if key == "$":
            continue

        meta_uid = ""
        if isinstance(value, dict):
            meta = value.get("_metadata")
            if isinstance(meta, dict) and meta.get("uid"):
                meta_uid = str(meta.get("uid"))

        meta_key_prefix = (meta_key + ".") if meta_key else ""
        updated_meta_key = f"{meta_key_prefix}{key}" if should_apply_variant else ""
        if meta_uid and updated_meta_key:
            updated_meta_key = updated_meta_key + "." + meta_uid

        if isinstance(value, list):
            for index, obj in enumerate(value):
                if obj is None:
                    continue

                child_key = f"{key}__{index}"
                parent_key = f"{key}__parent"

                obj_meta_uid = ""
                if isinstance(obj, dict):
                    meta = obj.get("_metadata")
                    if isinstance(meta, dict) and meta.get("uid"):
                        obj_meta_uid = str(meta.get("uid"))

                array_meta_key = f"{meta_key_prefix}{key}" if should_apply_variant else ""
                if obj_meta_uid and array_meta_key:
                    array_meta_key = array_meta_key + "." + obj_meta_uid

                tags[child_key] = _tags_value(
                    f"{prefix}.{key}.{index}",
                    tags_as_object,
                    applied_variants,
                    array_meta_key,
                    should_apply_variant,
                )
                tags[parent_key] = _parent_tags_value(f"{prefix}.{key}", tags_as_object)

                # Reference entries in array
                if isinstance(obj, dict) and obj.get("_content_type_uid") is not None and obj.get("uid") is not None:
                    new_applied_variants = obj.get("_applied_variants")
                    if new_applied_variants is None and isinstance(obj.get("system"), dict):
                        new_applied_variants = cast(dict, obj["system"]).get("applied_variants")
                    new_should_apply_variant = bool(new_applied_variants)

                    obj_locale = obj.get("locale") or locale
                    obj["$"] = getTag(
                        obj,
                        f"{obj.get('_content_type_uid')}.{obj.get('uid')}.{obj_locale}",
                        tags_as_object,
                        locale,
                        cast(AppliedVariants, new_applied_variants),
                        new_should_apply_variant,
                        meta_key="",
                    )
                    continue

                if isinstance(obj, dict):
                    obj["$"] = getTag(
                        obj,
                        f"{prefix}.{key}.{index}",
                        tags_as_object,
                        locale,
                        applied_variants,
                        should_apply_variant,
                        meta_key=array_meta_key,
                    )

            tags[key] = _tags_value(
                f"{prefix}.{key}",
                tags_as_object,
                applied_variants,
                updated_meta_key,
                should_apply_variant,
            )
            continue

        if isinstance(value, dict):
            value["$"] = getTag(
                value,
                f"{prefix}.{key}",
                tags_as_object,
                locale,
                applied_variants,
                should_apply_variant,
                meta_key=updated_meta_key,
            )
            tags[key] = _tags_value(
                f"{prefix}.{key}",
                tags_as_object,
                applied_variants,
                updated_meta_key,
                should_apply_variant,
            )
            continue

        tags[key] = _tags_value(
            f"{prefix}.{key}",
            tags_as_object,
            applied_variants,
            updated_meta_key,
            should_apply_variant,
        )

    return tags


def addTags(  # pylint: disable=invalid-name
    entry: Optional[dict],
    contentTypeUid: str,
    tagsAsObject: bool,
    locale: str = "en-us",
    options: Optional[dict] = None,
) -> None:
    """
    Port of JS addTags() from `src/entry-editable.ts`.
    Mutates `entry` by attaching a `$` dict of CSLP tags.
    """
    if not entry:
        return

    use_lower_case_locale = True
    if isinstance(options, dict) and "useLowerCaseLocale" in options:
        use_lower_case_locale = bool(options.get("useLowerCaseLocale"))

    content_type_uid = (contentTypeUid or "").lower()
    resolved_locale = (locale or "en-us")
    if use_lower_case_locale:
        resolved_locale = resolved_locale.lower()

    applied_variants = entry.get("_applied_variants")
    if applied_variants is None and isinstance(entry.get("system"), dict):
        applied_variants = cast(dict, entry["system"]).get("applied_variants")
    should_apply_variant = bool(applied_variants)

    entry["$"] = getTag(
        entry,
        f"{content_type_uid}.{entry.get('uid')}.{resolved_locale}",
        tagsAsObject,
        resolved_locale,
        cast(AppliedVariants, applied_variants),
        should_apply_variant,
        meta_key="",
    )


# JS parity export name
addEditableTags = addTags  # pylint: disable=invalid-name

# Pythonic aliases
add_tags = addTags
get_tags = getTag

