# from tecton import types as sdk_types
import pytest

from tecton import types as sdk_types
from tecton_core.errors import TectonValidationError


def test_field_with_primitives():
    sdk_types.Field("I32_COL", sdk_types.Int32)
    sdk_types.Field("I64_COL", sdk_types.Int64)
    sdk_types.Field("F32_COL", sdk_types.Float32)
    sdk_types.Field("F64_COL", sdk_types.Float64)
    sdk_types.Field("STR_COL", sdk_types.String)
    sdk_types.Field("BOOL_COL", sdk_types.Bool)
    sdk_types.Field("TS_COL", sdk_types.Timestamp)


def test_field_enforces_instantiating_complex_data_types():
    # Passing the class should fail
    with pytest.raises(
        TectonValidationError,
        match="Expected <class 'tecton.types.Array'> to be instance of Array for field asdf, got class object instead",
    ) as exc_info:
        sdk_types.Field("asdf", sdk_types.Array)
    with pytest.raises(
        TectonValidationError,
        match="Expected <class 'tecton.types.Struct'> to be instance of Struct for field asdf, got class object instead",
    ) as exc_info:
        sdk_types.Field("asdf", sdk_types.Struct)
    with pytest.raises(
        TectonValidationError,
        match="Expected <class 'tecton.types.Map'> to be instance of Map for field asdf, got class object instead",
    ) as exc_info:
        sdk_types.Field("asdf", sdk_types.Map)

    # Instances of each class succeed
    sdk_types.Field("asdf", sdk_types.Array(sdk_types.String))
    sdk_types.Field("asdf", sdk_types.Struct(sdk_types.String))
    sdk_types.Field("asdf", sdk_types.Map(sdk_types.String, sdk_types.String))
