# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import pyarrow as pa
import pytest
from lance.blob import BlobType
from lance.schema import LanceSchema

from geneva.utils.parse_rust_debug import (
    extract_field_ids,
    extract_field_ids_and_column_indices,
)


class _FakeLanceField:
    def __init__(
        self, name: str, field_id: int, children: list["_FakeLanceField"] | None = None
    ) -> None:
        self._name = name
        self._id = field_id
        self._children = children or []

    def name(self) -> str:
        return self._name

    def id(self) -> int:
        return self._id

    def children(self) -> list["_FakeLanceField"]:
        return self._children


class _FakeLanceSchema:
    def __init__(self, fields: list[_FakeLanceField]) -> None:
        self._fields = fields

    def fields(self) -> list[_FakeLanceField]:
        return self._fields


def _packed_struct_schema() -> LanceSchema:
    struct_type = pa.struct(
        [
            pa.field("x", pa.int32()),
            pa.field("y", pa.int32()),
        ]
    )
    schema = pa.schema(
        [
            pa.field(
                "packed_struct",
                struct_type,
                metadata={"lance-encoding:packed": "true"},
            ),
            pa.field("plain", pa.int32()),
        ]
    )
    return LanceSchema.from_pyarrow(schema)


def test_extract_field_ids_handles_packed_struct_leaf_v21() -> None:
    lance_schema = _packed_struct_schema()
    field_ids, column_indices = extract_field_ids_and_column_indices(
        lance_schema,
        ["packed_struct"],
        "2.1",
    )

    packed_field = lance_schema.field("packed_struct")
    expected_field_ids = [packed_field.id(), *[c.id() for c in packed_field.children()]]
    assert field_ids == expected_field_ids
    assert column_indices[0] == 0
    assert column_indices[1:] == [-1, -1]


def test_extract_field_ids_handles_blob_leaf_v21() -> None:
    schema = pa.schema([pa.field("blob_col", BlobType())])
    lance_schema = LanceSchema.from_pyarrow(schema)
    field_ids, column_indices = extract_field_ids_and_column_indices(
        lance_schema,
        ["blob_col"],
        "2.1",
    )

    blob_field = lance_schema.field("blob_col")
    expected_field_ids = [blob_field.id(), *[c.id() for c in blob_field.children()]]
    assert field_ids == expected_field_ids
    assert column_indices[0] == 0
    assert column_indices[1:] == [-1] * len(blob_field.children())


def test_standard_struct_still_reports_children_columns_v21() -> None:
    schema = pa.schema(
        [
            pa.field(
                "struct_col",
                pa.struct(
                    [pa.field("child_a", pa.int32()), pa.field("child_b", pa.int32())]
                ),
            ),
            pa.field("value", pa.int32()),
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)
    field_ids, column_indices = extract_field_ids_and_column_indices(
        lance_schema,
        ["struct_col"],
        "2.1",
    )

    struct_field = lance_schema.field("struct_col")
    expected_field_ids = [struct_field.id(), *[c.id() for c in struct_field.children()]]
    assert field_ids == expected_field_ids
    # Parent struct should have -1 and children should get concrete column indices
    assert column_indices[0] == -1
    assert column_indices[1:] == [0, 1]


def test_extract_field_ids_supports_dotted_path() -> None:
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field(
                "image",
                pa.struct(
                    [
                        pa.field(
                            "image_bytes",
                            pa.large_binary(),
                            metadata={"lance-encoding:blob": "true"},
                        ),
                        pa.field("error_code", pa.string()),
                    ]
                ),
            ),
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)

    parent = lance_schema.field("image")
    blob_child = next(c for c in parent.children() if c.name() == "image_bytes")

    ids = extract_field_ids(lance_schema, "image.image_bytes")
    # blob leaf has children (position/size); extract_subfield_ids returns
    # the leaf plus those descriptor children.
    assert ids[0] == blob_child.id()
    expected = [blob_child.id(), *[c.id() for c in blob_child.children()]]
    assert ids == expected

    string_child = next(c for c in parent.children() if c.name() == "error_code")
    assert extract_field_ids(lance_schema, "image.error_code") == [string_child.id()]


def test_extract_field_ids_supports_escaped_literal_dot_path() -> None:
    schema = pa.schema(
        [
            pa.field(
                "literal",
                pa.struct([pa.field("a.b", pa.int32())]),
            ),
            pa.field(
                "meta-data",
                pa.struct([pa.field("user-id", pa.int64())]),
            ),
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)

    literal_parent = lance_schema.field("literal")
    literal_child = next(c for c in literal_parent.children() if c.name() == "a.b")
    assert extract_field_ids(lance_schema, "literal.`a.b`") == [literal_child.id()]

    escaped_parent = lance_schema.field("meta-data")
    escaped_child = next(c for c in escaped_parent.children() if c.name() == "user-id")
    assert extract_field_ids(lance_schema, "`meta-data`.`user-id`") == [
        escaped_child.id()
    ]


def test_extract_field_ids_preserves_exact_top_level_literal_dot_name() -> None:
    lance_schema = _FakeLanceSchema(
        [
            _FakeLanceField("literal.a.b", 1),
            _FakeLanceField("literal", 2, [_FakeLanceField("a.b", 3)]),
        ]
    )

    assert extract_field_ids(lance_schema, "literal.a.b") == [1]  # type: ignore[arg-type]
    assert extract_field_ids(lance_schema, "literal.`a.b`") == [3]  # type: ignore[arg-type]


def test_extract_field_ids_distinguishes_unescaped_literal_dot_path() -> None:
    schema = pa.schema(
        [
            pa.field(
                "literal",
                pa.struct([pa.field("a.b", pa.int32())]),
            )
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)

    with pytest.raises(ValueError, match="Field not found"):
        extract_field_ids(lance_schema, "literal.a.b")


def test_extract_field_ids_and_column_indices_supports_nested_leaf_v21() -> None:
    schema = pa.schema(
        [
            pa.field(
                "left",
                pa.struct([pa.field("value", pa.int32())]),
            ),
            pa.field(
                "right",
                pa.struct([pa.field("value", pa.int64())]),
            ),
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)

    left_parent = lance_schema.field("left")
    left_leaf = next(c for c in left_parent.children() if c.name() == "value")
    right_parent = lance_schema.field("right")
    right_leaf = next(c for c in right_parent.children() if c.name() == "value")

    field_ids, column_indices = extract_field_ids_and_column_indices(
        lance_schema,
        ["left.value", "right.value"],
        "2.1",
    )

    assert field_ids == [left_leaf.id(), right_leaf.id()]
    assert column_indices == [0, 1]


def test_extract_field_ids_resolves_case_insensitive_path() -> None:
    schema = pa.schema(
        [
            pa.field(
                "MetaData",
                pa.struct([pa.field("UserId", pa.int32())]),
            )
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)

    parent = lance_schema.field("MetaData")
    child = next(c for c in parent.children() if c.name() == "UserId")
    assert extract_field_ids(lance_schema, "metadata.userid") == [child.id()]


def test_extract_field_ids_raises_on_unknown_dotted_path() -> None:
    schema = pa.schema(
        [
            pa.field(
                "image",
                pa.struct([pa.field("image_bytes", pa.large_binary())]),
            ),
        ]
    )
    lance_schema = LanceSchema.from_pyarrow(schema)

    with pytest.raises(ValueError, match="Field not found"):
        extract_field_ids(lance_schema, "image.missing")
    with pytest.raises(ValueError, match="Field not found"):
        extract_field_ids(lance_schema, "missing.something")


def test_v20_assigns_columns_to_all_fields() -> None:
    lance_schema = _packed_struct_schema()
    field_ids, column_indices = extract_field_ids_and_column_indices(
        lance_schema,
        ["packed_struct"],
        "2.0",
    )

    packed_field = lance_schema.field("packed_struct")
    expected_field_ids = [packed_field.id(), *[c.id() for c in packed_field.children()]]
    assert field_ids == expected_field_ids
    assert column_indices == [0, 1, 2]
