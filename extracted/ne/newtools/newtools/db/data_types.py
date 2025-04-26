# (c) 2012-2018 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)


class BaseType:
    def __repr__(self) -> str:
        return self.__class__.__name__.replace('Type', '')


class BooleanType(BaseType):
    ATHENA_TYPE = 'boolean'


class IntegerType(BaseType):
    ATHENA_TYPE = 'integer'


class BigIntType(BaseType):
    ATHENA_TYPE = 'bigint'


class DoubleType(BaseType):
    ATHENA_TYPE = 'double'


class FloatType(BaseType):
    ATHENA_TYPE = 'float'


class DecimalType(BaseType):
    def __init__(self, precision: int, scale: int) -> None:
        self.precision = precision
        self.scale = scale

        self.ATHENA_TYPE = f'decimal({precision}, {scale})'

    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.precision}, {self.scale})'


class StringType(BaseType):
    ATHENA_TYPE = 'string'


class VarCharType(BaseType):
    def __init__(self, length: int) -> None:
        self.length = length

        self.ATHENA_TYPE = f'varchar({length})'

    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.length})'


class TimestampType(BaseType):
    ATHENA_TYPE = 'timestamp'


class DateType(BaseType):
    ATHENA_TYPE = 'date'


ALL_TYPES = [
    BooleanType,
    IntegerType,
    BigIntType,
    DoubleType,
    FloatType,
    DecimalType,
    StringType,
    VarCharType,
    TimestampType,
    DateType
]
