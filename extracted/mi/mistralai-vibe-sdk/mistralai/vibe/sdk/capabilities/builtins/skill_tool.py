"""Builtin skill loader tool for SDK agents."""

from collections.abc import Mapping

from pydantic import BaseModel, Field, JsonValue

from mistralai.vibe.sdk.agent.skills import SkillDefinition
from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.adapters.local_function import ToolTaskConfig


class SkillToolContext(BaseModel):
    """Injected skill definitions keyed by skill name."""

    skills: dict[str, SkillDefinition]


class SkillArgs(BaseModel):
    """Input for the builtin skill loader."""

    name: str = Field(description="The exact name of the skill to load.")


class SkillResult(BaseModel):
    """Loaded skill content returned to the model."""

    name: str
    content: str
    description: str
    license: str | None = None
    compatibility: str | None = None
    allowed_tools: list[str] = Field(default_factory=list)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


def configured_skill_count(tasks: Mapping[str, object]) -> int:
    skill_task = tasks.get("skill")
    if not isinstance(skill_task, ToolTaskConfig) or not isinstance(skill_task.ctx, Mapping):
        return 0

    skills = skill_task.ctx.get("skills")
    if not isinstance(skills, Mapping):
        return 0
    return len(skills)


@tool(
    name="skill",
    description=(
        "Load a specialized skill that provides domain-specific instructions and"
        " workflows. When a task matches one of the available skills listed in"
        " your system prompt, call this tool with the exact skill name to load"
        " the full skill instructions."
    ),
    input_schema=SkillArgs,
    ctx_schema=SkillToolContext,
)
async def skill(ctx: SkillToolContext, args: SkillArgs) -> SkillResult:
    skill_def = ctx.skills.get(args.name)
    if skill_def is None:
        raise ValueError(f'Skill "{args.name}" not found.')

    content = "\n".join(
        [
            f'<skill_content name="{skill_def.name}">',
            f"# Skill: {skill_def.name}",
            "",
            skill_def.content.strip(),
            "",
            "</skill_content>",
        ]
    )

    return SkillResult(
        name=skill_def.name,
        content=content,
        description=skill_def.description,
        license=skill_def.license,
        compatibility=skill_def.compatibility,
        allowed_tools=skill_def.allowed_tools,
        metadata=skill_def.metadata,
    )
