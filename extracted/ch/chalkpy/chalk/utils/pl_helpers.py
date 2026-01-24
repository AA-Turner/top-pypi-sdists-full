from __future__ import annotations

import itertools
import zoneinfo
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Iterator, TypeGuard, TypeVar, overload

import pyarrow as pa
from packaging.version import parse

from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

_logger = get_logger(__name__)

try:
    import orjson

    json_loads = orjson.loads
except ImportError:
    import json

    json_loads = json.loads


def json_loads_as_str(x: str | None):
    if x is None:
        return None
    x = json_loads(x)
    return x if x is None else str(x)


def is_version_gte(version: str, target: str) -> bool:
    return parse(version) >= parse(target)


try:
    import polars as pl

    is_new_polars = is_version_gte(pl.__version__, "0.18.0")
    polars_has_pad_start = is_version_gte(pl.__version__, "0.19.12")
    polars_array_uses_shape = is_version_gte(pl.__version__, "1.0.0")
    polars_uses_schema_overrides = is_version_gte(pl.__version__, "0.20.31")
    polars_join_ignores_nulls = is_version_gte(pl.__version__, "0.20.0")
    polars_broken_concat_on_nested_list = is_version_gte(pl.__version__, "1.0.0")
    polars_group_by_instead_of_groupby = is_version_gte(pl.__version__, "1.0.0")
    polars_name_dot_suffix_instead_of_suffix = is_version_gte(pl.__version__, "1.0.0")
    polars_lazy_frame_collect_schema = is_version_gte(pl.__version__, "1.0.0")
    polars_allow_lit_empty_struct = is_version_gte(pl.__version__, "1.0.0")
except ImportError:
    is_new_polars = False
    polars_has_pad_start = False
    polars_array_uses_shape = False
    polars_uses_schema_overrides = False
    polars_join_ignores_nulls = False
    polars_broken_concat_on_nested_list = False
    polars_group_by_instead_of_groupby = False
    polars_name_dot_suffix_instead_of_suffix = False
    polars_lazy_frame_collect_schema = False
    polars_allow_lit_empty_struct = False


def pl_array(inner: pl.PolarsDataType, size: int) -> pl.Array:
    """Create a Polars Array type with version-compatible parameter names.

    Args:
        inner: The inner data type of the array
        size: The fixed size of the array

    Returns:
        A Polars Array type
    """
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if polars_array_uses_shape:
        return pl.Array(inner=inner, shape=size)
    else:
        return pl.Array(inner=inner, width=size)  # type: ignore[call-arg]


def chunked_df_slices(df: pl.LazyFrame | pl.DataFrame, chunk_size: int) -> Iterator[pl.DataFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if len(df.columns) == 0:
        return
    if isinstance(df, pl.LazyFrame):
        df = df.collect()
    if len(df) == 0:
        return
    if chunk_size == -1:
        yield df
        return
    assert chunk_size > 0, "Chunk size must be -1 (for no chunking) or positive"
    for i in itertools.count():
        df_slice = df.slice(offset=i * chunk_size, length=chunk_size)
        if len(df_slice) == 0:
            # _logger.info("Chunk has length of 0; breaking")
            # No more data to write!
            break
        # _logger.info(f"Yielding chunk {i} of size {len(df_slice)}")
        yield df_slice


def pl_datetime_to_iso_string(expr: pl.Expr, tz_key: str | None) -> pl.Expr:
    """Convert a datetime expression, optionally with a timezone, into an ISO-formatted string
    The ``tz_key`` should be a timezone understood by ``zoneinfo``.
    """
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if tz_key is None:
        timezone = ""
    else:
        tzinfo = zoneinfo.ZoneInfo(tz_key)
        utc_offset = tzinfo.utcoffset(None)
        if utc_offset is None:
            raise ValueError(f"Timezone has no UTC offset: {tz_key}")
        sign = "-" if utc_offset < timedelta(0) else "+"
        seconds = abs(utc_offset.seconds + utc_offset.days * 24 * 3600)
        hours = seconds // 3600
        minutes = seconds % 3600
        timezone = f"{sign}{hours:02d}:{minutes:02d}"
    if polars_has_pad_start:
        return pl.format(
            "{}-{}-{}T{}:{}:{}.{}" + timezone,
            expr.dt.year().cast(pl.Utf8).str.pad_start(4, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.month().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.day().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.hour().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.minute().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.second().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.microsecond().cast(pl.Utf8).str.pad_start(6, "0"),  # pyright: ignore -- polars backcompat
        )
    else:
        return pl.format(
            "{}-{}-{}T{}:{}:{}.{}" + timezone,
            expr.dt.year().cast(pl.Utf8).str.rjust(4, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.month().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.day().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.hour().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.minute().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.second().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.microsecond().cast(pl.Utf8).str.rjust(6, "0"),  # pyright: ignore -- polars backcompat
        )


def pl_date_to_iso_string(expr: pl.Expr) -> pl.Expr:
    """Convert a date expression into an ISO-formatted string"""
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if is_new_polars:
        return pl.format(
            "{}-{}-{}",
            expr.dt.year().cast(pl.Utf8).str.pad_start(4, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.month().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.day().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
        )
    else:
        return pl.format(
            "{}-{}-{}",
            expr.dt.year().cast(pl.Utf8).str.rjust(4, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.month().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.day().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
        )


def pl_time_to_iso_string(expr: pl.Expr) -> pl.Expr:
    """Convert a time expression into an ISO-formatted string"""
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if is_new_polars:
        return pl.format(
            "{}:{}:{}.{}",
            expr.dt.hour().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.minute().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.second().cast(pl.Utf8).str.pad_start(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.microsecond().cast(pl.Utf8).str.pad_start(6, "0"),  # pyright: ignore -- polars backcompat
        )
    else:
        return pl.format(
            "{}:{}:{}.{}",
            expr.dt.hour().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.minute().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.second().cast(pl.Utf8).str.rjust(2, "0"),  # pyright: ignore -- polars backcompat
            expr.dt.microsecond().cast(pl.Utf8).str.rjust(6, "0"),  # pyright: ignore -- polars backcompat
        )


def pl_dtype_swap(dtype: pl.PolarsDataType, _from: pl.PolarsDataType, to: pl.PolarsDataType) -> pl.PolarsDataType:
    if isinstance(dtype, _from):
        return to
    if isinstance(dtype, pl.List):
        return pl.List(inner=pl_dtype_swap(dtype.inner, _from, to))
    if isinstance(dtype, pl.Struct):
        return pl.Struct(
            {field_name: pl_dtype_swap(field_dtype, _from, to) for field_name, field_dtype in dtype.to_schema().items()}
        )
    return dtype


def pl_json_decode(series: pl.Series, dtype: pl.PolarsDataType) -> pl.Series:
    if is_new_polars:
        swapped_dtype = pl_dtype_swap(dtype, pl.Binary, pl.Utf8)
        if swapped_dtype == pl.Utf8:
            decoded_series = series.map_elements(json_loads_as_str, return_dtype=swapped_dtype).cast(
                dtype
            )  # pyright: ignore -- polars backcompat
        else:
            decoded_series = series.map_elements(json_loads, return_dtype=swapped_dtype).cast(
                dtype
            )  # pyright: ignore -- polars backcompat
    else:
        decoded_series = series.apply(json_loads, return_dtype=dtype)  # pyright: ignore -- polars backcompat
    decoded_series = decoded_series.cast(dtype)
    return decoded_series


def pl_duration_to_iso_string(expr: pl.Expr) -> pl.Expr:
    """Convert a duration expression into an ISO-formatted string"""
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    try:
        return pl.format(
            "{}P{}DT{}H{}M{}.{}S",
            pl.when(expr.dt.microseconds() < 0)  # pyright: ignore -- polars backcompat
            .then(pl.lit("-"))
            .otherwise(pl.lit("")),  # pyright: ignore -- polars backcompat
            expr.dt.days().abs().cast(pl.Utf8),  # pyright: ignore -- polars backcompat
            (expr.dt.hours().abs() % 24).cast(pl.Utf8),  # pyright: ignore -- polars backcompat
            (expr.dt.minutes().abs() % 60).cast(pl.Utf8),  # pyright: ignore -- polars backcompat
            (expr.dt.seconds().abs() % 60).cast(pl.Utf8),  # pyright: ignore -- polars backcompat
            (expr.dt.microseconds().abs() % 1_000_000)  # pyright: ignore -- polars backcompat
            .cast(pl.Utf8)
            .str.pad_start(6, "0")  # pyright: ignore -- polars backcompat
            if is_new_polars
            else (expr.dt.microseconds().abs() % 1_000_000)  # pyright: ignore -- polars backcompat
            .cast(pl.Utf8)
            .str.rjust(6, "0"),  # pyright: ignore -- polars backcompat
        )
    except AttributeError:
        return (
            pl.format("{}P{}DT{}H{}M{}.{}S", expr.dt.total_microseconds().abs() % 1_000_000)
            .cast(pl.Utf8)
            .str.pad_start(
                6,
                "0",
            )
        )


def pl_json_encode(expr: pl.Expr, dtype: pl.PolarsDataType):
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(dtype, pl.Struct):
        # Polars does not distinguish between none and an empty struct
        return _json_encode_inner(expr, dtype)
    else:
        return pl.when(expr.is_null()).then(pl.lit("null", dtype=pl.Utf8)).otherwise(_json_encode_inner(expr, dtype))


def _py_escape_str(x: str) -> str:
    # See https://stackoverflow.com/questions/4901133/json-and-escaping-characters for the characters that must be escaped
    return (
        x.replace("\\", "\\\\")
        .replace("\u0000", "\\u0000")
        .replace("\u0001", "\\u0001")
        .replace("\u0002", "\\u0002")
        .replace("\u0003", "\\u0003")
        .replace("\u0004", "\\u0004")
        .replace("\u0005", "\\u0005")
        .replace("\u0006", "\\u0006")
        .replace("\u0007", "\\u0007")
        .replace("\b", "\\b")  # equal to \u0008
        .replace("\t", "\\t")  # equal to \u0009
        .replace("\n", "\\n")  # equal to \u000a
        .replace("\u000b", "\\u000b")
        .replace("\f", "\\f")  # equal to \u000c
        .replace("\r", "\\r")  # equal to \u000d
        .replace("\u000e", "\\u000e")
        .replace("\u000f", "\\u000f")
        .replace("\u0010", "\\u0010")
        .replace("\u0011", "\\u0011")
        .replace("\u0012", "\\u0012")
        .replace("\u0013", "\\u0013")
        .replace("\u0014", "\\u0014")
        .replace("\u0015", "\\u0015")
        .replace("\u0016", "\\u0016")
        .replace("\u0017", "\\u0017")
        .replace("\u0018", "\\u0018")
        .replace("\u0019", "\\u0019")
        .replace("\u001a", "\\u001a")
        .replace("\u001b", "\\u001b")
        .replace("\u001c", "\\u001c")
        .replace("\u001d", "\\u001d")
        .replace("\u001e", "\\u001e")
        .replace("\u001f", "\\u001f")
        .replace('"', '\\"')
    )


def pl_escape_str(x: pl.Expr) -> pl.Expr:
    # Not sure if using a regex would be faster, but literal expressions are easier to write
    # See https://stackoverflow.com/questions/4901133/json-and-escaping-characters for the characters that must be escaped
    return (
        x.str.replace_all("\\", "\\\\", literal=True)
        .str.replace_all("\u0000", "\\u0000", literal=True)
        .str.replace_all("\u0001", "\\u0001", literal=True)
        .str.replace_all("\u0002", "\\u0002", literal=True)
        .str.replace_all("\u0003", "\\u0003", literal=True)
        .str.replace_all("\u0004", "\\u0004", literal=True)
        .str.replace_all("\u0005", "\\u0005", literal=True)
        .str.replace_all("\u0006", "\\u0006", literal=True)
        .str.replace_all("\u0007", "\\u0007", literal=True)
        .str.replace_all("\b", "\\b", literal=True)  # equal to \u0008
        .str.replace_all("\t", "\\t", literal=True)  # equal to \u0009
        .str.replace_all("\n", "\\n", literal=True)  # equal to \u000a
        .str.replace_all("\u000b", "\\u000b", literal=True)
        .str.replace_all("\f", "\\f", literal=True)  # equal to \u000c
        .str.replace_all("\r", "\\r", literal=True)  # equal to \u000d
        .str.replace_all("\u000e", "\\u000e", literal=True)
        .str.replace_all("\u000f", "\\u000f", literal=True)
        .str.replace_all("\u0010", "\\u0010", literal=True)
        .str.replace_all("\u0011", "\\u0011", literal=True)
        .str.replace_all("\u0012", "\\u0012", literal=True)
        .str.replace_all("\u0013", "\\u0013", literal=True)
        .str.replace_all("\u0014", "\\u0014", literal=True)
        .str.replace_all("\u0015", "\\u0015", literal=True)
        .str.replace_all("\u0016", "\\u0016", literal=True)
        .str.replace_all("\u0017", "\\u0017", literal=True)
        .str.replace_all("\u0018", "\\u0018", literal=True)
        .str.replace_all("\u0019", "\\u0019", literal=True)
        .str.replace_all("\u001a", "\\u001a", literal=True)
        .str.replace_all("\u001b", "\\u001b", literal=True)
        .str.replace_all("\u001c", "\\u001c", literal=True)
        .str.replace_all("\u001d", "\\u001d", literal=True)
        .str.replace_all("\u001e", "\\u001e", literal=True)
        .str.replace_all("\u001f", "\\u001f", literal=True)
        .str.replace_all('"', '\\"', literal=True)
    )


def _backup_json_encode(x: Any) -> str:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(x, pl.Series):
        x = x.to_list()
    return orjson.dumps(x, option=orjson.OPT_SORT_KEYS | orjson.OPT_UTC_Z | orjson.OPT_NAIVE_UTC).decode("utf8")


T = TypeVar("T", bound=type)


def _check_is_type(dtype: pl.PolarsDataType, typ: T) -> TypeGuard[T]:
    # polars < 0.20
    if isinstance(dtype, type):
        return issubclass(dtype, typ)
    else:
        # polars >= 0.20
        return isinstance(dtype, typ)


def _json_encode_inner(expr: pl.Expr, dtype: pl.PolarsDataType) -> pl.Expr:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(dtype, (type, pl.DataType)):  # pyright: ignore [reportUnnecessaryIsInstance]
        if _check_is_type(dtype, pl.Boolean):
            return pl.when(expr).then(pl.lit("true", dtype=pl.Utf8)).otherwise(pl.lit("false", dtype=pl.Utf8))
        if _check_is_type(dtype, (pl.Float32, pl.Float64)):  # pyright: ignore[reportArgumentType]
            # Floats of nan, +inf, or -inf cannot be represented as json, so instead convert them to "null"
            # Otherwise, they can be cast directly
            return (
                pl.when(expr.is_nan() | expr.is_infinite())
                .then(pl.lit("null", dtype=pl.Utf8))
                .otherwise(expr.cast(pl.Utf8))
            )

        if _check_is_type(
            dtype,
            (
                pl.Float32,
                pl.Float64,
                pl.Int16,
                pl.Int32,
                pl.Int64,
                pl.Int8,
                pl.UInt16,
                pl.UInt32,
                pl.UInt64,
                pl.UInt8,
            ),  # pyright: ignore[reportArgumentType]
        ):
            # Ints can be cast directly
            return expr.cast(pl.Utf8, strict=True)
        if _check_is_type(dtype, pl.Utf8):
            # Must escape any quote and backslashes
            # First escape all backslashes to double backslash
            # Then, wrap the result in quotes

            return pl.format('"{}"', pl_escape_str(expr))

        if _check_is_type(dtype, pl.Time):
            # Convert time to iso
            return pl_json_encode(pl_time_to_iso_string(expr), pl.Utf8)
        if _check_is_type(dtype, pl.Date):
            # Convert a date to iso
            return pl_json_encode(pl_date_to_iso_string(expr), pl.Utf8)
    if isinstance(dtype, pl.Datetime):
        # Convert datetime to iso
        return pl_json_encode(pl_datetime_to_iso_string(expr, dtype.time_zone), pl.Utf8)
    if isinstance(dtype, pl.Duration):
        # Convert duration to iso
        return pl_json_encode(pl_duration_to_iso_string(expr), pl.Utf8)
    if isinstance(dtype, pl.List):
        inner_dtype = dtype.inner
        assert inner_dtype is not None
        # TODO -- this will likely break on lists of structs or lists of lists
        # However, .eval cannot be called on an empty list
        # So we append an empty element, eval, and then remove it
        if isinstance(inner_dtype, (pl.List, pl.Struct)):
            # TODO: We do NOT support nested collections right now, because of how we must append a default
            # value in the case of an empty collection
            # Need to add support for this eventually
            # For now, use a (slow) UDF
            _logger.warning(f"Including the python UDF json encode in the polars expression to handle dtype {dtype}")
            if is_new_polars:
                return expr.map_elements(  # pyright: ignore -- polars backcompat
                    _backup_json_encode, return_dtype=pl.Utf8
                )
            else:
                return expr.apply(_backup_json_encode, return_dtype=pl.Utf8)  # pyright: ignore -- polars backcompat
        expr = expr.fill_null([])
        lists_with_extra_none = (
            expr.list.concat(pl.lit(None))  # pyright: ignore -- back compat
            if is_new_polars
            else expr.arr.concat(pl.lit(None))  # pyright: ignore -- back compat
        )
        encoded_with_extra = (
            lists_with_extra_none.list.eval(  # pyright: ignore -- polars backcompat
                pl_json_encode(pl.element(), inner_dtype)
            )
            if is_new_polars
            else lists_with_extra_none.arr.eval(  # pyright: ignore -- back compat
                pl_json_encode(pl.element(), inner_dtype)
            )
        )
        encoded_without_extra = (
            encoded_with_extra.list.slice(offset=0, length=expr.list.len())  # pyright: ignore -- polars backcompat
            if is_new_polars
            else encoded_with_extra.arr.slice(offset=0, length=expr.arr.lengths())  # pyright: ignore -- back compat
        )
        return (
            pl.format("[{}]", encoded_without_extra.list.join(","))  # pyright: ignore -- polars backcompat
            if is_new_polars
            else pl.format("[{}]", encoded_without_extra.arr.join(","))  # pyright: ignore -- back compat
        )
    if isinstance(dtype, pl.Struct):
        fields_encoded = [
            pl.format((f'"{_py_escape_str(f.name)}":' "{}"), pl_json_encode(expr.struct.field(f.name), f.dtype))
            for f in sorted(dtype.fields, key=lambda x: x.name)
        ]
        format_str = "{" + ",".join(["{}"] * len(fields_encoded)) + "}"
        if len(fields_encoded) == 0:
            return pl.lit("{}")
        return pl.format(format_str, *fields_encoded)

    if dtype == pl.Binary:  # pyright: ignore[reportUnnecessaryComparison]
        return pl_json_encode(expr.bin.encode("base64"), pl.Utf8)

    raise TypeError(f"Unsupported dtype for json encoding: {dtype}")


def recursively_has_float16(dtype: pa.DataType) -> bool:
    """Check whether this dtype has a float16 field in it"""
    if pa.types.is_float16(dtype):
        return True
    if pa.types.is_struct(dtype):
        assert isinstance(dtype, pa.StructType)
        return any(recursively_has_float16(dtype.field(i).type) for i in range(dtype.num_fields))
    if pa.types.is_list(dtype) or pa.types.is_large_list(dtype) or pa.types.is_fixed_size_list(dtype):
        assert isinstance(dtype, (pa.LargeListType, pa.ListType, pa.FixedSizeListType))
        return recursively_has_float16(dtype.value_type)
    if pa.types.is_map(dtype):
        assert isinstance(dtype, pa.MapType)
        return recursively_has_float16(dtype.key_type) or recursively_has_float16(dtype.item_type)
    return False


def pl_is_uniquable_on(dtype: pl.PolarsDataType) -> bool:
    """Check whether the Polars dtype can be uniqued upon, which currently tests for existence of lists in the dtype"""
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(dtype, pl.Struct):
        return all(pl_is_uniquable_on(f.dtype) for f in dtype.fields)
    if isinstance(dtype, pl.List):
        return False
    if is_new_polars:
        if isinstance(dtype, pl.Array):
            return False
    return True


def pa_is_uniquable_on(dtype: pa.DataType) -> bool:
    """Check whether the PyArrow dtype can be uniqued upon, which currently tests for existence of lists in the dtype"""
    if pa.types.is_struct(dtype):
        assert isinstance(dtype, pa.StructType)
        return all(pa_is_uniquable_on(dtype.field(i).type) for i in range(dtype.num_fields))
    if pa.types.is_list(dtype) or pa.types.is_large_list(dtype) or pa.types.is_fixed_size_list(dtype):
        return False
    return True


def recursively_has_struct(dtype: pa.DataType) -> bool:
    """Check whether this dtype has a struct field in it"""
    if pa.types.is_struct(dtype):
        return True
    if pa.types.is_list(dtype) or pa.types.is_large_list(dtype) or pa.types.is_fixed_size_list(dtype):
        assert isinstance(dtype, (pa.LargeListType, pa.ListType, pa.FixedSizeListType))
        return recursively_has_struct(dtype.value_type)
    if pa.types.is_map(dtype):
        assert isinstance(dtype, pa.MapType)
        return recursively_has_struct(dtype.key_type) or recursively_has_struct(dtype.item_type)
    return False


def apply_compat(
    expr: "pl.Expr",
    function: Any,
    return_dtype: "pl.PolarsDataType | None" = None,
    **kwargs: Any,
) -> "pl.Expr":
    """
    Apply a custom function to an expression in a version-compatible way.

    In Polars >= 0.19, expr.apply() was deprecated in favor of expr.map_elements().
    This function provides compatibility between versions.

    Args:
        expr: The Polars expression to apply the function to
        function: The function to apply to each element
        return_dtype: The return data type for the expression (optional)
        **kwargs: Additional keyword arguments to pass to the underlying method

    Returns:
        A Polars expression with the function applied

    Example:
        >>> import polars as pl
        >>> from chalkengine.utils.polars_compat_util import apply_compat
        >>> df = pl.DataFrame({"a": [1, 2, 3]})
        >>> df.select(apply_compat(pl.col("a"), lambda x: x * 2))
    """
    # Build kwargs for the call
    call_kwargs = kwargs.copy()
    if return_dtype is not None:
        call_kwargs["return_dtype"] = return_dtype

    try:
        # Try newer API first: map_elements()
        return expr.map_elements(function, **call_kwargs)  # type: ignore
    except AttributeError:
        # Fall back to older API: apply()
        return expr.apply(function, **call_kwargs)  # type: ignore


@overload
def str_json_decode_compat(expr: "pl.Expr", dtype: "pl.PolarsDataType") -> "pl.Expr":
    ...


@overload
def str_json_decode_compat(expr: "pl.Series", dtype: "pl.PolarsDataType") -> "pl.Series":
    ...


def str_json_decode_compat(expr: "pl.Expr | pl.Series", dtype: "pl.PolarsDataType") -> "pl.Expr | pl.Series":
    """
    Parse/decode JSON strings in a version-compatible way.

    In newer Polars versions (>= 1.0), str.json_extract() was renamed to str.json_decode().
    This function provides compatibility between versions.

    Args:
        expr: The Polars expression containing JSON strings to parse
        dtype: The Polars data type to extract to

    Returns:
        A Polars expression that parses the JSON strings
    """
    try:
        # Try newer API first: str.json_decode()
        return expr.str.json_decode(dtype=dtype)  # type: ignore
    except AttributeError:
        # Fall back to older API: str.json_extract()
        return expr.str.json_extract(dtype=dtype)  # type: ignore


def schema_compat(df: "pl.DataFrame | pl.LazyFrame"):
    if polars_lazy_frame_collect_schema and isinstance(df, pl.LazyFrame):
        return df.collect_schema()
    return df.schema
