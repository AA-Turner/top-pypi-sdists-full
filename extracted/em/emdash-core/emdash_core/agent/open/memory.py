"""Multi-layer memory system for Open Agent.

Provides a two-layer memory architecture:
- Long-term Memory: Learned preferences and capabilities (evolves slowly)
- Short-term Memory: Recent context and session state (ephemeral)

User identity is stored in .emdash/rules/USER.md (not in memory).
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any, Set
from collections import deque
import hashlib


@dataclass
class MemoryEntry:
    """A single memory entry with metadata."""

    content: str
    context: str
    importance: float = 1.0  # 0.0-1.0, higher = more important
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_accessed: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 1
    source: str = "user"  # user, inference, system
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryEntry":
        return cls(**data)

    def touch(self) -> None:
        """Update last accessed time and count."""
        self.last_accessed = datetime.now().isoformat()
        self.access_count += 1


class LongTermMemory:
    """Long-term memory layer - learned preferences and patterns.

    This layer contains:
    - Learned preferences (coding style, communication style)
    - Recurring patterns and workflows
    - Successful strategies that worked for user
    - Important facts about projects/contexts

    Uses importance scoring and access patterns for retention.
    """

    MAX_ENTRIES = 100
    DECAY_DAYS = 90  # Entries decay after 90 days without access

    def __init__(self, storage_path: Optional[Path] = None):
        self.entries: Dict[str, MemoryEntry] = {}
        self._storage_path = storage_path or Path(".emdash/memory/long_term.json")
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        """Load long-term memory from storage."""
        if self._storage_path.exists():
            try:
                with open(self._storage_path, "r") as f:
                    data = json.load(f)
                self.entries = {
                    k: MemoryEntry.from_dict(v) for k, v in data.get("entries", {}).items()
                }
                self._decay_entries()
            except Exception as e:
                print(f"Warning: Could not load long-term memory: {e}")

    def _save(self) -> None:
        """Save long-term memory to storage."""
        data = {
            "layer": "long_term",
            "updated_at": datetime.now().isoformat(),
            "entry_count": len(self.entries),
            "entries": {k: v.to_dict() for k, v in self.entries.items()},
        }
        with open(self._storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def _decay_entries(self) -> None:
        """Remove or decay old entries based on last access."""
        now = datetime.now()
        to_remove = []

        for key, entry in self.entries.items():
            last_access = datetime.fromisoformat(entry.last_accessed)
            days_since = (now - last_access).days

            if days_since > self.DECAY_DAYS:
                # Decay importance based on time
                decay_factor = 0.9 ** (days_since / 30)  # Decay monthly
                entry.importance *= decay_factor

                if entry.importance < 0.1:
                    to_remove.append(key)

        for key in to_remove:
            del self.entries[key]

    def store(
        self,
        key: str,
        content: str,
        importance: float = 0.5,
        context: str = "general",
        tags: Optional[List[str]] = None,
        source: str = "inference",
    ) -> None:
        """Store a long-term memory.

        Args:
            key: Memory identifier
            content: The information to store
            importance: Retention priority (0.0-1.0)
            context: Category/domain
            tags: Optional tags
            source: How this was learned (user, inference, system)
        """
        # Check capacity
        if key not in self.entries and len(self.entries) >= self.MAX_ENTRIES:
            # Remove least important and least accessed
            sorted_entries = sorted(
                self.entries.items(),
                key=lambda x: (x[1].importance, x[1].access_count)
            )
            if sorted_entries[0][1].importance < importance:
                del self.entries[sorted_entries[0][0]]
            else:
                return

        self.entries[key] = MemoryEntry(
            content=content,
            context=context,
            importance=importance,
            source=source,
            tags=tags or [],
        )
        self._save()

    def get(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve a memory and update access stats."""
        entry = self.entries.get(key)
        if entry:
            entry.touch()
            self._save()
        return entry

    def query(self, query_text: str, context: Optional[str] = None, top_k: int = 5) -> List[tuple]:
        """Query memories by relevance to text.

        Simple keyword matching - could be enhanced with embeddings.
        """
        query_lower = query_text.lower()
        words = set(query_lower.split())

        scored = []
        for key, entry in self.entries.items():
            score = 0.0

            # Context match
            if context and entry.context == context:
                score += 0.3

            # Content word overlap
            entry_words = set(entry.content.lower().split())
            overlap = len(words & entry_words) / len(words | entry_words)
            score += overlap * 0.5

            # Tag match
            entry_tags = set(t.lower() for t in entry.tags)
            query_tags = words  # Treat query words as potential tags
            tag_overlap = len(entry_tags & query_tags)
            score += tag_overlap * 0.2

            # Importance boost
            score += entry.importance * 0.1

            # Recency boost
            days_since = (datetime.now() - datetime.fromisoformat(entry.last_accessed)).days
            if days_since < 7:
                score += 0.1

            scored.append((key, entry, score))

        # Sort by score and return top_k
        scored.sort(key=lambda x: -x[2])
        return [(k, e) for k, e, _ in scored[:top_k]]

    def get_by_context(self, context: str) -> Dict[str, MemoryEntry]:
        """Get all memories for a specific context."""
        return {
            k: v for k, v in self.entries.items()
            if v.context == context
        }

    def build_prompt_section(self, context: Optional[str] = None, max_entries: int = 10) -> str:
        """Build long-term memory section for system prompt."""
        entries = self.entries.values()

        if context:
            entries = [e for e in entries if e.context == context]

        # Sort by importance and recency
        sorted_entries = sorted(
            entries,
            key=lambda e: (e.importance, e.access_count),
            reverse=True
        )[:max_entries]

        if not sorted_entries:
            return ""

        lines = ["## Learned Preferences & Patterns", ""]

        # Group by context
        by_context: Dict[str, List[MemoryEntry]] = {}
        for entry in sorted_entries:
            ctx = entry.context
            if ctx not in by_context:
                by_context[ctx] = []
            by_context[ctx].append(entry)

        for ctx, ctx_entries in sorted(by_context.items()):
            lines.append(f"### {ctx.title()}")
            for entry in ctx_entries:
                conf_str = ""
                if entry.importance < 0.7:
                    conf_str = f" (confidence: {entry.importance:.0%})"
                lines.append(f"- {entry.content}{conf_str}")
            lines.append("")

        return "\n".join(lines)


class ShortTermMemory:
    """Short-term memory layer - recent context and session state.

    This layer contains:
    - Recent conversation snippets
    - Current task/project context
    - Temporary working memory
    - Session-specific facts

    Automatically pruned based on age and capacity.
    """

    MAX_ENTRIES = 50
    MAX_AGE_HOURS = 24  # Entries expire after 24 hours

    def __init__(self, session_id: str, storage_path: Optional[Path] = None):
        self.session_id = session_id
        self.entries: deque = deque(maxlen=self.MAX_ENTRIES)
        self._storage_path = storage_path or Path(f".emdash/memory/short_term/{session_id}.json")
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        """Load short-term memory if recent enough."""
        if self._storage_path.exists():
            try:
                with open(self._storage_path, "r") as f:
                    data = json.load(f)

                # Check if session is still fresh
                session_time = datetime.fromisoformat(data.get("session_time", "1970-01-01"))
                age_hours = (datetime.now() - session_time).total_seconds() / 3600

                if age_hours < self.MAX_AGE_HOURS:
                    entries_data = data.get("entries", [])
                    self.entries = deque(
                        [MemoryEntry.from_dict(e) for e in entries_data],
                        maxlen=self.MAX_ENTRIES
                    )
                else:
                    # Session expired, clear it
                    self._storage_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"Warning: Could not load short-term memory: {e}")

    def _save(self) -> None:
        """Save short-term memory to storage."""
        data = {
            "layer": "short_term",
            "session_id": self.session_id,
            "session_time": datetime.now().isoformat(),
            "entries": [e.to_dict() for e in self.entries],
        }
        with open(self._storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, content: str, context: str = "session", importance: float = 0.3, tags: Optional[List[str]] = None) -> None:
        """Add an entry to short-term memory."""
        entry = MemoryEntry(
            content=content,
            context=context,
            importance=importance,
            source="session",
            tags=tags or [],
        )
        self.entries.append(entry)
        self._save()

    def get_recent(self, n: int = 10, context: Optional[str] = None) -> List[MemoryEntry]:
        """Get most recent entries, optionally filtered by context."""
        entries = list(self.entries)
        if context:
            entries = [e for e in entries if e.context == context]
        return entries[-n:]

    def clear(self) -> None:
        """Clear short-term memory."""
        self.entries.clear()
        self._storage_path.unlink(missing_ok=True)

    def build_context_string(self, max_entries: int = 5) -> str:
        """Build recent context string for prompt augmentation."""
        recent = self.get_recent(max_entries)
        if not recent:
            return ""

        lines = ["## Recent Context", ""]
        for entry in recent:
            lines.append(f"- [{entry.context}] {entry.content}")

        return "\n".join(lines)


class HierarchicalMemory:
    """Unified interface to memory layers.

    Provides:
    - Long-term memory (learned patterns, decays slowly)
    - Short-term memory (session context, ephemeral)

    User identity is stored in .emdash/rules/USER.md.
    """

    def __init__(
        self,
        session_id: str,
        emdash_dir: Optional[Path] = None,
    ):
        self._emdash_dir = emdash_dir or Path(".emdash")
        self._memory_dir = self._emdash_dir / "memory"
        self._memory_dir.mkdir(parents=True, exist_ok=True)

        # Initialize layers
        self.long_term = LongTermMemory(self._memory_dir / "long_term.json")
        self.short_term = ShortTermMemory(session_id, self._memory_dir / f"short_term/{session_id}.json")

    def store(
        self,
        content: str,
        layer: str = "long_term",
        key: Optional[str] = None,
        importance: float = 0.5,
        context: str = "general",
        tags: Optional[List[str]] = None,
    ) -> str:
        """Store a memory in the appropriate layer.

        Args:
            content: The information to store
            layer: Which layer ("long_term", "short_term")
            key: Optional identifier (auto-generated if not provided)
            importance: How important this memory is
            context: Category/domain
            tags: Optional tags

        Returns:
            The key used to store the memory
        """
        if key is None:
            # Generate key from content hash
            key = hashlib.md5(content.encode()).hexdigest()[:12]

        if layer == "long_term":
            self.long_term.store(key, content, importance, context, tags)
        elif layer == "short_term":
            self.short_term.add(content, context, importance, tags)

        return key

    def query(
        self,
        query: str,
        layers: Optional[List[str]] = None,
        context: Optional[str] = None,
        top_k: int = 5,
    ) -> Dict[str, List[tuple]]:
        """Query memory layers.

        Args:
            query: Search query
            layers: Which layers to search (defaults to all)
            context: Optional context filter
            top_k: Max results per layer

        Returns:
            Dict mapping layer names to results
        """
        layers = layers or ["long_term", "short_term"]
        results = {}

        if "long_term" in layers:
            results["long_term"] = self.long_term.query(query, context, top_k)

        if "short_term" in layers:
            # Recent entries from short-term, filtered by query text
            recent = self.short_term.get_recent(self.short_term.MAX_ENTRIES, context)
            query_lower = query.lower()
            query_words = set(query_lower.split())
            scored = []
            for i, entry in enumerate(recent):
                entry_lower = entry.content.lower()
                # Substring match
                if query_lower in entry_lower:
                    scored.append((f"session_{i}", entry, 1.0))
                    continue
                # Word overlap
                entry_words = set(entry_lower.split())
                overlap = len(query_words & entry_words)
                if overlap > 0:
                    scored.append((f"session_{i}", entry, overlap / len(query_words)))
            scored.sort(key=lambda x: -x[2])
            results["short_term"] = [(k, e) for k, e, _ in scored[:top_k]]

        return results

    def build_system_prompt(self, context: Optional[str] = None) -> str:
        """Build complete memory-augmented system prompt."""
        sections = []

        # Long-term preferences
        long_term_section = self.long_term.build_prompt_section(context)
        if long_term_section:
            sections.append(long_term_section)

        # Short-term context
        short_term_section = self.short_term.build_context_string()
        if short_term_section:
            sections.append(short_term_section)

        return "\n\n".join(sections)

    def consolidate_short_term(self) -> List[Dict]:
        """Analyze short-term memory and suggest long-term consolidation.

        Returns:
            List of suggested memories to promote to long-term
        """
        suggestions = []

        # Find frequently mentioned topics in short-term
        from collections import Counter

        all_content = " ".join([e.content for e in self.short_term.entries])
        words = [w.lower() for w in all_content.split() if len(w) > 4]
        frequent = Counter(words).most_common(10)

        # Check for patterns that should be remembered
        for entry in self.short_term.entries:
            # High importance short-term memories are candidates
            if entry.importance > 0.7:
                suggestions.append({
                    "content": entry.content,
                    "context": entry.context,
                    "reason": "high_importance",
                    "suggested_layer": "long_term",
                })

        return suggestions

    def export_all(self) -> dict:
        """Export all memory layers."""
        return {
            "long_term": {
                "entries": {k: v.to_dict() for k, v in self.long_term.entries.items()},
            },
            "short_term": {
                "session_id": self.short_term.session_id,
                "entries": [e.to_dict() for e in self.short_term.entries],
            },
        }

    def reset(self, layer: Optional[str] = None) -> None:
        """Reset memory layer(s).

        Args:
            layer: Which layer to reset ("long_term", "short_term", or None for all)
        """
        if layer is None or layer == "long_term":
            self.long_term.entries.clear()
            self.long_term._save()

        if layer is None or layer == "short_term":
            self.short_term.clear()

    def get_stats(self) -> dict:
        """Get memory statistics."""
        return {
            "long_term": {
                "entry_count": len(self.long_term.entries),
                "max_entries": self.long_term.MAX_ENTRIES,
            },
            "short_term": {
                "entry_count": len(self.short_term.entries),
                "max_entries": self.short_term.MAX_ENTRIES,
            },
        }

    # ------------------------------------------------------------------
    # Daily markdown log (pre-compaction memory flush target)
    # ------------------------------------------------------------------

    def append_daily_log(self, content: str, heading: Optional[str] = None) -> Path:
        """Append a block to today's daily log at ``memory/daily/YYYY-MM-DD.md``.

        This is the durable write target for the pre-compaction memory flush.
        Each call appends under a timestamped heading so that multiple flushes
        in one day accumulate rather than overwrite.

        Args:
            content: Markdown text to append.
            heading: Optional heading for this block.  Defaults to
                ``"Memory flush at HH:MM"``.

        Returns:
            Path to the daily log file.
        """
        daily_dir = self._memory_dir / "daily"
        daily_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_path = daily_dir / f"{today}.md"

        if heading is None:
            heading = f"Memory flush at {datetime.now().strftime('%H:%M')}"

        block = f"\n## {heading}\n\n{content.strip()}\n"

        # Create the file with a title if new
        if not log_path.exists():
            block = f"# Daily Log — {today}\n{block}"

        with open(log_path, "a") as f:
            f.write(block)

        return log_path
