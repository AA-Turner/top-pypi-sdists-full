"""Skill system for custom CLI commands.

Skills are SKILL.md files with YAML frontmatter. The Markdown body is the
prompt; the frontmatter carries ``name`` and ``description``.

Canonical layout::

    .anteroom/skills/
      deploy-check/
        SKILL.md          # name + description in frontmatter, prompt in body

Example SKILL.md::

    ---
    name: deploy-check
    description: Verify the app is ready to deploy
    ---

    Check that all tests pass and lint is clean.
    Run: pytest tests/unit/ -v && ruff check src/
    Report any issues found.

Legacy ``.yaml`` / ``.yml`` skill files are also loaded for backward
compatibility during migration. New skills should use ``SKILL.md``.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..services.skill_bundles import (
    _extract_yaml_frontmatter,
    _inline_resources,
    _parse_resource_list_from_frontmatter,
    _resolve_bundle_resources,
)

logger = logging.getLogger(__name__)

_VALID_SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_VALID_TOOL_NAME = re.compile(r"^[a-zA-Z0-9_-]{1,128}$")
MAX_SKILLS = 100
_ARGS_PLACEHOLDER = "{args}"
MAX_PROMPT_SIZE = 50_000  # 50KB limit on skill prompts

# Built-in slash commands that skill names must not shadow.
# Derived from the shared command engine — adding a command to commands.py
# automatically prevents skill name collisions.  Uses a lazy import to
# avoid circular dependency (commands.py imports SkillRegistry from here).
_BUILTIN_COMMANDS_CACHE: frozenset[str] | None = None


def _get_builtin_commands() -> frozenset[str]:
    global _BUILTIN_COMMANDS_CACHE  # noqa: PLW0603
    if _BUILTIN_COMMANDS_CACHE is None:
        from anteroom.cli.commands import get_builtin_names

        _BUILTIN_COMMANDS_CACHE = get_builtin_names()
    return _BUILTIN_COMMANDS_CACHE


# Regex to match fenced code blocks (``` ... ```)
_CODE_FENCE_RE = re.compile(r"(```[\s\S]*?```)", re.MULTILINE)

# Frontmatter keys consumed by the parser — everything else is promoted to metadata
_CORE_FRONTMATTER_KEYS = frozenset(
    {
        "name",
        "description",
        "prompt",
        "allowed-tools",
        "allowed_tools",
        "denied-tools",
        "denied_tools",
        "resources",
    }
)

# Spec-compliance: names should use only lowercase alphanumeric + hyphens
_SPEC_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Resource directories recognized by the Agent Skills spec
_RESOURCE_DIRS = frozenset({"scripts", "references", "assets"})


@dataclass(frozen=True)
class SkillPolicy:
    """Per-skill tool allow/deny policy.

    Default (empty sets) = no restrictions (backward compatible).
    Deny wins over allow when a tool appears in both sets.
    """

    allowed_tools: frozenset[str] = frozenset()
    denied_tools: frozenset[str] = frozenset()
    origin_format: str = ""  # "anteroom", "claude", or "" (unknown)

    def check_tool(self, tool_name: str) -> tuple[bool, str]:
        """Return (allowed, reason). Deny wins over allow."""
        if self.denied_tools and tool_name in self.denied_tools:
            return False, f"Tool '{tool_name}' is denied by skill policy"
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return False, f"Tool '{tool_name}' is not in the allowed tools for this skill"
        return True, ""

    def summary(self) -> str:
        """Human-readable summary for /skills output."""
        parts: list[str] = []
        if self.allowed_tools:
            parts.append(f"allow={','.join(sorted(self.allowed_tools))}")
        if self.denied_tools:
            parts.append(f"deny={','.join(sorted(self.denied_tools))}")
        return "; ".join(parts)


@dataclass
class Skill:
    name: str
    description: str
    prompt: str
    source: str = ""  # "default", "global", or "project"
    namespace: str = ""  # pack namespace, empty for filesystem skills
    resource_count: int = 0  # number of bundled resources (0 = no bundle)
    policy: SkillPolicy = field(default_factory=SkillPolicy)
    metadata: dict[str, Any] = field(default_factory=dict)  # non-core frontmatter fields
    fqn: str = ""  # artifact FQN for pack-backed skills
    update_guidance: str = ""  # human/model-readable update path guidance


def _compute_update_guidance(
    source: str,
    name: str,
    *,
    path: str = "",
    namespace: str = "",
    pack_name: str = "",
    pack_source_path: str = "",
) -> str:
    """Return a one-sentence update guidance string for a skill.

    The guidance tells the agent and user what the correct action is when
    asked to update or edit this skill.
    """
    if source == "default":
        return f"Built-in skill — create a local override with /new-skill {name}."
    if source == "reference":
        return f"Reference skill at {path}. Edit directly." if path else "Reference skill. Edit the referenced path."
    if source.startswith("artifact:"):
        label = f"pack {namespace}" if namespace else "a pack"
        if pack_source_path:
            return (
                f"From {label}. Source at {pack_source_path}. "
                f"Edit and /pack update, or create a local override with /new-skill {name}."
            )
        return (
            f"From {label}. Create a local override with /new-skill {name} "
            f"(overrides take precedence), or edit the pack source and reinstall."
        )
    # Local filesystem skill (global, project, etc.)
    if path:
        return f"Local skill at {path}. Edit directly."
    return "Local skill. Edit the skill file directly."


@dataclass
class _SearchedDir:
    """Record of a directory that was checked during skill loading."""

    path: str
    source: str  # "default", "global", or "project"
    skill_count: int
    exists: bool


@dataclass
class _LoadResult:
    skills: list[Skill] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    searched_dirs: list[_SearchedDir] = field(default_factory=list)


def _yaml_error_hint(error: yaml.YAMLError) -> str:
    """Return an actionable hint for common YAML errors."""
    msg = str(error)
    if "mapping values are not allowed here" in msg:
        return "Hint: values containing colons must be quoted, or use block scalar '|' for multi-line prompts"
    if "while parsing a flow mapping" in msg or "expected ',' or '}'" in msg:
        return (
            "Hint: '{args}' is interpreted as YAML flow mapping. "
            "Use block scalar 'prompt: |' for prompts containing curly braces"
        )
    if "found unknown escape character" in msg:
        return (
            "Hint: YAML double-quoted strings treat backslashes as escape sequences. "
            "Use block scalar 'prompt: |' instead of double quotes for prompts "
            "containing regex or backslash characters"
        )
    return ""


def _format_yaml_error(path: Path, error: yaml.YAMLError) -> str:
    """Format a YAML error with file location and hint."""
    parts = [f"Failed to load {path.name}"]
    if hasattr(error, "problem_mark") and error.problem_mark is not None:
        mark = error.problem_mark
        parts.append(f"line {mark.line + 1}, column {mark.column + 1}")
    parts_str = " (".join(parts) + (")" if len(parts) > 1 else "")
    msg = f"{parts_str}: {error.problem}" if hasattr(error, "problem") else f"{parts_str}: {error}"
    hint = _yaml_error_hint(error)
    if hint:
        msg = f"{msg}. {hint}"
    return msg


def _validate_skill_name(raw_name: str, stem: str) -> tuple[str, str | None]:
    """Validate and normalize a skill name.

    Returns (normalized_name, warning_or_none).
    """
    name = raw_name.strip() if raw_name else ""
    if not name:
        name = stem
    if not _VALID_SKILL_NAME.match(name):
        return "", f"Skipped {stem}: invalid skill name '{name}' (must match [a-z0-9][a-z0-9_-]*)"
    if name in _get_builtin_commands():
        return "", f"Skipped {stem}: skill name '{name}' conflicts with built-in /{name} command"
    return name, None


def _parse_tool_policy(data: dict[str, Any]) -> SkillPolicy:
    """Extract tool policy from frontmatter data.

    Supports both Claude format (``allowed-tools``, hyphenated) and
    Anteroom format (``allowed_tools``, underscored).  Hyphenated keys
    take precedence when both are present, and set ``origin_format``
    to ``"claude"``.
    """
    origin_format = ""

    # Detect format — hyphenated (Claude) takes precedence
    raw_allowed: list[str] | None = None
    raw_denied: list[str] | None = None

    if "allowed-tools" in data:
        raw_allowed = data["allowed-tools"]
        origin_format = "claude"
    elif "allowed_tools" in data:
        raw_allowed = data["allowed_tools"]
        origin_format = "anteroom"

    if "denied-tools" in data:
        raw_denied = data["denied-tools"]
        if not origin_format:
            origin_format = "claude"
    elif "denied_tools" in data:
        raw_denied = data["denied_tools"]
        if not origin_format:
            origin_format = "anteroom"

    def _validate_tool_list(raw: Any, field_name: str) -> frozenset[str]:
        if raw is None:
            return frozenset()
        if isinstance(raw, str):
            raw = [t.strip() for t in raw.split(",") if t.strip()]
        if not isinstance(raw, list):
            logger.warning("Skill policy: %s must be a list, got %s", field_name, type(raw).__name__)
            return frozenset()
        valid: list[str] = []
        for item in raw:
            name = str(item).strip()
            if _VALID_TOOL_NAME.match(name):
                valid.append(name)
            else:
                logger.warning("Skill policy: invalid tool name '%s' in %s (skipped)", name, field_name)
        return frozenset(valid)

    allowed = _validate_tool_list(raw_allowed, "allowed-tools")
    denied = _validate_tool_list(raw_denied, "denied-tools")

    if not allowed and not denied:
        return SkillPolicy()

    return SkillPolicy(allowed_tools=allowed, denied_tools=denied, origin_format=origin_format)


def _extract_metadata(data: dict[str, Any]) -> dict[str, Any]:
    """Extract non-core frontmatter fields, preserving YAML structure."""
    return {str(k): v for k, v in data.items() if k not in _CORE_FRONTMATTER_KEYS}


def _parse_skill_md(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Parse a SKILL.md file with YAML frontmatter.

    Returns ``(data_dict, None)`` on success or ``(None, warning)`` on
    failure. The ``data_dict`` has ``name``, ``description``, and
    ``prompt`` keys — the same shape as a parsed YAML skill, so the
    caller can process both formats uniformly.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as exc:
        return None, f"Failed to read {path}: {exc}"
    if not raw.strip():
        return None, f"Skipped {path}: empty file"
    if not raw.startswith("---\n") and not raw.startswith("---\r\n"):
        return None, f"Skipped {path}: missing YAML frontmatter (must start with ---)"
    try:
        body, fm = _extract_yaml_frontmatter(raw, path)
    except ValueError as exc:
        yaml_exc = getattr(exc, "__cause__", None)
        if isinstance(yaml_exc, yaml.YAMLError):
            return None, _format_yaml_error(path, yaml_exc)
        return None, f"Skipped {path}: {exc}"
    body = body.strip()
    if not body:
        return None, f"Skipped {path}: empty prompt body (nothing after frontmatter)"
    fm["prompt"] = body
    return fm, None


def _load_skills_from_dir(skills_dir: Path, source: str) -> _LoadResult:
    """Load ``*/SKILL.md`` skill files from a directory.

    Only the directory-based SKILL.md layout is supported::

        skills/
          deploy-check/
            SKILL.md

    YAML ``.yaml`` / ``.yml`` skill files are no longer loaded. If any are
    found, a warning is emitted directing the user to migrate to SKILL.md.
    """
    result = _LoadResult()
    if not skills_dir.is_dir():
        result.searched_dirs.append(_SearchedDir(str(skills_dir), source, 0, False))
        return result

    # Discover SKILL.md files (the only supported layout)
    md_paths = sorted(skills_dir.glob("*/SKILL.md"), key=lambda p: p.parent.name)

    # Warn about stale YAML files that will no longer load
    stale_yaml = sorted(set(skills_dir.glob("*.yaml")) | set(skills_dir.glob("*.yml")))
    for stale in stale_yaml:
        result.warnings.append(
            f"Ignored {stale.name}: YAML skills are no longer supported. "
            f"Migrate to {stale.stem}/SKILL.md (YAML frontmatter + Markdown body)."
        )

    for path in md_paths:
        effective_name = path.parent.name.lower()
        try:
            raw_content = path.read_text(encoding="utf-8")
            data, warning = _parse_skill_md(path)
            if warning:
                result.warnings.append(warning)
                continue
            assert data is not None

            raw_name = data.get("name", effective_name)
            if not isinstance(raw_name, str):
                result.warnings.append(f"Skipped {path}: 'name' must be a string, got {type(raw_name).__name__}")
                continue
            name, warning = _validate_skill_name(raw_name, effective_name)
            if warning:
                result.warnings.append(warning)
                continue
            prompt = data.get("prompt", "")
            if not isinstance(prompt, str):
                result.warnings.append(f"Skipped {path}: 'prompt' must be a string, got {type(prompt).__name__}")
                continue
            if not prompt.strip():
                result.warnings.append(f"Skipped {path}: empty prompt body")
                continue
            resource_count = 0
            resource_list = _parse_resource_list_from_frontmatter(raw_content, path)
            if resource_list:
                try:
                    resources = _resolve_bundle_resources(path.parent, resource_list, skills_dir)
                    prompt = _inline_resources(prompt, resources)
                    resource_count = len(resources)
                except ValueError as exc:
                    result.warnings.append(f"Skipped resources for {path}: {exc}")
            if len(prompt) > MAX_PROMPT_SIZE:
                result.warnings.append(
                    f"Skipped {path}: prompt exceeds {MAX_PROMPT_SIZE // 1000}KB limit ({len(prompt) // 1000}KB)"
                )
                continue
            description = data.get("description", "")
            if not description:
                result.warnings.append(f"{path} has no description")
            policy = _parse_tool_policy(data)
            metadata = _extract_metadata(data)
            result.skills.append(
                Skill(
                    name=name,
                    description=str(description) if description else "",
                    prompt=prompt,
                    source=source,
                    resource_count=resource_count,
                    policy=policy,
                    metadata=metadata,
                    update_guidance=_compute_update_guidance(
                        source,
                        name,
                        path=str(path),
                    ),
                )
            )

            # Spec-compliance advisory warnings (non-blocking)
            if not _SPEC_NAME_RE.match(name):
                if "--" in name:
                    logger.debug("Spec advisory: skill '%s' contains consecutive hyphens", name)
                elif "_" in name:
                    logger.debug("Spec advisory: skill '%s' uses underscores (spec prefers hyphens)", name)
            if effective_name != name and raw_name.strip().lower() != effective_name:
                logger.debug(
                    "Spec advisory: skill name '%s' does not match directory name '%s'",
                    name,
                    effective_name,
                )

            # Resource-directory detection (recognized, not loaded)
            skill_dir = path.parent
            for rdir in _RESOURCE_DIRS:
                if (skill_dir / rdir).is_dir():
                    logger.debug(
                        "Skill '%s' has %s/ directory (recognized; only files declared in resources are loaded)",
                        name,
                        rdir,
                    )
        except Exception as e:
            result.warnings.append(f"Failed to load {path}: {e}")
    result.searched_dirs.append(_SearchedDir(str(skills_dir), source, len(result.skills), True))
    return result


def _skill_dirs(working_dir: str | None = None) -> list[Path]:
    """Return skill directories (global + project).

    Walks up from working_dir looking for .anteroom/skills/, .claude/skills/,
    or .parlor/skills/. Collects ALL matching directories at the first level
    that has any match, not just the first one found.
    """
    from ..config import _resolve_data_dir

    data_dir = _resolve_data_dir()
    dirs = [data_dir / "skills"]
    current = Path(working_dir or os.getcwd()).resolve()
    while True:
        found: list[Path] = []
        for dirname in (".anteroom", ".claude", ".parlor"):
            project_dir = current / dirname / "skills"
            if project_dir.is_dir():
                found.append(project_dir)
        if found:
            dirs.extend(found)
            return dirs
        parent = current.parent
        if parent == current:
            break
        current = parent
    return dirs


def load_skills(working_dir: str | None = None) -> _LoadResult:
    """Load skills from global and project directories."""
    combined = _LoadResult()
    dirs = _skill_dirs(working_dir)
    sources = ["global"] + ["project"] * (len(dirs) - 1)
    for d, source in zip(dirs, sources):
        result = _load_skills_from_dir(d, source)
        combined.skills.extend(result.skills)
        combined.warnings.extend(result.warnings)
        combined.searched_dirs.extend(result.searched_dirs)
    return combined


def _expand_args(prompt: str, args: str) -> str:
    """Expand {args} placeholder in prompt, or append as context.

    - Empty/whitespace-only args are a no-op (returns prompt unchanged).
    - {args} inside fenced code blocks (``` ... ```) is NOT replaced.
    - When no {args} placeholder exists outside code blocks, args are appended.
    """
    if not args or not args.strip():
        return prompt

    # Check for {args} outside of fenced code blocks
    segments = _CODE_FENCE_RE.split(prompt)
    has_placeholder_outside_code = False
    for i, segment in enumerate(segments):
        is_code_block = i % 2 == 1  # odd indices are code fence captures
        if not is_code_block and _ARGS_PLACEHOLDER in segment:
            has_placeholder_outside_code = True
            break

    if has_placeholder_outside_code:
        # Replace {args} only in non-code-block segments
        result_parts = []
        for i, segment in enumerate(segments):
            is_code_block = i % 2 == 1
            if is_code_block:
                result_parts.append(segment)
            else:
                result_parts.append(segment.replace(_ARGS_PLACEHOLDER, args))
        return "".join(result_parts)

    return f"{prompt}\n\nAdditional context: {args}"


class SkillRegistry:
    """Manages loaded skills with namespace-aware resolution.

    Skills are stored by canonical key (``namespace/name`` for namespaced
    skills, bare ``name`` for filesystem skills).  When a name is unique
    across all namespaces, it can be invoked by bare name.  When two or
    more skills share a name, they must be invoked by ``namespace/name``.
    """

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}
        self.load_warnings: list[str] = []
        self.searched_dirs: list[_SearchedDir] = []
        # Maps bare name → list of canonical keys that share it
        self._name_index: dict[str, list[str]] = {}

    def _rebuild_name_index(self) -> None:
        """Rebuild the bare-name → canonical-keys index."""
        index: dict[str, list[str]] = {}
        for key, skill in self._skills.items():
            bare = skill.name.lower()
            index.setdefault(bare, []).append(key)
        self._name_index = index

    def _resolve_key(self, name: str) -> str | None:
        """Resolve a user-provided name to a canonical key.

        Accepts bare ``name`` (unique match) or ``namespace/name`` (exact).
        """
        lower = name.lower() if name else ""
        # Direct canonical key match (namespace/name or bare name)
        if lower in self._skills:
            return lower
        # Try bare name lookup
        candidates = self._name_index.get(lower, [])
        if len(candidates) == 1:
            return candidates[0]
        return None

    def _display_name(self, skill: Skill) -> str:
        """Return the display name: bare name if unique, namespace/name if ambiguous."""
        bare = skill.name.lower()
        candidates = self._name_index.get(bare, [])
        if len(candidates) > 1 and skill.namespace:
            return f"{skill.namespace}/{skill.name}"
        return skill.name

    def load(self, working_dir: str | None = None) -> list[Skill]:
        """Load skills from default, global, and project directories.

        Uses atomic swap: builds new dict fully before replacing self._skills,
        so concurrent readers never see a partially-loaded state.

        Returns the list of loaded skills (for callers that need to rebuild schemas).
        """
        new_skills: dict[str, Skill] = {}
        new_warnings: list[str] = []
        new_searched: list[_SearchedDir] = []

        default_dir = Path(__file__).parent / "default_skills"
        default_result = _load_skills_from_dir(default_dir, "default")
        new_warnings.extend(default_result.warnings)
        new_searched.extend(default_result.searched_dirs)
        default_names = set()
        for skill in default_result.skills:
            new_skills[skill.name] = skill
            default_names.add(skill.name)

        user_result = load_skills(working_dir)
        new_warnings.extend(user_result.warnings)
        new_searched.extend(user_result.searched_dirs)
        for skill in user_result.skills:
            if skill.name in default_names:
                new_warnings.append(f"User skill '{skill.name}' ({skill.source}) overrides built-in")
            new_skills[skill.name] = skill

        if len(new_skills) > MAX_SKILLS:
            new_warnings.append(
                f"Loaded {len(new_skills)} skills (limit: {MAX_SKILLS}). Consider removing unused skill files."
            )

        # Atomic swap — Python dict assignment is GIL-protected
        self._skills = new_skills
        self.load_warnings = new_warnings
        self.searched_dirs = new_searched
        self._rebuild_name_index()

        return sorted(new_skills.values(), key=lambda s: s.name)

    reload = load

    def get(self, name: str) -> Skill | None:
        key = self._resolve_key(name)
        return self._skills.get(key) if key else None

    def list_skills(self) -> list[Skill]:
        return sorted(self._skills.values(), key=lambda s: s.name)

    def has_skill(self, name: str) -> bool:
        return self._resolve_key(name) is not None

    def resolve_input(self, user_input: str) -> tuple[bool, str]:
        """Check if input is a skill invocation. Returns (is_skill, expanded_prompt)."""
        if not user_input.startswith("/"):
            return False, user_input
        parts = user_input.split(maxsplit=1)
        skill_name = parts[0][1:].lower()  # Remove leading /, normalize case
        skill = self.get(skill_name)
        if not skill:
            # Check if the name is ambiguous (multiple namespaces)
            candidates = self._name_index.get(skill_name, [])
            if len(candidates) > 1:
                options = ", ".join(f"/{c}" for c in candidates)
                logger.warning(
                    "Ambiguous skill '%s' — qualify with namespace: %s",
                    skill_name,
                    options,
                )
            return False, user_input
        args = parts[1] if len(parts) > 1 else ""
        prompt = skill.prompt
        if args:
            prompt = _expand_args(prompt, args)
        return True, prompt

    def resolve_input_with_skill(self, user_input: str) -> tuple[bool, str, Skill | None]:
        """Like resolve_input but also returns the Skill object."""
        if not user_input.startswith("/"):
            return False, user_input, None
        parts = user_input.split(maxsplit=1)
        skill_name = parts[0][1:].lower()
        skill = self.get(skill_name)
        if not skill:
            candidates = self._name_index.get(skill_name, [])
            if len(candidates) > 1:
                options = ", ".join(f"/{c}" for c in candidates)
                logger.warning(
                    "Ambiguous skill '%s' — qualify with namespace: %s",
                    skill_name,
                    options,
                )
            return False, user_input, None
        args = parts[1] if len(parts) > 1 else ""
        prompt = skill.prompt
        if args:
            prompt = _expand_args(prompt, args)
        return True, prompt, skill

    def get_skill_descriptions(self) -> list[tuple[str, str]]:
        """Return (display_name, description) pairs for all loaded skills.

        Uses bare name when unique, namespace/name when ambiguous.
        Includes update guidance when available so the model knows the
        correct update action for pack-backed skills.
        """
        result: list[tuple[str, str]] = []
        for s in self.list_skills():
            desc = s.description
            if s.update_guidance:
                desc = f"{desc} [update: {s.update_guidance}]"
            result.append((self._display_name(s), desc))
        return result

    def load_from_artifacts(self, artifact_registry: Any, *, db: Any = None) -> int:
        """Load skill-type artifacts from the artifact registry.

        Filesystem skills take precedence — artifact skills are only added
        when the exact ``namespace/name`` key is not already present.
        Bare-name filesystem skills still block artifact skills with the
        same bare name (filesystem wins).  Returns the number of skills added.

        When *db* is provided, pack provenance is looked up for each artifact
        so that ``update_guidance`` can name the pack source path.

        Clears previously loaded artifact skills first so that detached or
        removed packs don't leave stale entries in the registry.
        """
        # Remove stale artifact-sourced skills before re-adding
        self._skills = {k: v for k, v in self._skills.items() if not v.source.startswith("artifact:")}
        added = 0
        _pack_cache: dict[str, dict[str, Any] | None] = {}  # pack_id → pack info
        for art in artifact_registry.list_all(artifact_type="skill"):
            ns = art.namespace.lower()
            bare = art.name.lower()
            canonical = f"{ns}/{bare}"
            # Skip if this exact canonical key exists
            if canonical in self._skills:
                continue
            # Skip if a filesystem skill (no namespace) owns the bare name
            if bare in self._skills and not self._skills[bare].namespace:
                continue
            description = art.name
            prompt = art.content
            policy = SkillPolicy()
            # Try SKILL.md frontmatter format first, then fall back to
            # legacy YAML for backward compat with existing DB content.
            content = art.content or ""
            if content.startswith("---\n") or content.startswith("---\r\n"):
                try:
                    end = content.index("\n---", 4)
                    fm = yaml.safe_load(content[4:end])
                    if isinstance(fm, dict):
                        description = fm.get("description", art.name)
                        prompt = content[end + 4 :].strip()
                        policy = _parse_tool_policy(fm)
                except (ValueError, yaml.YAMLError):
                    pass
            else:
                try:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict):
                        description = data.get("description", art.name)
                        prompt = data.get("prompt", content)
                        policy = _parse_tool_policy(data)
                except yaml.YAMLError:
                    pass
            if not prompt or not prompt.strip():
                continue
            art_meta = getattr(art, "metadata", None) or {}
            # Promote non-core frontmatter from the artifact's stored metadata
            skill_metadata: dict[str, Any] = {}
            if isinstance(art_meta, dict):
                for k, v in art_meta.items():
                    if k not in ("bundle", "resource_count", "resource_names"):
                        skill_metadata[str(k)] = v
            # Look up pack provenance if DB is available
            pack_name = ""
            pack_source_path = ""
            if db is not None and art.artifact_id:
                from ..services.artifact_storage import get_pack_for_artifact

                pack_info = _pack_cache.get(art.artifact_id)
                if pack_info is None:
                    pack_info = get_pack_for_artifact(db, art.artifact_id)
                    if pack_info:
                        _pack_cache[art.artifact_id] = pack_info
                if pack_info:
                    pack_name = pack_info.get("pack_name", "")
                    pack_source_path = pack_info.get("source_path", "")
            source_str = f"artifact:{art.source.value}"
            self._skills[canonical] = Skill(
                name=art.name,
                description=description,
                prompt=prompt,
                source=source_str,
                namespace=ns,
                resource_count=int(art_meta.get("resource_count", 0)) if isinstance(art_meta, dict) else 0,
                policy=policy,
                metadata=skill_metadata,
                fqn=art.fqn,
                update_guidance=_compute_update_guidance(
                    source_str,
                    art.name,
                    namespace=ns,
                    pack_name=pack_name,
                    pack_source_path=pack_source_path,
                ),
            )
            added += 1
        self._rebuild_name_index()
        return added

    def load_from_references(self, paths: list[str]) -> int:
        """Load skills from explicit ``references.skills`` config paths.

        Paths must be absolute (resolved during config loading).  Each path
        can be a directory containing ``SKILL.md`` or a direct ``.md`` file.
        Reference skills have the highest precedence — they overwrite
        same-name skills from any other source.

        Returns the number of skills loaded.
        """
        added = 0
        for p in paths:
            path = Path(p)
            # Directory: look for SKILL.md inside
            if path.is_dir():
                candidate = path / "SKILL.md"
                if not candidate.is_file():
                    logger.warning("references.skills: no SKILL.md in directory %s", path)
                    continue
                path = candidate
            elif not path.is_file():
                logger.warning("references.skills: path not found: %s", p)
                continue
            data, warning = _parse_skill_md(path)
            if warning:
                logger.warning("references.skills: %s", warning)
                continue
            assert data is not None
            effective_name = path.parent.name.lower() if path.name == "SKILL.md" else path.stem.lower()
            raw_name = data.get("name", effective_name)
            if not isinstance(raw_name, str):
                logger.warning("references.skills: %s: 'name' must be a string", path)
                continue
            name, warning = _validate_skill_name(raw_name, effective_name)
            if warning:
                logger.warning("references.skills: %s", warning)
                continue
            prompt = data.get("prompt", "")
            if not isinstance(prompt, str) or not prompt.strip():
                logger.warning("references.skills: %s: empty prompt", path)
                continue
            if len(prompt) > MAX_PROMPT_SIZE:
                logger.warning("references.skills: %s: prompt exceeds size limit", path)
                continue
            description = data.get("description", "")
            policy = _parse_tool_policy(data)
            metadata = _extract_metadata(data)
            self._skills[name] = Skill(
                name=name,
                description=str(description) if description else "",
                prompt=prompt,
                source="reference",
                policy=policy,
                metadata=metadata,
                update_guidance=_compute_update_guidance(
                    "reference",
                    name,
                    path=str(path),
                ),
            )
            added += 1
        if added:
            self._rebuild_name_index()
        return added

    def get_invoke_skill_definition(self) -> dict[str, Any] | None:
        """Return an OpenAI function schema for the invoke_skill tool.

        Returns None if no skills are loaded.  Uses display names
        (namespace-qualified when ambiguous) as the enum values.
        """
        skills = self.list_skills()
        if not skills:
            return None
        return {
            "type": "function",
            "function": {
                "name": "invoke_skill",
                "description": (
                    "Invoke a predefined skill/workflow. Use this when the user's request "
                    "clearly matches one of the available skills listed in <available_skills>."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "enum": [self._display_name(s) for s in skills],
                            "description": "The name of the skill to invoke.",
                        },
                        "args": {
                            "type": "string",
                            "description": "Optional additional context or arguments for the skill.",
                        },
                    },
                    "required": ["skill_name"],
                },
            },
        }
