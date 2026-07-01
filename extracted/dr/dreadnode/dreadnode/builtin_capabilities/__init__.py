"""Bundled capabilities that ship with the SDK package."""

import re
import typing as t
from pathlib import Path

from loguru import logger

if t.TYPE_CHECKING:
    from dreadnode.capabilities.capability import Capability
    from dreadnode.storage.storage import Storage


def builtin_capabilities_dir() -> Path:
    """Return the directory containing bundled capability assets."""
    return Path(__file__).resolve().parent


def _read_markdown_body(path: Path) -> str:
    """Read a markdown body, stripping YAML frontmatter when present."""
    if not path.exists():
        return ""

    content = path.read_text().strip()
    frontmatter_match = re.match(r"^---\s*\n[\s\S]*?\n---\s*\n([\s\S]*)", content)
    if frontmatter_match:
        return frontmatter_match.group(1).strip()
    return content


def read_builtin_agent_prompt(capability_name: str, agent_name: str) -> str:
    """Read a bundled agent markdown body, stripping YAML frontmatter."""
    agent_file = builtin_capabilities_dir() / capability_name / "agents" / f"{agent_name}.md"
    return _read_markdown_body(agent_file)


def read_builtin_skill_instructions(capability_name: str, skill_name: str) -> str:
    """Read bundled skill instructions, stripping frontmatter."""
    skill_file = builtin_capabilities_dir() / capability_name / "skills" / skill_name / "SKILL.md"
    return _read_markdown_body(skill_file)


def load_builtin_capabilities(
    *,
    cwd: Path | None = None,
    storage: "Storage | None" = None,
    capability_dirs: list[str | Path] | None = None,
) -> tuple[dict[str, "Capability"], list[dict[str, t.Any]]]:
    """Load bundled capabilities from the SDK package tree."""
    from dreadnode.capabilities.capability import Capability

    capabilities: dict[str, Capability] = {}
    failures: list[dict[str, t.Any]] = []
    root = builtin_capabilities_dir()

    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or not (entry / "capability.yaml").exists():
            continue
        try:
            capability = Capability(
                entry,
                cwd=cwd,
                storage=storage,
                capability_dirs=capability_dirs,
                bundled=True,
            )
        except Exception as exc:
            logger.warning("Failed to load bundled capability from {}: {}", entry, exc)
            failures.append(
                {
                    "name": entry.name,
                    "path": str(entry),
                    "error": str(exc),
                    "source": "builtin",
                }
            )
            continue
        capabilities[capability.name] = capability

    return capabilities, failures
