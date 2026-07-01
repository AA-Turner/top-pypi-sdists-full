"""
cvc.agent.instructions — CVC.md instruction loader (Claude Code CLAUDE.md equivalent).

Loads hierarchical project instructions from CVC.md files:
  1. ~/.cvc/CVC.md — user-global instructions (all projects)
  2. <workspace>/CVC.md — project instructions (checked in)
  3. <workspace>/CVC.local.md — local overrides (not checked in)
  4. <workspace>/.cvc/CVC.md — alternative location
  5. <workspace>/.cvc/rules/*.md — path-specific rules with YAML frontmatter

Features:
  - @import syntax: `@path/to/file.md` inlines another file
  - Path-specific rules: frontmatter `paths: ["src/**"]` limits scope
  - Size warning: > 200 lines degrades LLM adherence
  - Auto-loaded at session start, re-injected after compaction
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.instructions")

MAX_INSTRUCTION_LINES = 200  # Warn if total instructions exceed this


def load_instructions(workspace: Path) -> str:
    """
    Load and merge instructions from all CVC.md files.

    Returns the combined instruction text to be injected into the system prompt.
    """
    workspace = workspace.resolve()
    sections: list[str] = []

    # Level 1: User-global instructions
    user_cvc_md = Path.home() / ".cvc" / "CVC.md"
    if user_cvc_md.exists():
        text = _load_with_imports(user_cvc_md)
        if text:
            sections.append(f"# User Instructions (global)\n{text}")

    # Level 2a: Project CVC.md in workspace root
    project_cvc_md = workspace / "CVC.md"
    if project_cvc_md.exists():
        text = _load_with_imports(project_cvc_md)
        if text:
            sections.append(f"# Project Instructions\n{text}")

    # Level 2b: Alternative location in .cvc/
    alt_cvc_md = workspace / ".cvc" / "CVC.md"
    if alt_cvc_md.exists() and not project_cvc_md.exists():
        text = _load_with_imports(alt_cvc_md)
        if text:
            sections.append(f"# Project Instructions\n{text}")

    # Level 3: Local overrides
    local_cvc_md = workspace / "CVC.local.md"
    if local_cvc_md.exists():
        text = _load_with_imports(local_cvc_md)
        if text:
            sections.append(f"# Local Instructions (not committed)\n{text}")

    # Level 4: Path-specific rules
    rules_dir = workspace / ".cvc" / "rules"
    if rules_dir.is_dir():
        for rule_file in sorted(rules_dir.glob("*.md")):
            rule = _load_rule(rule_file)
            if rule:
                sections.append(rule)

    combined = "\n\n".join(sections)

    # Size warning
    line_count = combined.count("\n") + 1
    if line_count > MAX_INSTRUCTION_LINES:
        logger.warning(
            "CVC.md instructions are %d lines (recommended max: %d). "
            "Very long instructions may degrade LLM adherence.",
            line_count, MAX_INSTRUCTION_LINES,
        )

    return combined


def _load_with_imports(path: Path, depth: int = 0) -> str:
    """Load a file and process @import directives."""
    if depth > 5:  # Prevent infinite recursion
        return ""

    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as e:
        logger.warning("Failed to read %s: %s", path, e)
        return ""

    # Process @import directives: @path/to/file.md
    def _resolve_import(match: re.Match) -> str:
        import_path = match.group(1).strip()
        resolved = path.parent / import_path
        if resolved.exists() and resolved.is_file():
            return _load_with_imports(resolved, depth + 1)
        logger.warning("Import not found: %s (from %s)", import_path, path)
        return f"<!-- Import not found: {import_path} -->"

    text = re.sub(r"^@(.+)$", _resolve_import, text, flags=re.MULTILINE)
    return text


def _load_rule(rule_file: Path) -> str | None:
    """Load a path-specific rule file with optional YAML frontmatter."""
    try:
        text = rule_file.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return None

    paths: list[str] = []
    body = text

    # Extract YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if fm_match:
        body = text[fm_match.end():]
        try:
            import yaml
            fm = yaml.safe_load(fm_match.group(1)) or {}
            paths = fm.get("paths", [])
        except ImportError:
            # Minimal parsing
            for line in fm_match.group(1).splitlines():
                if line.strip().startswith("paths:"):
                    rest = line.split(":", 1)[1].strip()
                    if rest.startswith("[") and rest.endswith("]"):
                        paths = [p.strip().strip("'\"") for p in rest[1:-1].split(",")]

    if not body:
        return None

    if paths:
        paths_str = ", ".join(paths)
        return f"# Rule: {rule_file.name} (applies to: {paths_str})\n{body}"
    return f"# Rule: {rule_file.name}\n{body}"


def get_applicable_rules(
    workspace: Path,
    file_path: str,
) -> list[str]:
    """Get rules that apply to a specific file path."""
    from fnmatch import fnmatch

    rules_dir = workspace / ".cvc" / "rules"
    if not rules_dir.is_dir():
        return []

    applicable: list[str] = []
    for rule_file in sorted(rules_dir.glob("*.md")):
        try:
            text = rule_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not fm_match:
            continue

        body = text[fm_match.end():]
        paths: list[str] = []
        try:
            import yaml
            fm = yaml.safe_load(fm_match.group(1)) or {}
            paths = fm.get("paths", [])
        except ImportError:
            for line in fm_match.group(1).splitlines():
                if line.strip().startswith("paths:"):
                    rest = line.split(":", 1)[1].strip()
                    if rest.startswith("[") and rest.endswith("]"):
                        paths = [p.strip().strip("'\"") for p in rest[1:-1].split(",")]

        # Normalize file path
        rel_path = file_path.replace("\\", "/")
        for pattern in paths:
            if fnmatch(rel_path, pattern):
                applicable.append(body.strip())
                break

    return applicable
