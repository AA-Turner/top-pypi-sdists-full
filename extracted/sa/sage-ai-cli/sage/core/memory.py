"""Project memory for SAGE.

Two complementary primitives live in this file:

  - `ProjectMemory` (older): manages a single `SAGE.md` file holding
    long-lived project rules + style preferences. Like CLAUDE.md.

  - `MemoryStore` + `Memory` (D13): manages many session-spanning facts
    under `<root>/memory/`, each its own markdown file with YAML
    frontmatter. Mirrors Claude Code's auto-memory shape — user, project,
    feedback, reference entry types. Lets the agent persist things it
    learned (user preferences, ongoing initiatives, pointers to external
    systems) so future sessions don't start cold.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

class ProjectMemory:
    """Persistent project memory via SAGE.md file.

    Like CLAUDE.md, stores:
    - Coding style preferences
    - Architectural decisions
    - Project-specific rules
    - Forbidden patterns
    """

    DEFAULT_TEMPLATE = """# SAGE Project Memory

## Project Overview
<!-- Describe your project here -->

## Coding Style
- Use type hints for all functions
- Prefer composition over inheritance
- Write tests before implementation (TDD)

## Architecture Rules
<!-- Add project-specific architecture rules -->

## Forbidden Patterns
<!-- Patterns SAGE should never use -->
- No `print()` for logging (use proper logger)
- No hardcoded secrets

## Custom Commands
<!-- Define shortcuts for common tasks -->
# test: pytest -v
# lint: ruff check .
# format: ruff format .
"""

    def __init__(self, cwd: Path):
        self.cwd = cwd
        self.memory_file = cwd / "SAGE.md"
        self._cache: dict[str, Any] | None = None

    def exists(self) -> bool:
        """Check if SAGE.md exists."""
        return self.memory_file.exists()

    def create(self) -> None:
        """Create a default SAGE.md file."""
        self.memory_file.write_text(self.DEFAULT_TEMPLATE)

    def load(self) -> str:
        """Load the project memory content."""
        if self.exists():
            return self.memory_file.read_text(encoding="utf-8", errors="replace")
        return ""

    def get_rules(self) -> list[str]:
        """Extract rules from the memory file."""
        content = self.load()
        rules = []
        if not content:
            return rules
            
        in_rules_section = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("## Coding Style") or line.startswith("## Architecture Rules") or line.startswith("## Forbidden Patterns"):
                in_rules_section = True
                continue
            elif line.startswith("##"):
                in_rules_section = False
                continue
                
            if in_rules_section and line.startswith("-"):
                rules.append(line[1:].strip())
        return rules

    def get_custom_commands(self) -> dict[str, str]:
        """Extract custom command shortcuts."""
        content = self.load()
        commands = {}

        in_commands = False
        for line in content.split("\n"):
            if "## Custom Commands" in line:
                in_commands = True
            elif line.startswith("## "):
                in_commands = False
            elif in_commands and line.strip().startswith("# "):
                parts = line.strip()[2:].split(":", 1)
                if len(parts) == 2:
                    commands[parts[0].strip()] = parts[1].strip()

        return commands

    def get_context_injection(self) -> str:
        """Get context to inject into system prompt."""
        if not self.exists():
            return ""

        rules = self.get_rules()
        if not rules:
            return ""

        return "\n\n## Project-Specific Rules (from SAGE.md)\n" + "\n".join(
            f"- {r}" for r in rules[:20]
        )


# ── D13: Persistent session-spanning memory ──────────────────────────────


_VALID_MEMORY_TYPES = ("user", "feedback", "project", "reference")
_SLUG_RE = re.compile(r"[^A-Za-z0-9_-]+")


def _slugify(name: str) -> str:
    slug = _SLUG_RE.sub("_", name.strip().lower()).strip("_")
    return slug or "memory"


@dataclass
class Memory:
    """A single memory record."""

    name: str
    type: str
    description: str
    content: str
    path: Path | None = None  # populated when loaded from disk


class MemoryStore:
    """File-backed memory store rooted at `<root>/memory/`.

    Pass a project root (or `~/.sage` for user-wide memory). The
    `memory/` subdirectory is created lazily on first save. Each memory
    becomes its own markdown file with YAML frontmatter; an auto-
    maintained `MEMORY.md` indexes them.
    """

    def __init__(self, root: Path) -> None:
        self._root = Path(root)
        self._dir = self._root / "memory"
        self._index = self._dir / "MEMORY.md"

    def _ensure_dir(self) -> None:
        self._dir.mkdir(parents=True, exist_ok=True)

    def _file_for(self, name: str) -> Path:
        return self._dir / f"{_slugify(name)}.md"

    def _write_index(self, memories: list["Memory"]) -> None:
        lines = [
            "# MEMORY (auto-maintained — do not hand-edit unless removing entries)",
            "",
        ]
        for kind in _VALID_MEMORY_TYPES:
            in_kind = [m for m in memories if m.type == kind]
            if not in_kind:
                continue
            lines.append(f"## {kind}")
            for m in in_kind:
                file_name = (m.path or self._file_for(m.name)).name
                hook = m.description.replace("\n", " ").strip()
                if len(hook) > 110:
                    hook = hook[:107].rstrip() + "..."
                lines.append(f"- [{m.name}]({file_name}) — {hook}")
            lines.append("")
        self._index.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    def save(self, name: str, description: str, type: str, content: str) -> "Memory":
        """Persist a memory. Overwrites if a memory of the same name exists."""
        if type not in _VALID_MEMORY_TYPES:
            raise ValueError(
                f"invalid type {type!r}; expected one of {_VALID_MEMORY_TYPES}"
            )
        self._ensure_dir()
        path = self._file_for(name)
        body = (
            "---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            f"type: {type}\n"
            "---\n\n"
            f"{content.rstrip()}\n"
        )
        path.write_text(body, encoding="utf-8")
        memory = Memory(name=name, type=type, description=description,
                        content=content, path=path)
        self._write_index(self.load_all())
        return memory

    def load_all(self, type_filter: str | None = None) -> list["Memory"]:
        if not self._dir.is_dir():
            return []
        out: list[Memory] = []
        for path in sorted(self._dir.glob("*.md")):
            if path.name == "MEMORY.md":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            mem = self._parse(path, text)
            if mem is None:
                continue
            if type_filter and mem.type != type_filter:
                continue
            out.append(mem)
        return out

    def _parse(self, path: Path, text: str) -> "Memory | None":
        if not text.startswith("---"):
            return None
        try:
            _, fm, body = text.split("---", 2)
        except ValueError:
            return None
        meta: dict[str, str] = {}
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        if "name" not in meta or "type" not in meta:
            return None
        return Memory(
            name=meta["name"],
            type=meta.get("type", "user"),
            description=meta.get("description", ""),
            content=body.strip(),
            path=path,
        )

    def delete(self, name: str) -> bool:
        path = self._file_for(name)
        if not path.exists():
            return False
        path.unlink()
        if self._dir.is_dir():
            self._write_index(self.load_all())
        return True

    def format_for_prompt(self, max_chars: int = 4000) -> str:
        """Render the memory store as a markdown section for prompt injection.

        Returns an empty string when there are no memories. `max_chars`
        caps the section so a runaway memory file can't blow up the
        system prompt. Entries are truncated proportionally.
        """
        memories = self.load_all()
        if not memories:
            return ""

        header = "## SESSION MEMORY (from prior conversations)\n"
        sections: list[str] = []
        per_memory_budget = max(
            200, (max_chars - len(header) - 100) // max(1, len(memories))
        )
        for m in memories:
            content = m.content
            if len(content) > per_memory_budget:
                content = content[:per_memory_budget - 3].rstrip() + "..."
            sections.append(
                f"### {m.name} ({m.type}) — {m.description}\n{content}\n"
            )

        body = "\n".join(sections)
        out = header + body
        if len(out) > max_chars:
            out = out[:max_chars - 3].rstrip() + "..."
        return out
