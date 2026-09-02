from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Standard configs we want to surface to the UI for human review instead of silently injecting
TARGET_CONTEXT_FILES = [
    ".cursorrules",
    "CLAUDE.md",
    "AGENTS.md",
    ".antigravity/rules.md",
    ".matrx/skills/default.md",
]


def sniff_workspace_contexts(workspace_root: str | Path) -> dict[str, str]:
    """
    Scans the provided workspace root for known agentic/coding environment configs.
    
    Instead of auto-injecting these into the system prompt, they are read 
    into a dictionary. The UnifiedResponse API can attach these as 'detected_contexts' 
    so the human operator in the Cloud UI can explicitly review and enable them.
    
    Returns:
        A dictionary mapping the filename (e.g., '.cursorrules') to its raw content.
    """
    root = Path(workspace_root)
    detected: dict[str, str] = {}

    if not root.is_absolute() or not root.is_dir():
        return detected

    for target in TARGET_CONTEXT_FILES:
        target_path = root / target
        if target_path.is_file():
            try:
                content = target_path.read_text(encoding="utf-8", errors="replace")
                if len(content.strip()) > 0:
                    detected[target] = content
            except Exception as e:
                logger.warning(f"Failed to read context file {target_path}: {e}")

    return detected
