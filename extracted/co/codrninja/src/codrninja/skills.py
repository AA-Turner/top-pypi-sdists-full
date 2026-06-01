"""Skills system for codrninja — extensible abilities loaded from disk."""

import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .tools import ToolRegistry


SKILLS_DIR = Path.home() / ".codrninja" / "skills"


@dataclass
class Skill:
    """A single skill loaded from a SKILL.md."""
    name: str
    path: Path
    description: str = ""
    tools: List[str] = field(default_factory=list)
    prompts: List[str] = field(default_factory=list)
    system_prompt: str = ""
    raw_markdown: str = ""
    source: str = "user"   # "user" | "project"


class SkillRegistry:
    """Discovers and manages skills from ~/.codrninja/skills/ and .codrninja/skills/."""

    def __init__(self, skills_dir: Optional[Path] = None):
        self.skills_dir = skills_dir or SKILLS_DIR
        self.skills: Dict[str, Skill] = {}

    def discover(self) -> List[Skill]:
        """Scan user-global and project-local skills directories."""
        self.skills.clear()

        # 1. User-global skills (~/.codrninja/skills/)
        self._scan_dir(self.skills_dir, source="user")

        # 2. Project-local skills (.codrninja/skills/) — override user skills with same name
        project_skills_dir = Path(os.getcwd()) / ".codrninja" / "skills"
        self._scan_dir(project_skills_dir, source="project")

        return list(self.skills.values())

    def _scan_dir(self, skills_dir: Path, source: str) -> None:
        if not skills_dir.exists():
            return
        for entry in sorted(skills_dir.iterdir()):
            if entry.is_dir() and (entry / "SKILL.md").exists():
                skill = self._load_skill(entry, source=source)
                if skill:
                    self.skills[skill.name] = skill

    def _load_skill(self, path: Path, source: str = "user") -> Optional[Skill]:
        """Parse a skill directory into a Skill object."""
        skill_md = path / "SKILL.md"
        if not skill_md.exists():
            return None

        raw = skill_md.read_text(encoding="utf-8")
        name = path.name
        description = ""
        tools = []
        prompts = []
        system_prompt = ""

        # Simple markdown parsing — extract sections
        current_section = ""
        for line in raw.splitlines():
            if line.startswith("# "):
                continue  # title
            elif line.startswith("## "):
                current_section = line[3:].strip().lower()
                continue
            elif line.strip() == "":
                continue

            if current_section == "description":
                description += line.strip() + " "
            elif current_section in ("tools", "available tools"):
                tools.append(line.strip().lstrip("- ").strip())
            elif current_section in ("prompts", "system prompt"):
                prompts.append(line.strip())
            elif current_section == "system prompt":
                system_prompt += line + "\n"

        return Skill(
            name=name,
            path=path,
            description=description.strip(),
            tools=tools,
            prompts=prompts,
            system_prompt=system_prompt.strip(),
            raw_markdown=raw,
            source=source,
        )

    def add_skill(self, source_path: str) -> Optional[Skill]:
        """Copy a skill directory into the skills folder."""
        source = Path(source_path).resolve()
        if not source.exists() or not source.is_dir():
            return None
        if not (source / "SKILL.md").exists():
            return None

        dest = self.skills_dir / source.name
        self.skills_dir.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(str(source), str(dest))

        skill = self._load_skill(dest)
        if skill:
            self.skills[skill.name] = skill
        return skill

    def register_tools(self, tool_registry: ToolRegistry):
        """Register skill-provided tools with the tool registry."""
        # Skills declare which built-in tools they need; they can also
        # provide executable scripts that get wrapped as tools.
        for skill in self.skills.values():
            scripts_dir = skill.path / "scripts"
            if scripts_dir.exists():
                for script in scripts_dir.iterdir():
                    if script.is_file() and os.access(str(script), os.X_OK):
                        tool_name = f"skill_{skill.name}_{script.stem}"
                        tool_registry.tools[tool_name] = _make_script_tool(script)

    def get_system_prompts(self) -> str:
        """Concatenate all skill system prompts."""
        parts = []
        for skill in self.skills.values():
            if skill.system_prompt:
                parts.append(f"[Skill: {skill.name}]\n{skill.system_prompt}")
            elif skill.description:
                parts.append(f"[Skill: {skill.name}] {skill.description}")
        return "\n\n".join(parts)

    def get_skill_instruction(self, name: str) -> Optional[str]:
        """Return the full SKILL.md content for a skill (for injection as agent instruction)."""
        skill = self.skills.get(name)
        return skill.raw_markdown if skill else None

    def list_skills(self) -> List[Dict]:
        """Return skill info as serializable dicts."""
        return [
            {
                "name": s.name,
                "description": s.description,
                "tools": s.tools,
                "path": str(s.path),
                "source": s.source,
            }
            for s in self.skills.values()
        ]


def _make_script_tool(script_path: Path):
    """Create a tool function that wraps an executable script."""
    import subprocess

    def script_tool(**kwargs) -> "ToolResult":
        from .tools import ToolResult
        try:
            args = [str(script_path)]
            for k, v in kwargs.items():
                args.extend([f"--{k}", str(v)])
            result = subprocess.run(
                args, capture_output=True, text=True, timeout=60
            )
            return ToolResult(
                result.returncode == 0,
                result.stdout or result.stderr,
                result.stderr if result.returncode != 0 else None,
            )
        except Exception as e:
            return ToolResult(False, "", str(e))

    script_tool.__name__ = script_path.stem
    return script_tool