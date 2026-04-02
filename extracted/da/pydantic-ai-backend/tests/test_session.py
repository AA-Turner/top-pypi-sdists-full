"""Tests for SessionManager."""

import time
from unittest.mock import MagicMock, patch

import pytest

from pydantic_ai_backends import RuntimeConfig, SessionManager


class MockDockerSandbox:
    """Mock DockerSandbox for testing SessionManager."""

    def __init__(
        self,
        runtime: RuntimeConfig | str | None = None,
        session_id: str | None = None,
        idle_timeout: int = 3600,
        volumes: dict[str, str] | None = None,
        **kwargs: object,
    ) -> None:
        self._id = session_id or "test-id"
        self._runtime = runtime
        self._idle_timeout = idle_timeout
        self._last_activity = time.time()
        self._alive = True
        self._volumes = volumes or {}

    @property
    def session_id(self) -> str:
        return self._id

    def is_alive(self) -> bool:
        return self._alive

    def start(self) -> None:
        self._alive = True

    def stop(self) -> None:
        self._alive = False


class TestSessionManager:
    """Tests for SessionManager class."""

    def test_init_defaults(self):
        """Test default initialization."""
        manager = SessionManager()
        assert manager._default_runtime is None
        assert manager._default_idle_timeout == 3600
        assert manager.session_count == 0
        assert len(manager) == 0

    def test_init_with_runtime(self):
        """Test initialization with default runtime."""
        runtime = RuntimeConfig(name="test")
        manager = SessionManager(default_runtime=runtime)
        assert manager._default_runtime is runtime

    def test_init_with_string_runtime(self):
        """Test initialization with runtime name."""
        manager = SessionManager(default_runtime="python-datascience")
        assert manager._default_runtime == "python-datascience"

    def test_init_with_timeout(self):
        """Test initialization with custom timeout."""
        manager = SessionManager(default_idle_timeout=1800)
        assert manager._default_idle_timeout == 1800

    @pytest.mark.asyncio
    async def test_get_or_create_new_session(self):
        """Test creating a new session."""
        manager = SessionManager()

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox = await manager.get_or_create("user-123")
            assert sandbox.session_id == "user-123"
            assert "user-123" in manager
            assert manager.session_count == 1

    @pytest.mark.asyncio
    async def test_get_or_create_existing_session(self):
        """Test retrieving existing session."""
        manager = SessionManager()

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox1 = await manager.get_or_create("user-123")
            sandbox2 = await manager.get_or_create("user-123")
            assert sandbox1 is sandbox2
            assert manager.session_count == 1

    @pytest.mark.asyncio
    async def test_get_or_create_dead_session_recreates(self):
        """Test that dead sessions are recreated."""
        manager = SessionManager()

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox1 = await manager.get_or_create("user-123")
            sandbox1._alive = False  # type: ignore[attr-defined]  # Mock attribute

            sandbox2 = await manager.get_or_create("user-123")
            assert sandbox1 is not sandbox2
            assert manager.session_count == 1

    @pytest.mark.asyncio
    async def test_release_existing_session(self):
        """Test releasing an existing session."""
        manager = SessionManager()

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            await manager.get_or_create("user-123")
            assert manager.session_count == 1

            result = await manager.release("user-123")
            assert result is True
            assert manager.session_count == 0
            assert "user-123" not in manager

    @pytest.mark.asyncio
    async def test_release_nonexistent_session(self):
        """Test releasing a non-existent session."""
        manager = SessionManager()
        result = await manager.release("nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_cleanup_idle_sessions(self):
        """Test cleaning up idle sessions."""
        manager = SessionManager(default_idle_timeout=10)

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox1 = await manager.get_or_create("user-1")
            sandbox2 = await manager.get_or_create("user-2")

            # Make one session idle
            sandbox1._last_activity = time.time() - 20  # 20 seconds ago
            sandbox2._last_activity = time.time()  # Just now

            cleaned = await manager.cleanup_idle(max_idle=10)
            assert cleaned == 1
            assert manager.session_count == 1
            assert "user-1" not in manager
            assert "user-2" in manager

    @pytest.mark.asyncio
    async def test_cleanup_idle_uses_default_timeout(self):
        """Test cleanup uses default timeout when not specified."""
        manager = SessionManager(default_idle_timeout=5)

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox = await manager.get_or_create("user-1")
            sandbox._last_activity = time.time() - 10  # 10 seconds ago

            cleaned = await manager.cleanup_idle()
            assert cleaned == 1

    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test shutting down all sessions."""
        manager = SessionManager()

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            await manager.get_or_create("user-1")
            await manager.get_or_create("user-2")
            await manager.get_or_create("user-3")
            assert manager.session_count == 3

            count = await manager.shutdown()
            assert count == 3
            assert manager.session_count == 0

    def test_sessions_property(self):
        """Test sessions property returns copy."""
        manager = SessionManager()
        manager._sessions["test"] = MagicMock()

        sessions = manager.sessions
        assert "test" in sessions
        # Verify it's a copy
        sessions["new"] = MagicMock()
        assert "new" not in manager._sessions

    def test_contains(self):
        """Test __contains__ method."""
        manager = SessionManager()
        manager._sessions["test"] = MagicMock()

        assert "test" in manager
        assert "other" not in manager

    def test_len(self):
        """Test __len__ method."""
        manager = SessionManager()
        assert len(manager) == 0

        manager._sessions["a"] = MagicMock()
        manager._sessions["b"] = MagicMock()
        assert len(manager) == 2

    def test_start_cleanup_loop(self):
        """Test starting cleanup loop."""
        manager = SessionManager()
        assert manager._cleanup_task is None

        # We can't actually test the async loop without running it,
        # but we can verify it's created
        with patch("asyncio.create_task") as mock_create_task:
            manager.start_cleanup_loop(interval=60)
            mock_create_task.assert_called_once()

        # Calling again should do nothing
        with patch("asyncio.create_task") as mock_create_task:
            manager._cleanup_task = MagicMock()
            manager.start_cleanup_loop()
            mock_create_task.assert_not_called()

    def test_stop_cleanup_loop(self):
        """Test stopping cleanup loop."""
        manager = SessionManager()
        mock_task = MagicMock()
        manager._cleanup_task = mock_task

        manager.stop_cleanup_loop()
        mock_task.cancel.assert_called_once()
        assert manager._cleanup_task is None

    def test_stop_cleanup_loop_when_not_running(self):
        """Test stopping cleanup loop when not running."""
        manager = SessionManager()
        manager.stop_cleanup_loop()  # Should not raise
        assert manager._cleanup_task is None

    def test_init_with_workspace_root_string(self):
        """Test initialization with workspace_root as string."""
        manager = SessionManager(workspace_root="/tmp/sessions")
        assert manager._workspace_root is not None
        assert str(manager._workspace_root) == "/tmp/sessions"

    def test_init_with_workspace_root_path(self):
        """Test initialization with workspace_root as Path."""
        from pathlib import Path

        manager = SessionManager(workspace_root=Path("/tmp/sessions"))
        assert manager._workspace_root is not None
        assert str(manager._workspace_root) == "/tmp/sessions"

    def test_init_without_workspace_root(self):
        """Test initialization without workspace_root."""
        manager = SessionManager()
        assert manager._workspace_root is None

    @pytest.mark.asyncio
    async def test_get_or_create_with_workspace_root(self, tmp_path):
        """Test that workspace_root creates directories and passes volumes."""
        manager = SessionManager(workspace_root=tmp_path)

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox = await manager.get_or_create("user-123")

            # Check that directory was created
            expected_dir = tmp_path / "user-123" / "workspace"
            assert expected_dir.exists()
            assert expected_dir.is_dir()

            # Check that volumes were passed to sandbox
            assert sandbox._volumes is not None
            assert str(expected_dir.resolve()) in sandbox._volumes
            assert sandbox._volumes[str(expected_dir.resolve())] == "/workspace"

    @pytest.mark.asyncio
    async def test_get_or_create_without_workspace_root_no_volumes(self):
        """Test that without workspace_root, no volumes are set."""
        manager = SessionManager()

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox = await manager.get_or_create("user-123")
            assert sandbox._volumes == {}

    @pytest.mark.asyncio
    async def test_get_or_create_multiple_sessions_separate_dirs(self, tmp_path):
        """Test that multiple sessions get separate workspace directories."""
        manager = SessionManager(workspace_root=tmp_path)

        with patch("pydantic_ai_backends.backends.docker.sandbox.DockerSandbox", MockDockerSandbox):
            sandbox1 = await manager.get_or_create("user-1")
            sandbox2 = await manager.get_or_create("user-2")

            # Check separate directories
            dir1 = tmp_path / "user-1" / "workspace"
            dir2 = tmp_path / "user-2" / "workspace"

            assert dir1.exists()
            assert dir2.exists()
            assert dir1 != dir2

            # Check separate volumes
            assert str(dir1.resolve()) in sandbox1._volumes
            assert str(dir2.resolve()) in sandbox2._volumes
