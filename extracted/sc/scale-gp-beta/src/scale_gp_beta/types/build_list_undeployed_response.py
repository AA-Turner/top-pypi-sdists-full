# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .._models import BaseModel
from .agentex_cloud_build import AgentexCloudBuild

__all__ = ["BuildListUndeployedResponse", "BuildListUndeployedResponseItem"]


class BuildListUndeployedResponseItem(BaseModel):
    """An agent that exists only as cloud builds — no healthy deployment yet."""

    agent_name: str
    """The agent name from cloud builds"""

    latest_build: AgentexCloudBuild
    """The most recent cloud build for this agent"""

    total_builds: int
    """Total number of builds for this agent"""


BuildListUndeployedResponse: TypeAlias = List[BuildListUndeployedResponseItem]
