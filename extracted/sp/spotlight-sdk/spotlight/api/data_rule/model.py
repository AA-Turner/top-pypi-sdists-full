from datetime import datetime
from typing import Optional, Union

from pydantic import Field

from spotlight.api.data.model import WhereClause
from spotlight.core.common.base import Base
from spotlight.core.common.enum import RuleSeverity, RuleType, EventType


class DataRuleRequest(Base):
    display_name: str
    dataset_id: str
    severity: RuleSeverity
    type: RuleType
    predicate: Optional[Union[str, WhereClause]] = Field(default=None)


class DataRuleResponse(Base):
    id: str
    display_name: str
    dataset_id: str
    severity: RuleSeverity
    type: RuleType
    predicate: Optional[Union[str, WhereClause]] = Field(default=None)
    created_by: str
    created_at: datetime
    updated_by: Optional[str] = Field(default=None)
    updated_at: Optional[int] = Field(default=None)


class DataRuleEvent(Base):
    rule: DataRuleResponse
    type: EventType
