"""
Advanced context management for SAGE.

P1-51: Implement semantic summarization of trimmed context
P1-52: Add embedding-based relevance scoring
P1-53: Improve token estimation accuracy
P1-54: Add conversation branching/versioning
P1-55: Implement conversation search/filtering (Token display in tokens.py)
P1-56: Add explicit importance ranking
P1-57: Implement semantic-aware trimming
P1-58: Add conversation merging/consolidation
P1-59: Implement inter-conversation context sharing
P1-60: Add vector embeddings for semantic search
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# =============================================================================
# Importance Ranking (P1-56)
# =============================================================================


class ImportanceLevel(Enum):
    """Importance levels for context content."""

    CRITICAL = 5  # Must never be removed
    HIGH = 4  # Very important, remove only if necessary
    MEDIUM = 3  # Moderately important
    LOW = 2  # Can be removed if needed
    TRIVIAL = 1  # First to be removed


@dataclass
class ImportanceMarker:
    """A marker that indicates importance in text."""

    pattern: str
    level: ImportanceLevel
    description: str


class ImportanceRanker:
    """
    Ranks content by importance.

    P1-56: Add explicit importance ranking
    """

    MARKERS = [
        # Critical markers
        ImportanceMarker(r"\bCRITICAL\b", ImportanceLevel.CRITICAL, "Critical information"),
        ImportanceMarker(r"\bIMPORTANT\b", ImportanceLevel.HIGH, "Important note"),
        ImportanceMarker(r"\bARCHITECTURE\b", ImportanceLevel.HIGH, "Architecture decision"),
        ImportanceMarker(r"\bDECISION\b", ImportanceLevel.HIGH, "Key decision"),
        ImportanceMarker(r"\bSECURITY\b", ImportanceLevel.HIGH, "Security concern"),
        # Code-related
        ImportanceMarker(r"```[\w]*\n", ImportanceLevel.MEDIUM, "Code block"),
        ImportanceMarker(r"\bFILE:\s*\S+", ImportanceLevel.MEDIUM, "File reference"),
        ImportanceMarker(r"\bTODO\b", ImportanceLevel.MEDIUM, "TODO item"),
        ImportanceMarker(r"\bFIXME\b", ImportanceLevel.MEDIUM, "FIXME item"),
        # Low importance
        ImportanceMarker(r"^\s*$", ImportanceLevel.TRIVIAL, "Empty line"),
        ImportanceMarker(r"^#\s", ImportanceLevel.LOW, "Comment"),
    ]

    def __init__(self, custom_markers: list[ImportanceMarker] | None = None):
        self.markers = self.MARKERS + (custom_markers or [])
        self._compiled = [(re.compile(m.pattern, re.MULTILINE), m) for m in self.markers]

    def rank(self, text: str) -> ImportanceLevel:
        """Rank the importance of text."""
        max_level = ImportanceLevel.LOW

        for pattern, marker in self._compiled:
            if pattern.search(text):
                if marker.level.value > max_level.value:
                    max_level = marker.level

        return max_level

    def rank_messages(
        self,
        messages: list[dict[str, str]],
    ) -> list[tuple[dict[str, str], ImportanceLevel]]:
        """Rank a list of messages by importance."""
        return [(msg, self.rank(msg.get("content", ""))) for msg in messages]

    def filter_by_importance(
        self,
        messages: list[dict[str, str]],
        min_level: ImportanceLevel,
    ) -> list[dict[str, str]]:
        """Filter messages by minimum importance level."""
        ranked = self.rank_messages(messages)
        return [msg for msg, level in ranked if level.value >= min_level.value]


# =============================================================================
# Semantic Summarization (P1-51)
# =============================================================================


class ContextSummarizer:
    """
    Summarizes context to preserve meaning while reducing tokens.

    P1-51: Implement semantic summarization of trimmed context
    """

    def __init__(self, model_callback: Callable[[str], str] | None = None):
        self.model_callback = model_callback
        self._summary_cache: dict[str, str] = {}

    def summarize_conversation(
        self,
        messages: list[dict[str, str]],
        max_summary_tokens: int = 500,
    ) -> str:
        """Summarize a conversation into key points."""
        # Create cache key
        content_hash = hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest()[
            :16
        ]

        if content_hash in self._summary_cache:
            return self._summary_cache[content_hash]

        # If we have a model callback, use it
        if self.model_callback:
            prompt = self._build_summary_prompt(messages, max_summary_tokens)
            summary = self.model_callback(prompt)
            self._summary_cache[content_hash] = summary
            return summary

        # Fallback to extractive summarization
        summary = self._extractive_summarize(messages, max_summary_tokens)
        self._summary_cache[content_hash] = summary
        return summary

    def _build_summary_prompt(
        self,
        messages: list[dict[str, str]],
        max_tokens: int,
    ) -> str:
        """Build prompt for LLM summarization."""
        conversation_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)

        return f"""Summarize this conversation into key points. Focus on:
1. Main topics discussed
2. Key decisions made
3. Code changes mentioned
4. Important context for future reference

Keep summary under {max_tokens} tokens.

CONVERSATION:
{conversation_text}

SUMMARY:"""

    def _extractive_summarize(
        self,
        messages: list[dict[str, str]],
        max_tokens: int,
    ) -> str:
        """Extract key sentences without LLM."""
        ranker = ImportanceRanker()
        ranked = ranker.rank_messages(messages)

        # Sort by importance
        ranked.sort(key=lambda x: x[1].value, reverse=True)

        # Extract key content
        summary_parts = []
        estimated_tokens = 0
        chars_per_token = 4

        for msg, level in ranked:
            if level.value >= ImportanceLevel.MEDIUM.value:
                content = msg.get("content", "")
                # Extract first meaningful sentence
                sentences = re.split(r"[.!?]\s+", content)
                for sent in sentences[:2]:
                    sent_tokens = len(sent) // chars_per_token
                    if estimated_tokens + sent_tokens < max_tokens:
                        summary_parts.append(f"• {sent.strip()}")
                        estimated_tokens += sent_tokens

        return "\n".join(summary_parts) if summary_parts else "No key points extracted."


# =============================================================================
# Semantic-Aware Trimming (P1-57)
# =============================================================================


class SemanticTrimmer:
    """
    Trims context while preserving semantic coherence.

    P1-57: Implement semantic-aware trimming
    """

    def __init__(
        self,
        ranker: ImportanceRanker | None = None,
        summarizer: ContextSummarizer | None = None,
    ):
        self.ranker = ranker or ImportanceRanker()
        self.summarizer = summarizer or ContextSummarizer()

    def trim(
        self,
        messages: list[dict[str, str]],
        max_tokens: int,
        preserve_recent: int = 4,
        summarize_removed: bool = True,
    ) -> tuple[list[dict[str, str]], str | None]:
        """
        Trim messages to fit within token limit.

        Args:
            messages: List of messages
            max_tokens: Maximum token count
            preserve_recent: Number of recent message pairs to always keep
            summarize_removed: Whether to summarize removed content

        Returns:
            Tuple of (trimmed_messages, summary_of_removed)
        """
        if not messages:
            return [], None

        chars_per_token = 4

        # Calculate current token count
        current_tokens = sum(len(m.get("content", "")) for m in messages) // chars_per_token

        if current_tokens <= max_tokens:
            return messages, None

        # Rank messages by importance
        ranked = self.ranker.rank_messages(messages)

        # Split into protected (recent) and candidates (older)
        protected_count = preserve_recent * 2  # pairs
        protected = messages[-protected_count:] if protected_count > 0 else []
        candidates = list(
            zip(messages[:-protected_count], [r[1] for r in ranked[:-protected_count]])
        )

        # Sort candidates by importance (least important first)
        candidates.sort(key=lambda x: x[1].value)

        # Remove messages until under limit
        removed = []
        remaining = [msg for msg, _ in candidates]

        protected_tokens = sum(len(m.get("content", "")) for m in protected) // chars_per_token
        target_tokens = max_tokens - protected_tokens

        while remaining:
            current = sum(len(m.get("content", "")) for m in remaining) // chars_per_token
            if current <= target_tokens:
                break

            # Remove least important
            removed.append(remaining.pop(0))

        # Combine remaining with protected
        result = remaining + protected

        # Summarize removed content if requested
        summary = None
        if summarize_removed and removed:
            summary = self.summarizer.summarize_conversation(removed, max_summary_tokens=200)

        return result, summary


# =============================================================================
# Conversation Branching (P1-54)
# =============================================================================


@dataclass
class ConversationBranch:
    """A branch in a conversation."""

    id: str
    parent_id: str | None
    name: str
    messages: list[dict[str, str]]
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


class BranchingConversation:
    """
    Conversation with branching support.

    P1-54: Add conversation branching/versioning
    """

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.branches: dict[str, ConversationBranch] = {}
        self.current_branch_id: str = "main"

        # Initialize main branch
        self.branches["main"] = ConversationBranch(
            id="main",
            parent_id=None,
            name="Main",
            messages=[],
        )

    def create_branch(
        self,
        name: str,
        from_branch: str | None = None,
        from_message_index: int | None = None,
    ) -> str:
        """Create a new branch from existing conversation."""
        branch_id = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:8]
        source_branch = from_branch or self.current_branch_id
        source = self.branches.get(source_branch)

        if source is None:
            raise ValueError(f"Source branch not found: {source_branch}")

        # Copy messages up to the specified index
        if from_message_index is not None:
            messages = source.messages[: from_message_index + 1].copy()
        else:
            messages = source.messages.copy()

        self.branches[branch_id] = ConversationBranch(
            id=branch_id,
            parent_id=source_branch,
            name=name,
            messages=messages,
        )

        return branch_id

    def switch_branch(self, branch_id: str) -> bool:
        """Switch to a different branch."""
        if branch_id in self.branches:
            self.current_branch_id = branch_id
            return True
        return False

    def add_message(self, role: str, content: str) -> None:
        """Add message to current branch."""
        branch = self.branches[self.current_branch_id]
        branch.messages.append({"role": role, "content": content})

    def get_messages(self, branch_id: str | None = None) -> list[dict[str, str]]:
        """Get messages from a branch."""
        branch_id = branch_id or self.current_branch_id
        return self.branches[branch_id].messages.copy()

    def get_branch_tree(self) -> dict[str, Any]:
        """Get the branch tree structure."""

        def build_tree(branch_id: str) -> dict:
            branch = self.branches[branch_id]
            children = [
                build_tree(b.id) for b in self.branches.values() if b.parent_id == branch_id
            ]
            return {
                "id": branch.id,
                "name": branch.name,
                "message_count": len(branch.messages),
                "children": children,
            }

        return build_tree("main")

    def merge_branch(self, source_id: str, target_id: str | None = None) -> bool:
        """Merge a branch into another."""
        target_id = target_id or self.current_branch_id
        source = self.branches.get(source_id)
        target = self.branches.get(target_id)

        if source is None or target is None:
            return False

        # Find divergence point
        source_msgs = source.messages
        target_msgs = target.messages

        # Simple merge: append new messages from source
        common_len = min(len(source_msgs), len(target_msgs))
        for i in range(common_len):
            if source_msgs[i] != target_msgs[i]:
                break
        else:
            i = common_len

        # Add unique messages from source
        if i < len(source_msgs):
            target.messages.extend(source_msgs[i:])

        return True


# =============================================================================
# Conversation Search (P1-55)
# =============================================================================


class ConversationSearch:
    """
    Search and filter conversations.

    P1-55: Implement conversation search/filtering
    """

    def __init__(self):
        self._index: dict[
            str, list[tuple[str, int, str]]
        ] = {}  # word -> [(conv_id, msg_idx, role)]

    def index_conversation(self, conversation_id: str, messages: list[dict[str, str]]) -> None:
        """Index a conversation for search."""
        for idx, msg in enumerate(messages):
            content = msg.get("content", "").lower()
            role = msg.get("role", "")

            # Tokenize and index
            words = re.findall(r"\b\w+\b", content)
            for word in words:
                if word not in self._index:
                    self._index[word] = []
                self._index[word].append((conversation_id, idx, role))

    def search(
        self,
        query: str,
        conversation_id: str | None = None,
        role_filter: str | None = None,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Search indexed conversations.

        Returns list of matches with conversation_id, message_index, and relevance.
        """
        query_words = re.findall(r"\b\w+\b", query.lower())
        if not query_words:
            return []

        # Find matches
        scores: dict[tuple[str, int], float] = {}

        for word in query_words:
            if word in self._index:
                for conv_id, msg_idx, role in self._index[word]:
                    # Apply filters
                    if conversation_id and conv_id != conversation_id:
                        continue
                    if role_filter and role != role_filter:
                        continue

                    key = (conv_id, msg_idx)
                    scores[key] = scores.get(key, 0) + 1

        # Sort by score
        results = [
            {
                "conversation_id": conv_id,
                "message_index": msg_idx,
                "relevance": score / len(query_words),
            }
            for (conv_id, msg_idx), score in sorted(
                scores.items(), key=lambda x: x[1], reverse=True
            )[:max_results]
        ]

        return results

    def filter_messages(
        self,
        messages: list[dict[str, str]],
        predicate: Callable[[dict[str, str]], bool],
    ) -> list[tuple[int, dict[str, str]]]:
        """Filter messages by predicate."""
        return [(i, m) for i, m in enumerate(messages) if predicate(m)]


# =============================================================================
# Conversation Merging (P1-58)
# =============================================================================


class ConversationMerger:
    """
    Merges multiple conversations.

    P1-58: Add conversation merging/consolidation
    """

    def __init__(self, summarizer: ContextSummarizer | None = None):
        self.summarizer = summarizer or ContextSummarizer()

    def merge(
        self,
        conversations: list[list[dict[str, str]]],
        strategy: str = "chronological",
    ) -> list[dict[str, str]]:
        """
        Merge multiple conversations.

        Strategies:
        - chronological: Sort by timestamp
        - interleave: Alternate between conversations
        - summarize: Create summaries of each
        """
        if not conversations:
            return []

        if strategy == "chronological":
            return self._merge_chronological(conversations)
        elif strategy == "interleave":
            return self._merge_interleave(conversations)
        elif strategy == "summarize":
            return self._merge_summarize(conversations)
        else:
            raise ValueError(f"Unknown merge strategy: {strategy}")

    def _merge_chronological(
        self,
        conversations: list[list[dict[str, str]]],
    ) -> list[dict[str, str]]:
        """Merge by combining all messages."""
        # Add conversation markers
        merged = []
        for i, conv in enumerate(conversations):
            merged.append(
                {
                    "role": "system",
                    "content": f"--- Conversation {i + 1} ---",
                }
            )
            merged.extend(conv)
        return merged

    def _merge_interleave(
        self,
        conversations: list[list[dict[str, str]]],
    ) -> list[dict[str, str]]:
        """Interleave messages from conversations."""
        merged = []
        max_len = max(len(c) for c in conversations)

        for i in range(max_len):
            for j, conv in enumerate(conversations):
                if i < len(conv):
                    msg = conv[i].copy()
                    msg["content"] = f"[Conv {j + 1}] {msg['content']}"
                    merged.append(msg)

        return merged

    def _merge_summarize(
        self,
        conversations: list[list[dict[str, str]]],
    ) -> list[dict[str, str]]:
        """Merge by summarizing each conversation."""
        merged = []

        for i, conv in enumerate(conversations):
            summary = self.summarizer.summarize_conversation(conv, max_summary_tokens=300)
            merged.append(
                {
                    "role": "system",
                    "content": f"Summary of Conversation {i + 1}:\n{summary}",
                }
            )

        return merged


# =============================================================================
# Shared Context Pool (P1-59)
# =============================================================================


class SharedContextPool:
    """
    Shared context between conversations.

    P1-59: Implement inter-conversation context sharing
    """

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path
        self._pool: dict[str, dict[str, Any]] = {}
        self._subscribers: dict[str, list[str]] = {}  # key -> [conversation_ids]

        if storage_path and storage_path.exists():
            self._load()

    def set(self, key: str, value: Any, source_conversation: str | None = None) -> None:
        """Set a shared value."""
        self._pool[key] = {
            "value": value,
            "source": source_conversation,
            "updated_at": time.time(),
        }
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a shared value."""
        entry = self._pool.get(key)
        return entry["value"] if entry else default

    def subscribe(self, key: str, conversation_id: str) -> None:
        """Subscribe a conversation to updates for a key."""
        if key not in self._subscribers:
            self._subscribers[key] = []
        if conversation_id not in self._subscribers[key]:
            self._subscribers[key].append(conversation_id)

    def get_subscribers(self, key: str) -> list[str]:
        """Get conversations subscribed to a key."""
        return self._subscribers.get(key, [])

    def get_all_for_conversation(self, conversation_id: str) -> dict[str, Any]:
        """Get all shared values relevant to a conversation."""
        result = {}
        for key, subscribers in self._subscribers.items():
            if conversation_id in subscribers and key in self._pool:
                result[key] = self._pool[key]["value"]
        return result

    def _load(self) -> None:
        """Load from storage."""
        if self.storage_path:
            pool_file = self.storage_path / "shared_context.json"
            if pool_file.exists():
                data = json.loads(pool_file.read_text(encoding="utf-8", errors="replace"))
                self._pool = data.get("pool", {})
                self._subscribers = data.get("subscribers", {})

    def _save(self) -> None:
        """Save to storage."""
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            pool_file = self.storage_path / "shared_context.json"
            pool_file.write_text(
                json.dumps(
                    {
                        "pool": self._pool,
                        "subscribers": self._subscribers,
                    },
                    indent=2,
                )
            )


# =============================================================================
# Simple Embedding Support (P1-60)
# =============================================================================


class SimpleEmbedding:
    """
    Simple embedding support for semantic search.

    P1-52, P1-60: Add embedding-based relevance scoring

    Note: This is a simple implementation. For production,
    use a proper embedding model (OpenAI, sentence-transformers, etc.)
    """

    def __init__(self):
        self._embeddings: dict[str, list[float]] = {}

    def _simple_embed(self, text: str, dim: int = 64) -> list[float]:
        """
        Create a simple embedding based on character and word features.

        This is NOT a semantic embedding - just a placeholder.
        For real semantic search, integrate sentence-transformers or similar.
        """

        # Normalize text
        text = text.lower().strip()

        # Character frequency features
        char_freq = [0.0] * 26
        for c in text:
            if "a" <= c <= "z":
                char_freq[ord(c) - ord("a")] += 1

        # Normalize
        total = sum(char_freq) or 1
        char_freq = [f / total for f in char_freq]

        # Word features
        words = text.split()
        word_features = [
            len(words) / 100,  # Word count normalized
            sum(len(w) for w in words) / max(len(words), 1) / 10,  # Avg word length
            len(set(words)) / max(len(words), 1),  # Vocabulary diversity
        ]

        # Combine features
        features = char_freq + word_features + [0.0] * (dim - len(char_freq) - len(word_features))

        # Ensure correct dimension
        return features[:dim]

    def embed(self, text: str, cache_key: str | None = None) -> list[float]:
        """Get embedding for text."""
        if cache_key and cache_key in self._embeddings:
            return self._embeddings[cache_key]

        embedding = self._simple_embed(text)

        if cache_key:
            self._embeddings[cache_key] = embedding

        return embedding

    def similarity(self, embedding1: list[float], embedding2: list[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        import math

        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = math.sqrt(sum(a * a for a in embedding1))
        norm2 = math.sqrt(sum(b * b for b in embedding2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def find_similar(
        self,
        query: str,
        candidates: list[tuple[str, str]],  # [(id, text), ...]
        top_k: int = 5,
    ) -> list[tuple[str, float]]:
        """Find similar texts to query."""
        query_embedding = self.embed(query)

        results = []
        for cand_id, cand_text in candidates:
            cand_embedding = self.embed(cand_text, cache_key=cand_id)
            score = self.similarity(query_embedding, cand_embedding)
            results.append((cand_id, score))

        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


# =============================================================================
# Enhanced Conversation Engine
# =============================================================================


class EnhancedConversationEngine:
    """
    Enhanced conversation engine with all P1-51 to P1-60 features.
    """

    def __init__(
        self,
        system_prompt: str = "",
        max_tokens: int = 128000,
        storage_path: Path | None = None,
    ):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.storage_path = storage_path

        # Core components
        self.ranker = ImportanceRanker()
        self.summarizer = ContextSummarizer()
        self.trimmer = SemanticTrimmer(self.ranker, self.summarizer)
        self.search = ConversationSearch()
        self.shared_pool = SharedContextPool(storage_path)
        self.embeddings = SimpleEmbedding()

        # State
        self._messages: list[dict[str, str]] = []
        self._summaries: list[str] = []
        self._conversation_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]

    def add_message(self, role: str, content: str) -> None:
        """Add a message with automatic indexing."""
        self._messages.append({"role": role, "content": content})
        self.search.index_conversation(self._conversation_id, self._messages[-1:])

    def get_messages(self) -> list[dict[str, str]]:
        """Get all messages."""
        return self._messages.copy()

    def smart_trim(self, preserve_recent: int = 4) -> str | None:
        """Trim with semantic awareness."""
        trimmed, summary = self.trimmer.trim(
            self._messages,
            self.max_tokens,
            preserve_recent=preserve_recent,
            summarize_removed=True,
        )

        if summary:
            self._summaries.append(summary)

        self._messages = trimmed
        return summary

    def search_history(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        """Search conversation history."""
        return self.search.search(query, self._conversation_id, max_results=max_results)

    def get_relevant_context(self, query: str, max_messages: int = 5) -> list[dict[str, str]]:
        """Get messages most relevant to query."""
        # Use embeddings for similarity
        candidates = [(str(i), m.get("content", "")) for i, m in enumerate(self._messages)]

        similar = self.embeddings.find_similar(query, candidates, top_k=max_messages)
        indices = [int(idx) for idx, _ in similar]

        return [self._messages[i] for i in sorted(indices)]

    def share_context(self, key: str, value: Any) -> None:
        """Share context with other conversations."""
        self.shared_pool.set(key, value, self._conversation_id)

    def get_shared_context(self) -> dict[str, Any]:
        """Get all shared context for this conversation."""
        return self.shared_pool.get_all_for_conversation(self._conversation_id)
