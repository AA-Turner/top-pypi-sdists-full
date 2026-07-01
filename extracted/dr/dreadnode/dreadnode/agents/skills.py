"""
Skill loader and discovery.

Loads skills from SKILL.md files following the Agent Skills specification.
https://agentskills.io/specification
"""

import re
import typing as t
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import pathname2url

import yaml
from loguru import logger

from dreadnode.agents.tools import tool
from dreadnode.capabilities.capability import Capability

# CAP-IDENT-010 (skill surface): unsafe characters are replaced with `_` and
# the segment is trimmed of leading/trailing `_`. Unlike the tool wire surface,
# `-` is preserved — the skill qualified id is a free-form string argument,
# not constrained by the LLM function-calling regex. A cap like `mythic-c2`
# projects as `mythic-c2:recon`, not `mythic_c2:recon`.
_SKILL_NAMESPACE_SAFE = re.compile(r"[^a-zA-Z0-9_-]+")


def _sanitize_skill_segment(segment: str) -> str:
    return _SKILL_NAMESPACE_SAFE.sub("_", segment).strip("_")


# Skill name validation: lowercase letters, numbers, hyphens only, max 64 chars
# - Must not start/end with "-"
# - Must not contain consecutive hyphens
SKILL_NAME_PATTERN = re.compile(r"^(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)$")
SKILL_DESCRIPTION_MAX_LENGTH = 1024
SKILL_COMPATIBILITY_MAX_LENGTH = 500

SkillSource = t.Literal["builtin", "python", "bundled"]
"""The origin of a skill. See CAP-IDENT-001 in specs/capabilities/runtime.md.

Skills have fewer variants than tools — there is no MCP-sourced skill
or synthetic skill; skills come from SKILL.md files only.
"""


@dataclass
class Skill:
    """
    A skill that teaches an agent how to perform a specific task.

    Follows the Agent Skills specification exactly:
    https://agentskills.io/specification

    Attributes:
        name: Unique skill identifier (lowercase, numbers, hyphens; max 64 chars)
        description: What the skill does and when to use it (max 1024 chars)
        instructions: Full markdown instructions (body of SKILL.md)
        allowed_tools: Tools the skill can use without asking permission
        license: License name or reference
        compatibility: Environment requirements
        metadata: Arbitrary key-value mapping
        path: Path to the SKILL.md file
    """

    name: str
    description: str
    instructions: str
    allowed_tools: list[str] = field(default_factory=list)
    license: str | None = None
    compatibility: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    path: Path | None = None
    source: SkillSource = "builtin"
    """The skill's origin. Paired with `namespace` to determine qualified id.
    See CAP-IDENT-001. Stamped at the discovery boundary (see
    `CapabilityRegistry.all_skills`)."""
    namespace: tuple[str, ...] = ()
    """Structural namespace path. Empty for builtin and bundled skills;
    `(cap,)` for capability-sourced skills. See CAP-IDENT-001, CAP-IDENT-009."""

    @property
    def directory(self) -> Path | None:
        """Get the skill directory (parent of SKILL.md)."""
        return self.path.parent if self.path else None

    @property
    def qualified_id(self) -> str:
        """User-facing qualified identifier for this skill.

        Projects structural identity (`namespace` + `name`) through the `:`
        separator rule (CAP-IDENT-009). Builtin and bundled skills render
        bare because their namespace is empty. There is no length cap —
        unlike tool wire names, skill identifiers are not constrained by
        the LLM function-calling regex.
        """
        if not self.namespace:
            return self.name
        segments = []
        for raw in self.namespace:
            cleaned = _sanitize_skill_segment(raw)
            if not cleaned:
                raise ValueError(
                    f"Namespace segment {raw!r} sanitizes to empty; "
                    "capability names must contain at least one [a-zA-Z0-9_-] character."
                )
            segments.append(cleaned)
        return ":".join([*segments, self.name])

    def to_dict(self) -> dict[str, t.Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "allowed_tools": self.allowed_tools,
            "license": self.license,
            "compatibility": self.compatibility,
            "metadata": self.metadata,
            "path": str(self.path) if self.path else None,
            "source": self.source,
            "namespace": list(self.namespace),
            "qualified_id": self.qualified_id,
        }

    def _allowed_tools_xml(self, indent: str = "") -> str:
        """Render allowed tools as XML. Returns empty string if none."""
        if not self.allowed_tools:
            return ""
        tool_tags = "\n".join(f"{indent}  <tool>{t}</tool>" for t in self.allowed_tools)
        return f"\n{indent}<allowed_tools>\n{tool_tags}\n{indent}</allowed_tools>\n"

    def render_content(self) -> str:
        """Render full skill content for loading into a conversation.

        Produces the same output as the skill tool: instructions,
        allowed tools advisory, base directory, and skill file listing.
        The `<skill_content name>` attribute uses the qualified id so
        the LLM sees the same identifier it invoked the skill with
        (CAP-IDENT-016).
        """
        skill_files = ""
        base_line = ""
        if self.directory:
            base_url = _path_to_file_url(self.directory)
            base_line = (
                f"Base directory for this skill: {base_url}\n"
                "Relative paths in this skill (e.g., scripts/, reference/) "
                "are relative to this base directory.\n"
                "Note: file list is sampled."
            )
            files = _list_skill_files(self.directory)
            if files:
                file_tags = "\n".join(f"<file>{f}</file>" for f in files)
                skill_files = f"\n<skill_files>\n{file_tags}\n</skill_files>"

        return "\n".join(
            [
                f'<skill_content name="{self.qualified_id}">',
                f"# Skill: {self.qualified_id}",
                "",
                self.instructions.strip(),
                "",
                self._allowed_tools_xml(),
                base_line,
                skill_files,
                "</skill_content>",
            ]
        )

    def to_prompt_xml(self) -> str:
        """Generate XML for tool description (metadata only).

        Emits the qualified identifier in `<name>` (CAP-IDENT-016) so the
        agent invokes the skill with the same string it sees.
        """
        location = _path_to_file_url(self.path) if self.path else ""
        return (
            f"  <skill>\n"
            f"    <name>{self.qualified_id}</name>\n"
            f"    <description>{self.description}</description>\n"
            f"    <location>{location}</location>"
            f"  </skill>"
        )


def load_skill(path: Path, *, validate: bool = True) -> Skill:
    """
    Load a skill from a SKILL.md file.

    The file should have YAML frontmatter followed by markdown content:

        ---
        name: my-skill
        description: What it does
        allowed-tools: tool1 tool2
        license: Apache-2.0
        compatibility: Requires git and docker
        metadata:
          author: example-org
          version: "1.0"
        ---

        # My Skill

        Instructions here...

    Args:
        path: Path to SKILL.md file
        validate: Whether to validate name/description constraints (default True)

    Returns:
        Loaded Skill object

    Raises:
        ValueError: If the file format is invalid or validation fails
    """
    content = path.read_text()

    # Parse YAML frontmatter
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)

    if not frontmatter_match:
        raise ValueError(f"Invalid SKILL.md format: missing YAML frontmatter in {path}")

    yaml_content = frontmatter_match.group(1)
    markdown_content = frontmatter_match.group(2).strip()

    try:
        frontmatter = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter in {path}: {e}") from e

    if not isinstance(frontmatter, dict):
        raise ValueError(f"Invalid SKILL.md frontmatter in {path}: must be a mapping")  # noqa: TRY004

    # Extract required fields
    name = frontmatter.get("name")
    if not name or not isinstance(name, str):
        raise ValueError(f"Missing 'name' in SKILL.md frontmatter: {path}")

    # Validate name format (lowercase, numbers, hyphens, max 64 chars)
    if validate and not SKILL_NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid skill name '{name}' in {path}: must be lowercase letters, "
            f"numbers, and hyphens only, max 64 characters"
        )

    description = frontmatter.get("description")
    if not isinstance(description, str):
        description = ""
    description = description.strip()

    if validate and not description:
        raise ValueError(f"Skill description in {path} must be non-empty")

    # Validate description length
    if validate and len(description) > SKILL_DESCRIPTION_MAX_LENGTH:
        raise ValueError(
            f"Skill description in {path} exceeds {SKILL_DESCRIPTION_MAX_LENGTH} characters "
            f"(got {len(description)})"
        )

    # Validate skill directory name matches skill name
    skill_dir = path.parent
    if validate and skill_dir.name != name:
        raise ValueError(
            f"Skill name '{name}' in {path} must match directory name '{skill_dir.name}'"
        )

    # Parse allowed tools (space-delimited list per spec)
    allowed_tools_raw = frontmatter.get("allowed-tools", frontmatter.get("allowed_tools", []))
    if isinstance(allowed_tools_raw, str):
        # Space-delimited string per spec
        allowed_tools = [item for item in allowed_tools_raw.split() if item]
    elif allowed_tools_raw is None:
        allowed_tools = []
    elif isinstance(allowed_tools_raw, list):
        allowed_tools = [str(item).strip() for item in allowed_tools_raw if str(item).strip()]
    else:
        raise ValueError(f"Invalid 'allowed-tools' in {path}: must be string or list")

    license_value = frontmatter.get("license")
    if license_value is not None and not isinstance(license_value, str):
        raise ValueError(f"Invalid 'license' in {path}: must be a string")

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None and not isinstance(compatibility, str):
        raise ValueError(f"Invalid 'compatibility' in {path}: must be a string")
    if isinstance(compatibility, str):
        compatibility = compatibility.strip()
        if validate and len(compatibility) > SKILL_COMPATIBILITY_MAX_LENGTH:
            raise ValueError(
                f"Skill compatibility in {path} exceeds {SKILL_COMPATIBILITY_MAX_LENGTH} characters "
                f"(got {len(compatibility)})"
            )
        if validate and compatibility == "":
            raise ValueError(f"Skill compatibility in {path} must be non-empty if provided")

    metadata_field = frontmatter.get("metadata") or {}
    if not isinstance(metadata_field, dict):
        raise ValueError(f"Invalid 'metadata' in {path}: must be a mapping")  # noqa: TRY004
    metadata_values: dict[str, str] = {}
    for key, value in metadata_field.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError(f"Invalid 'metadata' in {path}: keys and values must be strings")  # noqa: TRY004
        metadata_values[key] = value

    return Skill(
        name=name,
        description=description,
        instructions=markdown_content,
        allowed_tools=allowed_tools,
        license=license_value,
        compatibility=compatibility,
        metadata=metadata_values,
        path=path,
    )


def discover_skills(directory: Path | None = None) -> list[Skill]:
    """
    Discover skills in a directory.

    Scans the directory for subdirectories containing a SKILL.md file.
    Each valid skill directory is loaded.

    Args:
        directory: Directory to scan (defaults to cwd)

    Returns:
        List of discovered and loaded skills
    """
    if directory is None:
        directory = Path.cwd()

    directory = directory.resolve()
    skills: list[Skill] = []

    if not directory.exists():
        return skills

    # Scan for directories containing SKILL.md
    for item in directory.iterdir():
        if item.is_dir():
            skill_file = item / "SKILL.md"
            if skill_file.exists():
                try:
                    skill = load_skill(skill_file)
                    skills.append(skill)
                    logger.debug("Discovered skill: {} at {}", skill.name, skill_file)
                except Exception as e:
                    logger.error("Failed to load skill from {}: {}", skill_file, e)

    return skills


def load_instructions(path: Path) -> str:
    """
    Load instructions from a file with YAML frontmatter.

    The file should have the same format as SKILL.md:

        ---
        name: my-instructions
        description: What these instructions do
        ---

        # Instructions

        Your instructions here...

    Args:
        path: Path to the instructions file

    Returns:
        The markdown instructions (body after frontmatter)

    Raises:
        ValueError: If the file format is invalid
    """
    content = path.read_text()

    # Parse YAML frontmatter
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)

    if not frontmatter_match:
        # No frontmatter - treat entire content as instructions
        return content.strip()

    return frontmatter_match.group(2).strip()


def discover_instructions(directory: Path | None = None) -> str | None:
    """
    Discover instructions.md in a directory.

    Looks for an instructions.md file (with optional YAML frontmatter).

    Args:
        directory: Directory to search (defaults to cwd)

    Returns:
        Instructions string if instructions.md found, None otherwise
    """
    if directory is None:
        directory = Path.cwd()

    directory = directory.resolve()
    instructions_file = directory / "instructions.md"

    if not instructions_file.exists():
        return None

    try:
        return load_instructions(instructions_file)
    except Exception as e:
        logger.warning(f"Failed to load instructions from {instructions_file}: {e}")
        return None


def _list_skill_files(skill_dir: Path, *, limit: int = 10) -> list[str]:
    """List supporting files in a skill directory (excluding SKILL.md), up to limit."""
    files: list[str] = []
    for item in sorted(skill_dir.rglob("*")):
        if not item.is_file() or item.name == "SKILL.md":
            continue
        files.append(str(item))
        if len(files) >= limit:
            break
    return files


def _path_to_file_url(p: Path) -> str:
    """Convert a Path to a file:// URL."""
    return "file://" + pathname2url(str(p.resolve()))


def resolve_skill(name: str, skills: t.Sequence[Skill]) -> Skill:
    """Resolve a user-supplied skill identifier against a list of effective skills.

    Resolution order (CAP-IDENT-017, CAP-IDENT-018):
      1. Exact qualified-id match (`{cap}:{name}` or bare for builtin/bundled).
      2. Bare-name match if exactly one skill has that bare name.
      3. Error if bare input is ambiguous; surface qualified candidates.

    Raises:
        ValueError: skill not found, or bare input is ambiguous.
    """
    by_qualified = {s.qualified_id: s for s in skills}
    if name in by_qualified:
        return by_qualified[name]

    bare_matches = [s for s in skills if s.name == name]
    if len(bare_matches) == 1:
        return bare_matches[0]
    if len(bare_matches) > 1:
        candidates = ", ".join(sorted(s.qualified_id for s in bare_matches))
        raise ValueError(
            f"Skill name '{name}' is ambiguous across capabilities. "
            f"Use a qualified identifier. Candidates: {candidates}"
        )

    available = ", ".join(sorted(by_qualified)) or "none"
    raise ValueError(f"Skill '{name}' not found. Available skills: {available}")


def create_skill_tool(skills: list[Skill]) -> t.Any:
    """
    Create a single skill tool bound to a list of discovered skills.

    Follows the OpenCode pattern: one tool with available skills listed in the
    description. When invoked, returns the full skill content and a listing of
    supporting files.

    Skills are addressed by qualified identifier (`{cap}:{name}`) in
    `<available_skills>` so the LLM always sees a stable, unambiguous handle
    (CAP-IDENT-016). Invocation accepts either the qualified id or a bare name
    when that bare name is unambiguous across the effective set
    (CAP-IDENT-017).

    Args:
        skills: List of effective skills to make available. Callers are
            expected to have already stamped `source`/`namespace` on each
            skill (typically via ``CapabilityRegistry.all_skills``).

    Returns:
        A single skill tool.
    """
    # Build description with available skills embedded as XML
    # Follows the OpenCode pattern exactly for description and parameter hint.
    if not skills:
        description = (
            "Load a specialized skill that provides domain-specific instructions "
            "and workflows. No skills are currently available."
        )
    else:
        skill_xml = "\n".join(s.to_prompt_xml() for s in skills)
        description = (
            "Load a specialized skill that provides domain-specific instructions and workflows.\n"
            "\n"
            "Skills contain step-by-step methodology, payload references, and edge-case guidance "
            "for specific tasks. When a task matches an available skill, you MUST load it before "
            "proceeding — do not attempt the task from general knowledge alone.\n"
            "\n"
            "If a skill is even plausibly relevant to the current task, load it. "
            "Do not mention a skill without invoking this tool. "
            "Skill use is expected whenever a matching skill exists.\n"
            "\n"
            "<available_skills>\n"
            f"{skill_xml}\n"
            "</available_skills>"
        )

    examples = ", ".join(f"'{s.qualified_id}'" for s in skills[:3])
    hint = f" (e.g., {examples}, ...)" if examples else ""

    @tool(description=description)
    async def skill(
        name: t.Annotated[str, f"The name of the skill from available_skills{hint}"],
    ) -> str:
        """Load a skill's full instructions and supporting files."""
        return resolve_skill(name, skills).render_content()

    return skill


def attach_capability_skills(*, agent: t.Any, capability: Capability) -> None:
    """Attach capability-local skills to the reconstructed agent, if any."""

    all_skills: list[Skill] = []
    for skills_path in capability.skills_paths or []:
        all_skills.extend(discover_skills(skills_path))
    if all_skills:
        agent.tools.append(create_skill_tool(all_skills))
