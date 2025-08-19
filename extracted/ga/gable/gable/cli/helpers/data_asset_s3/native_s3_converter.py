from __future__ import annotations

from typing import Any, Dict, List

import duckdb
import pyarrow as pa


# ────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────
def _duck_type_to_recap(duck_type: str) -> str | Dict[str, Any]:
    mapping = {
        "BOOLEAN": "boolean",
        "TINYINT": "int8",
        "SMALLINT": "int16",
        "INTEGER": "int32",
        "BIGINT": "int64",
        "UTINYINT": "uint8",
        "USMALLINT": "uint16",
        "UINTEGER": "uint32",
        "UBIGINT": "uint64",
        "FLOAT": "float32",
        "DOUBLE": "float64",
        "DECIMAL": "decimal",
        "VARCHAR": "string",
        "TIME": "time",
        "TIMESTAMP": "timestamp",
        "DATE": "date",
        "BLOB": "bytes",
        "LIST": {"type": "array", "items": None},
        "MAP": "map",
        "STRUCT": {"type": "struct", "fields": []},
    }
    return mapping.get(duck_type.upper(), "string")


def _process_duck_type(duck_type: Any, col_name: str) -> Dict[str, Any]:
    """Process a single DuckDB type, handling nested structs and lists recursively."""
    recap_type = _duck_type_to_recap(str(duck_type.id))

    field_dict = {
        "name": col_name,
    }

    if isinstance(recap_type, dict):
        if recap_type.get("type") == "struct":
            # DuckDB: struct children is a list of (name, type) tuples
            if hasattr(duck_type, "children") and duck_type.children:
                nested_fields = []
                for child_name, child_type in duck_type.children:
                    nested_field_dict = _process_duck_type(child_type, child_name)
                    nested_fields.append(nested_field_dict)
                field_dict.update(
                    {
                        "type": "struct",
                        "fields": nested_fields,
                    }  # type: ignore
                )
            else:
                field_dict["type"] = "struct"
        elif recap_type.get("type") == "array":
            # DuckDB: list children is a list with one (name, type) tuple
            if hasattr(duck_type, "children") and duck_type.children:
                child_name, child_type = duck_type.children[0]
                item_type = _process_duck_type(child_type, "item")
                field_dict.update(
                    {
                        "type": "array",
                        "items": item_type,
                    }  # type: ignore
                )
            else:
                field_dict["type"] = "array"
    else:
        field_dict["type"] = recap_type
    return field_dict


def _arrow_type_to_recap(a_type: pa.DataType) -> str | Dict[str, Any]:
    if pa.types.is_boolean(a_type):
        return "boolean"
    if pa.types.is_integer(a_type):
        signed = a_type.bit_width < 64 and a_type.bit_width != 0
        return ("u" if not signed else "") + f"int{a_type.bit_width}"
    if pa.types.is_floating(a_type):
        return f"float{a_type.bit_width}"
    if pa.types.is_binary(a_type) or pa.types.is_large_binary(a_type):
        return "bytes"
    if pa.types.is_string(a_type) or pa.types.is_large_string(a_type):
        return "string"
    if pa.types.is_timestamp(a_type):
        return "timestamp"
    if pa.types.is_date(a_type):
        return "date"
    if pa.types.is_list(a_type):
        # Return a dict for list types to be processed recursively
        return {"type": "array", "items": None}
    if pa.types.is_struct(a_type):
        # Return a dict for struct types to be processed recursively
        return {"type": "struct", "fields": []}
    return "string"


# ────────────────────────────────────────────────────────────────────────────
# Converter
# ────────────────────────────────────────────────────────────────────────────
class NativeS3Converter:
    """
    Convert DuckDB relations **or** Arrow tables to a Gable/Recap schema dict
    with no pandas dependency.
    """

    def to_recap(self, table: Any, event_name: str) -> Dict[str, Any]:
        if isinstance(table, duckdb.DuckDBPyRelation):
            return self._from_duck_relation(table, event_name)
        if isinstance(table, pa.Table):
            return self._from_arrow_table(table, event_name)
        raise TypeError(
            "NativeS3Converter.to_recap() accepts duckdb.DuckDBPyRelation or pyarrow.Table"
        )

    # ─────────────────────────────  DuckDB path  ─────────────────────────────
    def _from_duck_relation(
        self, rel: duckdb.DuckDBPyRelation, event_name: str
    ) -> Dict[str, Any]:
        """
        Build Recap schema from a DuckDB relation *without* pulling in pandas.

        • We issue a single COUNT(col) per column to know how many NULLs exist.
        fetchall() returns plain Python tuples, so no pandas is involved.
        """
        # ----- 1. build COUNT expression for every column -------------------
        cnt_sql = ", ".join(
            f'COUNT("{col}") AS cnt_{i}' for i, col in enumerate(rel.columns)
        )

        # ----- 2. run aggregation & retrieve counts as a tuple --------------
        non_null_counts = rel.aggregate(cnt_sql).fetchall()[0]  # e.g. (100, 95, 100, …)
        # total_rows WITH the correct syntax
        total_rows_result = rel.aggregate("COUNT(*)").fetchone()
        total_rows = total_rows_result[0] if total_rows_result is not None else 0

        # ----- 3. craft Recap fields ----------------------------------------
        fields: List[Dict[str, Any]] = []
        for idx, col_name in enumerate(rel.columns):
            duck_type = rel.types[idx]  # DuckDBPyType
            field_dict = _process_duck_type(duck_type, col_name)

            non_null_cnt = non_null_counts[idx]

            # If the table is empty, all fields are nullable
            if total_rows == 0:
                nullable = True
            else:
                nullable = (total_rows - non_null_cnt) > 0

            field_dict["nullable"] = nullable
            fields.append(field_dict)

        return {
            "type": "struct",
            "name": event_name,
            "fields": fields,
        }

    # ─────────────────────────────  Arrow path  ─────────────────────────────
    def _from_arrow_table(self, tbl: pa.Table, event_name: str) -> Dict[str, Any]:
        fields: List[Dict[str, Any]] = []
        for field in tbl.schema:
            field_dict = self._process_arrow_field(field)
            fields.append(field_dict)
        return {
            "type": "struct",
            "name": event_name,
            "fields": fields,
        }

    def _process_arrow_field(self, field: pa.Field) -> Dict[str, Any]:
        """Process a single Arrow field, handling nested structs and lists recursively."""
        recap_type = _arrow_type_to_recap(field.type)

        field_dict = {
            "name": field.name,
            "nullable": field.nullable,
        }

        if isinstance(recap_type, dict):
            if recap_type.get("type") == "struct":
                # Handle nested struct - recursively process its fields
                if pa.types.is_struct(field.type):
                    nested_fields = []
                    for nested_field in field.type:
                        nested_field_dict = self._process_arrow_field(nested_field)
                        nested_fields.append(nested_field_dict)

                    field_dict.update(
                        {
                            "type": "struct",
                            "fields": nested_fields,
                        }
                    )
                else:
                    # Fallback for unexpected struct type
                    field_dict["type"] = "struct"
            elif recap_type.get("type") == "array":
                # Handle list type - recursively process its item type
                if pa.types.is_list(field.type):
                    # Create a temporary field for the list item type
                    item_field = pa.field(
                        "item",
                        field.type.value_type,
                        nullable=field.type.value_field.nullable,
                    )
                    item_type = self._process_arrow_field(item_field)

                    field_dict.update(
                        {
                            "type": "array",
                            "items": item_type,
                        }
                    )
                else:
                    # Fallback for unexpected list type
                    field_dict["type"] = "array"
        else:
            # Handle primitive types
            field_dict["type"] = recap_type

        return field_dict


def merge_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple Recap/Gable schemas into one:
    • Flattens field order
    • Recursively merges nested structs and arrays
    • Creates unions when same-named fields differ
    """
    result: dict[str, dict] = {}

    for schema in schemas:
        for field in schema.get("fields", []):
            name = field["name"]

            # first time we see the field → keep as-is
            if name not in result:
                result[name] = field
                continue

            # if both sides are structs, recurse on their fields
            if field["type"] == "struct" and result[name]["type"] == "struct":
                # Merge the nested structs by combining their field schemas
                left_fields = result[name].get("fields", [])
                right_fields = field.get("fields", [])

                # Create temporary schemas for the nested fields
                left_schema = {"type": "struct", "fields": left_fields}
                right_schema = {"type": "struct", "fields": right_fields}

                merged_inner = merge_schemas([left_schema, right_schema])
                result[name] = {
                    "type": "struct",
                    "name": name,
                    "fields": merged_inner["fields"],
                    "nullable": field.get(
                        "nullable", result[name].get("nullable", True)
                    ),
                }
                continue

            # if both sides are arrays, recurse on their items
            if field["type"] == "array" and result[name]["type"] == "array":
                left_item = result[name].get("items", {})
                right_item = field.get("items", {})

                # If both have items, merge them
                if left_item and right_item:
                    # Create temporary schemas for the items
                    left_schema = {"type": "struct", "fields": [left_item]}
                    right_schema = {"type": "struct", "fields": [right_item]}

                    merged_items = merge_schemas([left_schema, right_schema])
                    merged_item = (
                        merged_items["fields"][0] if merged_items["fields"] else {}
                    )

                    result[name] = {
                        "type": "array",
                        "name": name,
                        "items": merged_item,
                        "nullable": field.get(
                            "nullable", result[name].get("nullable", True)
                        ),
                    }
                else:
                    # If one or both don't have items, keep the one that does
                    if left_item:
                        result[name] = result[name]
                    elif right_item:
                        result[name] = field
                    else:
                        # Both are empty arrays, keep the left one
                        result[name] = result[name]
                continue

            # otherwise form / extend a union
            left = result[name]
            right = field

            left_types = left["types"] if left["type"] == "union" else [left]
            right_types = right["types"] if right["type"] == "union" else [right]

            union_types = _get_distinct_dicts(_remove_names(left_types + right_types))

            if len(union_types) == 1:
                result[name] = {"name": name, **union_types[0]}
                continue  # ✅ no union needed

            result[name] = {"type": "union", "name": name, "types": union_types}

    return {"type": "struct", "fields": list(result.values())}


def _get_distinct_dicts(items: list[dict]) -> list[dict]:
    """Return list with duplicates removed, preserving first-seen order."""
    seen, out = set(), []
    for d in items:
        frozen = frozenset(d.items())
        if frozen not in seen:
            seen.add(frozen)
            out.append(d)
    return out


def _remove_names(items: list[dict]) -> list[dict]:
    """Strip 'name' keys so identical types compare equal."""
    return [{k: v for k, v in d.items() if k != "name"} for d in items]
