# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from typing import Any

import lance

from geneva.utils.schema import parse_field_path

__all__ = ["extract_field_ids", "extract_field_ids_and_column_indices"]


def _get_metadata_value(field, key: str) -> str | None:
    metadata = field.metadata or {}
    if not metadata:
        return None
    value = metadata.get(key)
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return value


def _is_packed_struct_field(field) -> bool:
    metadata = field.metadata or {}
    for key in ("packed", "lance-encoding:packed"):
        value = metadata.get(key)
        if value is None:
            continue
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="ignore")
        if isinstance(value, str) and value.lower() == "true":
            return True
    return False


def _is_blob_field(field) -> bool:
    ext_name = _get_metadata_value(field, "ARROW:extension:name")
    if ext_name and ext_name.startswith("lance.blob"):
        return True
    blob_flag = _get_metadata_value(field, "lance-encoding:blob")
    return bool(blob_flag and blob_flag.lower() == "true")


def extract_subfield_ids(
    field, *, omit_special_leaf_children: bool = False
) -> list[int]:
    """Extract field id from a LanceField and all its children."""
    ids = [field.id()]
    if omit_special_leaf_children and (
        _is_packed_struct_field(field) or _is_blob_field(field)
    ):
        return ids
    for child in field.children():
        ids.extend(
            extract_subfield_ids(
                child, omit_special_leaf_children=omit_special_leaf_children
            )
        )
    return ids


def _field_name(field) -> str:
    return field.name()


def _find_lance_child(fields: list[Any], segment: str, full_path: str) -> Any:
    exact = [field for field in fields if _field_name(field) == segment]
    if exact:
        return exact[0]

    lowered = segment.lower()
    matches = [field for field in fields if _field_name(field).lower() == lowered]
    if not matches:
        raise ValueError("Field not found in schema: " + full_path)
    if len(matches) > 1:
        raise ValueError("Ambiguous field path in schema: " + full_path)
    return matches[0]


def _resolve_lance_field_path(schema: lance.lance.LanceSchema, field_name: str) -> Any:
    for field in schema.fields():
        if _field_name(field) == field_name:
            return field

    parts = parse_field_path(field_name)
    current = _find_lance_child(schema.fields(), parts[0], field_name)
    for part in parts[1:]:
        current = _find_lance_child(current.children(), part, field_name)
    return current


def _extract_subfield_ids_and_column_indices(
    field,
    column_counter: list[int],
    is_v21: bool,
    *,
    force_no_column: bool = False,
    omit_special_leaf_children: bool = False,
) -> tuple[list[int], list[int]]:
    """Extract field ids and their corresponding column indices from a LanceField.

    For Lance 2.1, only leaf fields (fields with no children) have actual columns.
    Non-leaf fields (list parents, struct parents) have column_index = -1.

    For Lance 2.0, all fields have columns.

    Parameters
    ----------
    field : LanceField
        The lance field to extract from.
    column_counter : list[int]
        A single-element list containing the current column index counter.
        Modified in place.
    is_v21 : bool
        True if the data storage version is 2.1 or later.

    Returns
    -------
    tuple[list[int], list[int]]
        A tuple of (field_ids, column_indices) with matching lengths.
    """
    field_ids = []
    column_indices = []

    children = field.children()
    has_children = len(children) > 0
    is_special_leaf = _is_packed_struct_field(field) or _is_blob_field(field)
    is_materialized_leaf = not has_children or is_special_leaf

    field_ids.append(field.id())

    if is_v21:
        if force_no_column:
            column_indices.append(-1)
        elif is_materialized_leaf:
            column_indices.append(column_counter[0])
            column_counter[0] += 1
        else:
            column_indices.append(-1)
    else:
        # In 2.0, all fields have columns
        column_indices.append(column_counter[0])
        column_counter[0] += 1

    if is_special_leaf and omit_special_leaf_children:
        return field_ids, column_indices

    child_force_no_column = force_no_column or is_special_leaf
    for child in children:
        child_ids, child_indices = _extract_subfield_ids_and_column_indices(
            child,
            column_counter,
            is_v21,
            force_no_column=child_force_no_column,
            omit_special_leaf_children=omit_special_leaf_children,
        )
        field_ids.extend(child_ids)
        column_indices.extend(child_indices)

    return field_ids, column_indices


def extract_field_ids_and_column_indices(
    schema: lance.lance.LanceSchema,
    field_names: list[str],
    data_storage_version: str,
    *,
    omit_special_leaf_children: bool = False,
) -> tuple[list[int], list[int]]:
    """Gets field ids and column indices for the specified fields.

    For Lance 2.1+, only leaf fields (primitives) have actual columns.
    Non-leaf fields (list/struct parents) have column_index = -1.

    For Lance 2.0, all fields have columns.

    Parameters
    ----------
    schema : lance.lance.LanceSchema
        The Lance schema to search in.
    field_names : list[str]
        The names of fields to extract.
    data_storage_version : str
        The data storage version string (e.g., "2.0", "2.1").

    Note
    ----
    This mirrors lance-core's 2.1 column mapping logic until Lance exposes a
    public helper. Remove once that utility exists.

    Returns
    -------
    tuple[list[int], list[int]]
        A tuple of (field_ids, column_indices) with matching lengths.

    Raises
    ------
    ValueError
        If a field is not found in the schema.
    """
    # Parse version to determine if we're using 2.1+ behavior
    major, minor = data_storage_version.split(".")
    is_v21 = int(major) > 2 or (int(major) == 2 and int(minor) >= 1)

    all_field_ids: list[int] = []
    all_column_indices: list[int] = []
    column_counter = [0]  # Use list to allow mutation in recursive calls

    for field_name in field_names:
        field = _resolve_lance_field_path(schema, field_name)
        field_ids, column_indices = _extract_subfield_ids_and_column_indices(
            field,
            column_counter,
            is_v21,
            omit_special_leaf_children=omit_special_leaf_children,
        )
        all_field_ids.extend(field_ids)
        all_column_indices.extend(column_indices)

    return all_field_ids, all_column_indices


def extract_field_ids(
    schema: lance.lance.LanceSchema,
    field_name: str,
    *,
    omit_special_leaf_children: bool = False,
) -> list[int]:
    """Gets the field id of the specified field name and its children if they
    are a compound type or nested compound type.

    Supports dotted paths (e.g. ``"image.image_bytes"``) by walking nested
    struct children by name.

    Parameters
    ----------
    schema : lance.lance.LanceSchema
        The Lance schema to search in.
    field_name : str
        The name of the field to search for. May be a dotted path into a
        struct (e.g. ``"parent.child"``).

    Raises
    ------
    ValueError
        If the field is not found in the schema.
    """
    return extract_subfield_ids(
        _resolve_lance_field_path(schema, field_name),
        omit_special_leaf_children=omit_special_leaf_children,
    )
