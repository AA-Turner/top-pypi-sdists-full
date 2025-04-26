from typing import Sequence
from typing import Tuple

from pyspark.sql import types as spark_types

from tecton._internals.tecton_pydantic import StrictFrozenModel
from tecton._internals.tecton_pydantic import pydantic_v1
from tecton_core import data_types as tecton_types
from tecton_core.errors import TectonValidationError


class SdkDataType(StrictFrozenModel):
    """Base class for SDK (i.e. public repo) data types."""

    @property
    def spark_type(self) -> spark_types.DataType:
        raise NotImplementedError

    @property
    def tecton_type(self) -> tecton_types.DataType:
        raise NotImplementedError

    def __repr__(self) -> str:
        # Don't use the default pydantic __repr__().
        raise NotImplementedError


class _Int32(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.IntegerType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.Int32Type()

    def __repr__(self) -> str:
        return "Int32"


# Should not be used directly by users. Use Int64 instead.
class _Int64(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.LongType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.Int64Type()

    def __repr__(self) -> str:
        return "Int64"


class _Float32(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.FloatType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.Float32Type()

    def __repr__(self) -> str:
        return "Float32"


class _Float64(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.DoubleType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.Float64Type()

    def __repr__(self) -> str:
        return "Float64"


class _String(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.StringType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.StringType()

    def __repr__(self) -> str:
        return "String"


class _Bool(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.BooleanType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.BoolType()

    def __repr__(self) -> str:
        return "Bool"


class _Timestamp(SdkDataType):
    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.TimestampType()

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.TimestampType()

    def __repr__(self) -> str:
        return "Timestamp"


# Public, instantiated versions of primitive types.
Int32 = _Int32()
Int64 = _Int64()
Float32 = _Float32()
Float64 = _Float64()
String = _String()
Bool = _Bool()
Timestamp = _Timestamp()


class Array(SdkDataType):
    element_type: SdkDataType

    def __init__(self, element_type: SdkDataType):
        """Overriden initializer. Pydantic does not support positional arguments."""
        super().__init__(element_type=element_type)

    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.ArrayType(self.element_type.spark_type)

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.ArrayType(self.element_type.tecton_type)

    def __repr__(self) -> str:
        return f"Array({repr(self.element_type)})"


# Note Field does not inherit from SdkDataType. This is because it's not directly convertible to a Tecton DataType.
class Field(StrictFrozenModel):
    name: str
    dtype: SdkDataType

    def __init__(self, name: str, dtype: SdkDataType):
        """Overriden initializer. Pydantic does not support positional arguments."""
        if isinstance(dtype, type):
            msg = f"Expected {dtype} to be instance of {dtype.__name__} for field {name}, got class object instead"
            raise TectonValidationError(msg)
        super().__init__(name=name, dtype=dtype)

    def spark_type(self) -> spark_types.StructField:
        return spark_types.StructField(self.name, self.dtype.spark_type)

    def tecton_type(self) -> tecton_types.StructField:
        return tecton_types.StructField(self.name, self.dtype.tecton_type)

    def __repr__(self) -> str:
        return f"Field('{self.name}', {repr(self.dtype)})"


class Struct(SdkDataType):
    # Use fields_ with an alias to avoid conflicting with a Pydantic BaseModel method fields(). Shadow that method with
    # a fields property so that callers can access the field intuitively.
    fields_: Tuple[Field, ...] = pydantic_v1.Field(alias="fields")

    def __init__(self, fields: Sequence[Field]):
        """Overriden initializer. Pydantic does not support positional arguments."""
        super().__init__(fields=tuple(fields) if fields else ())

    @property
    def spark_type(self) -> spark_types.DataType:
        spark_fields = [field.spark_type() for field in self.fields]
        return spark_types.StructType(spark_fields)

    @property
    def tecton_type(self) -> tecton_types.DataType:
        struct_fields = [field.tecton_type() for field in self.fields]
        return tecton_types.StructType(struct_fields)

    def __repr__(self) -> str:
        return f"Struct({self.fields})"

    @property
    def fields(self) -> Tuple[Field, ...]:
        return self.fields_


class Map(SdkDataType):
    # key_type only allows String as of 07/07/2023. From type annotations perspective, we allow all types to be passed
    # in here so users could receive better error message from MDS instead of python type checking error.
    key_type: SdkDataType
    value_type: SdkDataType

    def __init__(self, key_type: SdkDataType, value_type: SdkDataType):
        """Overriden initializer. Pydantic does not support positional arguments."""
        super().__init__(key_type=key_type, value_type=value_type)

    @property
    def spark_type(self) -> spark_types.DataType:
        return spark_types.MapType(self.key_type.spark_type, self.value_type.spark_type)

    @property
    def tecton_type(self) -> tecton_types.DataType:
        return tecton_types.MapType(self.key_type.tecton_type, self.value_type.tecton_type)

    def __repr__(self) -> str:
        return f"Map({repr(self.key_type)}, {repr(self.value_type)})"
