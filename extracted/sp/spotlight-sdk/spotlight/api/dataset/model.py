from typing import Any, Dict, Optional, Union

from pydantic import Field

from spotlight.api.data.model import WhereClause
from spotlight.core.common.base import Base


class DatasetRequest(Base):
    display_name: str
    grid_state: Optional[Dict[str, Any]] = Field(default=None)
    where_clause: Optional[Union[WhereClause, dict]] = Field(default=None)


class DatasetUpdateRequest(Base):
    display_name: Optional[str] = Field(default=None)
    grid_state: Optional[Dict[str, Any]] = Field(default=None)
    where_clause: Optional[Union[WhereClause, dict]] = Field(default=None)


class DatasetResponse(Base):
    id: str
    display_name: str
    grid_state: Dict[str, Any]
    where_clause: Optional[Union[WhereClause, dict]] = Field(default=None)


class SearchRequest(Base):
    query: str
