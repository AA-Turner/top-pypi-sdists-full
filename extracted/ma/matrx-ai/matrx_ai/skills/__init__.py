"""Agent skills — markdown-backed capability library, mirrored against the
canonical skill tools (``skill_list``, ``skill_get``, ``skill_search``).

Public API:
    - ``SkillProvider`` — protocol; ``DbSkillProvider`` is the canonical impl
    - ``SkillHint`` / ``SkillBody`` / ``SkillConfig`` / ``ResolvedSkills``
    - ``resolve_skills_for_agent`` — request-time resolver
    - ``render_preamble`` — system-prompt segment generator
    - ``validate_allowed_tools_on_startup`` — SK-R15 startup gate

See ``packages/matrx-ai/matrx_ai/skills/MODULE_README.md`` for the design
brief and ``/root/.claude/plans/that-is-really-good-snuggly-teapot.md`` for
the implementation plan.
"""
from matrx_ai.skills.ingest import (
    discover_skill_roots,
    ingest_filesystem,
    walk_filesystem,
    walk_paths,
    walk_via_proxy,
)
from matrx_ai.skills.models import (
    ResolvedSkills,
    SkillBody,
    SkillConfig,
    SkillHint,
    SkillPreamble,
    SkillTier,
)
from matrx_ai.skills.preamble import render_preamble
from matrx_ai.skills.providers import (
    DbSkillProvider,
    SkillProvider,
    invalidate_skill_catalog_cache,
    preload_skill_catalog,
)
from matrx_ai.skills.resolver import resolve_skills_for_agent
from matrx_ai.skills.startup_check import validate_allowed_tools_on_startup

__all__ = [
    "DbSkillProvider",
    "ResolvedSkills",
    "SkillBody",
    "SkillConfig",
    "SkillHint",
    "SkillPreamble",
    "SkillProvider",
    "SkillTier",
    "discover_skill_roots",
    "ingest_filesystem",
    "invalidate_skill_catalog_cache",
    "preload_skill_catalog",
    "render_preamble",
    "resolve_skills_for_agent",
    "validate_allowed_tools_on_startup",
    "walk_filesystem",
    "walk_paths",
    "walk_via_proxy",
]
