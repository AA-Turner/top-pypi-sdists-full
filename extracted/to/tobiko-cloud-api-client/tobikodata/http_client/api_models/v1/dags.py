import typing as t
from datetime import datetime
from enum import Enum

from pydantic import ConfigDict, HttpUrl

from tobikodata.pydantic import ForwardCompatiblePydanticModel


class V1DagNodeType(str, Enum):
    MODEL = "model"
    AUDIT = "audit"


class V1DagNodeSourceType(str, Enum):
    SQL = "sql"
    SEED = "seed"
    PYTHON = "python"
    EXTERNAL = "external"
    AUDIT = "audit"


class V1DagNode(ForwardCompatiblePydanticModel):
    # Prevents warning about property starting with model_
    model_config = ConfigDict(
        protected_namespaces=(),
    )

    name: str
    model_name: str
    description: t.Optional[str]
    source_type: V1DagNodeSourceType
    tags: t.List[str]
    parent_names: t.List[str]
    audit_names: t.List[str]
    type: V1DagNodeType
    link: HttpUrl


class V1Dag(ForwardCompatiblePydanticModel):
    environment: str
    start_at: datetime
    schedule_seconds: int
    schedule_cron: str
    nodes: t.List[V1DagNode]
    link: HttpUrl
