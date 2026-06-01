"""Tests for ai-code core functionality."""

import os
import tempfile
import pytest

from codrninja.core import AICode
from codrninja.config import Config


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    os.unlink(db_path)


@pytest.fixture
def ai(temp_db):
    """Create an AICode instance with temp database and isolated sessions dir."""
    sessions_dir = tempfile.mkdtemp(prefix="codrninja-test-sessions-")
    config = Config(db_path=temp_db)
    ai_instance = AICode(config)
    ai_instance.session_manager = type(ai_instance.session_manager)(sessions_dir=sessions_dir)
    yield ai_instance
    import shutil
    shutil.rmtree(sessions_dir, ignore_errors=True)


def test_create_session(ai):
    """Test session creation."""
    session = ai.create_session("test-session")
    assert session.name == "test-session"
    assert session.id is not None


def test_get_session(ai):
    """Test getting a session."""
    ai.create_session("test-session")
    session = ai.get_session("test-session")
    assert session is not None
    assert session.name == "test-session"


def test_get_nonexistent_session(ai):
    """Test getting a non-existent session."""
    session = ai.get_session("nonexistent")
    assert session is None


def test_list_sessions(ai):
    """Test listing sessions."""
    ai.create_session("session-1")
    ai.create_session("session-2")
    sessions = ai.list_sessions()
    assert len(sessions) == 2


def test_send_message(ai):
    """Test sending a message."""
    ai.create_session("test-session")
    # This would need a mock Ollama server for full testing
    result = ai.send_message("test-session", "What is 2+2?")
    assert "success" in result
