"""
cvc.agent.memory — Persistent memory across sessions.

Stores a summary of each session in ~/.cvc/memory.md so the agent can
automatically recall what was worked on previously. Also supports an
embedding-based memory index for semantic recall.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from cvc.core.models import get_global_config_dir

logger = logging.getLogger("cvc.agent.memory")

MEMORY_FILE = "memory.md"
MEMORY_INDEX_FILE = "memory_index.json"
MAX_MEMORY_ENTRIES = 50
MAX_SESSION_SUMMARY_LEN = 500


def _memory_dir() -> Path:
    """Get the global CVC directory for memory storage."""
    d = get_global_config_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _memory_path() -> Path:
    return _memory_dir() / MEMORY_FILE


def _index_path() -> Path:
    return _memory_dir() / MEMORY_INDEX_FILE


def load_memory() -> str:
    """
    Load the persistent memory file.
    Returns the content as a string, or empty string if no memory exists.
    """
    path = _memory_path()
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return ""
    return ""


def load_memory_entries() -> list[dict[str, Any]]:
    """Load the structured memory index."""
    path = _index_path()
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_memory_entry(
    workspace: str,
    summary: str,
    topics: list[str] | None = None,
    model: str = "",
    turn_count: int = 0,
    cost_usd: float = 0.0,
) -> None:
    """
    Append a session summary to the memory file and index.
    """
    now = datetime.now()

    # Update the markdown memory file
    md_path = _memory_path()
    entry_md = (
        f"\n---\n"
        f"## Session: {now.strftime('%Y-%m-%d %H:%M')}\n"
        f"- **Workspace**: {workspace}\n"
        f"- **Model**: {model}\n"
        f"- **Turns**: {turn_count}\n"
    )
    if cost_usd > 0:
        entry_md += f"- **Cost**: ${cost_usd:.4f}\n"
    if topics:
        entry_md += f"- **Topics**: {', '.join(topics)}\n"
    entry_md += f"\n{summary}\n"

    try:
        existing = md_path.read_text(encoding="utf-8") if md_path.exists() else (
            "# CVC Agent Memory\n\n"
            "This file stores summaries of past sessions for context.\n"
        )
        md_path.write_text(existing + entry_md, encoding="utf-8")
    except OSError as e:
        logger.warning("Failed to save memory: %s", e)

    # Update the structured index
    entries = load_memory_entries()
    entries.append({
        "timestamp": time.time(),
        "date": now.isoformat(),
        "workspace": workspace,
        "summary": summary[:MAX_SESSION_SUMMARY_LEN],
        "topics": topics or [],
        "model": model,
        "turn_count": turn_count,
        "cost_usd": cost_usd,
    })

    # Keep only the most recent entries
    entries = entries[-MAX_MEMORY_ENTRIES:]

    try:
        _index_path().write_text(
            json.dumps(entries, indent=2, default=str),
            encoding="utf-8",
        )
    except OSError as e:
        logger.warning("Failed to save memory index: %s", e)


def get_relevant_memories(workspace: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Get the most relevant past session memories for a workspace.
    Returns recent sessions for the same workspace, plus the most recent
    sessions from any workspace.
    """
    entries = load_memory_entries()
    if not entries:
        return []

    # Prioritize same-workspace sessions
    same_workspace = [e for e in entries if e.get("workspace") == workspace]
    other = [e for e in entries if e.get("workspace") != workspace]

    # Take recent same-workspace entries and fill with others
    result = same_workspace[-limit:]
    remaining = limit - len(result)
    if remaining > 0:
        result.extend(other[-remaining:])

    return result


def build_memory_context(workspace: str) -> str:
    """
    Build a memory context string for injection into the system prompt.
    Returns empty string if no relevant memories exist.
    """
    memories = get_relevant_memories(workspace, limit=5)
    if not memories:
        return ""

    parts = ["## Previous Session Memory"]
    for mem in memories:
        date = mem.get("date", "unknown")[:16]
        ws = mem.get("workspace", "?")
        summary = mem.get("summary", "")
        topics = mem.get("topics", [])

        part = f"- **{date}** ({ws})"
        if topics:
            part += f" — Topics: {', '.join(topics)}"
        part += f"\n  {summary}"
        parts.append(part)

    return "\n".join(parts)


def generate_session_summary(messages: list[dict]) -> tuple[str, list[str]]:
    """
    Generate a brief summary and topic list from conversation messages.
    This is a heuristic-based summary (not LLM-generated to avoid cost).
    """
    topics: set[str] = set()
    user_msgs: list[str] = []
    files_mentioned: set[str] = set()

    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, str) and content.strip():
                user_msgs.append(content[:200])

        # Track file operations
        if msg.get("role") == "assistant" and msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {})
                name = fn.get("name", "")
                if name in ("read_file", "write_file", "edit_file"):
                    try:
                        args = json.loads(fn.get("arguments", "{}"))
                        if "path" in args:
                            files_mentioned.add(args["path"])
                    except (json.JSONDecodeError, TypeError):
                        pass

                # Track topics from tool names
                if "cvc_" in name:
                    topics.add("CVC operations")
                elif name == "bash":
                    topics.add("shell commands")
                elif name in ("read_file", "write_file", "edit_file"):
                    topics.add("file editing")
                elif name in ("glob", "grep"):
                    topics.add("code search")

    # Build summary from first and last user messages
    summary_parts = []
    if user_msgs:
        summary_parts.append(f"Started with: {user_msgs[0][:100]}")
        if len(user_msgs) > 1:
            summary_parts.append(f"Last topic: {user_msgs[-1][:100]}")

    if files_mentioned:
        files_list = ", ".join(sorted(files_mentioned)[:5])
        summary_parts.append(f"Files touched: {files_list}")
        topics.add("file editing")

    summary = ". ".join(summary_parts) if summary_parts else "Brief session"

    return summary, list(topics)


# ── Topic-based auto-memory (Claude Code MEMORY.md equivalent) ───────────

def _project_memory_dir(workspace: str) -> Path:
    """Per-project memory directory under ~/.cvc/projects/<hash>/memory/."""
    import hashlib
    project_hash = hashlib.sha256(workspace.encode()).hexdigest()[:12]
    d = get_global_config_dir() / "projects" / project_hash / "memory"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_topic_memory(workspace: str, topic: str, content: str) -> str:
    """
    Save a memory entry under a topic file.

    This is called when the LLM wants to save a learned pattern, insight,
    or preference for future reference.

    Parameters
    ----------
    workspace : str
        The workspace path.
    topic : str
        Topic name (e.g., 'debugging', 'patterns', 'architecture').
        Will be sanitized for use as a filename.
    content : str
        The content to append to the topic file.

    Returns
    -------
    str
        Confirmation message.
    """
    import re as _re
    # Sanitize topic name for filename
    safe_topic = _re.sub(r"[^\w\-]", "_", topic.lower().strip())[:50]
    if not safe_topic:
        safe_topic = "general"

    mem_dir = _project_memory_dir(workspace)
    topic_path = mem_dir / f"{safe_topic}.md"

    # Append to topic file
    try:
        existing = topic_path.read_text(encoding="utf-8") if topic_path.exists() else ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        entry = f"\n## {timestamp}\n{content.strip()}\n"
        topic_path.write_text(existing + entry, encoding="utf-8")

        # Update the MEMORY.md index
        _update_memory_index(mem_dir)

        return f"Saved to memory: {safe_topic} ({len(content)} chars)"
    except OSError as e:
        logger.warning("Failed to save topic memory: %s", e)
        return f"Error saving memory: {e}"


def load_topic_memory(workspace: str, topic: str) -> str:
    """Load memory for a specific topic."""
    import re as _re
    safe_topic = _re.sub(r"[^\w\-]", "_", topic.lower().strip())[:50]
    mem_dir = _project_memory_dir(workspace)
    topic_path = mem_dir / f"{safe_topic}.md"

    if topic_path.exists():
        try:
            return topic_path.read_text(encoding="utf-8")
        except OSError:
            return ""
    return ""


def load_memory_index(workspace: str) -> str:
    """
    Load the MEMORY.md index (first 200 lines).
    This is auto-injected into the system prompt.
    """
    mem_dir = _project_memory_dir(workspace)
    index_path = mem_dir / "MEMORY.md"

    if not index_path.exists():
        return ""

    try:
        text = index_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > 200:
            return "\n".join(lines[:200]) + f"\n... ({len(lines) - 200} more lines)"
        return text
    except OSError:
        return ""


def _update_memory_index(mem_dir: Path) -> None:
    """Regenerate the MEMORY.md index from topic files."""
    index_path = mem_dir / "MEMORY.md"

    lines = ["# CVC Agent Memory Index", ""]
    lines.append("Auto-generated index of learned patterns and insights.")
    lines.append("Topic files are stored in this directory.")
    lines.append("")

    for topic_file in sorted(mem_dir.glob("*.md")):
        if topic_file.name == "MEMORY.md":
            continue
        try:
            text = topic_file.read_text(encoding="utf-8")
            line_count = len(text.splitlines())
            # Get the first non-empty, non-heading line as a preview
            preview = ""
            for line in text.splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
                    preview = stripped[:80]
                    break
            lines.append(f"- **{topic_file.stem}** ({line_count} lines): {preview}")
        except OSError:
            continue

    try:
        index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        pass


def list_topic_memories(workspace: str) -> list[dict[str, Any]]:
    """List all topic memory files for a workspace."""
    mem_dir = _project_memory_dir(workspace)
    result: list[dict[str, Any]] = []

    for topic_file in sorted(mem_dir.glob("*.md")):
        if topic_file.name == "MEMORY.md":
            continue
        try:
            text = topic_file.read_text(encoding="utf-8")
            result.append({
                "topic": topic_file.stem,
                "lines": len(text.splitlines()),
                "size": len(text),
            })
        except OSError:
            continue

    return result
