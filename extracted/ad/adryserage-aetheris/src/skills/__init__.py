"""
Skills Module for Aetheris (v3.0)

Provides AI agent skills for:
- File operations (read, write, search)
- Shell command execution
- Provider-specific adapters (Claude Tool Use, Gemini Function Calling)
- Custom skill registry
"""

from src.skills.base_skill import (
    Skill,
    SkillCall,
    SkillParameter,
    SkillResult,
    SkillResultStatus,
)
from src.skills.file_skills import (
    ReadFileSkill,
    WriteFileSkill,
    SearchFilesSkill,
)
from src.skills.shell_skill import ExecuteCommandSkill
from src.skills.registry import SkillRegistry

__all__ = [
    # Base types
    "Skill",
    "SkillCall",
    "SkillParameter",
    "SkillResult",
    "SkillResultStatus",
    # Built-in skills
    "ReadFileSkill",
    "WriteFileSkill",
    "SearchFilesSkill",
    "ExecuteCommandSkill",
    # Registry
    "SkillRegistry",
]
