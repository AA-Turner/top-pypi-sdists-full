"""System-prompt rendering helpers for SDK agents."""

from html import escape as html_escape

from mistralai.vibe.sdk.agent.skills import SkillDefinition


def render_system_prompt(
    *,
    system_prompt: str | None,
    skills: list[SkillDefinition],
) -> str | None:
    """Append a discoverable skill summary without exposing full skill bodies."""
    sections = []

    if system_prompt:
        sections.append(system_prompt)
    if skills:
        sections.append(render_available_skills_section(skills))
    if not sections:
        return None

    return "\n\n".join(sections)


def render_available_skills_section(skills: list[SkillDefinition]) -> str:
    if not skills:
        return ""

    entries: list[str] = []
    for skill in skills:
        entries.extend(
            [
                "  <skill>",
                f"    <name>{html_escape(skill.name)}</name>",
                f"    <description>{html_escape(skill.description)}</description>",
                "  </skill>",
            ]
        )

    return "\n".join(
        [
            "## Available Skills",
            "",
            "Skills are reusable instructions for specialized tasks. When a user request"
            " matches a skill's description, use the `skill` tool with the exact skill"
            " name to load the full skill instructions.",
            "",
            "You have access to the following skills:",
            "",
            "<available_skills>",
            *entries,
            "</available_skills>",
        ]
    )
