# src/canonmap/connectors/mysql_connector/models.py

from typing import Any, List, Optional, TypedDict, Literal, Union
from enum import Enum

from pydantic import BaseModel


class DMLResult(TypedDict):
    affected_rows: int

class QueryRequest(BaseModel):
    query: str
    params: Optional[List[Any]] = None

class QueryResult(BaseModel):
    rows: Optional[List[dict]] = None
    affected_rows: Optional[int] = None

class TableField(BaseModel):
    table_name: str
    field_name: str


class FieldTransformType(str, Enum):
    INITIALISM = "initialism"
    PHONETIC = "phonetic"
    SOUNDEX = "soundex"


class IfExists(Enum):
    REPLACE = "replace"
    APPEND = "append"
    ERROR = "error"
    SKIP = "skip"
    FILL_EMPTY = "fill_empty"


class CreateHelperFieldRequest(BaseModel):
    table_field: TableField
    transform_type: FieldTransformType
    chunk_size: int = 10000
    if_helper_exists: IfExists = IfExists.ERROR


class TableFieldDict(TypedDict):
    """Dictionary form of a table/field reference.

    Example:
    {"table_name": "passing_table", "field_name": "player"}
    """

    table_name: str
    field_name: str


TableFieldInput = Union[TableFieldDict, str]


class CreateHelperFieldsPayload(TypedDict, total=False):
    """TypedDict describing the JSON/dict contract for create_helper_fields.

    - table_fields: list of table/field references. Each item can be one of:
        - TableFieldDict: {"table_name": str, "field_name": str}
        - str: "table.field" or "table:field"
    - all_transforms: when true, generate all helper types; otherwise require transform_type
    - transform_type: one of "initialism" | "phonetic" | "soundex"
    - if_helper_exists: one of "replace" | "append" | "error" | "skip" | "fill_empty"
    - chunk_size: positive integer for batch size
    - parallel: whether to process fields concurrently (bounded workers)
    """

    table_fields: List[TableFieldInput]
    all_transforms: bool
    transform_type: Literal["initialism", "phonetic", "soundex"]
    if_helper_exists: Literal["replace", "append", "error", "skip", "fill_empty"]
    chunk_size: int
    parallel: bool
