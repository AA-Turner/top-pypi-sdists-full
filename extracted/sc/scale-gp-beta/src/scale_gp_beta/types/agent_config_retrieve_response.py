# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .repo_spec import RepoSpec

__all__ = ["AgentConfigRetrieveResponse"]


class AgentConfigRetrieveResponse(BaseModel):
    id: str

    allowed_tools: List[str]

    created_at: datetime

    harness: str

    model: str

    name: str

    system_prompt: str

    updated_at: datetime

    description: Optional[str] = None

    object: Optional[Literal["agent_config"]] = None

    persistent_workspace: Optional[bool] = None

    repos: Optional[List[RepoSpec]] = None
