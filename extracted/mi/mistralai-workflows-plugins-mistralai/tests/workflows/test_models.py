"""Tests for mistral plugin models."""

from mistralai.workflows.plugins.mistralai.models import (
    AgentUpdateRequest,
    ChatStreamState,
    ContentChunk,
    ConversationAppendRequest,
    ConversationStreamState,
)


class TestChatStreamState:
    def test_default_state(self):
        """Test creating ChatStreamState with default values."""
        state = ChatStreamState()
        assert state.contentChunks == []

    def test_state_with_content(self):
        """Test creating ChatStreamState with content chunks."""
        chunk = ContentChunk(text="Hello world")
        state = ChatStreamState(contentChunks=[chunk])
        assert len(state.contentChunks) == 1
        assert state.contentChunks[0].text == "Hello world"


class TestConversationStreamState:
    def test_default_state(self):
        """Test creating ConversationStreamState with default values."""
        state = ConversationStreamState()
        assert state.contentChunks == []

    def test_state_with_content(self):
        """Test creating ConversationStreamState with content chunks."""
        chunk = ContentChunk(text="Test content")
        state = ConversationStreamState(contentChunks=[chunk])
        assert len(state.contentChunks) == 1
        assert state.contentChunks[0].text == "Test content"


class TestConversationAppendRequest:
    def test_conversation_append_request(self):
        """Test creating a ConversationAppendRequest."""
        request = ConversationAppendRequest(conversation_id="conv-123", inputs=[])
        assert request.conversation_id == "conv-123"


class TestAgentUpdateRequest:
    def test_agent_update_request(self):
        """Test creating an AgentUpdateRequest."""
        request = AgentUpdateRequest(agent_id="agent-123")
        assert request.agent_id == "agent-123"
