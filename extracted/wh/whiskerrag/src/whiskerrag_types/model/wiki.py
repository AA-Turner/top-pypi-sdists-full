from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import Field, HttpUrl

from whiskerrag_types.model.timeStampedModel import TimeStampedModel


class WikiType(Enum):
    TEXT = "text"
    URL = "url"


class Wiki(TimeStampedModel):
    type: WikiType
    content: Union[str, HttpUrl]
    tenant_id: str = Field(..., description="boned whisker tenant_id")
    space_id: Optional[str] = Field(..., description="boned whisker space id")
    knowledge_id: Optional[str] = Field(..., description="boned whisker knowledge id")

    def update(self, **kwargs: Dict[str, Any]) -> "Wiki":
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self
