"""Shared loader and fixtures for derive_customization_disposition tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    """Load scripts/derive_customization_disposition.py as a module."""
    repo_root = Path(__file__).resolve().parents[3]
    script_path = repo_root / "scripts" / "derive_customization_disposition.py"
    spec = importlib.util.spec_from_file_location("derive_customization_disposition", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load derive_customization_disposition.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    # sys.modules registration is required so that @dataclass can resolve
    # forward references via sys.modules.get(cls.__module__).__dict__.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


derive = _load_module()

REPO_ROOT = Path(__file__).resolve().parents[3]

WRAPPER_BODY = """
## Purpose

Add a comment.

## Actions

1. Run the command:

   ```bash
   agdt-add-jira-comment
   ```

## Expected Outcome

A comment is added.
"""


def unit(
    *,
    slug: str = "agdt.add-jira-comment",
    kind: str = "agent",
    frontmatter: str = "",
    body: str = WRAPPER_BODY,
):
    """Build a Unit for one file."""
    suffix = ".agent.md" if kind == "agent" else ".prompt.md"
    directory = derive.AGENTS_DIR if kind == "agent" else derive.PROMPTS_DIR
    return derive.Unit(
        path=f"{directory}/{slug}{suffix}",
        slug=slug,
        kind=kind,
        frontmatter=frontmatter,
        body=body,
    )


def row(
    *,
    path: str = ".github/agents/agdt.example.agent.md",
    slug: str = "agdt.example",
    disposition: str = "skill",
    group: str = "singleton-a",
    target: str = "agdt-example",
    batch: str = "residue",
    reason: str = "",
):
    """Build a Row."""
    return derive.Row(
        path=path,
        slug=slug,
        disposition=disposition,
        group=group,
        target=target,
        batch=batch,
        reason=reason,
    )
