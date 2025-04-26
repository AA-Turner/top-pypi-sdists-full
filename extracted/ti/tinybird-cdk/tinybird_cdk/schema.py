class Schema:
    def __init__(self, scopes, table):
        self.scopes = scopes
        self.table = table
        self.columns = []

class Column:
    def __init__(self, name, src_type, ch_type, remark=None):
        self.name = name
        self.src_type = src_type
        self.ch_type = ch_type
        self.remark = remark

class Type:
    def __init__(self, name, null):
        self._name = name
        self._null = null

    @property
    def name(self):
        return self._name

    @property
    def null(self):
        return self._null

class CHType(Type):
    def __init__(self, name, null):
        super().__init__(name, null)
        if (i := self._name.find('(')) != -1:
            self.base_name = self._name[0:i]
        else:
            self.base_name = self._name

    @property
    def name(self):
        if self.null:
            return f'Nullable({self._name})'
        return self._name

# https://clickhouse.com/docs/en/sql-reference/data-types/int-uint
class Int8(CHType):
    def __init__(self, null):
        super().__init__('Int8', null)

class Int16(CHType):
    def __init__(self, null):
        super().__init__('Int16', null)

class Int32(CHType):
    def __init__(self, null):
        super().__init__('Int32', null)

class Int64(CHType):
    def __init__(self, null):
        super().__init__('Int64', null)

class Int128(CHType):
    def __init__(self, null):
        super().__init__('Int128', null)

class Int256(CHType):
    def __init__(self, null):
        super().__init__('Int256', null)

class UInt8(CHType):
    def __init__(self, null):
        super().__init__('UInt8', null)

class UInt16(CHType):
    def __init__(self, null):
        super().__init__('UInt16', null)

class UInt32(CHType):
    def __init__(self, null):
        super().__init__('UInt32', null)

class UInt64(CHType):
    def __init__(self, null):
        super().__init__('UInt64', null)

class UInt128(CHType):
    def __init__(self, null):
        super().__init__('UInt128', null)

class UInt256(CHType):
    def __init__(self, null):
        super().__init__('UInt256', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/float
class Float32(CHType):
    def __init__(self, null):
        super().__init__('Float32', null)

class Float64(CHType):
    def __init__(self, null):
        super().__init__('Float64', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/boolean
class Boolean(CHType):
    def __init__(self, null):
        super().__init__('Boolean', null)

class String(CHType):
    def __init__(self, null):
        super().__init__('String', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/uuid
class UUID(CHType):
    def __init__(self, null):
        super().__init__('UUID', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/date
class Date(CHType):
    def __init__(self, null):
        super().__init__('Date', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/date32
class Date32(CHType):
    def __init__(self, null):
        super().__init__('Date32', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/datetime
class DateTime(CHType):
    def __init__(self, null):
        super().__init__('DateTime', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/datetime64
class DateTime64(CHType):
    def __init__(self, null):
        super().__init__('DateTime64', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/json
class JSON(CHType):
    def __init__(self, null):
        super().__init__('JSON', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/domains/ipv4
class IPv4(CHType):
    def __init__(self, null):
        super().__init__('IPv4', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/domains/ipv6
class IPv6(CHType):
    def __init__(self, null):
        super().__init__('IPv6', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/geo/
class Point(CHType):
    def __init__(self, null):
        super().__init__('Point', null)

class Ring(CHType):
    def __init__(self, null):
        super().__init__('Ring', null)

class Polygon(CHType):
    def __init__(self, null):
        super().__init__('Polygon', null)

class MultiPolygon(CHType):
    def __init__(self, null):
        super().__init__('MultiPolygon', null)

# https://clickhouse.com/docs/en/sql-reference/data-types/decimal
class Decimal(CHType):
    def __init__(self, precision, scale, null):
        super().__init__(f'Decimal({precision}, {scale})', null)
        self.precision = precision
        self.scale = scale

# https://clickhouse.com/docs/en/sql-reference/data-types/fixedstring
class FixedString(CHType):
    def __init__(self, length, null):
        super().__init__(f'FixedString({length})', null)
        self.length = length

# https://clickhouse.com/docs/en/sql-reference/data-types/array
class Array(CHType):
    def __init__(self, type):
        super().__init__(f'Array({type.name})', False)
        self.type = type

# https://clickhouse.com/docs/en/sql-reference/data-types/tuple
class Tuple(CHType):
    def __init__(self, *types):
        params = ', '.join(t.name for t in types)
        super().__init__(f'Tuple({params})', False)
        self.types = types

# https://clickhouse.com/docs/en/sql-reference/data-types/map
class Map(CHType):
    def __init__(self, key_type, value_type):
        super().__init__(f'Map({key_type.name}, {value_type.name})', False)
        self.key_type = key_type
        self.value_type = value_type
