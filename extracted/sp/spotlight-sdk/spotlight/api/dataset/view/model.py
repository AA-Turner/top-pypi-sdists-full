from typing import Optional, List

from pydantic import Field as pyField

from spotlight.api.data.model import WhereClause, Sort
from spotlight.api.dataset.model import Field
from spotlight.core.common.base import Base


class DatasetViewResponse(Base):
    id: str
    reference_name: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: List[str]
    where_clause: Optional[WhereClause]
    row_limit: int
    max_limit: int
    sort: Optional[List[Sort]] = pyField(default=None)
    abstract_dataset_id: str
    custom: bool
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
    schema_: List[Field] = pyField(alias="schema")
