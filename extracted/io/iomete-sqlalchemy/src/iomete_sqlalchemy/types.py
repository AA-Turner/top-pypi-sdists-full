"""
Mapping from Spark/Iceberg type strings to SQLAlchemy types.
"""

import re

from sqlalchemy import types as sqltypes

# Spark/Iceberg types that map directly to a SQLAlchemy type with no arguments.
# Spark often has multiple aliases for the same type (e.g. "int" / "integer",
# "bigint" / "long"), so all aliases are listed here.
_KEYWORD_TYPE_MAP: dict[str, sqltypes.TypeEngine] = {
    # booleans
    "boolean": sqltypes.Boolean(),
    "bool": sqltypes.Boolean(),
    # integers
    "tinyint": sqltypes.SmallInteger(),
    "byte": sqltypes.SmallInteger(),
    "smallint": sqltypes.SmallInteger(),
    "short": sqltypes.SmallInteger(),
    "int": sqltypes.Integer(),
    "integer": sqltypes.Integer(),
    "bigint": sqltypes.BigInteger(),
    "long": sqltypes.BigInteger(),
    # floating-point
    "float": sqltypes.Float(precision=24),
    "real": sqltypes.Float(precision=24),
    "double": sqltypes.Float(precision=53),
    "double precision": sqltypes.Float(precision=53),
    # strings / binary
    "string": sqltypes.Text(),
    "text": sqltypes.Text(),
    "binary": sqltypes.LargeBinary(),
    "bytes": sqltypes.LargeBinary(),
    # date / time
    "date": sqltypes.Date(),
    "timestamp": sqltypes.DateTime(),
    "timestamp_ntz": sqltypes.DateTime(),
    "interval": sqltypes.Interval(),
    # misc
    "void": sqltypes.NullType(),
    "null": sqltypes.NullType(),
}

# Matches decimal(precision, scale)  e.g. "decimal(10, 2)"
_DECIMAL_WITH_SCALE    = re.compile(r"decimal\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)")

# Matches decimal(precision) only    e.g. "decimal(10)"
_DECIMAL_PRECISION_ONLY = re.compile(r"decimal\s*\(\s*(\d+)\s*\)")

# Matches char(length)    e.g. "char(64)"
_CHAR_WITH_LENGTH    = re.compile(r"char\s*\(\s*(\d+)\s*\)")

# Matches varchar(length) e.g. "varchar(255)"
_VARCHAR_WITH_LENGTH = re.compile(r"varchar\s*\(\s*(\d+)\s*\)")

# Spark complex type prefixes — no SQLAlchemy equivalent, mapped to JSON
_COMPLEX_TYPE_PREFIXES = ("array<", "map<", "struct<")

def spark_type_to_sqla(type_str: str) -> sqltypes.TypeEngine:
    """
    Convert a Spark/Iceberg type string (Spark → SQLAlchemy direction).

    Called during reflection: ``DESCRIBE TABLE`` returns a type string such as
    ``"decimal(10, 2)"`` or ``"array<string>"``; this function maps it to the
    corresponding SQLAlchemy ``TypeEngine`` instance.

    Handles parameterised forms such as:
      - decimal(10, 2)
      - char(64)
      - varchar(255)
      - array<string>
      - map<string, int>
      - struct<field:type, …>
    """
    if not type_str:
        return sqltypes.NullType()

    normalized = type_str.strip().lower()

    # ── decimal(precision, scale) ──────────────────────────────────────────
    match = _DECIMAL_WITH_SCALE.fullmatch(normalized)
    if match:
        precision, scale = int(match.group(1)), int(match.group(2))
        return sqltypes.Numeric(precision=precision, scale=scale)

    match = _DECIMAL_PRECISION_ONLY.fullmatch(normalized)
    if match:
        return sqltypes.Numeric(precision=int(match.group(1)))

    if normalized in ("decimal", "numeric"):
        return sqltypes.Numeric()

    # ── char(length) / varchar(length) ────────────────────────────────────
    match = _CHAR_WITH_LENGTH.fullmatch(normalized)
    if match:
        return sqltypes.CHAR(length=int(match.group(1)))

    match = _VARCHAR_WITH_LENGTH.fullmatch(normalized)
    if match:
        return sqltypes.VARCHAR(length=int(match.group(1)))

    if normalized in ("char", "varchar", "character varying"):
        return sqltypes.Text()

    # ── complex types: array<…>, map<…>, struct<…> ────────────────────────
    # SQLAlchemy has no native equivalent; JSON is the closest approximation
    # for schema reflection and metadata tooling.
    if normalized.startswith(_COMPLEX_TYPE_PREFIXES):
        return sqltypes.JSON()

    # ── plain keyword lookup ───────────────────────────────────────────────
    if normalized in _KEYWORD_TYPE_MAP:
        return _KEYWORD_TYPE_MAP[normalized]

    # ── unknown type → Text so reflection never crashes ───────────────────
    return sqltypes.Text()