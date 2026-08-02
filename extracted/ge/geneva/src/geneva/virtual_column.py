# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Utilities for marshaling UDFs into virtual column entries for the namespace API."""

from __future__ import annotations

from typing import Any

from geneva.transformer import UDF  # noqa: TC001 — used at runtime


def build_virtual_column_entry(
    col_name: str,
    udf: UDF,
    input_cols: list[str],
    packager: Any,
    table_ref: Any = None,
) -> dict[str, Any]:
    """Build an ``AddVirtualColumnEntry`` dict from a Geneva UDF.

    Marshals the UDF via the packager and builds the payload expected by
    the namespace API's ``alter_table_add_columns`` endpoint.
    """
    import base64

    from geneva.packager import DockerUDFSpecV1

    udf_spec = packager.marshal(udf, table_ref=table_ref)

    image = ""
    backend_spec = DockerUDFSpecV1.from_bytes(udf_spec.udf_payload)
    if backend_spec.image:
        image = backend_spec.image
        if backend_spec.tag:
            image = f"{image}:{backend_spec.tag}"

    data_type = _arrow_type_to_json(udf.data_type)

    entry: dict[str, Any] = {
        "input_columns": input_cols,
        "outputs": [
            {
                "column": col_name,
                "struct_field": "",
                "data_type": data_type,
                "nullable": True,
            }
        ],
        "image": image,
        "udf_version": udf.version or "",
        "udf_name": udf_spec.name,
        "udf_backend": udf_spec.backend,
        "udf": base64.b64encode(udf_spec.udf_payload).decode("ascii"),
        "auto_backfill": bool(udf.auto_backfill),
    }

    if udf.manifest is not None:
        manifest_json = udf.manifest.to_json()
        manifest_checksum = udf.manifest.compute_checksum()
        entry["manifest"] = manifest_json
        entry["manifest_checksum"] = manifest_checksum

    if udf.field_metadata:
        entry["field_metadata"] = dict(udf.field_metadata)

    return entry


def _arrow_type_to_json(dt: Any) -> dict[str, Any]:
    """Convert a PyArrow DataType to the JSON representation that
    lance's ``JsonDataType`` expects.
    """
    import pyarrow as pa

    simple_map: dict[Any, str] = {
        pa.null(): "null",
        pa.bool_(): "bool",
        pa.int8(): "int8",
        pa.int16(): "int16",
        pa.int32(): "int32",
        pa.int64(): "int64",
        pa.uint8(): "uint8",
        pa.uint16(): "uint16",
        pa.uint32(): "uint32",
        pa.uint64(): "uint64",
        pa.float16(): "halffloat",
        pa.float32(): "float",
        pa.float64(): "double",
        pa.string(): "string",
        pa.large_string(): "large_string",
        pa.binary(): "binary",
        pa.large_binary(): "large_binary",
        pa.date32(): "date32:day",
        pa.date64(): "date64:ms",
    }

    if dt in simple_map:
        return {"type": simple_map[dt]}

    if pa.types.is_list(dt):
        return {
            "type": "list",
            "fields": [_arrow_field_to_json("item", dt.value_type, nullable=True)],
        }

    if pa.types.is_large_list(dt):
        return {
            "type": "large_list",
            "fields": [_arrow_field_to_json("item", dt.value_type, nullable=True)],
        }

    if pa.types.is_fixed_size_list(dt):
        return {
            "type": "fixed_size_list",
            "fields": [_arrow_field_to_json("item", dt.value_type, nullable=True)],
            "length": dt.list_size,
        }

    if pa.types.is_struct(dt):
        fields = []
        for i in range(dt.num_fields):
            f = dt.field(i)
            fields.append(_arrow_field_to_json(f.name, f.type, f.nullable))
        return {"type": "struct", "fields": fields}

    return {"type": str(dt)}


def _arrow_field_to_json(name: str, dt: Any, nullable: bool = True) -> dict[str, Any]:
    """Convert to lance's ``JsonField`` format."""
    return {
        "name": name,
        "type": _arrow_type_to_json(dt),
        "nullable": nullable,
    }
