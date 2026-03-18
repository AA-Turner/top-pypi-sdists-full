"""Unit tests for pydoris.sqlalchemy.datatype — no Doris connection required.

Type-mapping expectations are based on real Doris 4.0.2 SHOW COLUMNS output:

    DDL type            SHOW COLUMNS reports as
    ─────────────────── ────────────────────────
    BOOLEAN             boolean
    TINYINT             tinyint
    SMALLINT            smallint
    INT / INTEGER       int
    BIGINT              bigint
    LARGEINT            largeint
    FLOAT               float
    DOUBLE              double
    DECIMALV3(18,6)     decimal(18,6)
    DECIMALV3           decimal(38,9)
    CHAR(50)            char(50)
    VARCHAR(255)        varchar(255)
    STRING / TEXT        text
    DATE / DATEV2       date
    DATETIME            datetime
    DATETIME(3)         datetime(3)
    DATETIMEV2(3)       datetime(3)
    JSON / JSONB        json
    ARRAY<INT>          array<int>
    MAP<STRING,INT>     map<text,int>
    STRUCT<…>           struct<…>
    IPV4                ipv4
    IPV6                ipv6
    VARIANT             variant
    HLL                 hll
    BITMAP              bitmap
    QUANTILE_STATE      quantile_state
    AGG_STATE           agg_state
"""
import datetime

import pytest
from sqlalchemy.sql import sqltypes

from pydoris.sqlalchemy.datatype import (
    TINYINT, LARGEINT, DOUBLE, HLL, BITMAP, QUANTILE_STATE, AGG_STATE,
    ARRAY, MAP, STRUCT, IPV4, IPV6, TIME, VARIANT,
    parse_sqltype, _type_map,
)


# ───────────────────────────────────────────────────────────────────────────
# _type_map completeness — every type name Doris might return or accept
# ───────────────────────────────────────────────────────────────────────────
class TestTypeMapCompleteness:

    @pytest.mark.parametrize("type_name", [
        # Boolean
        "boolean",
        # Integer
        "tinyint", "smallint", "int", "integer", "bigint", "largeint",
        # Floating-point
        "float", "double",
        # Fixed-precision (includes deprecated variants for backward-compat)
        "decimal", "decimalv2", "decimalv3",
        # String
        "varchar", "char", "json", "jsonb", "text", "string",
        # Date / time (includes v1/v2 variants that may appear in older schemas)
        "date", "datev1", "datev2",
        "datetime", "datetimev1", "datetimev2",
        "time",
        # Structural & aggregation
        "array", "map", "struct",
        "hll", "quantile_state", "bitmap", "agg_state",
        # Network
        "ipv4", "ipv6",
        # Semi-structured
        "variant",
    ])
    def test_type_registered(self, type_name):
        assert type_name in _type_map

    def test_tinyint_maps_to_custom_class(self):
        """TINYINT must map to our TINYINT, NOT sqltypes.SMALLINT."""
        assert _type_map["tinyint"] is TINYINT

    def test_integer_alias(self):
        """INTEGER is an alias for INT in Doris DDL."""
        assert _type_map["integer"] is _type_map["int"]


# ───────────────────────────────────────────────────────────────────────────
# parse_sqltype — basic types (the normalised forms SHOW COLUMNS returns)
# ───────────────────────────────────────────────────────────────────────────
class TestParseSqlTypeBasic:
    """Test parse_sqltype with the type strings Doris actually returns."""

    @pytest.mark.parametrize("type_str, expected_cls", [
        # What SHOW COLUMNS really returns (verified on Doris 4.0.2)
        ("boolean",   sqltypes.BOOLEAN),
        ("tinyint",   TINYINT),
        ("smallint",  sqltypes.SMALLINT),
        ("int",       sqltypes.INTEGER),
        ("bigint",    sqltypes.BIGINT),
        ("largeint",  LARGEINT),
        ("float",     sqltypes.FLOAT),
        ("double",    DOUBLE),
        ("date",      sqltypes.DATE),
        ("datetime",  sqltypes.DATETIME),
        ("time",      TIME),
        ("text",      sqltypes.TEXT),
        ("json",      sqltypes.JSON),
        ("ipv4",      IPV4),
        ("ipv6",      IPV6),
        ("variant",   VARIANT),
        ("hll",       HLL),
        ("bitmap",    BITMAP),
        ("quantile_state", QUANTILE_STATE),
        ("agg_state", AGG_STATE),
    ])
    def test_basic_type(self, type_str, expected_cls):
        result = parse_sqltype(type_str)
        assert isinstance(result, expected_cls)

    # Doris-specific aliases that might appear in older schemas
    @pytest.mark.parametrize("type_str, expected_cls", [
        ("integer",    sqltypes.INTEGER),
        ("datev1",     sqltypes.DATE),
        ("datev2",     sqltypes.DATE),
        ("datetimev1", sqltypes.DATETIME),
        ("datetimev2", sqltypes.DATETIME),
        ("decimalv2",  sqltypes.DECIMAL),
        ("decimalv3",  sqltypes.DECIMAL),
        ("jsonb",      sqltypes.JSON),
        ("string",     sqltypes.String),
    ])
    def test_alias_type(self, type_str, expected_cls):
        result = parse_sqltype(type_str)
        assert isinstance(result, expected_cls)

    def test_case_insensitive(self):
        assert isinstance(parse_sqltype("VARCHAR"), sqltypes.VARCHAR)
        assert isinstance(parse_sqltype("Int"), sqltypes.INTEGER)
        assert isinstance(parse_sqltype("BOOLEAN"), sqltypes.BOOLEAN)

    def test_leading_trailing_spaces(self):
        assert isinstance(parse_sqltype("  bigint  "), sqltypes.BIGINT)


# ───────────────────────────────────────────────────────────────────────────
# parse_sqltype — parameterised types
# Doris SHOW COLUMNS returns: varchar(255), char(50), decimal(18,6), datetime(3)
# ───────────────────────────────────────────────────────────────────────────
class TestParseSqlTypeWithParams:

    def test_varchar_length(self):
        t = parse_sqltype("varchar(255)")
        assert isinstance(t, sqltypes.VARCHAR)
        assert t.length == 255

    def test_varchar_max(self):
        t = parse_sqltype("varchar(65533)")
        assert t.length == 65533

    def test_char_length(self):
        t = parse_sqltype("char(50)")
        assert isinstance(t, sqltypes.CHAR)
        assert t.length == 50

    def test_char_one(self):
        t = parse_sqltype("char(1)")
        assert t.length == 1

    def test_string_length(self):
        t = parse_sqltype("string(65535)")
        assert isinstance(t, sqltypes.String)
        assert t.length == 65535

    def test_decimal_precision_and_scale(self):
        """Doris reports DECIMALV3(18,6) as decimal(18,6)."""
        t = parse_sqltype("decimal(18,6)")
        assert isinstance(t, sqltypes.DECIMAL)
        assert t.precision == 18
        assert t.scale == 6

    def test_decimal_default_params(self):
        """DECIMALV3 without params defaults to decimal(38,9) in SHOW COLUMNS."""
        t = parse_sqltype("decimal(38,9)")
        assert t.precision == 38
        assert t.scale == 9

    def test_decimal_precision_only(self):
        t = parse_sqltype("decimal(10)")
        assert t.precision == 10
        assert t.scale == 0

    def test_decimalv3_params(self):
        t = parse_sqltype("decimalv3(27,9)")
        assert t.precision == 27
        assert t.scale == 9

    def test_decimalv2_params(self):
        t = parse_sqltype("decimalv2(10,2)")
        assert t.precision == 10
        assert t.scale == 2

    def test_datetime_precision_ignored(self):
        """datetime(3) — precision parsed but DATETIME type doesn't store it."""
        t = parse_sqltype("datetime(3)")
        assert isinstance(t, sqltypes.DATETIME)

    def test_datetime_no_precision(self):
        t = parse_sqltype("datetime")
        assert isinstance(t, sqltypes.DATETIME)


# ───────────────────────────────────────────────────────────────────────────
# parse_sqltype — complex / structural types with angle brackets
# Doris returns: array<int>, map<text,int>, struct<name:text,age:int>
# ───────────────────────────────────────────────────────────────────────────
class TestParseSqlTypeComplexTypes:

    def test_array_with_subtype(self):
        """array<int> — our regex captures 'array' as type, '<int>' is not in parens."""
        t = parse_sqltype("array<int>")
        assert isinstance(t, ARRAY)

    def test_map_with_subtypes(self):
        t = parse_sqltype("map<text,int>")
        assert isinstance(t, MAP)

    def test_struct_with_fields(self):
        t = parse_sqltype("struct<name:text,age:int>")
        assert isinstance(t, STRUCT)


# ───────────────────────────────────────────────────────────────────────────
# parse_sqltype — unknown / invalid input
# ───────────────────────────────────────────────────────────────────────────
class TestParseSqlTypeEdgeCases:

    def test_unknown_type_returns_nulltype(self):
        t = parse_sqltype("some_future_type")
        assert t is sqltypes.NULLTYPE

    def test_empty_string_returns_nulltype(self):
        t = parse_sqltype("")
        assert t is sqltypes.NULLTYPE

    def test_garbage_returns_nulltype(self):
        t = parse_sqltype("!@#$%")
        assert t is sqltypes.NULLTYPE


# ───────────────────────────────────────────────────────────────────────────
# Custom type python_type property
# ───────────────────────────────────────────────────────────────────────────
class TestCustomTypePythonType:

    def test_array_python_type(self):
        assert ARRAY().python_type is list

    def test_map_python_type(self):
        assert MAP().python_type is dict

    def test_struct_python_type(self):
        assert STRUCT().python_type is None

    def test_ipv4_python_type(self):
        assert IPV4().python_type is str

    def test_ipv6_python_type(self):
        assert IPV6().python_type is str

    def test_time_python_type(self):
        assert TIME().python_type is datetime.timedelta

    def test_variant_python_type(self):
        assert VARIANT().python_type is dict
