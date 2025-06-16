from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class Resource(str, Enum):
    RETRIEVAL = "retrieval"
    TENANT = "tenant"
    SPACE = "space"
    KNOWLEDGE = "knowledge"
    CHUNK = "chunk"
    API_KEY = "api_key"
    TASK = "task"
    RULE = "rule"
    PUBLIC = "public"


class Action(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    ALL = "*"


class Permission(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    resource: Resource
    actions: List[Action]
    conditions: Optional[Dict[str, Any]] = None
