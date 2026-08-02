# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import pyarrow as pa
import pytest

from geneva.utils.schema import (
    format_field_path,
    parse_field_path,
    resolve_arrow_field_path,
    resolve_projected_field_path,
)


def _nested_schema() -> pa.Schema:
    return pa.schema(
        [
            pa.field(
                "metadata",
                pa.struct(
                    [
                        pa.field("user_id", pa.int64()),
                        pa.field("user.id", pa.string()),
                    ]
                ),
            ),
            pa.field(
                "MetaData",
                pa.struct([pa.field("UserId", pa.int32())]),
            ),
            pa.field(
                "literal",
                pa.struct([pa.field("a.b", pa.float32())]),
            ),
            pa.field(
                "left",
                pa.struct([pa.field("value", pa.int32())]),
            ),
            pa.field(
                "right",
                pa.struct([pa.field("value", pa.int64())]),
            ),
            pa.field(
                "meta-data",
                pa.struct([pa.field("user-id", pa.int16())]),
            ),
        ]
    )


def test_parse_and_format_field_path_quotes_literal_segments() -> None:
    assert parse_field_path("metadata.user_id") == ["metadata", "user_id"]
    assert parse_field_path("literal.`a.b`") == ["literal", "a.b"]
    assert parse_field_path("`meta-data`.`user-id`") == ["meta-data", "user-id"]
    assert parse_field_path("`a``b`") == ["a`b"]

    assert format_field_path(["metadata", "user_id"]) == "metadata.user_id"
    assert format_field_path(["literal", "a.b"]) == "literal.`a.b`"
    assert format_field_path(["meta-data", "user-id"]) == "`meta-data`.`user-id`"


def test_resolve_arrow_field_path_returns_canonical_schema_path() -> None:
    schema = _nested_schema()

    resolved = resolve_arrow_field_path(schema, "metadata.user_id")
    assert resolved.canonical_path == "metadata.user_id"
    assert resolved.segments == ("metadata", "user_id")
    assert resolved.field.type == pa.int64()

    literal = resolve_arrow_field_path(schema, "literal.`a.b`")
    assert literal.canonical_path == "literal.`a.b`"
    assert literal.segments == ("literal", "a.b")
    assert literal.field.type == pa.float32()

    escaped = resolve_arrow_field_path(schema, "`meta-data`.`user-id`")
    assert escaped.canonical_path == "`meta-data`.`user-id`"
    assert escaped.field.type == pa.int16()


def test_resolve_arrow_field_path_distinguishes_literal_dot_segment() -> None:
    schema = _nested_schema()

    with pytest.raises(KeyError):
        resolve_arrow_field_path(schema, "literal.a.b")
    assert resolve_arrow_field_path(schema, "literal.`a.b`").field.name == "a.b"


def test_resolve_arrow_field_path_is_case_insensitive_when_unambiguous() -> None:
    schema = pa.schema(
        [
            pa.field(
                "MetaData",
                pa.struct([pa.field("UserId", pa.int32())]),
            )
        ]
    )

    resolved = resolve_arrow_field_path(schema, "metadata.userid")
    assert resolved.canonical_path == "MetaData.UserId"
    assert resolved.field.type == pa.int32()


def test_resolve_arrow_field_path_carries_parent_nullability() -> None:
    schema = pa.schema(
        [
            pa.field(
                "metadata",
                pa.struct([pa.field("user_id", pa.int64(), nullable=False)]),
                nullable=True,
            )
        ]
    )

    resolved = resolve_arrow_field_path(schema, "metadata.user_id")

    assert resolved.field.nullable is False
    assert resolved.nullable is True
    assert resolved.as_projected_field().nullable is True


def test_resolve_projected_field_path_matches_flat_canonical_columns() -> None:
    schema = pa.schema(
        [
            pa.field("MetaData.UserId", pa.int32()),
            pa.field("literal.`a.b`", pa.string()),
        ]
    )

    assert resolve_projected_field_path(schema, "metadata.userid") == "MetaData.UserId"
    assert resolve_projected_field_path(schema, "literal.`a.b`") == "literal.`a.b`"


def test_resolve_arrow_field_path_same_leaf_names_do_not_collide() -> None:
    schema = _nested_schema()

    left = resolve_arrow_field_path(schema, "left.value")
    right = resolve_arrow_field_path(schema, "right.value")

    assert left.canonical_path == "left.value"
    assert right.canonical_path == "right.value"
    assert left.field.type == pa.int32()
    assert right.field.type == pa.int64()
