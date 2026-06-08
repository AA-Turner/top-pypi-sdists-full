"""Comprehensive tests for sage/core/context.py - Context Management."""

import hashlib
import time
from unittest.mock import MagicMock

import pytest

from sage.core.context import (
    ImportanceLevel,
    ImportanceMarker,
    ImportanceRanker,
    ContextSummarizer,
    SemanticTrimmer,
    ConversationBranch,
    BranchingConversation,
    ConversationSearch,
)


# =============================================================================
# Tests for ImportanceLevel Enum
# =============================================================================


class TestImportanceLevel:
    """Tests for ImportanceLevel enum."""

    def test_critical(self):
        """CRITICAL has value 5."""
        assert ImportanceLevel.CRITICAL.value == 5

    def test_high(self):
        """HIGH has value 4."""
        assert ImportanceLevel.HIGH.value == 4

    def test_medium(self):
        """MEDIUM has value 3."""
        assert ImportanceLevel.MEDIUM.value == 3

    def test_low(self):
        """LOW has value 2."""
        assert ImportanceLevel.LOW.value == 2

    def test_trivial(self):
        """TRIVIAL has value 1."""
        assert ImportanceLevel.TRIVIAL.value == 1

    def test_order(self):
        """Levels are ordered correctly."""
        assert ImportanceLevel.CRITICAL.value > ImportanceLevel.HIGH.value
        assert ImportanceLevel.HIGH.value > ImportanceLevel.MEDIUM.value
        assert ImportanceLevel.MEDIUM.value > ImportanceLevel.LOW.value
        assert ImportanceLevel.LOW.value > ImportanceLevel.TRIVIAL.value


# =============================================================================
# Tests for ImportanceMarker Dataclass
# =============================================================================


class TestImportanceMarker:
    """Tests for ImportanceMarker dataclass."""

    def test_create(self):
        """Create importance marker."""
        marker = ImportanceMarker(
            pattern=r"\bCRITICAL\b",
            level=ImportanceLevel.CRITICAL,
            description="Critical information",
        )
        assert marker.pattern == r"\bCRITICAL\b"
        assert marker.level == ImportanceLevel.CRITICAL
        assert marker.description == "Critical information"


# =============================================================================
# Tests for ImportanceRanker
# =============================================================================


class TestImportanceRanker:
    """Tests for ImportanceRanker class."""

    def test_init_with_default_markers(self):
        """Initialize with default markers."""
        ranker = ImportanceRanker()
        assert len(ranker.markers) > 0

    def test_init_with_custom_markers(self):
        """Initialize with custom markers."""
        custom = [
            ImportanceMarker(r"\bURGENT\b", ImportanceLevel.CRITICAL, "Urgent"),
        ]
        ranker = ImportanceRanker(custom_markers=custom)
        assert len(ranker.markers) > len(ImportanceRanker.MARKERS)

    def test_rank_critical(self):
        """Rank CRITICAL text."""
        ranker = ImportanceRanker()
        result = ranker.rank("This is CRITICAL information")
        assert result == ImportanceLevel.CRITICAL

    def test_rank_important(self):
        """Rank IMPORTANT text."""
        ranker = ImportanceRanker()
        result = ranker.rank("This is IMPORTANT to note")
        assert result == ImportanceLevel.HIGH

    def test_rank_architecture(self):
        """Rank ARCHITECTURE text."""
        ranker = ImportanceRanker()
        result = ranker.rank("ARCHITECTURE decision made")
        assert result == ImportanceLevel.HIGH

    def test_rank_security(self):
        """Rank SECURITY text."""
        ranker = ImportanceRanker()
        result = ranker.rank("SECURITY concern here")
        assert result == ImportanceLevel.HIGH

    def test_rank_code_block(self):
        """Rank code block."""
        ranker = ImportanceRanker()
        result = ranker.rank("```python\nprint('hello')\n```")
        assert result.value >= ImportanceLevel.MEDIUM.value

    def test_rank_todo(self):
        """Rank TODO."""
        ranker = ImportanceRanker()
        result = ranker.rank("TODO: implement this")
        assert result.value >= ImportanceLevel.MEDIUM.value

    def test_rank_fixme(self):
        """Rank FIXME."""
        ranker = ImportanceRanker()
        result = ranker.rank("FIXME: bug here")
        assert result.value >= ImportanceLevel.MEDIUM.value

    def test_rank_normal_text(self):
        """Rank normal text."""
        ranker = ImportanceRanker()
        result = ranker.rank("This is just normal text")
        assert result == ImportanceLevel.LOW

    def test_rank_messages(self):
        """Rank multiple messages."""
        ranker = ImportanceRanker()
        messages = [
            {"role": "user", "content": "CRITICAL issue"},
            {"role": "assistant", "content": "Normal response"},
        ]
        result = ranker.rank_messages(messages)
        assert len(result) == 2
        assert result[0][1] == ImportanceLevel.CRITICAL
        assert result[1][1] == ImportanceLevel.LOW

    def test_filter_by_importance(self):
        """Filter messages by importance."""
        ranker = ImportanceRanker()
        messages = [
            {"role": "user", "content": "CRITICAL issue"},
            {"role": "assistant", "content": "Normal response"},
            {"role": "user", "content": "IMPORTANT note"},
        ]
        result = ranker.filter_by_importance(messages, ImportanceLevel.HIGH)
        # Should include CRITICAL and IMPORTANT but not normal
        assert len(result) == 2


# =============================================================================
# Tests for ContextSummarizer
# =============================================================================


class TestContextSummarizer:
    """Tests for ContextSummarizer class."""

    def test_init_without_callback(self):
        """Initialize without model callback."""
        summarizer = ContextSummarizer()
        assert summarizer.model_callback is None
        assert summarizer._summary_cache == {}

    def test_init_with_callback(self):
        """Initialize with model callback."""
        callback = MagicMock(return_value="Summary")
        summarizer = ContextSummarizer(model_callback=callback)
        assert summarizer.model_callback is callback

    def test_summarize_empty(self):
        """Summarize empty messages."""
        summarizer = ContextSummarizer()
        result = summarizer.summarize_conversation([])
        # Should return something meaningful
        assert isinstance(result, str)

    def test_summarize_with_callback(self):
        """Summarize with model callback."""
        callback = MagicMock(return_value="AI Summary")
        summarizer = ContextSummarizer(model_callback=callback)

        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ]
        result = summarizer.summarize_conversation(messages)

        assert result == "AI Summary"
        callback.assert_called_once()

    def test_summarize_uses_cache(self):
        """Summarization uses cache."""
        callback = MagicMock(return_value="AI Summary")
        summarizer = ContextSummarizer(model_callback=callback)

        messages = [{"role": "user", "content": "Hello"}]

        # First call
        result1 = summarizer.summarize_conversation(messages)
        # Second call with same messages
        result2 = summarizer.summarize_conversation(messages)

        assert result1 == result2
        # Callback should only be called once due to caching
        assert callback.call_count == 1

    def test_extractive_summarize(self):
        """Extractive summarization without callback."""
        summarizer = ContextSummarizer()

        messages = [
            {"role": "user", "content": "CRITICAL: The server is down."},
            {"role": "assistant", "content": "IMPORTANT: I'll investigate immediately."},
        ]
        result = summarizer.summarize_conversation(messages)

        # Should extract key points
        assert isinstance(result, str)
        assert len(result) > 0


# =============================================================================
# Tests for SemanticTrimmer
# =============================================================================


class TestSemanticTrimmer:
    """Tests for SemanticTrimmer class."""

    def test_init_defaults(self):
        """Initialize with defaults."""
        trimmer = SemanticTrimmer()
        assert trimmer.ranker is not None
        assert trimmer.summarizer is not None

    def test_init_custom(self):
        """Initialize with custom components."""
        ranker = ImportanceRanker()
        summarizer = ContextSummarizer()
        trimmer = SemanticTrimmer(ranker=ranker, summarizer=summarizer)
        assert trimmer.ranker is ranker
        assert trimmer.summarizer is summarizer

    def test_trim_empty(self):
        """Trim empty messages."""
        trimmer = SemanticTrimmer()
        result, summary = trimmer.trim([], max_tokens=100)
        assert result == []
        assert summary is None

    def test_trim_under_limit(self):
        """No trimming when under limit."""
        trimmer = SemanticTrimmer()
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        result, summary = trimmer.trim(messages, max_tokens=1000)
        assert len(result) == 2
        assert summary is None

    def test_trim_over_limit(self):
        """Trim when over limit."""
        trimmer = SemanticTrimmer()
        messages = [
            {"role": "user", "content": "A" * 100},
            {"role": "assistant", "content": "B" * 100},
            {"role": "user", "content": "C" * 100},
            {"role": "assistant", "content": "D" * 100},
            {"role": "user", "content": "E" * 100},
            {"role": "assistant", "content": "F" * 100},
        ]
        result, summary = trimmer.trim(messages, max_tokens=50, preserve_recent=1)
        # Should remove some messages
        assert len(result) < len(messages)

    def test_trim_preserves_recent(self):
        """Trimming preserves recent messages."""
        trimmer = SemanticTrimmer()
        messages = [
            {"role": "user", "content": "Old message " + "A" * 100},
            {"role": "assistant", "content": "Old response " + "B" * 100},
            {"role": "user", "content": "Recent message"},
            {"role": "assistant", "content": "Recent response"},
        ]
        result, _ = trimmer.trim(messages, max_tokens=30, preserve_recent=1)
        # Recent messages should be preserved
        assert result[-1]["content"] == "Recent response"
        assert result[-2]["content"] == "Recent message"


# =============================================================================
# Tests for ConversationBranch Dataclass
# =============================================================================


class TestConversationBranch:
    """Tests for ConversationBranch dataclass."""

    def test_create_minimal(self):
        """Create with required fields."""
        branch = ConversationBranch(
            id="branch-1",
            parent_id=None,
            name="Main",
            messages=[],
        )
        assert branch.id == "branch-1"
        assert branch.parent_id is None
        assert branch.name == "Main"
        assert branch.messages == []

    def test_create_with_parent(self):
        """Create with parent."""
        branch = ConversationBranch(
            id="branch-2",
            parent_id="branch-1",
            name="Feature",
            messages=[{"role": "user", "content": "Hello"}],
        )
        assert branch.parent_id == "branch-1"
        assert len(branch.messages) == 1

    def test_has_timestamp(self):
        """Branch has created_at timestamp."""
        branch = ConversationBranch(
            id="branch-1",
            parent_id=None,
            name="Main",
            messages=[],
        )
        assert branch.created_at > 0

    def test_has_metadata(self):
        """Branch has metadata dict."""
        branch = ConversationBranch(
            id="branch-1",
            parent_id=None,
            name="Main",
            messages=[],
        )
        assert isinstance(branch.metadata, dict)


# =============================================================================
# Tests for BranchingConversation
# =============================================================================


class TestBranchingConversation:
    """Tests for BranchingConversation class."""

    def test_init(self):
        """Initialize conversation."""
        conv = BranchingConversation("conv-1")
        assert conv.conversation_id == "conv-1"
        assert conv.current_branch_id == "main"
        assert "main" in conv.branches

    def test_main_branch_created(self):
        """Main branch is created automatically."""
        conv = BranchingConversation("conv-1")
        main = conv.branches["main"]
        assert main.id == "main"
        assert main.parent_id is None
        assert main.name == "Main"
        assert main.messages == []

    def test_add_message(self):
        """Add message to current branch."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Hello")
        conv.add_message("assistant", "Hi there")

        messages = conv.get_messages()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"

    def test_create_branch(self):
        """Create a new branch."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Hello")

        branch_id = conv.create_branch("Feature")
        assert branch_id in conv.branches
        assert conv.branches[branch_id].parent_id == "main"

    def test_create_branch_copies_messages(self):
        """New branch copies messages from source."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Hello")
        conv.add_message("assistant", "Hi")

        branch_id = conv.create_branch("Feature")
        messages = conv.branches[branch_id].messages
        assert len(messages) == 2

    def test_create_branch_from_index(self):
        """Create branch from specific message index."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Message 1")
        conv.add_message("assistant", "Response 1")
        conv.add_message("user", "Message 2")

        branch_id = conv.create_branch("Feature", from_message_index=1)
        messages = conv.branches[branch_id].messages
        assert len(messages) == 2  # Only first two messages

    def test_create_branch_invalid_source(self):
        """Create branch from invalid source raises."""
        conv = BranchingConversation("conv-1")
        with pytest.raises(ValueError):
            conv.create_branch("Feature", from_branch="nonexistent")

    def test_switch_branch(self):
        """Switch to different branch."""
        conv = BranchingConversation("conv-1")
        branch_id = conv.create_branch("Feature")

        result = conv.switch_branch(branch_id)
        assert result is True
        assert conv.current_branch_id == branch_id

    def test_switch_branch_invalid(self):
        """Switch to invalid branch returns False."""
        conv = BranchingConversation("conv-1")
        result = conv.switch_branch("nonexistent")
        assert result is False
        assert conv.current_branch_id == "main"

    def test_get_messages_from_branch(self):
        """Get messages from specific branch."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Main message")

        branch_id = conv.create_branch("Feature")
        conv.switch_branch(branch_id)
        conv.add_message("user", "Feature message")

        main_msgs = conv.get_messages("main")
        feature_msgs = conv.get_messages(branch_id)

        assert len(main_msgs) == 1
        assert len(feature_msgs) == 2  # Copied + new

    def test_get_branch_tree(self):
        """Get branch tree structure."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Hello")
        branch_id = conv.create_branch("Feature")

        tree = conv.get_branch_tree()
        assert tree["id"] == "main"
        assert tree["name"] == "Main"
        assert tree["message_count"] == 1
        assert len(tree["children"]) == 1
        assert tree["children"][0]["id"] == branch_id

    def test_merge_branch(self):
        """Merge branch into another."""
        conv = BranchingConversation("conv-1")
        conv.add_message("user", "Main message")

        branch_id = conv.create_branch("Feature")
        conv.switch_branch(branch_id)
        conv.add_message("user", "Feature message")

        # Merge feature into main
        result = conv.merge_branch(branch_id, "main")
        assert result is True

        main_msgs = conv.get_messages("main")
        assert len(main_msgs) >= 2

    def test_merge_branch_invalid(self):
        """Merge invalid branch returns False."""
        conv = BranchingConversation("conv-1")
        result = conv.merge_branch("nonexistent", "main")
        assert result is False


# =============================================================================
# Tests for ConversationSearch
# =============================================================================


class TestConversationSearch:
    """Tests for ConversationSearch class."""

    def test_init(self):
        """Initialize search."""
        search = ConversationSearch()
        assert search._index == {}

    def test_index_conversation(self):
        """Index a conversation."""
        search = ConversationSearch()
        messages = [
            {"role": "user", "content": "Hello world"},
            {"role": "assistant", "content": "Hi there"},
        ]
        search.index_conversation("conv-1", messages)

        assert "hello" in search._index
        assert "world" in search._index
        assert "there" in search._index

    def test_search_basic(self):
        """Basic search."""
        search = ConversationSearch()
        messages = [
            {"role": "user", "content": "Python programming"},
            {"role": "assistant", "content": "I can help with Python"},
        ]
        search.index_conversation("conv-1", messages)

        results = search.search("python")
        assert len(results) > 0
        assert results[0]["conversation_id"] == "conv-1"

    def test_search_multiple_words(self):
        """Search with multiple words."""
        search = ConversationSearch()
        messages = [
            {"role": "user", "content": "Python programming language"},
        ]
        search.index_conversation("conv-1", messages)

        results = search.search("python programming")
        assert len(results) > 0
        # Higher relevance for matching both words
        assert results[0]["relevance"] > 0.5

    def test_search_no_results(self):
        """Search with no results."""
        search = ConversationSearch()
        messages = [{"role": "user", "content": "Hello world"}]
        search.index_conversation("conv-1", messages)

        results = search.search("xyz123")
        assert results == []

    def test_search_empty_query(self):
        """Search with empty query."""
        search = ConversationSearch()
        results = search.search("")
        assert results == []

    def test_search_filter_conversation(self):
        """Search with conversation filter."""
        search = ConversationSearch()
        search.index_conversation("conv-1", [{"role": "user", "content": "Python"}])
        search.index_conversation("conv-2", [{"role": "user", "content": "Python"}])

        results = search.search("python", conversation_id="conv-1")
        assert len(results) == 1
        assert results[0]["conversation_id"] == "conv-1"

    def test_search_filter_role(self):
        """Search with role filter."""
        search = ConversationSearch()
        messages = [
            {"role": "user", "content": "Python question"},
            {"role": "assistant", "content": "Python answer"},
        ]
        search.index_conversation("conv-1", messages)

        results = search.search("python", role_filter="user")
        assert all(r["message_index"] == 0 for r in results)

    def test_search_max_results(self):
        """Search respects max_results."""
        search = ConversationSearch()
        for i in range(100):
            search.index_conversation(f"conv-{i}", [{"role": "user", "content": "test"}])

        results = search.search("test", max_results=10)
        assert len(results) == 10

    def test_filter_messages(self):
        """Filter messages by predicate."""
        search = ConversationSearch()
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "Goodbye"},
        ]

        result = search.filter_messages(
            messages,
            predicate=lambda m: m["role"] == "user",
        )
        assert len(result) == 2
        assert result[0][0] == 0  # index
        assert result[1][0] == 2  # index


# =============================================================================
# Integration Tests
# =============================================================================


class TestContextIntegration:
    """Integration tests for context management."""

    def test_full_importance_ranking_flow(self):
        """Full importance ranking flow."""
        ranker = ImportanceRanker()

        messages = [
            {"role": "user", "content": "CRITICAL: Server is down!"},
            {"role": "assistant", "content": "Investigating..."},
            {"role": "user", "content": "IMPORTANT: Check the logs"},
            {"role": "assistant", "content": "Found the issue in logs"},
            {"role": "user", "content": "TODO: Fix the config"},
        ]

        ranked = ranker.rank_messages(messages)

        # Verify correct ranking
        assert ranked[0][1] == ImportanceLevel.CRITICAL
        assert ranked[2][1] == ImportanceLevel.HIGH

    def test_full_trimming_flow(self):
        """Full trimming flow with summarization."""
        trimmer = SemanticTrimmer()

        # Create many messages to trigger trimming
        messages = []
        for i in range(20):
            messages.append({"role": "user", "content": f"Question {i} " + "x" * 50})
            messages.append({"role": "assistant", "content": f"Answer {i} " + "y" * 50})

        result, summary = trimmer.trim(messages, max_tokens=100, preserve_recent=2)

        # Should be trimmed
        assert len(result) < len(messages)
        # Recent should be preserved
        assert "Answer 19" in result[-1]["content"]

    def test_full_branching_flow(self):
        """Full branching workflow."""
        conv = BranchingConversation("main-conv")

        # Add initial messages
        conv.add_message("user", "Start project")
        conv.add_message("assistant", "Project started")

        # Create feature branch
        feature_id = conv.create_branch("Feature-A")
        conv.switch_branch(feature_id)
        conv.add_message("user", "Implement feature A")
        conv.add_message("assistant", "Feature A implemented")

        # Create another branch from main
        conv.switch_branch("main")
        feature_b_id = conv.create_branch("Feature-B")
        conv.switch_branch(feature_b_id)
        conv.add_message("user", "Implement feature B")

        # Verify tree structure
        tree = conv.get_branch_tree()
        assert len(tree["children"]) == 2

        # Merge feature A into main
        conv.merge_branch(feature_id, "main")
        main_msgs = conv.get_messages("main")
        assert len(main_msgs) >= 3

    def test_full_search_flow(self):
        """Full search workflow."""
        search = ConversationSearch()

        # Index multiple conversations
        search.index_conversation("conv-1", [
            {"role": "user", "content": "Python async programming"},
            {"role": "assistant", "content": "Use asyncio for async"},
        ])
        search.index_conversation("conv-2", [
            {"role": "user", "content": "Python web frameworks"},
            {"role": "assistant", "content": "Try FastAPI or Django"},
        ])
        search.index_conversation("conv-3", [
            {"role": "user", "content": "JavaScript basics"},
        ])

        # Search for Python
        results = search.search("python")
        assert len(results) >= 2
        # Python conversations should rank higher
        conv_ids = [r["conversation_id"] for r in results[:2]]
        assert "conv-1" in conv_ids or "conv-2" in conv_ids
