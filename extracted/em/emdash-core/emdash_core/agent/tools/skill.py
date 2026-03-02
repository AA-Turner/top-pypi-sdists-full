"""Skill invocation tool.

Allows the agent to activate and invoke skills during task execution.
Skills provide specialized instructions for repeatable tasks.
"""

from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ..skills import SkillRegistry, Skill


class SkillTool(BaseTool):
    """Tool for invoking skills.

    Skills are markdown-based instruction files that teach the agent
    how to perform specific, repeatable tasks. This tool allows
    explicit skill invocation.
    """

    name = "skill"
    description = """Invoke a skill for specialized task execution.

Skills provide focused instructions for common tasks like:
- commit: Generate commit messages following conventions
- review-pr: Review PRs with code standards
- security-review: Security-focused code review

When you invoke a skill, you receive its instructions which you should follow.
Use list_skills to see available skills."""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(
        self,
        skill: str,
        args: str = "",
        **kwargs,
    ) -> ToolResult:
        """Invoke a skill.

        Args:
            skill: Name of the skill to invoke
            args: Optional arguments to pass to the skill

        Returns:
            ToolResult with skill instructions
        """
        registry = SkillRegistry.get_instance()
        skill_obj = registry.get_skill(skill)

        if skill_obj is None:
            available = registry.list_skills()
            if available:
                return ToolResult.error_result(
                    f"Skill '{skill}' not found",
                    suggestions=[f"Available skills: {', '.join(available)}"],
                )
            else:
                return ToolResult.error_result(
                    f"Skill '{skill}' not found. No skills are currently loaded.",
                    suggestions=[
                        "Create skills in .emdash/skills/<skill-name>/SKILL.md",
                        "Skills are loaded from the .emdash/skills/ directory",
                    ],
                )

        # Build the skill activation response
        response_parts = [
            f"# Skill Activated: {skill_obj.name}",
            "",
            f"**Description**: {skill_obj.description}",
            "",
        ]

        if args:
            response_parts.extend([
                f"**Arguments**: {args}",
                "",
            ])

        if skill_obj.tools:
            response_parts.extend([
                f"**Required tools**: {', '.join(skill_obj.tools)}",
                "",
            ])

        # Include available scripts
        scripts_paths = []
        if skill_obj.scripts:
            response_parts.extend([
                "**Available Scripts**:",
                "",
            ])
            for script in skill_obj.scripts:
                script_path = str(script)
                scripts_paths.append(script_path)
                response_parts.append(f"- `{script_path}` - Run with: `bash {script_path}` or `./{script.name}` from skill directory")
            response_parts.extend([
                "",
                "*Scripts are self-contained executables. Run them using Bash tool when needed.*",
                "",
            ])

        response_parts.extend([
            "---",
            "",
            skill_obj.instructions,
        ])

        return ToolResult.success_result(
            data={
                "skill_name": skill_obj.name,
                "description": skill_obj.description,
                "instructions": skill_obj.instructions,
                "tools": skill_obj.tools,
                "scripts": scripts_paths,
                "args": args,
                "message": "\n".join(response_parts),
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        registry = SkillRegistry.get_instance()
        available_skills = registry.list_skills()

        description = self.description
        if available_skills:
            description += f"\n\nCurrently available skills: {', '.join(available_skills)}"

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill": {
                            "type": "string",
                            "description": "Name of the skill to invoke",
                        },
                        "args": {
                            "type": "string",
                            "description": "Optional arguments for the skill (e.g., PR number, file path)",
                        },
                    },
                    "required": ["skill"],
                },
            },
        }


class ListSkillsTool(BaseTool):
    """Tool for listing available skills."""

    name = "list_skills"
    description = "List all available skills and their descriptions."
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(self, **kwargs) -> ToolResult:
        """List available skills.

        Returns:
            ToolResult with list of skills
        """
        registry = SkillRegistry.get_instance()
        skills = registry.get_all_skills()

        if not skills:
            return ToolResult.success_result(
                data={
                    "skills": [],
                    "message": "No skills loaded. Create skills in .emdash/skills/<skill-name>/SKILL.md",
                },
            )

        skills_list = []
        for skill in skills.values():
            skills_list.append({
                "name": skill.name,
                "description": skill.description,
                "user_invocable": skill.user_invocable,
                "tools": skill.tools,
                "scripts": [str(s) for s in skill.scripts] if skill.scripts else [],
            })

        # Build human-readable message
        lines = ["# Available Skills", ""]
        for s in skills_list:
            invocable = f" (invoke with /{s['name']})" if s["user_invocable"] else ""
            scripts_note = f" [has {len(s['scripts'])} script(s)]" if s["scripts"] else ""
            lines.append(f"- **{s['name']}**: {s['description']}{invocable}{scripts_note}")

        return ToolResult.success_result(
            data={
                "skills": skills_list,
                "count": len(skills_list),
                "message": "\n".join(lines),
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(properties={}, required=[])
