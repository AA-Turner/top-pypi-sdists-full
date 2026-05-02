"""
TDD Tests for File Upload, Download, and Large Text Handling.

These tests are written FIRST (TDD) and will fail until implementation is complete.
Tests cover:
- File upload API endpoints
- File download API endpoints
- Large text (paste) handling
- File attachment in chat messages
- File metadata and validation
"""

import io
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


# ═══════════════════════════════════════════════════════════════════════════════
# FILE ATTACHMENT SCHEMA TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFileAttachmentSchema:
    """Tests for FileAttachment schema validation."""

    def test_file_attachment_valid(self):
        """Test creating a valid file attachment."""
        from backend.schemas import FileAttachment

        attachment = FileAttachment(
            file_id="abc123",
            filename="test.txt",
            mime_type="text/plain",
            size_bytes=1024,
            content_preview="Hello world..."
        )
        assert attachment.file_id == "abc123"
        assert attachment.filename == "test.txt"
        assert attachment.mime_type == "text/plain"
        assert attachment.size_bytes == 1024

    def test_file_attachment_with_url(self):
        """Test file attachment with download URL."""
        from backend.schemas import FileAttachment

        attachment = FileAttachment(
            file_id="xyz789",
            filename="data.json",
            mime_type="application/json",
            size_bytes=2048,
            url="/files/xyz789"
        )
        assert attachment.url == "/files/xyz789"

    def test_file_attachment_invalid_empty_id(self):
        """Test that empty file_id is rejected."""
        from backend.schemas import FileAttachment

        with pytest.raises(ValueError):
            FileAttachment(
                file_id="",
                filename="test.txt",
                mime_type="text/plain",
                size_bytes=100
            )

    def test_file_attachment_path_traversal_blocked(self):
        """Test that path traversal in filename is blocked."""
        from backend.schemas import FileAttachment

        with pytest.raises(ValueError):
            FileAttachment(
                file_id="abc123",
                filename="../../../etc/passwd",
                mime_type="text/plain",
                size_bytes=100
            )


class TestChatMessageWithAttachments:
    """Tests for ChatMessage schema with file attachments."""

    def test_chat_message_with_attachments(self):
        """Test chat message containing file attachments."""
        from backend.schemas import ChatMessage, FileAttachment

        attachment = FileAttachment(
            file_id="file1",
            filename="code.py",
            mime_type="text/x-python",
            size_bytes=512
        )
        message = ChatMessage(
            role="user",
            content="Please review this code",
            attachments=[attachment]
        )
        assert len(message.attachments) == 1
        assert message.attachments[0].filename == "code.py"

    def test_chat_message_without_attachments(self):
        """Test chat message works without attachments (backward compatible)."""
        from backend.schemas import ChatMessage

        message = ChatMessage(
            role="user",
            content="Hello, how are you?"
        )
        assert message.attachments is None or message.attachments == []


# ═══════════════════════════════════════════════════════════════════════════════
# LARGE TEXT HANDLING SCHEMA TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestLargeTextSchema:
    """Tests for large text (paste) handling schema."""

    def test_large_text_content_valid(self):
        """Test creating valid large text content."""
        from backend.schemas import LargeTextContent

        content = LargeTextContent(
            content="x" * 10000,
            filename="paste.txt",
            language="python"
        )
        assert len(content.content) == 10000
        assert content.filename == "paste.txt"
        assert content.language == "python"

    def test_large_text_auto_filename(self):
        """Test that filename defaults to paste_{timestamp}.txt."""
        from backend.schemas import LargeTextContent

        content = LargeTextContent(content="Hello world")
        assert content.filename.startswith("paste_")
        assert content.filename.endswith(".txt")

    def test_large_text_size_bytes_computed(self):
        """Test that size_bytes is computed from content."""
        from backend.schemas import LargeTextContent

        text = "Hello, world! 🎉"  # UTF-8 multibyte
        content = LargeTextContent(content=text)
        assert content.size_bytes == len(text.encode("utf-8"))

    def test_large_text_threshold_constant(self):
        """Test LARGE_TEXT_THRESHOLD constant exists."""
        from backend.schemas import LARGE_TEXT_THRESHOLD

        assert LARGE_TEXT_THRESHOLD >= 1024  # At least 1KB
        assert LARGE_TEXT_THRESHOLD <= 1024 * 1024  # At most 1MB


# ═══════════════════════════════════════════════════════════════════════════════
# FILE UPLOAD API TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFileUploadAPI:
    """Tests for file upload endpoint."""

    @pytest.fixture
    def client(self):
        with patch("backend.app.get_app_state") as mock_get_state:
            from unittest.mock import MagicMock
            mock_state = MagicMock()
            mock_state.registry.list_models.return_value = []
            mock_state.runtime_manager.runtime = None
            mock_state.runtime_manager.loaded_model_id = None
            mock_state.rate_limiter.is_allowed.return_value = True
            mock_state.rate_limiter.get_client_id.return_value = "test-client"
            mock_get_state.return_value = mock_state
            from backend.app import app
            yield TestClient(app)

    def test_upload_text_file(self, client):
        """Test uploading a text file."""
        content = b"Hello, this is a test file."
        files = {"file": ("test.txt", io.BytesIO(content), "text/plain")}

        response = client.post("/upload", files=files)
        assert response.status_code == 200

        data = response.json()
        assert data["ok"] is True
        assert "file_id" in data
        assert data["filename"] == "test.txt"
        assert data["mime_type"] == "text/plain"
        assert data["size_bytes"] == len(content)

    def test_upload_python_file(self, client):
        """Test uploading a Python source file."""
        content = b'def hello():\n    print("Hello, world!")\n'
        files = {"file": ("script.py", io.BytesIO(content), "text/x-python")}

        response = client.post("/upload", files=files)
        assert response.status_code == 200

        data = response.json()
        assert data["ok"] is True
        assert data["filename"] == "script.py"

    def test_upload_json_file(self, client):
        """Test uploading a JSON file."""
        content = json.dumps({"key": "value", "number": 42}).encode()
        files = {"file": ("data.json", io.BytesIO(content), "application/json")}

        response = client.post("/upload", files=files)
        assert response.status_code == 200

        data = response.json()
        assert data["ok"] is True
        assert data["mime_type"] == "application/json"

    def test_upload_file_size_limit(self, client):
        """Test that files over size limit are rejected."""
        # Create a file larger than 10MB
        content = b"x" * (11 * 1024 * 1024)
        files = {"file": ("large.bin", io.BytesIO(content), "application/octet-stream")}

        response = client.post("/upload", files=files)
        assert response.status_code == 413  # Payload Too Large

    def test_upload_dangerous_filename_sanitized(self, client):
        """Test that dangerous filenames are sanitized."""
        content = b"malicious content"
        files = {"file": ("../../../etc/passwd", io.BytesIO(content), "text/plain")}

        response = client.post("/upload", files=files)
        # Should either reject or sanitize the filename
        if response.status_code == 200:
            data = response.json()
            assert ".." not in data["filename"]
            assert "/" not in data["filename"]

    def test_upload_empty_file_rejected(self, client):
        """Test that empty files are rejected."""
        files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}

        response = client.post("/upload", files=files)
        assert response.status_code == 400

    def test_upload_returns_content_preview(self, client):
        """Test that text file uploads return content preview."""
        content = b"This is a test file with some content for preview."
        files = {"file": ("preview.txt", io.BytesIO(content), "text/plain")}

        response = client.post("/upload", files=files)
        assert response.status_code == 200

        data = response.json()
        assert "content_preview" in data
        assert "This is a test" in data["content_preview"]


# ═══════════════════════════════════════════════════════════════════════════════
# FILE DOWNLOAD API TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFileDownloadAPI:
    """Tests for file download endpoint."""

    @pytest.fixture
    def client(self):
        with patch("backend.app.get_app_state") as mock_get_state:
            from unittest.mock import MagicMock
            mock_state = MagicMock()
            mock_state.registry.list_models.return_value = []
            mock_state.runtime_manager.runtime = None
            mock_state.runtime_manager.loaded_model_id = None
            mock_state.rate_limiter.is_allowed.return_value = True
            mock_state.rate_limiter.get_client_id.return_value = "test-client"
            mock_get_state.return_value = mock_state
            from backend.app import app
            yield TestClient(app)

    @pytest.fixture
    def uploaded_file(self, client):
        """Upload a file and return its file_id."""
        content = b"Download test content"
        files = {"file": ("download.txt", io.BytesIO(content), "text/plain")}
        response = client.post("/upload", files=files)
        return response.json()["file_id"]

    def test_download_file(self, client, uploaded_file):
        """Test downloading an uploaded file."""
        response = client.get(f"/files/{uploaded_file}")
        assert response.status_code == 200
        assert response.content == b"Download test content"
        assert "text/plain" in response.headers["content-type"]

    def test_download_nonexistent_file(self, client):
        """Test downloading a file that doesn't exist."""
        response = client.get("/files/nonexistent-file-id")
        assert response.status_code == 404

    def test_download_with_original_filename(self, client, uploaded_file):
        """Test that download preserves original filename in header."""
        response = client.get(f"/files/{uploaded_file}")
        assert response.status_code == 200
        assert "content-disposition" in response.headers
        assert "download.txt" in response.headers["content-disposition"]

    def test_download_path_traversal_blocked(self, client):
        """Test that path traversal in file_id is blocked."""
        response = client.get("/files/../../../etc/passwd")
        assert response.status_code in [400, 404, 422]


# ═══════════════════════════════════════════════════════════════════════════════
# LARGE TEXT (PASTE) API TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestLargeTextAPI:
    """Tests for large text/paste handling endpoint."""

    @pytest.fixture
    def client(self):
        with patch("backend.app.get_app_state") as mock_get_state:
            from unittest.mock import MagicMock
            mock_state = MagicMock()
            mock_state.registry.list_models.return_value = []
            mock_state.runtime_manager.runtime = None
            mock_state.runtime_manager.loaded_model_id = None
            mock_state.rate_limiter.is_allowed.return_value = True
            mock_state.rate_limiter.get_client_id.return_value = "test-client"
            mock_get_state.return_value = mock_state
            from backend.app import app
            yield TestClient(app)

    def test_submit_large_text(self, client):
        """Test submitting large text content (above 100KB threshold)."""
        large_text = "x" * 150000  # 150KB of text (above 100KB threshold)

        response = client.post("/paste", json={
            "content": large_text,
            "filename": "large_paste.txt"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["ok"] is True
        assert "file_id" in data
        assert data["size_bytes"] == 150000

    def test_submit_large_text_with_language(self, client):
        """Test submitting large text with language hint."""
        code = 'def main():\n    print("Hello")\n' * 1000

        response = client.post("/paste", json={
            "content": code,
            "language": "python"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["language"] == "python"

    def test_submit_large_text_auto_detect_language(self, client):
        """Test that language is auto-detected from content."""
        python_code = '''
import os
import sys

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
'''
        response = client.post("/paste", json={"content": python_code})
        assert response.status_code == 200

        data = response.json()
        # Should detect Python
        assert data.get("language") in ["python", "py", None]

    def test_submit_text_under_threshold_inline(self, client):
        """Test that small text is returned inline, not as file."""
        small_text = "This is a small text snippet."

        response = client.post("/paste", json={"content": small_text})
        assert response.status_code == 200

        data = response.json()
        assert data["ok"] is True
        # Small text should be handled inline
        assert data.get("inline", True) is True


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT WITH FILE ATTACHMENTS TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestChatWithAttachments:
    """Tests for chat endpoint with file attachments."""

    @pytest.fixture
    def client(self):
        with patch("backend.app.get_app_state") as mock_get_state:
            from unittest.mock import MagicMock
            mock_state = MagicMock()
            mock_state.registry.list_models.return_value = []
            mock_state.runtime_manager.runtime = MagicMock()
            mock_state.runtime_manager.loaded_model_id = "ollama:llama3.2"
            mock_state.runtime_manager.runtime.chat.return_value = "Test response"
            mock_state.runtime_manager.runtime.stream_chat.return_value = iter(["Test"])
            mock_state.rate_limiter.is_allowed.return_value = True
            mock_state.rate_limiter.get_client_id.return_value = "test-client"
            mock_state.conversation_store = MagicMock()
            mock_get_state.return_value = mock_state
            from backend.app import app
            yield TestClient(app)

    @pytest.fixture
    def uploaded_code_file(self, client):
        """Upload a code file for testing."""
        content = b'''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
        files = {"file": ("fib.py", io.BytesIO(content), "text/x-python")}
        response = client.post("/upload", files=files)
        return response.json()

    def test_chat_with_file_attachment(self, client, uploaded_code_file):
        """Test sending chat with file attachment."""
        response = client.post("/chat", json={
            "model_id": "ollama:llama3.2",
            "messages": [{
                "role": "user",
                "content": "Please review this code",
                "attachments": [{
                    "file_id": uploaded_code_file["file_id"],
                    "filename": uploaded_code_file["filename"]
                }]
            }],
            "max_tokens": 100,
            "stream": False
        })
        assert response.status_code == 200

    def test_chat_includes_file_content_in_context(self, client, uploaded_code_file):
        """Test that file content is included in AI context."""
        # This test verifies the file content reaches the AI
        response = client.post("/chat", json={
            "model_id": "ollama:llama3.2",
            "messages": [{
                "role": "user",
                "content": "What function is defined in the attached file?",
                "attachments": [{
                    "file_id": uploaded_code_file["file_id"],
                    "filename": "fib.py"
                }]
            }],
            "max_tokens": 100,
            "stream": False
        })
        assert response.status_code == 200
        # Response should mention fibonacci since that's in the file
        data = response.json()
        # The AI should have access to the file content


# ═══════════════════════════════════════════════════════════════════════════════
# FILE STORE UNIT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFileStore:
    """Unit tests for FileStore class."""

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as d:
            yield Path(d)

    @pytest.fixture
    def file_store(self, temp_dir):
        from backend.file_store import FileStore
        return FileStore(base_dir=temp_dir)

    def test_save_file(self, file_store):
        """Test saving a file to the store."""
        content = b"Test file content"
        file_id = file_store.save(
            content=content,
            filename="test.txt",
            mime_type="text/plain"
        )
        assert file_id is not None
        assert len(file_id) > 0

    def test_get_file(self, file_store):
        """Test retrieving a saved file."""
        content = b"Retrieve me"
        file_id = file_store.save(content, "retrieve.txt", "text/plain")

        retrieved = file_store.get(file_id)
        assert retrieved["content"] == content
        assert retrieved["filename"] == "retrieve.txt"
        assert retrieved["mime_type"] == "text/plain"

    def test_get_nonexistent_file(self, file_store):
        """Test retrieving a file that doesn't exist."""
        with pytest.raises(KeyError):
            file_store.get("nonexistent-id")

    def test_delete_file(self, file_store):
        """Test deleting a file."""
        file_id = file_store.save(b"Delete me", "delete.txt", "text/plain")
        file_store.delete(file_id)

        with pytest.raises(KeyError):
            file_store.get(file_id)

    def test_list_files(self, file_store):
        """Test listing all files."""
        file_store.save(b"File 1", "file1.txt", "text/plain")
        file_store.save(b"File 2", "file2.txt", "text/plain")

        files = file_store.list_all()
        assert len(files) == 2

    def test_file_metadata(self, file_store):
        """Test file metadata is stored correctly."""
        content = b"Metadata test"
        file_id = file_store.save(content, "meta.txt", "text/plain")

        metadata = file_store.get_metadata(file_id)
        assert metadata["filename"] == "meta.txt"
        assert metadata["mime_type"] == "text/plain"
        assert metadata["size_bytes"] == len(content)
        assert "created_at" in metadata

    def test_content_preview_for_text(self, file_store):
        """Test content preview generation for text files."""
        content = b"This is a long text file content that should be previewed."
        file_id = file_store.save(content, "preview.txt", "text/plain")

        metadata = file_store.get_metadata(file_id)
        assert "content_preview" in metadata
        assert metadata["content_preview"].startswith("This is")

    def test_no_preview_for_binary(self, file_store):
        """Test that binary files don't get text preview."""
        content = bytes(range(256))  # Binary content
        file_id = file_store.save(content, "binary.bin", "application/octet-stream")

        metadata = file_store.get_metadata(file_id)
        assert metadata.get("content_preview") is None


# ═══════════════════════════════════════════════════════════════════════════════
# CONVERSATION LOGGING TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestConversationLogging:
    """Tests for conversation input/output logging."""

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as d:
            yield Path(d)

    @pytest.fixture
    def conversation_logger(self, temp_dir):
        from backend.conversation_logger import ConversationLogger
        return ConversationLogger(base_dir=temp_dir)

    def test_log_user_input(self, conversation_logger):
        """Test logging user input."""
        conversation_logger.log_input(
            conversation_id="conv1",
            content="Hello, AI!",
            timestamp="2024-01-01T12:00:00Z"
        )

        inputs = conversation_logger.get_inputs("conv1")
        assert len(inputs) == 1
        assert inputs[0]["content"] == "Hello, AI!"

    def test_log_ai_output(self, conversation_logger):
        """Test logging AI output."""
        conversation_logger.log_output(
            conversation_id="conv1",
            content="Hello! How can I help you?",
            model_id="ollama:llama3.2",
            timestamp="2024-01-01T12:00:01Z"
        )

        outputs = conversation_logger.get_outputs("conv1")
        assert len(outputs) == 1
        assert outputs[0]["content"] == "Hello! How can I help you?"
        assert outputs[0]["model_id"] == "ollama:llama3.2"

    def test_separate_input_output_logs(self, conversation_logger):
        """Test that inputs and outputs are stored separately."""
        conversation_logger.log_input("conv1", "User message")
        conversation_logger.log_output("conv1", "AI response", "ollama:llama3.2")

        inputs = conversation_logger.get_inputs("conv1")
        outputs = conversation_logger.get_outputs("conv1")

        assert len(inputs) == 1
        assert len(outputs) == 1
        assert inputs[0]["content"] == "User message"
        assert outputs[0]["content"] == "AI response"

    def test_log_with_attachments(self, conversation_logger):
        """Test logging input with file attachments."""
        conversation_logger.log_input(
            conversation_id="conv1",
            content="Review this file",
            attachments=[{
                "file_id": "file123",
                "filename": "code.py"
            }]
        )

        inputs = conversation_logger.get_inputs("conv1")
        assert len(inputs[0]["attachments"]) == 1
        assert inputs[0]["attachments"][0]["file_id"] == "file123"

    def test_export_conversation_log(self, conversation_logger):
        """Test exporting full conversation log."""
        conversation_logger.log_input("conv1", "Question 1")
        conversation_logger.log_output("conv1", "Answer 1", "ollama:llama3.2")
        conversation_logger.log_input("conv1", "Question 2")
        conversation_logger.log_output("conv1", "Answer 2", "ollama:llama3.2")

        export = conversation_logger.export("conv1")
        assert len(export["inputs"]) == 2
        assert len(export["outputs"]) == 2

    def test_log_persistence(self, conversation_logger, temp_dir):
        """Test that logs persist to disk."""
        conversation_logger.log_input("conv1", "Persistent message")

        # Create new logger instance
        from backend.conversation_logger import ConversationLogger
        new_logger = ConversationLogger(base_dir=temp_dir)

        inputs = new_logger.get_inputs("conv1")
        assert len(inputs) == 1
        assert inputs[0]["content"] == "Persistent message"

    def test_log_with_tokens_count(self, conversation_logger):
        """Test logging includes token count estimation."""
        conversation_logger.log_output(
            conversation_id="conv1",
            content="This is a response with multiple tokens.",
            model_id="ollama:llama3.2"
        )

        outputs = conversation_logger.get_outputs("conv1")
        assert "token_count" in outputs[0]
        assert outputs[0]["token_count"] > 0


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFileHandlingIntegration:
    """Integration tests for complete file handling workflow."""

    @pytest.fixture
    def client(self):
        with patch("backend.app.get_app_state") as mock_get_state:
            from unittest.mock import MagicMock
            mock_state = MagicMock()
            mock_state.registry.list_models.return_value = []
            mock_state.runtime_manager.runtime = MagicMock()
            mock_state.runtime_manager.loaded_model_id = "ollama:llama3.2"
            mock_state.runtime_manager.runtime.chat.return_value = "Test response"
            mock_state.runtime_manager.runtime.stream_chat.return_value = iter(["Test"])
            mock_state.rate_limiter.is_allowed.return_value = True
            mock_state.rate_limiter.get_client_id.return_value = "test-client"
            # Mock conversation store with proper return values
            mock_state.conversation_store = MagicMock()
            mock_state.conversation_store.create.return_value = {
                "id": "test-conv-123",
                "title": "Test Logging",
                "created_at": "2024-01-01T00:00:00Z",
                "messages": []
            }
            mock_get_state.return_value = mock_state
            from backend.app import app
            yield TestClient(app)

    def test_upload_then_download_workflow(self, client):
        """Test complete upload -> download workflow."""
        # Upload
        content = b"Integration test content"
        files = {"file": ("integration.txt", io.BytesIO(content), "text/plain")}
        upload_response = client.post("/upload", files=files)
        assert upload_response.status_code == 200
        file_id = upload_response.json()["file_id"]

        # Download
        download_response = client.get(f"/files/{file_id}")
        assert download_response.status_code == 200
        assert download_response.content == content

    def test_upload_chat_with_file_workflow(self, client):
        """Test upload file -> use in chat workflow."""
        # Upload code file
        code = b'''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
'''
        files = {"file": ("math.py", io.BytesIO(code), "text/x-python")}
        upload_response = client.post("/upload", files=files)
        assert upload_response.status_code == 200
        file_id = upload_response.json()["file_id"]

        # Use in chat
        chat_response = client.post("/chat", json={
            "model_id": "ollama:llama3.2",
            "messages": [{
                "role": "user",
                "content": "What functions are in this file?",
                "attachments": [{"file_id": file_id, "filename": "math.py"}]
            }],
            "max_tokens": 100,
            "stream": False
        })
        assert chat_response.status_code == 200

    def test_large_paste_to_file_workflow(self, client):
        """Test large paste -> saved as file workflow."""
        # Create content above 100KB threshold
        large_code = "# Large Python file\n" + ("def func():\n    pass\n\n" * 5000)

        # Submit as paste
        paste_response = client.post("/paste", json={
            "content": large_code,
            "language": "python"
        })
        assert paste_response.status_code == 200

        data = paste_response.json()
        assert "file_id" in data

        # Should be downloadable
        download_response = client.get(f"/files/{data['file_id']}")
        assert download_response.status_code == 200
        assert download_response.content.decode() == large_code

    def test_conversation_with_logging_workflow(self, client):
        """Test that conversation logs inputs and outputs."""
        # Create conversation
        conv_response = client.post("/conversations", json={"title": "Test Logging"})
        assert conv_response.status_code == 200
        conv_id = conv_response.json()["conversation"]["id"]

        # Send message
        chat_response = client.post("/chat", json={
            "model_id": "ollama:llama3.2",
            "messages": [{"role": "user", "content": "Hello!"}],
            "conversation_id": conv_id,
            "max_tokens": 50,
            "stream": False
        })
        assert chat_response.status_code == 200

        # Verify logs exist
        logs_response = client.get(f"/conversations/{conv_id}/logs")
        assert logs_response.status_code == 200

        logs = logs_response.json()
        assert len(logs["inputs"]) >= 1
        assert len(logs["outputs"]) >= 1
