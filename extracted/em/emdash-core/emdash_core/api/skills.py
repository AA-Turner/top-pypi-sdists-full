"""Skill management endpoints."""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import get_config

router = APIRouter(prefix="/skills", tags=["skills"])


class SkillInfo(BaseModel):
    """Skill information."""
    name: str
    description: str
    user_invocable: bool
    tools: list[str]
    path: str
    exists: bool


class SkillListResponse(BaseModel):
    """Response for listing skills."""
    skills: list[SkillInfo]
    count: int


class CreateSkillRequest(BaseModel):
    """Request to create a skill."""
    name: str = Field(..., description="Skill name (lowercase, hyphens allowed, max 64 chars)")
    description: str = Field(..., description="Brief description of when to use this skill")
    user_invocable: bool = Field(default=True, description="Whether skill can be invoked with /name")
    tools: list[str] = Field(default=[], description="List of tools this skill needs")
    instructions: str = Field(default="", description="Skill instructions/content")


class CreateSkillResponse(BaseModel):
    """Response from creating a skill."""
    success: bool
    name: str
    path: Optional[str] = None
    error: Optional[str] = None


class InvokeSkillRequest(BaseModel):
    """Request to invoke a skill."""
    args: str = Field(default="", description="Optional arguments for the skill")


class InvokeSkillResponse(BaseModel):
    """Response from invoking a skill."""
    skill_name: str
    description: str
    instructions: str
    tools: list[str]
    args: str


def _get_skills_dir() -> Path:
    """Get the skills directory for the current repo."""
    config = get_config()
    if config.repo_root:
        return Path(config.repo_root) / ".emdash" / "skills"
    return Path.cwd() / ".emdash" / "skills"


@router.get("", response_model=SkillListResponse)
async def list_skills():
    """List all configured skills.

    Returns skills from the .emdash/skills directory.
    """
    from ..agent.skills import SkillRegistry

    skills_dir = _get_skills_dir()
    registry = SkillRegistry.get_instance()

    # Reload skills to get latest
    registry.load_skills(skills_dir)

    skills = []
    for skill in registry.get_all_skills().values():
        skills.append(SkillInfo(
            name=skill.name,
            description=skill.description,
            user_invocable=skill.user_invocable,
            tools=skill.tools,
            path=str(skill.file_path) if skill.file_path else "",
            exists=True,
        ))

    return SkillListResponse(skills=skills, count=len(skills))


@router.post("", response_model=CreateSkillResponse)
async def create_skill(request: CreateSkillRequest):
    """Create a new skill.

    Creates a skill directory with SKILL.md in .emdash/skills/
    """
    # Validate name
    name = request.name.lower().strip()
    if len(name) > 64:
        raise HTTPException(
            status_code=400,
            detail="Skill name must be 64 characters or less"
        )

    if not name.replace("-", "").replace("_", "").isalnum():
        raise HTTPException(
            status_code=400,
            detail="Skill name must contain only lowercase letters, numbers, hyphens, and underscores"
        )

    skills_dir = _get_skills_dir()
    skill_dir = skills_dir / name
    skill_file = skill_dir / "SKILL.md"

    if skill_dir.exists():
        raise HTTPException(
            status_code=409,
            detail=f"Skill '{name}' already exists"
        )

    # Build frontmatter
    tools_str = ", ".join(request.tools) if request.tools else ""

    content = f"""---
name: {name}
description: {request.description}
user_invocable: {str(request.user_invocable).lower()}
tools: [{tools_str}]
---

# {name.replace('-', ' ').title()}

{request.instructions if request.instructions else f"Instructions for {name} skill."}

## Usage

Describe how this skill should be used.

## Examples

Provide example scenarios here.
"""

    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(content)
        return CreateSkillResponse(
            success=True,
            name=name,
            path=str(skill_file),
        )
    except Exception as e:
        return CreateSkillResponse(
            success=False,
            name=name,
            error=str(e),
        )


@router.get("/{name}", response_model=SkillInfo)
async def get_skill(name: str):
    """Get a specific skill's information."""
    from ..agent.skills import SkillRegistry

    skills_dir = _get_skills_dir()
    registry = SkillRegistry.get_instance()
    registry.load_skills(skills_dir)

    skill = registry.get_skill(name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{name}' not found"
        )

    return SkillInfo(
        name=skill.name,
        description=skill.description,
        user_invocable=skill.user_invocable,
        tools=skill.tools,
        path=str(skill.file_path) if skill.file_path else "",
        exists=True,
    )


@router.delete("/{name}")
async def delete_skill(name: str):
    """Delete a skill."""
    skills_dir = _get_skills_dir()
    skill_dir = skills_dir / name

    if not skill_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{name}' not found"
        )

    import shutil
    shutil.rmtree(skill_dir)

    # Reset registry to remove cached skill
    from ..agent.skills import SkillRegistry
    SkillRegistry.reset()

    return {"deleted": True, "name": name}


@router.post("/{name}/invoke", response_model=InvokeSkillResponse)
async def invoke_skill(name: str, request: InvokeSkillRequest):
    """Invoke a skill and get its instructions.

    Returns the skill's instructions for the agent to follow.
    """
    from ..agent.skills import SkillRegistry

    skills_dir = _get_skills_dir()
    registry = SkillRegistry.get_instance()
    registry.load_skills(skills_dir)

    skill = registry.get_skill(name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{name}' not found"
        )

    return InvokeSkillResponse(
        skill_name=skill.name,
        description=skill.description,
        instructions=skill.instructions,
        tools=skill.tools,
        args=request.args,
    )
