"""Project memory for SAGE.

Provides persistent project rules and context via SAGE.md file.
"""

from __future__ import annotations

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
