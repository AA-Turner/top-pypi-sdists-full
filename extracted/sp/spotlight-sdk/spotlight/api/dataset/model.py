from typing import Optional, List

from pydantic import Field as pyField

from spotlight.api.data.model import WhereClause, Sort
from spotlight.core.common.base import Base
from spotlight.core.common.enum import FieldType


class Field(Base):
    display_name: str
    logical_name: str
    type: FieldType
    width: int
    editable: bool
    hidden: bool
    display_order: int
    tags: List[str]
    field_group_display_name: str
    field_group_logical_name: str


class DatasetRequest(Base):
    display_name: str
    description: Optional[str]
    filter_field: Optional[str]
    reference_name: Optional[str]
    tags: Optional[List[str]]
    where_clause: Optional[WhereClause]
    row_limit: Optional[int]
    max_limit: Optional[int]
    sort: Optional[List[Sort]] = pyField(default=None)
    schema_: Optional[List[Field]] = pyField(alias="schema")
    dataset_id: str
    custom: bool


class DatasetResponse(Base):
    id: str
    display_name: str
    description: Optional[str]
    filter_field: Optional[str]
    reference_name: Optional[str]
    tags: List[str]
    schema_: Optional[List[Field]] = pyField(alias="schema")
    where_clause: Optional[WhereClause]
    row_limit: Optional[int]
    max_limit: Optional[int]
    sort: Optional[List[Sort]] = pyField(default=None)
    abstract_dataset_id: str
    custom: bool
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class SearchRequest(Base):
    query: str
