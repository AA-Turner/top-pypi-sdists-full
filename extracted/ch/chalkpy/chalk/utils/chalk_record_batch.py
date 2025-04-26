from __future__ import annotations

import collections.abc
import functools
import random
import weakref
from itertools import zip_longest
from typing import Any, Generator, Iterable, Iterator, Literal, Mapping, Sequence, TypeVar, cast

import pyarrow as pa
import pyarrow.compute
from typing_extensions import Self, assert_never

from chalk.utils.collections import FrozenOrderedSet
from chalk.utils.df_utils import pa_cast, pa_table_to_pl_df, to_pylist
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.weak_set_by_identity import WeakSetByIdentity

_LEFT_INDEX_COL = "__chalk__.ChalkRecordBatch.LEFT_INDEX_COL"
_RIGHT_INDEX_COL = "__chalk__.ChalkRecordBatch.RIGHT_INDEX_COL"

# We are missing good type stubs for pyarrow compute
pc = cast(Any, pyarrow.compute)

# For small tables, no need to construct a sequential index list for each join
# Instead, we'll use this preallocated list, and slice from it
# By using 32 bit integers, this list will take up 4 * (2**24) bytes ~= 67 MB
_PREALLOCATED_INDEX_ARRAY_LEN = 2**24
_PREALLOCATED_INDEX_ARRAY = pc.subtract_checked(
    pc.cumulative_sum_checked(pa.nulls(_PREALLOCATED_INDEX_ARRAY_LEN, pa.int32()).fill_null(1)),
    pa.scalar(1, pa.int32()),
)

_MIN_NUM_ROWS_FOR_POLARS_JOIN = 10_000
"""Minimum number of rows on either side before converting the table to/from polars to use a polars join. Found that polars
becomes faster around 10_000 rows on my mac"""

T = TypeVar("T")


_MATERIALIZED_ARRAYS: dict[int, list[Any]] = {}
"""A cache containing the result of calling `.to_list()` on a PyArrow array.

This cache is indexed by the id(array), and a weakref finalizer is used to clear memory from this array
when the underlying pyarrow array is freed. This design, unlike passing the materialized values through
the ChalkRecordBatch, allows for new tables to reuse the existing materialization of a .to_pylist() call
if another ChalkRecordBatch had to materialize the same underlying array.
"""

_logger = get_logger(__name__)


def _clear_from_materialized(id: int):
    # FIXME: This if guard shouldn't be necessary. Added for CHA-2917
    if id in _MATERIALIZED_ARRAYS:
        del _MATERIALIZED_ARRAYS[id]
    else:
        _logger.warning(f"Could not find id {id} in the materialized arrays cache")


_sequential_index_column_set: WeakSetByIdentity[pa.Array] = WeakSetByIdentity()


def make_sequential_index_col(n: int) -> pa.Array:
    """
    Returns a `pa.Array` with exactly `n` rows, having values 0, 1, 2, 3, ...
    If possible, uses a slice of the _PREALLOCATED_INDEX_ARRAY to reduce memory overhead.

    The type of the returned array is pa.int64().
    """

    if n <= _PREALLOCATED_INDEX_ARRAY_LEN:
        array = _PREALLOCATED_INDEX_ARRAY.slice(0, n).cast(pa.int64())
    else:
        # The desired array is larger than the preallocated sequential list,
        # so we need to construct a new one.
        array = pc.subtract_checked(
            pc.cumulative_sum_checked(pa.nulls(n, pa.int64()).fill_null(pa.scalar(1, type=pa.int64()))),
            pa.scalar(1, pa.int64()),
        )

    _sequential_index_column_set.add(array)
    return array


def is_definitely_sequential_index_column(array: pa.Array) -> bool:
    """
    This function can be used for optimization - if `True` is returned, then the array
    is a sequential array of `0, 1, 2, 3, 4, ...` up to its length, allowing for rapid
    comparison.
    """
    return array in _sequential_index_column_set


@functools.lru_cache(None)
def _randomize_join_result_order():
    """Whether to randomize the results of ChalkRecordBatch.join. Useful during testing
    to ensure that we do not inadvertanetly assume that a ChalkRecordBatch.join does not change row order"""
    return env_var_bool("CHALK_TABLE_RANDOMIZE_JOIN_RESULT_ORDER")


def _randomize_row_order(tbl: ChalkRecordBatch) -> ChalkRecordBatch:
    if len(tbl) <= 1:
        return tbl
    offset = random.randint(0, len(tbl) - 1)
    len_scalar = pa.scalar(len(tbl), pa.int64())
    idxs = pc.add_checked(make_sequential_index_col(len(tbl)), pa.scalar(offset, pa.int64()))
    idxs = pc.if_else(pc.greater_equal(idxs, len_scalar), pc.subtract_checked(idxs, len_scalar), idxs)
    tbl = tbl.take(idxs)
    return tbl


class ChalkRecordBatch:
    """A collection of same-length PyArrow arrays, similar to a pa.RecordBatch, but with an easier to use API
    and better performance
    """

    # Private variables
    _data: Mapping[str, pa.Array]  # pyright: ignore[reportUninitializedInstanceVariable]
    _column_names: tuple[str, ...]  # pyright: ignore[reportUninitializedInstanceVariable]
    _len: int  # pyright: ignore[reportUninitializedInstanceVariable]
    _schema: Mapping[str, pa.DataType]  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(self):
        super().__init__()
        raise RuntimeError(
            "Do not construct a ChalkRecordBatch directly. Instead, please use one of the ChalkRecordBatch.from_XXX methods."
        )

    def __repr__(self):
        """
        Render contents as a well-formatted table in debugging contexts.
        """
        equivalent_df = pa_table_to_pl_df(self.to_table())
        return repr(equivalent_df)

    def __hash__(self):
        # This isn't perfect, but it's better than always returning the same thing
        return hash((self._column_names, self._len))

    def __eq__(self, other: object):
        if not isinstance(other, ChalkRecordBatch):
            return NotImplemented
        return self.equals(other, check_column_order=True)

    @classmethod
    def _internal_constructor(
        cls,
        data: Mapping[str, pa.Array],
        columns: tuple[str, ...],
        data_len: int,
        schema: Mapping[str, pa.DataType],
    ) -> Self:
        self = super().__new__(cls)
        self._data = data
        self._column_names = columns
        self._len = data_len
        self._schema = schema
        if __debug__:
            assert tuple(data.keys()) == columns, "The order of the keys in the data dict must match the column names"
            assert (
                tuple(schema.keys()) == columns
            ), "The order of the keys in the schema dict must match the column names"
            assert FrozenOrderedSet(columns) == FrozenOrderedSet(
                data.keys()
            ), "The columns list must contain all keys in ``data``"
            assert all(isinstance(x, pa.Array) for x in data.values()), "All values must be pa.Array"
            assert len(columns) == len(data), "The columns contains duplicate entries"
            assert schema == (
                actual_schema := {k: v.type for (k, v) in data.items()}
            ), f"Schema mismatch. Declared {schema}, but got {actual_schema}"
            if len(self._data) == 0:
                assert self._len == 0
            else:
                assert all(len(x) == self._len for x in self._data.values()), "All arrays must have the same length"
        return self

    __slots__ = ("_data", "_column_names", "_len", "_schema")

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, name: str) -> pa.Array:
        try:
            return self._data[name]
        except KeyError:
            raise ValueError(f"Column '{name}' not in the table") from None

    def append_column(self, field: str, column: pa.Array | pa.ChunkedArray):
        """Create a new table with this additional column at the end of the table

        Parameters
        ----------
        field
            The column name to append. A column with this name cannot currently be in the table
        column
            The PyArrow array containing the data

        Returns
        -------
        A new ChalkRecordBatch
        """
        return self.append_columns({field: column})

    def append_columns(
        self,
        columns: Mapping[str, pa.Array | pa.ChunkedArray | pa.Scalar],
    ):
        """Create a new table by appending the ``columns`` to the table.

        Column order is preserved, with new columns appearing at the end of the table.

        This API is more performant than creating a new ChalkRecordBatch from scratch or repeated ``append_column`` calls
        """
        if len(self.columns) > 0:
            expected_len = self._len
            expected_len_src = "the table"
        else:
            # If the table is 0x0, then use the length of the first column in columns for the length check
            # It's impossible to have an expression if the table is 0x0, since the expression must come from an existing column
            first_real_col = next(
                iter(x for x in columns.values() if isinstance(x, (pa.Array, pa.ChunkedArray))),
                None,
            )
            if first_real_col is None:
                raise ValueError("Cannot append only scalars to a 0x0 table")
            expected_len = len(first_real_col)
            expected_len_src = "the other appended columns"
        new_data = {**self._data}
        new_schema = {**self._schema}
        for col_name, column in columns.items():
            if not isinstance(col_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column names must be strings")
            if isinstance(column, pa.Scalar):
                column = pa.nulls(expected_len, column.type).fill_null(column)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            if not isinstance(column, (pa.Array, pa.Scalar)):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column values must be PyArrow arrays, ChunkedArrays, or an expression")
            if len(column) != expected_len:
                raise ValueError(
                    f"Column {col_name} has a length of {len(column)}, which differs from the length of {expected_len_src} ({expected_len})"
                )
            if col_name in self._data:
                raise ValueError(
                    f"Column '{col_name}' is already in the table. Please use ``replace_columns`` to update existing columns in the table."
                )
            new_data[col_name] = column
            new_schema[col_name] = column.type
        return self._internal_constructor(
            new_data,
            tuple(new_data.keys()),
            expected_len or self._len,
            new_schema,
        )

    def column(self, idx_or_name: str | int) -> pa.Array:
        """Get a column from the table

        Parameters
        ----------
        idx_or_name
            The name or integer index of the column
        """
        if isinstance(idx_or_name, int):
            try:
                idx_or_name = self._column_names[idx_or_name]
            except IndexError:
                raise ValueError(
                    (
                        f"Index {idx_or_name} is not in the table. The table has {len(self._data)} columns, "
                        f"so the index must be between 0 and {len(self._data) - 1}"
                    )
                ) from None
        if not isinstance(idx_or_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("idx_or_name must be the integer index or the column name string")
        try:
            return self._data[idx_or_name]
        except KeyError:
            raise ValueError(f"Column '{idx_or_name}' not found") from None

    @property
    def column_names(self) -> tuple[str, ...]:
        return self._column_names

    def contains_column_name(self, name: str) -> bool:
        return name in self._data

    @property
    def columns(self) -> tuple[pa.Array, ...]:
        # The order of data must be the same order of the columns
        return tuple(self._data.values())

    @property
    def data(self) -> Mapping[str, pa.Array]:
        """Get the columns as a mapping of {column_name: Array}"""
        return self._data

    def drop_columns(self, columns: str | Iterable[str]):
        if isinstance(columns, str):
            columns = (columns,)
        else:
            columns = tuple(columns)
        for column in columns:
            if not isinstance(column, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"Each column name must be a string. Got {column}")
            if column not in self._data:
                raise ValueError(f"Column '{columns}' not in the table")
        new_datas = {k: v for (k, v) in self._data.items() if k not in columns}
        new_columns = tuple(x for x in self._column_names if x not in columns)
        new_schema = {k: v for (k, v) in self._schema.items() if k not in columns}
        new_len = 0 if len(new_datas) == 0 else self._len
        return self._internal_constructor(new_datas, new_columns, new_len, new_schema)

    def equals(self, other: ChalkRecordBatch, check_column_order: bool = True) -> bool:
        if self is other:
            return True
        if check_column_order:
            if other.column_names != self.column_names:
                return False
        else:
            if FrozenOrderedSet(self.column_names) != FrozenOrderedSet(other.column_names):
                return False
        if not isinstance(other, ChalkRecordBatch):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("ChalkRecordBatch.equals can only be used with another ChalkRecordBatch")
        if self._len != other._len:
            return False
        if self._schema != other._schema:
            return False
        ans = pa.nulls(self._len, pa.bool_()).fill_null(True)
        for col_name in self.column_names:
            ans = pc.and_(ans, pc.equal(self._data[col_name], other._data[col_name]))
        ret = pc.all(ans, min_count=0).as_py()
        assert isinstance(ret, bool)
        return ret

    def filter(self, mask: pa.Array | pa.ChunkedArray | pa.Scalar):
        if isinstance(mask, pa.Scalar):
            raise ValueError("A scalar mask doesn't make sense")
        if isinstance(mask, pa.ChunkedArray):
            mask = mask.combine_chunks()
        if not isinstance(mask, pa.Array):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"The mask must be an array, a chunked array, or a scalar; got {mask}")
        if mask.null_count > 0:
            raise ValueError("The mask cannot contain null values")
        if len(mask) != self._len:
            raise ValueError(
                f"The length of the mask ({len(mask)}) must be the same as the length of the table ({self._len})"
            )
        new_datas = {k: v.filter(mask) for (k, v) in self._data.items()}
        new_len = 0 if len(new_datas) == 0 else len(next(iter(new_datas.values())))
        return self._internal_constructor(new_datas, self.column_names, new_len, self._schema)

    @classmethod
    def from_arrays(
        cls,
        arrays: Iterable[pa.Array | pa.ChunkedArray],
        names: Iterable[str],
    ) -> Self:
        data: dict[str, pa.Array] = {}
        data_len = None
        names = tuple(names)
        if len(FrozenOrderedSet(names)) != len(names):
            raise ValueError(f"Duplicate name are not allowed: {names}")
        for name, arr in zip_longest(names, arrays, fillvalue=None):
            if name is None or arr is None:
                raise ValueError("The length of the arrays must match the length of the names")
            if not isinstance(name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("The column name must be a string")
            if isinstance(arr, pa.ChunkedArray):
                arr = arr.combine_chunks()
            if not isinstance(arr, pa.Array):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Each array must be an array or a chunked array")
            if pa.types.is_date32(arr.type):
                arr = arr.cast(pa.date64())
            if data_len is None:
                data_len = len(arr)
            elif len(arr) != data_len:
                raise ValueError(
                    f"Cannot construct a ChalkRecordBatch with different array lengths. {data_len=}, {len(arr)=}. Failed on column {name=}"
                )
            data[name] = arr
        if data_len is None:
            data_len = 0
        schema = {k: v.type for (k, v) in data.items()}
        return cls._internal_constructor(data, names, data_len, schema)

    @classmethod
    def from_pydict(
        cls,
        data: Mapping[str, Iterable[object] | pa.Array | pa.ChunkedArray],
        schema: Mapping[str, pa.DataType] | None = None,
    ) -> ChalkRecordBatch:
        new_data: dict[str, pa.Array] = {}
        if schema is None:
            new_schema: dict[str, pa.DataType] = {}
            data_len = None
            for k, v in data.items():
                if not isinstance(k, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                    raise TypeError(f"Column names must be strings; got {k}")
                if isinstance(v, pa.ChunkedArray):
                    v = v.combine_chunks()  # pyright: ignore[reportAttributeAccessIssue]
                if not isinstance(v, pa.Array):
                    raise TypeError("If no schema is provided, columns must be PyArrow arrays or chunked arrays")
                if data_len is None:
                    data_len = len(v)  # pyright: ignore[reportArgumentType]
                elif len(v) != data_len:  # pyright: ignore[reportArgumentType]
                    raise ValueError("Cannot construct a ChalkRecordBatch with different array lengths")
                new_data[k] = v
                new_schema[k] = v.type  # pyright: ignore[reportAttributeAccessIssue]
            if data_len is None:
                data_len = 0
            return cls._internal_constructor(new_data, tuple(data.keys()), data_len, new_schema)

        for k, v in schema.items():
            if not isinstance(k, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"Schema keys must be strings. Got {k}")
            if not isinstance(v, pa.DataType):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"Schema values must be pa.DataTypes. Got {v}")
        if FrozenOrderedSet(data.keys()) != FrozenOrderedSet(schema.keys()):
            raise ValueError("The `data` and `schema` must have the same keys")
        new_data: dict[str, pa.Array] = {}
        data_len = None
        for k in schema:
            v = data[k]
            if isinstance(v, (pa.Array, pa.ChunkedArray)):
                raise TypeError("When providing a schema, values cannot be existing pyarrow arrays")
            v = tuple(v)
            if data_len is None:
                data_len = len(v)
            elif len(v) != data_len:
                raise ValueError("Cannot construct a ChalkRecordBatch with different array lengths")

            v = pa.array(v, schema[k])
            if isinstance(v, pa.ChunkedArray):
                v = v.combine_chunks()
            new_data[k] = v
        if data_len is None:
            data_len = 0
        columns = tuple(schema.keys())  # Using the (implicit) ordering from the schema
        return cls._internal_constructor(new_data, columns, data_len, schema)

    @classmethod
    def from_table(cls, table: pa.Table | pa.RecordBatch) -> ChalkRecordBatch:
        if isinstance(table, cls):
            return table
        if not isinstance(table, (pa.Table, pa.RecordBatch)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"The table must be an existing PyArrow table or RecordBatch; got {table}")
        if isinstance(table, pa.Table):
            column_names = tuple(table.column_names)
        else:
            column_names = tuple(table.schema.names)
        columns = tuple(table.columns)
        return cls._internal_constructor(
            {k: v if isinstance(v, pa.Array) else v.combine_chunks() for (k, v) in zip(column_names, columns)},
            column_names,
            0 if len(column_names) == 0 else len(table),
            {k: v.type for (k, v) in zip(column_names, columns)},
        )

    def get_total_buffer_size(self):
        return sum(x.get_total_buffer_size() for x in self._data.values())

    def itercolumns(self) -> Generator[pa.Array, None, None]:
        yield from self._data.values()

    @property
    def nbytes(self):
        return sum(x.nbytes for x in self._data.values())

    @property
    def num_columns(self):
        return len(self._data)

    @property
    def num_rows(self):
        return self._len

    def remove_column(self, name_or_idx: int | str):
        if isinstance(name_or_idx, int):
            if name_or_idx < 0:
                raise ValueError("Index must be >= 0")
            if name_or_idx >= len(self._data):
                raise ValueError(
                    f"Invalid index -- table has {len(self._data)} columns. Cannot drop index {name_or_idx}."
                )
            name_or_idx = self._column_names[name_or_idx]
        else:
            if not isinstance(name_or_idx, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"Argument must be a string or int; got {type(name_or_idx)}")
            if name_or_idx not in self._data:
                raise ValueError(f"Column '{name_or_idx}' is not a valid column name")
        return self.drop_columns((name_or_idx,))

    def rename_columns(self, names: Iterable[str] | Mapping[str, str]):
        if isinstance(names, str):
            raise TypeError("names must be a mapping or an iterable of strings, not a singular string")

        if isinstance(names, collections.abc.Mapping):
            # This "cast" tells pyright to remember the generic arguments,
            # so that we can still perform value lookups.
            names_map: Mapping[str, str] = names
            for name in names:
                if name not in self._data:
                    raise ValueError(f"The table does not contain a column called '{name}'")
            names = tuple(names_map.get(k, k) for k in self._column_names)
        else:
            names = tuple(names)
            if len(names) != len(self._data):
                raise ValueError(
                    f"The new names (of length {len(names)}) do not match the number of columns in the table ({len(self._data)})"
                )
        # Since the data and schema are ordered dicts, we can simply iterate over them
        new_data = dict(zip(names, self._data.values()))
        new_schema = dict(zip(names, self._schema.values()))
        if len(new_data) != len(names):
            raise ValueError(f"New names contain duplicates: {names}")
        return self._internal_constructor(new_data, tuple(names), self._len, new_schema)

    @property
    def schema_dict(self) -> Mapping[str, pa.DataType]:
        return self._schema

    def set_column(self, i: int, field: str, column: pa.Array | pa.ChunkedArray):
        """Set the column at position ``i`` to have name ``field`` and value ``column``

        Creates a new table -- doesn't modify the table in-place
        """
        if not isinstance(i, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The index must be an int")
        if not isinstance(field, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The field must be a string")
        if not isinstance(column, (pa.Array, pa.ChunkedArray)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The replacement column must be a pyarrow array")
        if isinstance(column, pa.ChunkedArray):
            column = column.combine_chunks()
        if i < 0:
            raise ValueError("Negative indexes are not supported")
        if i >= len(self._data):
            raise ValueError(f"Index {i} is greater than the largest column index {len(self._column_names) - 1}")
        if len(column) != self._len:
            raise ValueError(
                f"The length of the new column ({len(column)}) differs from the existing table length ({self._len})"
            )
        new_data = {
            (field if i == j else c): (column if i == j else self._data[self._column_names[j]])
            for (j, c) in enumerate(self.column_names)
        }
        new_columns = tuple(field if i == j else c for (j, c) in enumerate(self._column_names))
        if len(FrozenOrderedSet(new_columns)) != len(new_columns):
            raise ValueError(f"Columns would contain a duplicate entry after this set operation: {new_columns}")
        new_schema = {
            (field if i == j else c): (column.type if i == j else self._schema[self._column_names[j]])
            for (j, c) in enumerate(self.column_names)
        }
        return self._internal_constructor(new_data, new_columns, self._len, new_schema)

    @property
    def shape(self) -> tuple[int, int]:
        return (self._len, len(self._data))

    def slice(self, offset: int, length: int | None = None) -> ChalkRecordBatch:
        """Slice the dataframe starting at ``offset`` for up to ``length`` rows

        If ``length`` is None, then all remaining rows (starting at the offset) are returned
        If ``length`` is greater than the number of remaining rows, it has the same effect as being called with ``None``
        It is not permitted for ``length`` to be negative.
        """
        if not isinstance(offset, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The offset must be an int")
        if offset < 0:
            raise ValueError("Negative offsets are not supported")
        if offset > self._len:
            raise ValueError(f"Offset {offset} is greater than the length of the table {self._len}")
        if length is None:
            length = self._len - offset
        if not isinstance(length, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The length must be an integer or None")
        if length < 0:
            raise ValueError("Negative lengths are not supported")
        if length > self._len - offset:
            length = self._len - offset
        if offset == 0 and length >= self._len:
            # Not actually slicing!
            return self
        return self._internal_constructor(
            {k: v.slice(offset, length) for (k, v) in self._data.items()},
            self._column_names,
            length,
            self._schema,
        )

    def take(self, indices: pa.Array | pa.ChunkedArray):
        """Create a new table with the specified indices"""
        if isinstance(indices, pa.ChunkedArray):
            indices = indices.combine_chunks()
        if not isinstance(indices, pa.Array):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The indices must be an Array or a ChunkedArray")
        if indices.null_count > 0:
            raise ValueError("The indices for ``take`` cannot have any null values")
        new_data = {k: v.take(indices) for (k, v) in self._data.items()}
        return self._internal_constructor(new_data, self._column_names, len(indices), self._schema)

    def to_table(self) -> pa.Table:
        return pa.Table.from_pydict(self._data)

    def to_record_batch(self) -> pa.RecordBatch:
        return pa.RecordBatch.from_pydict(self._data)

    def to_pydict(self) -> Mapping[str, list[object]]:
        ans: dict[str, list[object]] = {}
        for k, v in self._data.items():
            materialized = _MATERIALIZED_ARRAYS.get(id(v))
            if materialized is None:
                try:
                    materialized = to_pylist(v)
                except Exception as e:
                    raise ValueError(f"while processing {k}\n{e}")
                _MATERIALIZED_ARRAYS[id(v)] = materialized
                weakref.finalize(v, _clear_from_materialized, id(v))
            ans[k] = materialized
        return ans

    def to_string(self, show_metadata: bool = False, preview_cols: int = 0) -> str:
        ans: list[str] = [f"ChalkRecordBatch (length={self._len})"]
        if show_metadata:
            for k, v in self._schema.items():
                ans.append(f"{k}: {str(v)}")
        ans.append("---")
        if preview_cols:
            for k, v in self._data.items():
                col_formatted = v.to_string(window=(preview_cols - 1) // 2 + 1, skip_new_lines=True)
                ans.append(f"{k}: {col_formatted}")
        return "\n".join(ans)

    def hstack(self, other: ChalkRecordBatch, right_suffix: str | None = None):
        """Create a new table by horizontally concatenating another table onto this one. Both tables must have the same length, unless
        if one of the tables is zero-by-zero, then the other table will be returned.

        Parameters
        ----------
        other
            The other table to combine
        right_suffix
            If there are any overlapping columns, a suffix to append to the names of the columns in the right table
            If not specified (or there are overlapping columns after applying this suffix), then a ValueError will be raised
        """
        if not isinstance(other, ChalkRecordBatch):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The other table must be a ChalkRecordBatch")
        if len(other.column_names) == 0:
            return self
        if len(self.column_names) == 0:
            return other
        if other._len != self._len:
            raise ValueError(f"The tables have different lengths. Left: {self._len}, Right: {other._len}")

        new_data = {**self._data}  # shallow copy
        new_schema = {**self._schema}  # shallow copy
        for k, v in other._data.items():
            new_col_name = k
            if k in new_data and right_suffix is not None:
                new_col_name = k + right_suffix
                if new_col_name in other._data:
                    raise ValueError(
                        f"Column '{k}' was renamed to '{new_col_name}', which already exists in the right table. Please try changing the ``right_suffix``"
                    )
            if new_col_name in new_data:
                raise ValueError(
                    f"Column '{k}' appears in both the original and hstacked table. Please try specifying the ``right_suffix``"
                )
            new_data[new_col_name] = v
            new_schema[new_col_name] = other._schema[k]
        new_columns = tuple(new_data.keys())
        return self._internal_constructor(new_data, new_columns, self._len, new_schema)

    def union_all(self, others: Sequence[ChalkRecordBatch]):
        if not all([x.schema_dict == self.schema_dict for x in others]):
            raise ValueError("All tables must have the same schema to union all")

        data: dict[str, pa.Array] = {}
        for k, v in self._data.items():
            other_v = [x._data[k] for x in others]
            data[k] = pa.concat_arrays([v] + other_v)

        return self._internal_constructor(
            data,
            self._column_names,
            len(self) + sum(len(x) for x in others),
            self._schema,
        )

    def replace_columns(
        self,
        columns: Mapping[str, pa.Array | pa.ChunkedArray | pa.Scalar],
    ):
        """Create a new table by replacing the ``columns``.

        Column order is preserved.

        This API is more performant than creating a new ChalkRecordBatch from scratch or repeated ``set_column` calls.
        """
        if len(columns) == 0:
            return self
        new_data = {**self._data}
        new_schema = {**self._schema}
        for col_name, column in columns.items():
            if not isinstance(col_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column names must be strings")
            if isinstance(column, pa.Scalar):
                column = pa.nulls(self._len, column.type).fill_null(column)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            if not isinstance(column, pa.Array):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column values must be PyArrow arrays, ChunkedArrays, Scalars, or Expressions")
            if len(column) != self._len:
                raise ValueError(
                    f"Column '{col_name}' has a length of {len(column)}, which differs from the length of the table ({self._len})"
                )
            if col_name not in new_data:
                raise ValueError(
                    f"Column '{col_name}' is not already in the table. Please use ``append_columns`` to add new columns to the table"
                )
            new_data[col_name] = column
            new_schema[col_name] = column.type
        return self._internal_constructor(new_data, self._column_names, self._len, new_schema)

    def project(
        self,
        columns: Mapping[str, pa.Array | pa.ChunkedArray | pa.Scalar],
    ):
        if len(columns) == 0:
            return ChalkRecordBatch.from_pydict({}, {})
        new_data: dict[str, pa.Array] = {}
        new_schema: dict[str, pa.DataType] = {}
        if len(self.columns) > 0:
            expected_len = self._len
            expected_len_src = "the table"
        else:
            # If the table is 0x0, then use the length of the first column in columns for the length check
            # It's impossible to have an expression if the table is 0x0, since the expression must come from an existing column
            first_real_col = next(
                iter(x for x in columns.values() if isinstance(x, (pa.Array, pa.ChunkedArray))),
                None,
            )
            if first_real_col is None:
                raise ValueError("Cannot append only scalars to a 0x0 table")
            expected_len = len(first_real_col)
            expected_len_src = "the other appended columns"
        for col_name, column in columns.items():
            if not isinstance(col_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column names must be strings")
            if isinstance(column, pa.Scalar):
                column = pa.nulls(expected_len, column.type).fill_null(column)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            if not isinstance(column, pa.Array):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column values must be PyArrow arrays or ChunkedArrays")
            if len(column) != expected_len:
                raise ValueError(
                    f"Column {col_name} has a length of {len(column)}, which differs from the length of {expected_len_src} ({expected_len})"
                )
            new_data[col_name] = column
            new_schema[col_name] = column.type
        return self._internal_constructor(new_data, tuple(new_data.keys()), expected_len, new_schema)

    def with_columns(
        self,
        columns: Mapping[str, pa.Array | pa.ChunkedArray | pa.Scalar],
    ):
        """Create a new table by appending (or replacing, if the columns currently exist), the ``columns`` to the table.
        It is similar to ``append_columns`` and ``replace_columns``, but does not validate whether or not the column name already appears in the table

        Column order is preserved, with new columns appearing at the end of the table.

        This API is more performant than creating a new ChalkRecordBatch from scratch or repeated ``append_column`` calls
        """
        if len(columns) == 0:
            return self
        new_data = {**self._data}
        new_schema = {**self._schema}
        if len(self.columns) > 0:
            expected_len = self._len
            expected_len_src = "the table"
        else:
            # If the table is 0x0, then use the length of the first column in columns for the length check
            # It's impossible to have an expression if the table is 0x0, since the expression must come from an existing column
            first_real_col = next(
                iter(x for x in columns.values() if isinstance(x, (pa.Array, pa.ChunkedArray))),
                None,
            )
            if first_real_col is None:
                raise ValueError("Cannot append only scalars to a 0x0 table")
            expected_len = len(first_real_col)
            expected_len_src = "the other appended columns"
        for col_name, column in columns.items():
            if not isinstance(col_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column names must be strings")
            if isinstance(column, pa.Scalar):
                column = pa.nulls(expected_len, column.type).fill_null(column)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            if not isinstance(column, pa.Array):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError("Column values must be PyArrow arrays or ChunkedArrays")
            if len(column) != expected_len:
                raise ValueError(
                    f"Column {col_name} has a length of {len(column)}, which differs from the length of {expected_len_src} ({expected_len})"
                )
            new_data[col_name] = column
            new_schema[col_name] = column.type
        return self._internal_constructor(new_data, tuple(new_data.keys()), expected_len, new_schema)

    def iter_pyrows(self, chunk_size: int = 1000) -> Iterator[dict[str, Any]]:
        """Iterate each row in the table as a python dictionary

        Parameters
        ----------
        chunk_size
            The number of rows to collect into python objects in one chunk. This parameter has no effect on correctness
        """
        if chunk_size < 1:
            raise ValueError("The chunk size must be at least 1")
        start = 0
        while start < self._len:
            slc = self.slice(start, chunk_size)
            start += len(slc)
            slc_dict = slc.to_pydict()
            for i in range(len(slc)):
                yield {k: v[i] for (k, v) in slc_dict.items()}

    def join(
        self,
        right_table: ChalkRecordBatch,
        keys: str | Iterable[str],
        join_type: Literal[
            "inner",
            "left outer",
            "merge",
        ],
        right_keys: str | Iterable[str] | None = None,
        right_suffix: str | None = None,
        use_threads: bool = True,
        unmatched_metadata: int | None = None,
        use_polars: bool | None = None,
    ) -> ChalkRecordBatch:
        """Create a new table by joining ``right_table`` against the current table.

        Unlike a PyArrow ``Table.join``, ``ChalkRecordBatch.join`` supports all data types, including list and struct columns
        In addition, our "inner" join isn't broken (see https://github.com/apache/arrow/issues/37729)
        NOTE: The returned column order is not guaranteed to be in any particular order

        Parameters
        ----------
        right_table
            The table to join against
        keys
            The columns in the left table to use as join keys
        join_type
            The type of join to perform
        right_keys
            The columns in the right table to use as the join keys. If not specified, the same keys as the keys will be used
        right_suffix
            A suffix to append to any non-join columns in the right table that are also in the left table. If not specified,
            or duplicate columns still exist after applying this suffix, a ValueError will be raised
        use_threads
            Whether to use threads for the join
        use_polars
            Whether to use polars for the join. If None, then heuristics will be used to determine if polars is faster
        unmatched_metadata
            In outer joins, what values to fill into the metadata for unmatched entries
        """
        # Pyarrow does not support joining on tables containing structs or lists in the non-join columns
        # To get around this limitation, we'll construct a pyarrow table for the left join keys and an index column.
        # We'll join this against a table containing the right join keys and an index column
        # Then, we'll hstack on the other non-join columns that match the indices from the left and right
        if not isinstance(right_table, ChalkRecordBatch):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"The right_table must be a ChalkRecordBatch; got {right_table}")
        if isinstance(keys, str):
            # If only one `str` key is given, convert it into a singleton list.
            # Remember that `str` is also an `Iterable[str]` (over characters), which could otherwise lead to confusion.
            keys = (keys,)
        else:
            keys = tuple(keys)
        if len(FrozenOrderedSet(keys)) != len(keys):
            raise ValueError(f"The left keys contained duplicate keys: {keys}")

        if right_keys is None:
            # If no `right_keys` are given, use `keys` as a fallback.
            right_keys = keys
        elif isinstance(right_keys, str):
            # If only one `str` key is given, convert it into a singleton list.
            # Remember that `str` is also an `Iterable[str]` (over characters), which could otherwise lead to confusion.
            right_keys = (right_keys,)
        else:
            right_keys = tuple(right_keys)
        if len(FrozenOrderedSet(right_keys)) != len(right_keys):
            raise ValueError(f"The right keys contained duplicate keys: {right_keys}")
        right_keys_set = set(right_keys)  # Build a set to make set-membership checks faster.

        # In order to perform a join, after we compute the key tuples, they must have the
        # same cardinality. Otherwise, it would be impossible for the left/right values to match.
        if len(keys) != len(right_keys):
            raise ValueError(f"The left keys ({keys}) must have the same length of the right keys ({right_keys})")

        # Ensure that all of the left keys exist in the left (self) table.
        missing_left_keys = tuple(x for x in keys if x not in self._data)
        if len(missing_left_keys) > 0:
            raise ValueError(f"The following join keys are not in the lhs table: {missing_left_keys}")

        # Ensure that all of the right keys exist in the right table.
        missing_right_keys = tuple(x for x in right_keys if x not in right_table._data)
        if len(missing_right_keys) > 0:
            raise ValueError(f"The following join keys are not in the lhs table: {missing_right_keys}")
        if join_type == "merge":
            if len(keys) != 1:
                raise ValueError("Merge join requires exactly one join key")
            if __debug__:
                assert pc.all(
                    pc.equal(
                        self.column(keys[0]),
                        right_table.column(right_keys[0]),
                    ),
                    min_count=0,
                ).as_py(), "Both sides must have an identical join column when merge joining"
            if len(self) != len(right_table):
                # This check is much cheaper to perform, even when PYTHONDEBUG=0
                raise ValueError(
                    f"Merge join requires identical columns when joining. The left hand side had {len(self)} elements, while the right hand side had {len(right_table)} elements"
                )

            # Merge join is a special case of left outer. Should implement the hstack codepath
            join_type = "left outer"

        if (
            len(keys) == 1
            and is_definitely_sequential_index_column(self._data[keys[0]])
            and is_definitely_sequential_index_column(right_table._data[right_keys[0]])
            and (
                len(self) == len(right_table)
                or join_type == "inner"
                or (len(self) < len(right_table) and join_type == "left outer")
                or (
                    len(self) > len(right_table)
                    and join_type == "right outer"  # pyright: ignore[reportUnnecessaryComparison]
                )  # pyright: ignore[reportUnnecessaryComparison]
            )
        ):
            # This is a fast path for joining two ChalkTables by a sequential column (0, 1, 2, 3, ...).
            #
            # If we know that both join columns are the sequential integers, then a join is the same as
            # just sticking all of the columns into one table. If the tables are the same length,
            # regardless of the specific type of merge, since there are no duplicates or missing values.
            # This works if the join type is such that there would never be nulls added (i.e. doing a left join
            # when there are more rows in the right)
            #
            # This should be a lot faster, since we don't have to even _look_ at the data!
            left_table = self
            if len(left_table) > len(right_table):
                left_table = left_table.slice(0, len(right_table))
            if len(left_table) < len(right_table):
                right_table = right_table.slice(0, len(left_table))

            add_columns_from_right: dict[str, pa.Array] = {}
            for right_column_name in right_table.column_names:
                if right_column_name == right_keys[0]:
                    # The join column in the right table gets skipped, since definitionally
                    # its values are the same as what came from the left table.
                    continue

                # By default, the right column name is used unchanged in the output.
                # Only if there's a conflict will we add a suffix.
                new_column_name = right_column_name

                if right_column_name in self.data:
                    if right_suffix is None:
                        raise ValueError(
                            f"Column {right_column_name} appears in both sides of the table. Please set the `right_suffix` to disambiguate."
                        )
                    new_column_name += right_suffix

                if new_column_name in self.data or new_column_name in add_columns_from_right:
                    raise ValueError(
                        f"Column '{right_column_name}' was renamed to '{new_column_name}', which already exists in the right table. Please try changing the ``right_suffix``"
                    )

                add_columns_from_right[new_column_name] = right_table._data[right_column_name]

            # Append all of the columns that we just added.
            res = left_table.append_columns(add_columns_from_right)
            if _randomize_join_result_order():
                res = _randomize_row_order(res)

            return res

        if use_polars is None:
            use_polars = len(self) > _MIN_NUM_ROWS_FOR_POLARS_JOIN or len(right_table) > _MIN_NUM_ROWS_FOR_POLARS_JOIN

        if (
            use_polars
            # Not allowing polars on list/struct types because I'm concerned about how it would handle nulls / empty lists and structs and recursion
            and not any(
                pa.types.is_struct(x)
                or pa.types.is_list(x)
                or pa.types.is_large_list(x)
                or pa.types.is_fixed_size_list(x)
                for x in self.schema_dict.values()
            )
            and not any(
                pa.types.is_struct(x)
                or pa.types.is_list(x)
                or pa.types.is_large_list(x)
                or pa.types.is_fixed_size_list(x)
                for x in right_table.schema_dict.values()
            )
        ):
            expected_schema = {**self.schema_dict}  # shallow copy
            for right_column_name, right_dtype in right_table.schema_dict.items():
                if right_column_name in right_keys_set:
                    # The join column in the right table gets skipped, since definitionally
                    # its values are the same as what came from the left table.
                    continue

                # By default, the right column name is used unchanged in the output.
                # Only if there's a conflict will we add a suffix.
                new_column_name = right_column_name

                if right_column_name in self.data:
                    if right_suffix is None:
                        raise ValueError(
                            f"Column {right_column_name} appears in both sides of the table. Please set the `right_suffix` to disambiguate."
                        )
                    new_column_name += right_suffix

                if new_column_name in expected_schema:
                    raise ValueError(
                        f"Column '{right_column_name}' was renamed to '{new_column_name}', which already exists in the right table. Please try changing the ``right_suffix``"
                    )
                expected_schema[new_column_name] = right_dtype

            left_df = pa_table_to_pl_df(self.to_table())
            right_df = pa_table_to_pl_df(right_table.to_table())
            if join_type == "inner":
                how = "inner"
            elif join_type == "left outer":
                how = "left"
            else:
                assert_never(join_type)
            df = left_df.join(
                right_df,
                how=how,
                left_on=keys,
                right_on=right_keys,
                suffix=right_suffix or "",
            )
            joined_table = df.to_arrow()
            res = ChalkRecordBatch.from_table(pa_cast(joined_table, pa.schema(expected_schema)))
            if _randomize_join_result_order():
                res = _randomize_row_order(res)
            return res

        # We need an "index" column to remember where each row in the join table came from.
        # If possible, we re-use a preallocated index array (0, 1, 2, 3, 4, ...), otherwise
        # we make a new one.
        left_idx_col = make_sequential_index_col(self._len)

        # The left_join_table has columns:
        # - one for each column in (left) "keys"
        # - plus the left_idx_col to remember where each row came from
        # The columns retain their original names, with `_LEFT_INDEX_COL` being a special name for the index col.
        left_join_table: pa.Table = pa.Table.from_arrays(
            [*(self._data[k] for k in keys), left_idx_col], [*keys, _LEFT_INDEX_COL]
        )
        del left_idx_col  # free memory; it will be kept alive in `left_join_table` only.

        # We need an "index" column to remember where each row in the join table came from.
        # If possible, we re-use a preallocated index array (0, 1, 2, 3, 4, ...), otherwise
        # we make a new one.
        right_idx_col = make_sequential_index_col(right_table._len)

        # The right_join_table has columns:
        # - one for each column in "right_keys"
        # - plus the right_idx_col to remember where each row came from
        # The columns retain their original names, with `_RIGHT_INDEX_COL` being a special name for the index col.
        right_join_table = pa.Table.from_arrays(
            [*(right_table._data[k] for k in right_keys), right_idx_col],
            [*right_keys, _RIGHT_INDEX_COL],
        )
        del right_idx_col  # free memory; it will be kept alive in `right_join_table` only.

        # Ask pyarrow to join the tables for us. We can recover the rest of the original rows later by using the special
        # `_LEFT_INDEX_COL` and `_RIGHT_INDEX_COL` columns.
        #
        # The resulting columns in `joined_table` are ONLY the (left) `keys` (not `right_keys`) and the two special
        # index columns `_LEFT_INDEX_COL` and `_RIGHT_INDEX_COL`.
        # NOTE: pyarrow inner joins are broken (see https://github.com/apache/arrow/issues/37729)
        # So, we will always do a "left outer" join, but if the join type is "inner", we will drop rows where the _RIGHT_INDEX_COL is null
        joined_table = left_join_table.join(
            right_table=right_join_table,
            keys=keys,
            right_keys=right_keys,
            join_type="left outer" if join_type == "inner" else join_type,
            # Since there aren't any other columns, there is no chance of a conflict.
            # Therefore, we don't need to set `right_suffix`.
            # The only other columns are `_LEFT_INDEX_COL` and `_RIGHT_INDEX_COL`, which
            # we don't want to be suffixes.
            use_threads=use_threads,
        )
        if join_type == "inner":
            joined_table = joined_table.filter(joined_table.column(_RIGHT_INDEX_COL).is_valid())
        del left_join_table, right_join_table  # free memory

        data_len = len(joined_table)

        # Convert the table back into a mapping from column-name to array.
        # Note: this only includes the (left) `keys` columns, since the `pyarrow.Table.join` operator
        # only includes the left side's key columns (which is where it gets the names).
        data: dict[str, pa.Array] = {
            col_name: col.combine_chunks() for (col_name, col) in zip(joined_table.column_names, joined_table.columns)
        }
        del joined_table  # free memory

        # We now assume that the `_LEFT_INDEX_COL` and `_RIGHT_INDEX_COL` columns have been scrambled
        # (order-wise) by the join, but they're now matched up exactly how we want to select from the
        # original tables. Remove them from `data` since we don't want them in the final output.
        left_indices = data.pop(_LEFT_INDEX_COL)
        right_indices = data.pop(_RIGHT_INDEX_COL)

        # The `schema` here will be for the output table, which includes the `key` columns, as well as
        # all of the original columns in the left and right tables, excluding anything from `right_keys`
        # in the right table.
        #
        # If there's a conflict between a column name in the left table and a column name in the right
        # table, `right_suffix` will be preprended to the right column. If it's `None` or this still
        # somehow results in a conflict, then we raise an exception.
        #
        # Initially, we just fill `schema` with the join key columns. All others are added subsequently.
        schema = {k: self._schema[k] for k in data}

        # Add in all of the columns in self (left table) that weren't used for the join.
        for col_name, col in self._data.items():
            if col_name in data:
                # It is a join key, so it is already present in the joined table.
                assert col_name in keys
            else:
                # Grab the corresponding rows from this column in the left table (self).
                taken = col.take(left_indices)
                if isinstance(taken, pa.ChunkedArray):
                    # It is unclear from the types whether this code is reachable or not.
                    taken = taken.combine_chunks()
                # Store this column in the output.
                data[col_name] = taken
                # Remember that this column is included in the output.
                schema[col_name] = self._schema[col_name]

        # Add in all of the columns in `right_table` that weren't already used for the join.
        # Note that `right_keys` are excluded below, so there is no chance for them to conflict.
        for col_name, col in right_table._data.items():
            if col_name in right_keys_set:
                # It is a join key, so it is already in `data`.
                continue

            # The resulting name will either be `col_name` if it does not conflict, or
            # `f"{right_suffix}{col_name}"` if it does. If that still conflicts or
            # `right_suffix` is `None`, then an error gets raised.
            # Thus we ensure that the resulting table has no duplicate columns and the
            # right table doesn't trample over any values from the left.
            final_col_name = col_name
            if col_name in data and right_suffix is not None:
                final_col_name = col_name + right_suffix
                if final_col_name in right_table._data:
                    raise ValueError(
                        f"Column '{col_name}' was renamed to '{final_col_name}', which already exists in the right table. Please try changing the ``right_suffix``"
                    )
            if final_col_name in data:
                raise ValueError(
                    f"Column {final_col_name} appears in both sides of the table. Please set the `right_suffix` to disambiguate."
                )
            # Grab the corresponding rows from this column in the left table (self).
            taken = col.take(right_indices)
            if isinstance(taken, pa.ChunkedArray):
                # It is unclear from the types whether this code is reachable or not.
                taken = taken.combine_chunks()
            # Store this column in the output.
            data[final_col_name] = taken
            # Remember that this column is included in the output.
            schema[final_col_name] = right_table.schema_dict[col_name]
        # Set the unmatched metadata
        if unmatched_metadata is not None:
            unmatched_metadata_scalar = pa.scalar(unmatched_metadata, pa.uint64())
            for col_name, col in tuple(data.items()):
                if col_name.startswith("__chalk__.__metadata__."):
                    col = col.fill_null(unmatched_metadata_scalar)
                    data[col_name] = col
        columns = tuple(data)
        if __debug__:
            assert len(data) == (
                expected_num_cols := len(self._data) + len(right_table._data) - len(keys)
            ), f"Resulting column mismatch. Expected {expected_num_cols} columns; got {len(data)}"
            for k in self._data:
                assert k in data, f"Missing column {k}"
            for k in right_table._data:
                assert (
                    k in data
                    or (k in right_keys and keys[right_keys.index(k)] in data)
                    or (right_suffix is not None and k + right_suffix in data)
                ), f"Missing column '{k}'"

        res = self._internal_constructor(data, columns, data_len, schema)
        if _randomize_join_result_order():
            res = _randomize_row_order(res)
        return res

    def __str__(self):
        return self.to_string(show_metadata=True, preview_cols=10)

    def pprint_string(self) -> str:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        return str(pl.from_arrow(self.to_table()))

    def with_row_count(self, name: str):
        """Append a row count column to the table. This column will be called ``name``, and the first row will have the ``start`` value"""
        return self.append_column(name, make_sequential_index_col(len(self)))

    def with_unique_id(self, name: str) -> Self:
        # When creating a new unique id index, we will randomize the start of it
        # This makes debugging easier to find when we should have used with_row_count()
        # Instead of with_unique_id()
        if len(self) == 0:
            # There's a bug with polars where roundtripping with a slice of length zero crashes
            return self.append_column(name, pa.nulls(0, pa.int64()))
        offset = random.randint(0, _PREALLOCATED_INDEX_ARRAY_LEN // 2)
        return self.append_column(name, make_sequential_index_col(len(self) + offset).slice(offset, len(self)))

    def sort_by(self, by: Iterable[tuple[str, Literal["ascending", "descending"]]]):
        by = list(by)
        if len(by) == 0:
            raise ValueError("Must have at least one column to sort by")
        return ChalkRecordBatch.from_table(self.to_table().sort_by(by))

    def distinct(
        self,
        on: Sequence[str] | None,
        order_by: Iterable[tuple[str, Literal["ascending", "descending"]]],
    ):
        order_by = list(order_by)
        table = self
        if len(order_by) > 0:
            table = self.sort_by(order_by)
        df = pa_table_to_pl_df(table.to_table())
        df = df.unique(on, keep="first")
        return ChalkRecordBatch.from_table(
            pa_cast(
                df.to_arrow(),
                pa.schema(self.schema_dict),
            )
        )

    def aggregate(self, by: Sequence[str], metrics: Sequence[tuple[str, str]]):
        return ChalkRecordBatch.from_table(self.to_table().group_by(list(by)).aggregate(list(metrics)))

    def select(self, cols: str | Iterable[str]) -> Self:
        if isinstance(cols, str):
            cols = (cols,)
        else:
            cols = tuple(cols)
        new_data: dict[str, pa.Array] = {}
        new_schema: dict[str, pa.DataType] = {}
        for c in cols:
            col = self._data.get(c)
            if col is None:
                raise ValueError(f"Column '{c}' does not exist")
            if c in new_data:
                raise ValueError(f"Column '{c}' cannot appear twice")
            new_data[c] = col
            new_schema[c] = self._schema[c]
        return self._internal_constructor(
            new_data,
            tuple(new_data.keys()),
            0 if len(new_data) == 0 else len(self),
            new_schema,
        )


def assert_table_equal(
    left: ChalkRecordBatch,
    right: ChalkRecordBatch,
    *,
    check_row_order: bool = True,
    check_column_order: bool = True,
):
    try:
        import polars.testing
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    polars.testing.assert_frame_equal(
        pa_table_to_pl_df(left.to_table()),
        pa_table_to_pl_df(right.to_table()),
        check_row_order=check_row_order,
        check_column_order=check_column_order,
    )
