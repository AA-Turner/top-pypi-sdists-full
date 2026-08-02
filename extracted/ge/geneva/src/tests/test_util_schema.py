# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors


from __future__ import annotations

from typing import NoReturn, Optional

import attrs
import lancedb
import numpy as np
import pyarrow as pa
import pytest

from geneva.utils.schema import alter_or_create_table, attrs_to_arrow_schema

# ---------- fixtures ----------


@pytest.fixture
def db(tmp_path) -> lancedb.Connection:
    return lancedb.connect(str(tmp_path))


# ---------- models used in tests ----------


@attrs.define
class SupportedAll:
    # primitives
    s: str = attrs.field(metadata={"pa_type": pa.string()}, default="")
    i: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
    f: float = attrs.field(metadata={"pa_type": pa.float64()}, default=0.0)
    b: bool = attrs.field(metadata={"pa_type": pa.bool_()}, default=False)
    by: bytes | None = attrs.field(metadata={"pa_type": pa.binary()}, default=None)

    # optionals
    os_: Optional[str] = attrs.field(metadata={"pa_type": pa.string()}, default=None)
    of: Optional[float] = attrs.field(metadata={"pa_type": pa.float64()}, default=None)
    oi: Optional[int] = attrs.field(metadata={"pa_type": pa.int64()}, default=None)
    ob: Optional[bool] = attrs.field(metadata={"pa_type": pa.bool_()}, default=None)
    oby: Optional[bytes] = attrs.field(metadata={"pa_type": pa.binary()}, default=None)

    # lists
    tags: list[str] = attrs.field(
        metadata={"pa_type": pa.list_(pa.string())}, factory=list
    )


@attrs.define
class MinimalV1:
    id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)


@attrs.define
class MinimalV2(MinimalV1):
    # new columns to be added later
    s: str = attrs.field(metadata={"pa_type": pa.string()}, default="hi")
    f: float = attrs.field(metadata={"pa_type": pa.float64()}, default=1.5)
    b: bool = attrs.field(metadata={"pa_type": pa.bool_()}, default=True)
    by: bytes | None = attrs.field(metadata={"pa_type": pa.binary()}, default=b"")
    tags: list[str] = attrs.field(
        metadata={"pa_type": pa.list_(pa.string())}, default=["a", "b"]
    )


@attrs.define
class UnsupportedDict:
    id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
    meta: dict[str, int] = attrs.field(default={})  # not supported by inference


@attrs.define
class Inner:
    a: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)


@attrs.define
class UnsupportedNestedList:
    id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
    items: list[Inner] = attrs.field(factory=list)  # not supported by inference


@attrs.define
class MapSupportedWithPaType:
    id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
    # explicitly specify Arrow type for a dict-like column
    dims: dict[str, float] = attrs.field(
        metadata={"pa_type": pa.map_(pa.string(), pa.float64())}, factory=dict
    )


# ---------- tests ----------


def test_create_with_all_supported_types(db) -> None:
    tbl = alter_or_create_table(db, "t_supported", SupportedAll())
    sch = tbl.schema

    # types
    assert sch.field("s").type == pa.string()
    assert sch.field("i").type == pa.int64()
    assert sch.field("f").type == pa.float64()
    assert sch.field("b").type == pa.bool_()
    assert sch.field("by").type == pa.binary()
    assert sch.field("tags").type == pa.list_(pa.string())

    # nullability: optionals should be nullable, others depend on default/annotation
    assert sch.field("os_").nullable
    assert sch.field("of").nullable
    assert sch.field("oi").nullable
    assert sch.field("ob").nullable
    assert sch.field("oby").nullable

    # round-trip: table exists, no changes on re-run
    tbl2 = alter_or_create_table(db, "t_supported", SupportedAll())
    assert tbl2.schema == sch


def test_create_race_from_namespace_manifest_reopens_table() -> None:
    class FakeTable:
        schema = pa.schema([pa.field("id", pa.int64())])

    class FakeDB:
        def __init__(self) -> None:
            self.open_calls = 0
            self.create_calls = 0

        def open_table(self, table_name: str, namespace_path: list[str]) -> FakeTable:
            assert table_name == "geneva_errors"
            assert namespace_path == ["__system"]
            self.open_calls += 1
            if self.open_calls == 1:
                raise RuntimeError("Table not found: __system$geneva_errors")
            return FakeTable()

        def create_table(self, table_name: str, **kwargs: object) -> NoReturn:
            assert table_name == "geneva_errors"
            self.create_calls += 1
            raise RuntimeError(
                "Failed to declare table: Merge insert failed: found matching "
                'row with key values: object_id = "__system$geneva_errors"'
            )

    db = FakeDB()
    table = alter_or_create_table(
        db, "geneva_errors", MinimalV1(), namespace_path=["__system"]
    )  # type: ignore[arg-type]

    assert isinstance(table, FakeTable)
    assert db.open_calls == 2
    assert db.create_calls == 1


def test_overwrite_on_empty_when_new_cols_added(db) -> None:
    # create table (empty)
    tbl = alter_or_create_table(db, "t_empty_overwrite", MinimalV1())
    assert len(tbl) == 0

    # now "evolve" schema while table is still empty → should overwrite
    tbl2 = alter_or_create_table(db, "t_empty_overwrite", MinimalV2())
    sch = tbl2.schema
    assert set(sch.names) >= {"id", "s", "f", "b", "by", "tags"}


def _to_py_list(v) -> list:
    # Arrow ListScalar -> Python list
    if isinstance(v, pa.lib.ListScalar):
        return v.as_py()
    # NumPy array -> list
    if isinstance(v, np.ndarray):
        return v.tolist()
    # already a list/tuple
    if isinstance(v, list | tuple):
        return list(v)
    # pandas might give object-dtyped scalar that *is* a list already
    try:
        return list(v)  # last resort (will raise for non-iterables)
    except Exception:
        return v  # let the assert fail noisily


def test_add_columns_on_non_empty_applies_defaults(db) -> None:
    tbl = alter_or_create_table(db, "t_add_cols", MinimalV1())
    tbl.add([{"id": 42}])

    # evolve → newly added columns will be NULL for existing rows
    # (changed behavior: now defaults to NULL instead of model default values)
    tbl = alter_or_create_table(db, "t_add_cols", MinimalV2())
    df = tbl.to_pandas()

    assert set(df.columns) >= {"id", "s", "f", "b", "by", "tags"}
    row = df.iloc[0]
    assert row["id"] == 42
    # Newly added columns are NULL for existing rows
    assert row["s"] is None or (isinstance(row["s"], float) and np.isnan(row["s"]))
    assert row["f"] is None or (isinstance(row["f"], float) and np.isnan(row["f"]))
    assert row["b"] is None or (isinstance(row["b"], float) and np.isnan(row["b"]))
    assert row["by"] is None
    assert row["tags"] is None or (
        isinstance(row["tags"], float) and np.isnan(row["tags"])
    )


def test_drop_columns(db) -> None:
    # make table with extra columns first
    tbl = alter_or_create_table(db, "t_drop", MinimalV2())
    # drop back to MinimalV1
    tbl = alter_or_create_table(db, "t_drop", MinimalV1(), del_cols=True)
    assert set(tbl.schema.names) == {"id"}


def test_unsupported_types_raise_on_create(db) -> None:
    # dict[...] cannot be inferred → TypeError during initial create
    with pytest.raises(TypeError):
        alter_or_create_table(db, "t_bad_dict", UnsupportedDict())

    # list[nested-attrs] cannot be inferred → TypeError during initial create
    with pytest.raises(TypeError):
        alter_or_create_table(db, "t_bad_nested_list", UnsupportedNestedList())


def test_attrs_to_arrow_schema_map_builds_schema_only() -> None:
    @attrs.define
    class MapCol:
        id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
        dims: dict[str, float] = attrs.field(
            metadata={"pa_type": pa.map_(pa.string(), pa.float64())}, factory=dict
        )

    schema = attrs_to_arrow_schema(MapCol())
    assert schema.field("dims").type == pa.map_(pa.string(), pa.float64())


def test_create_with_map_type(db) -> None:  # noqa: ANN001
    """LanceDB supports Arrow Map types in table schemas"""

    @attrs.define
    class MapCol:
        id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
        dims: dict[str, float] = attrs.field(
            metadata={"pa_type": pa.map_(pa.string(), pa.float64())}, factory=dict
        )

    alter_or_create_table(db, "t_map_supported", MapCol())


def test_struct_override_allows_create(db) -> None:
    @attrs.define
    class WithStruct:
        id: int = attrs.field(metadata={"pa_type": pa.int64()}, default=0)
        info: dict[str, int] = attrs.field(
            metadata={"pa_type": pa.struct([pa.field("a", pa.int64())])},
            default={"a": 0},
        )

    tbl = alter_or_create_table(db, "t_struct_ok", WithStruct())
    assert set(tbl.schema.names) == {"id", "info"}
    assert tbl.schema.field("info").type == pa.struct([pa.field("a", pa.int64())])


# ---------- race / stale-cache recovery tests ----------


def test_create_table_failure_falls_back_to_open(db, monkeypatch) -> None:
    """``alter_or_create_table`` must remain idempotent when ``create_table``
    fails but the table actually exists. Common causes:

    - Another worker created the table between our ``open_table`` (404) and
      ``create_table`` call (race).
    - The catalog served a stale "not found" snapshot to ``open_table`` even
      though the table exists; ``create_table`` then fails because the
      underlying namespace sees the directory.
    - Phalanx 500s with a non-JSON body so the client-side exception no
      longer contains "already exists" — string-matching the error is too
      fragile, hence the unconditional re-open path.
    """
    # First create the real table so a subsequent open_table will succeed.
    alter_or_create_table(db, "t_race", SupportedAll())

    real_open = db.open_table
    open_calls = {"n": 0}

    def fake_open(name: str, *args, **kwargs) -> lancedb.table.Table:  # type: ignore[no-untyped-def]
        open_calls["n"] += 1
        if open_calls["n"] == 1:
            # First open: pretend the catalog hasn't seen the table yet.
            raise ValueError(f"Table '{name}' was not found")
        return real_open(name, *args, **kwargs)

    def fake_create(*args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        # Phalanx-style 500 whose body did not survive translation, so the
        # client never sees "already exists" — exactly the bug from the
        # auto-backfill report.
        raise RuntimeError(
            "Runtime error: Failed to declare table: ... "
            "status=500 Internal Server Error, body=Internal server error"
        )

    monkeypatch.setattr(db, "open_table", fake_open)
    monkeypatch.setattr(db, "create_table", fake_create)

    tbl = alter_or_create_table(db, "t_race", SupportedAll())
    assert set(tbl.schema.names).issuperset({"s", "i", "f", "b", "by", "tags"})
    # Sanity: we actually exercised the fallback path.
    assert open_calls["n"] >= 2


def test_create_and_open_both_failing_surfaces_original_create_error(
    db, monkeypatch
) -> None:
    """When the table genuinely doesn't exist, ``create_table`` failing AND
    the fallback ``open_table`` failing should surface the ORIGINAL create
    error (the open retry is best-effort, not a replacement)."""

    def fake_open(name: str, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        raise ValueError(f"Table '{name}' was not found")

    def fake_create(*args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        raise RuntimeError("phalanx down: 503 service unavailable")

    monkeypatch.setattr(db, "open_table", fake_open)
    monkeypatch.setattr(db, "create_table", fake_create)

    with pytest.raises(RuntimeError, match="phalanx down"):
        alter_or_create_table(db, "t_truly_missing", SupportedAll())
