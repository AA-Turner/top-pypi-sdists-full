"""Skill loader from .emdash/skills/*/SKILL.md files.

Skills are markdown-based instruction files that teach the agent how to
perform specific, repeatable tasks. They can be automatically applied
when relevant or explicitly invoked via /skill_name.

Similar to Claude Code's skills system:
https://docs.anthropic.com/en/docs/claude-code/skills

Skills are loaded from three locations (in order, later overrides earlier):
1. Built-in skills bundled with emdash_core (always available)
2. Global skills in ~/.emdash/skills/ (user's home directory)
3. Repo-local skills in .emdash/skills/ (can override global and built-in)
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import os
import stat

from ..utils.logger import log


def _get_builtin_skills_dir() -> Path:
    """Get the directory containing built-in skills bundled with emdash_core."""
    return Path(__file__).parent.parent / "skills"


def _get_global_skills_dir() -> Path:
    """Get the global skills directory in user's home (~/.emdash/skills/)."""
    return Path.home() / ".emdash" / "skills"


def _discover_scripts(skill_dir: Path) -> list[Path]:
    """Discover executable scripts in a skill directory.

    Scripts are self-contained bash executables that can be run by the agent
    to perform specific actions. They must be either:
    - Files with .sh extension
    - Files with executable permission and a shebang (#!/bin/bash, #!/usr/bin/env bash, etc.)

    Args:
        skill_dir: Path to the skill directory

    Returns:
        List of paths to executable scripts
    """
    scripts = []

    if not skill_dir.exists() or not skill_dir.is_dir():
        return scripts

    # Files to skip (not scripts)
    skip_files = {"SKILL.md", "skill.md", "README.md", "readme.md"}

    for file_path in skill_dir.iterdir():
        if not file_path.is_file():
            continue

        if file_path.name in skip_files:
            continue

        # Check if it's a .sh file
        is_shell_script = file_path.suffix == ".sh"

        # Check if it has a shebang
        has_shebang = False
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                first_line = f.readline().strip()
                if first_line.startswith("#!"):
                    # Check for bash/sh shebang
                    if any(shell in first_line for shell in ["bash", "/sh", "python", "node", "ruby", "perl"]):
                        has_shebang = True
        except (OSError, IOError):
            continue

        if is_shell_script or has_shebang:
            # Ensure the file is executable
            try:
                current_mode = file_path.stat().st_mode
                if not (current_mode & stat.S_IXUSR):
                    # Make it executable for the user
                    os.chmod(file_path, current_mode | stat.S_IXUSR)
                    log.debug(f"Made script executable: {file_path}")
            except OSError as e:
                log.warning(f"Could not make script executable: {file_path}: {e}")

            scripts.append(file_path)

    return sorted(scripts, key=lambda p: p.name)


@dataclass
class Skill:
    """A skill configuration loaded from SKILL.md.

    Attributes:
        name: Unique skill identifier (from directory name or frontmatter)
        description: Brief description of when to use this skill
        instructions: The main prompt/instructions content
        tools: List of tools this skill needs access to
        user_invocable: Whether skill can be invoked with /name
        file_path: Source file path
        scripts: List of executable script paths in the skill directory
        _builtin: Whether this is a built-in skill bundled with emdash_core
        _global: Whether this is a global skill from ~/.emdash/skills/
    """

    name: str
    description: str = ""
    instructions: str = ""
    tools: list[str] = field(default_factory=list)
    user_invocable: bool = False
    file_path: Optional[Path] = None
    scripts: list[Path] = field(default_factory=list)
    _builtin: bool = False
    _global: bool = False


class SkillRegistry:
    """Registry for managing loaded skills.

    Singleton that maintains the list of available skills
    and provides lookup functionality.
    """

    _instance: Optional["SkillRegistry"] = None
    _skills: dict[str, Skill]
    _skills_dir: Optional[Path]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._skills = {}
            cls._instance._skills_dir = None
        return cls._instance

    @classmethod
    def get_instance(cls) -> "SkillRegistry":
        """Get the singleton instance."""
        return cls()

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance."""
        if cls._instance is not None:
            cls._instance._skills = {}
            cls._instance._skills_dir = None

    def load_skills(self, skills_dir: Optional[Path] = None) -> dict[str, Skill]:
        """Load skills from built-in, global, and user repo directories.

        Skills are loaded from three locations (in order, later overrides earlier):
        1. Built-in skills bundled with emdash_core (always available)
        2. Global skills in ~/.emdash/skills/ (user's home directory)
        3. Repo-local skills in .emdash/skills/ (can override global and built-in)

        Each skill is a directory containing a SKILL.md file:

        ```
        .emdash/skills/
        ├── commit/
        │   └── SKILL.md
        └── review-pr/
            └── SKILL.md
        ```

        SKILL.md format:
        ```markdown
        ---
        name: commit
        description: Generate commit messages following conventions
        user_invocable: true
        tools: [execute_command, read_file]
        ---

        # Commit Message Generation

        Instructions for the skill...
        ```

        Args:
            skills_dir: Directory containing user skill subdirectories.
                       Defaults to .emdash/skills/ in cwd.

        Returns:
            Dict mapping skill name to Skill
        """
        if skills_dir is None:
            skills_dir = Path.cwd() / ".emdash" / "skills"

        self._skills_dir = skills_dir

        skills = {}

        # First, load built-in skills bundled with emdash_core
        builtin_dir = _get_builtin_skills_dir()
        if builtin_dir.exists():
            builtin_skills = self._load_skills_from_dir(builtin_dir, source="built-in")
            skills.update(builtin_skills)

        # Second, load global skills from ~/.emdash/skills/
        global_dir = _get_global_skills_dir()
        if global_dir.exists():
            global_skills = self._load_skills_from_dir(global_dir, source="global")
            skills.update(global_skills)

        # Finally, load repo-local skills (can override global and built-in)
        if skills_dir.exists():
            user_skills = self._load_skills_from_dir(skills_dir, source="local")
            skills.update(user_skills)

        if skills:
            builtin_count = len([s for s in self._skills.values() if getattr(s, "_builtin", False)])
            global_count = len([s for s in self._skills.values() if getattr(s, "_global", False)])
            local_count = len(skills) - builtin_count - global_count
            log.info(
                f"Loaded {len(skills)} skills "
                f"({builtin_count} built-in, {global_count} global, {local_count} local)"
            )

        return skills

    def _load_skills_from_dir(
        self, skills_dir: Path, source: str = "local"
    ) -> dict[str, Skill]:
        """Load skills from a specific directory.

        Args:
            skills_dir: Directory containing skill subdirectories
            source: Source type - "built-in", "global", or "local"

        Returns:
            Dict mapping skill name to Skill
        """
        skills = {}

        # Look for SKILL.md in subdirectories
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                # Also try lowercase
                skill_file = skill_dir / "skill.md"
                if not skill_file.exists():
                    continue

            try:
                skill = _parse_skill_file(skill_file, skill_dir.name)
                if skill:
                    # Mark source type
                    skill._builtin = source == "built-in"
                    skill._global = source == "global"
                    # Discover scripts in the skill directory
                    skill.scripts = _discover_scripts(skill_dir)
                    if skill.scripts:
                        log.debug(f"Found {len(skill.scripts)} scripts in skill: {skill.name}")
                    skills[skill.name] = skill
                    self._skills[skill.name] = skill
                    log.debug(f"Loaded {source} skill: {skill.name}")
            except Exception as e:
                log.warning(f"Failed to load skill from {skill_file}: {e}")

        return skills

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a specific skill by name.

        Args:
            name: Skill name

        Returns:
            Skill or None if not found
        """
        return self._skills.get(name)

    def list_skills(self) -> list[str]:
        """List available skill names.

        Returns:
            List of skill names
        """
        return list(self._skills.keys())

    def get_all_skills(self) -> dict[str, Skill]:
        """Get all loaded skills.

        Returns:
            Dict mapping skill name to Skill
        """
        return self._skills.copy()

    def get_user_invocable_skills(self) -> list[Skill]:
        """Get skills that can be invoked with /name.

        Returns:
            List of user-invocable skills
        """
        return [s for s in self._skills.values() if s.user_invocable]

    def get_skills_for_prompt(self) -> str:
        """Generate skills section for system prompt.

        Returns:
            Formatted string describing available skills
        """
        if not self._skills:
            return ""

        lines = ["## Available Skills\n"]
        lines.append("The following skills are available. Use them when the task matches their description:\n")

        for skill in self._skills.values():
            invocable = " (user-invocable: /{})".format(skill.name) if skill.user_invocable else ""
            scripts_note = f" [has {len(skill.scripts)} script(s)]" if skill.scripts else ""
            lines.append(f"- **{skill.name}**: {skill.description}{invocable}{scripts_note}")

        lines.append("")
        lines.append("To activate a skill, use the `skill` tool with the skill name.")
        lines.append("")

        # Add note about skill scripts if any skill has scripts
        has_scripts = any(skill.scripts for skill in self._skills.values())
        if has_scripts:
            lines.append("### Skill Scripts")
            lines.append("")
            lines.append("Some skills include executable scripts that can be run using the Bash tool.")
            lines.append("When you invoke a skill with scripts, the script paths will be provided.")
            lines.append("Scripts are self-contained and can be executed directly.")
            lines.append("")

        return "\n".join(lines)


def _parse_skill_file(file_path: Path, default_name: str) -> Optional[Skill]:
    """Parse a single SKILL.md file.

    Args:
        file_path: Path to the SKILL.md file
        default_name: Default name from directory (used if not in frontmatter)

    Returns:
        Skill or None if parsing fails
    """
    content = file_path.read_text()

    # Extract frontmatter
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = _parse_frontmatter(parts[1])
            body = parts[2].strip()

    # Get name from frontmatter or use directory name
    name = frontmatter.get("name", default_name)

    # Validate name format (lowercase, hyphens, max 64 chars)
    if len(name) > 64:
        log.warning(f"Skill name '{name}' exceeds 64 characters, truncating")
        name = name[:64]

    return Skill(
        name=name,
        description=frontmatter.get("description", ""),
        instructions=body,
        tools=frontmatter.get("tools", []),
        user_invocable=frontmatter.get("user_invocable", False),
        file_path=file_path,
    )


def _parse_frontmatter(frontmatter_str: str) -> dict:
    """Parse YAML-like frontmatter.

    Simple parser for key: value pairs.

    Args:
        frontmatter_str: Frontmatter string

    Returns:
        Dict of parsed values
    """
    result = {}

    for line in frontmatter_str.strip().split("\n"):
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Parse boolean values
        if value.lower() == "true":
            result[key] = True
        elif value.lower() == "false":
            result[key] = False
        # Parse list values
        elif value.startswith("[") and value.endswith("]"):
            items = value[1:-1].split(",")
            result[key] = [item.strip().strip("'\"") for item in items if item.strip()]
        else:
            result[key] = value.strip("'\"")

    return result


# Convenience functions


def load_skills(skills_dir: Optional[Path] = None) -> dict[str, Skill]:
    """Load skills from directory.

    Args:
        skills_dir: Optional skills directory

    Returns:
        Dict mapping skill name to Skill
    """
    registry = SkillRegistry.get_instance()
    return registry.load_skills(skills_dir)


def get_skill(name: str) -> Optional[Skill]:
    """Get a specific skill by name.

    Args:
        name: Skill name

    Returns:
        Skill or None if not found
    """
    registry = SkillRegistry.get_instance()
    return registry.get_skill(name)


def list_skills() -> list[str]:
    """List available skill names.

    Returns:
        List of skill names
    """
    registry = SkillRegistry.get_instance()
    return registry.list_skills()


def get_user_invocable_skills() -> list[Skill]:
    """Get skills that can be invoked with /name.

    Returns:
        List of user-invocable skills
    """
    registry = SkillRegistry.get_instance()
    return registry.get_user_invocable_skills()
