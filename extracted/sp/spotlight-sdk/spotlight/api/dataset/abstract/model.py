from typing import Optional, List

from pydantic import Field as pyField

from spotlight.api.data.model import WhereClause, Sort
from spotlight.api.dataset.model import Field
from spotlight.core.common.base import Base


class AbstractDatasetRequest(Base):
    dataset_name: str
    display_name: str
    description: Optional[str]
    table_name: str
    where_clause: Optional[WhereClause]
    row_limit: int
    max_limit: int
    sort: Optional[List[Sort]] = pyField(default=None)
    tags: List[str]
    schema_: List[Field] = pyField(alias="schema")


class AbstractDatasetResponse(Base):
    id: str
    dataset_name: str
    display_name: str
    description: Optional[str]
    table_name: str
    where_clause: Optional[WhereClause]
    row_limit: int
    max_limit: int
    sort: Optional[List[Sort]] = pyField(default=None)
    tags: List[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
    schema_: List[Field] = pyField(alias="schema")
