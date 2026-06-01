from typing import List

from pydantic import BaseModel, Field


class NamespaceListResponse(BaseModel):
    namespaces: List[str] = Field(description="A list of workflow namespaces")


class NamespaceResponse(BaseModel):
    name: str
    workflow_execution_retention_ttl: int = Field(description="Workflow execution retention time (in seconds)")
