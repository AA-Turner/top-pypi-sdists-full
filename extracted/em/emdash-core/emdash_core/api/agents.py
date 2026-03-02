"""Agent management endpoints."""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import get_config

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentInfo(BaseModel):
    """Agent information."""
    name: str
    path: str
    exists: bool


class AgentListResponse(BaseModel):
    """Response for listing agents."""
    agents: list[AgentInfo]


class CreateAgentRequest(BaseModel):
    """Request to create an agent."""
    name: str = Field(..., description="Agent name")
    description: Optional[str] = Field(default=None, description="Agent description")


class CreateAgentResponse(BaseModel):
    """Response from creating an agent."""
    success: bool
    name: str
    path: Optional[str] = None
    error: Optional[str] = None


def _get_agents_dir() -> Path:
    """Get the agents directory for the current repo."""
    config = get_config()
    if config.repo_root:
        return Path(config.repo_root) / ".emdash" / "agents"
    return Path.cwd() / ".emdash" / "agents"


@router.get("", response_model=AgentListResponse)
async def list_agents():
    """List all configured agents.

    Returns agents from the .emdash/agents directory.
    """
    agents_dir = _get_agents_dir()
    agents = []

    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            agents.append(AgentInfo(
                name=agent_file.stem,
                path=str(agent_file),
                exists=True,
            ))

    return AgentListResponse(agents=agents)


@router.post("", response_model=CreateAgentResponse)
async def create_agent(request: CreateAgentRequest):
    """Create a new agent configuration.

    Creates an agent markdown file in .emdash/agents/
    """
    agents_dir = _get_agents_dir()
    agents_dir.mkdir(parents=True, exist_ok=True)

    agent_file = agents_dir / f"{request.name}.md"

    if agent_file.exists():
        raise HTTPException(
            status_code=409,
            detail=f"Agent '{request.name}' already exists"
        )

    # Create agent template
    description = request.description or f"Custom agent: {request.name}"
    content = f"""# {request.name}

{description}

## Instructions

Define the agent's behavior and capabilities here.

## Tools

List the tools this agent can use:
- search
- read_file
- write_file

## Examples

Provide example interactions here.
"""

    try:
        agent_file.write_text(content)
        return CreateAgentResponse(
            success=True,
            name=request.name,
            path=str(agent_file),
        )
    except Exception as e:
        return CreateAgentResponse(
            success=False,
            name=request.name,
            error=str(e),
        )


@router.get("/{name}", response_model=AgentInfo)
async def get_agent(name: str):
    """Get a specific agent's information."""
    agents_dir = _get_agents_dir()
    agent_file = agents_dir / f"{name}.md"

    if not agent_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{name}' not found"
        )

    return AgentInfo(
        name=name,
        path=str(agent_file),
        exists=True,
    )


@router.get("/{name}/content")
async def get_agent_content(name: str):
    """Get an agent's file content."""
    agents_dir = _get_agents_dir()
    agent_file = agents_dir / f"{name}.md"

    if not agent_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{name}' not found"
        )

    return {"name": name, "content": agent_file.read_text()}


@router.delete("/{name}")
async def delete_agent(name: str):
    """Delete an agent configuration."""
    agents_dir = _get_agents_dir()
    agent_file = agents_dir / f"{name}.md"

    if not agent_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{name}' not found"
        )

    agent_file.unlink()
    return {"deleted": True, "name": name}
