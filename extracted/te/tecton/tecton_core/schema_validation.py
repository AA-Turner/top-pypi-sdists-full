from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

import pandas
import pyarrow

from tecton_core import data_types
from tecton_core.errors import TectonValidationError
from tecton_core.schema import Schema


@dataclass
class FieldTypeDiff:
    field: str
    msg: str


@dataclass
class DiffResult:
    missing_fields: List[str] = field(default_factory=list)
    missmatch_types: List[FieldTypeDiff] = field(default_factory=list)

    def __bool__(self):
        return len(self.missing_fields) > 0 or len(self.missmatch_types) > 0

    def as_str(self):
        def lines():
            if self.missing_fields:
                yield f"Missing fields: {', '.join(self.missing_fields)}"

            if self.missmatch_types:
                yield "Types do not match:"
                for item in self.missmatch_types:
                    yield f"  Field {item.field}: {item.msg}"

        return "\n".join(lines())


class CastError(TectonValidationError):
    def __init__(self, msg):
        super().__init__(msg, can_drop_traceback=True)

    @staticmethod
    def for_diff(diff_result: DiffResult) -> "CastError":
        return CastError("Schema mismatch:\n" + diff_result.as_str())


_ColumnGetter = Callable[[str, pyarrow.DataType], pyarrow.Array]


def cast(
    obj: Union[pyarrow.Table, pyarrow.RecordBatch, pandas.DataFrame], schema: Union[Schema, pyarrow.Schema]
) -> pyarrow.Table:
    if isinstance(schema, Schema):
        arrow_schema = tecton_schema_to_arrow_schema(schema)
    elif isinstance(schema, pyarrow.Schema):
        arrow_schema = schema
    else:
        msg = f"Unsupported schema type: {type(schema)}"
        raise TypeError(msg)

    if isinstance(obj, (pyarrow.RecordBatch, pyarrow.Table)):

        def get_column(name: str, dtype: pyarrow.DataType) -> pyarrow.Array:
            return obj.column(name).cast(dtype)

    elif isinstance(obj, pandas.DataFrame):
        columns = _pandas_columns(obj)

        def get_column(name: str, dtype: pyarrow.DataType) -> pyarrow.Array:
            series = columns[name]
            if len(series) != 1:
                msg = f"Ambiguous column label {name}. Ensure only one column exists with a given label."
                raise CastError(msg)
            return pyarrow.Array.from_pandas(series[0], type=dtype)

    else:
        msg = f"Unexpected type: {type(obj)}"
        raise TypeError(msg)
    arrays = cast_columns(get_column, arrow_schema)
    return pyarrow.Table.from_arrays(arrays, schema=arrow_schema)


def cast_batch(batch: pyarrow.RecordBatch, schema: Union[Schema, pyarrow.Schema]) -> pyarrow.RecordBatch:
    if isinstance(schema, Schema):
        arrow_schema = tecton_schema_to_arrow_schema(schema)
    elif isinstance(schema, pyarrow.Schema):
        arrow_schema = schema
    else:
        msg = f"Unsupported schema type: {type(schema)}"
        raise TypeError(msg)

    def get_column(name: str, dtype: pyarrow.DataType) -> pyarrow.Array:
        return batch.column(name).cast(dtype)

    arrays = cast_columns(get_column, arrow_schema)
    return pyarrow.RecordBatch.from_arrays(arrays, schema=arrow_schema)


def _pandas_columns(df: pandas.DataFrame) -> Dict[str, List[pandas.Series]]:
    def _series_iter():
        axes = df.axes
        if len(axes) != 2:
            msg = f"Pandas DataFrame should have 2 axes; not {len(axes)}"
            raise CastError(msg)

        index = df.index
        if isinstance(index, pandas.MultiIndex):
            for level_name in index.names:
                yield level_name, index.get_level_values(level_name)
        elif isinstance(index, pandas.Index):
            if index.name is not None:
                yield index.name, index
        else:
            msg = "First axis of a Pandas DataFrame should be an Index"
            raise CastError(msg)

        yield from df.items()

    ret = {}
    for label, series in _series_iter():
        ret.setdefault(label, []).append(series)
    return ret


def cast_columns(column_getter: _ColumnGetter, schema: pyarrow.Schema) -> List[pyarrow.Array]:
    diff = DiffResult()
    arrays = []
    for name, dtype in zip(schema.names, schema.types):
        try:
            arrays.append(column_getter(name, dtype))
        except KeyError:
            diff.missing_fields.append(name)
        except pyarrow.ArrowTypeError as e:
            diff.missmatch_types.append(FieldTypeDiff(name, str(e)))
        except pyarrow.ArrowInvalid as e:
            diff.missmatch_types.append(FieldTypeDiff(name, str(e)))
    if diff:
        raise CastError.for_diff(diff)
    else:
        return arrays


_PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE: Dict[data_types.DataType, pyarrow.DataType] = {
    data_types.Int32Type(): pyarrow.int32(),
    data_types.Int64Type(): pyarrow.int64(),
    data_types.Float32Type(): pyarrow.float32(),
    data_types.Float64Type(): pyarrow.float64(),
    data_types.StringType(): pyarrow.string(),
    data_types.TimestampType(): pyarrow.timestamp("ns", "UTC"),
    data_types.BoolType(): pyarrow.bool_(),
}

_PRIMITIVE_ARROW_TYPE_TO_TECTON_TYPE: Dict[pyarrow.DataType, data_types.DataType] = {
    arrow: tecton for tecton, arrow in _PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE.items()
}


def _tecton_type_to_arrow_type(tecton_type: data_types.DataType) -> pyarrow.DataType:
    if tecton_type in _PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE:
        return _PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE[tecton_type]

    if isinstance(tecton_type, data_types.ArrayType):
        return pyarrow.list_(_tecton_type_to_arrow_type(tecton_type.element_type))

    if isinstance(tecton_type, data_types.MapType):
        return pyarrow.map_(
            _tecton_type_to_arrow_type(tecton_type.key_type),
            _tecton_type_to_arrow_type(tecton_type.value_type),
        )

    if isinstance(tecton_type, data_types.StructType):
        fields = []
        for tecton_field in tecton_type.fields:
            fields.append(pyarrow.field(tecton_field.name, _tecton_type_to_arrow_type(tecton_field.data_type)))
        return pyarrow.struct(fields)

    msg = f"Tecton type {tecton_type} can't be converted to arrow type"
    raise ValueError(msg)


def _arrow_type_to_tecton_type(arrow_type: pyarrow.DataType) -> data_types.DataType:
    if isinstance(arrow_type, pyarrow.TimestampType):
        return data_types.TimestampType()

    if arrow_type in _PRIMITIVE_ARROW_TYPE_TO_TECTON_TYPE:
        return _PRIMITIVE_ARROW_TYPE_TO_TECTON_TYPE[arrow_type]

    if isinstance(arrow_type, pyarrow.ListType):
        return data_types.ArrayType(_arrow_type_to_tecton_type(arrow_type.value_type))

    if isinstance(arrow_type, pyarrow.MapType):
        return data_types.MapType(
            _arrow_type_to_tecton_type(arrow_type.key_type),
            _arrow_type_to_tecton_type(arrow_type.item_type),
        )

    if isinstance(arrow_type, pyarrow.StructType):
        fields = []
        for f in arrow_type:
            fields.append(data_types.StructField(f.name, _arrow_type_to_tecton_type(f.type)))
        return data_types.StructType(fields)

    # TODO (Oleksii): update schema validation to handle extra columns of various types in input spine
    if pyarrow.types.is_date32(arrow_type):
        return data_types.TimestampType()

    msg = f"Arrow type {arrow_type} can't be converted to tecton type"
    raise TypeError(msg)


def tecton_schema_to_arrow_schema(schema: Schema) -> pyarrow.Schema:
    fields = []
    for column, data_type in schema.column_name_and_data_types():
        fields.append(pyarrow.field(column, _tecton_type_to_arrow_type(data_type)))
    return pyarrow.schema(fields)


def arrow_schema_to_tecton_schema(schema: pyarrow.Schema, ignore_unsupported_types: bool = False) -> Schema:
    fields = {}
    for f in schema:
        try:
            fields[f.name] = _arrow_type_to_tecton_type(f.type)
        except TypeError:
            if ignore_unsupported_types:
                continue
            raise
    return Schema.from_dict(fields)
