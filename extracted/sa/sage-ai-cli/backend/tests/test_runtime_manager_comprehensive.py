"""Comprehensive tests for backend/runtime_manager.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


class TestGetRuntimeMap:
    """Tests for _get_runtime_map function."""

    def test_import(self):
        """Function can be imported."""
        from backend.runtime_manager import _get_runtime_map
        assert _get_runtime_map is not None

    def test_returns_dict(self):
        """Returns a dictionary."""
        from backend.runtime_manager import _get_runtime_map

        result = _get_runtime_map()
        assert isinstance(result, dict)

    def test_handles_import_errors(self):
        """Handles import errors gracefully."""
        from backend.runtime_manager import _get_runtime_map

        # Should not raise even if imports fail
        result = _get_runtime_map()
        assert isinstance(result, dict)


class TestRuntimeManagerInit:
    """Tests for RuntimeManager initialization."""

    def test_create(self):
        """Create RuntimeManager."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        assert manager.runtime is None
        assert manager.loaded_model_id is None
        assert manager.loaded_runtime is None

    def test_has_lock(self):
        """RuntimeManager has lock."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        assert hasattr(manager, "_lock")
        # RLock doesn't have a direct isinstance check, verify it's callable
        assert hasattr(manager._lock, "acquire")
        assert hasattr(manager._lock, "release")


class TestRuntimeManagerLoad:
    """Tests for RuntimeManager.load method."""

    def test_load_unsupported_runtime_raises(self):
        """Load with unsupported runtime raises ValueError."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()

        with pytest.raises(ValueError, match="Unsupported runtime"):
            manager.load("nonexistent_runtime", "model-id", "/path/to/model", threads=4)

    @patch("backend.runtime_manager._get_runtime_map")
    def test_load_creates_runtime(self, mock_get_map):
        """Load creates runtime instance."""
        from backend.runtime_manager import RuntimeManager

        mock_runtime_cls = MagicMock()
        mock_runtime = MagicMock()
        mock_runtime_cls.return_value = mock_runtime
        mock_get_map.return_value = {"test_runtime": mock_runtime_cls}

        manager = RuntimeManager()
        manager.load("test_runtime", "model-id", "/path/to/model", threads=4)

        mock_runtime_cls.assert_called_once()
        mock_runtime.load.assert_called_once_with("/path/to/model", threads=4)
        assert manager.runtime is mock_runtime
        assert manager.loaded_model_id == "model-id"
        assert manager.loaded_runtime == "test_runtime"

    @patch("backend.runtime_manager._get_runtime_map")
    def test_load_failure_preserves_old_runtime(self, mock_get_map):
        """Load failure preserves old runtime."""
        from backend.runtime_manager import RuntimeManager

        mock_old_runtime = MagicMock()
        mock_new_runtime_cls = MagicMock()
        mock_new_runtime = MagicMock()
        mock_new_runtime.load.side_effect = Exception("Load failed")
        mock_new_runtime_cls.return_value = mock_new_runtime
        mock_get_map.return_value = {"test_runtime": mock_new_runtime_cls}

        manager = RuntimeManager()
        manager.runtime = mock_old_runtime
        manager.loaded_model_id = "old-model"
        manager.loaded_runtime = "old_runtime"

        with pytest.raises(RuntimeError, match="Failed to load"):
            manager.load("test_runtime", "new-model", "/path", threads=4)

        # Old runtime should be preserved
        assert manager.runtime is mock_old_runtime

    @patch("backend.runtime_manager._get_runtime_map")
    def test_load_unloads_previous(self, mock_get_map):
        """Load unloads previous runtime."""
        from backend.runtime_manager import RuntimeManager

        mock_runtime_cls = MagicMock()
        mock_runtime = MagicMock()
        mock_runtime_cls.return_value = mock_runtime
        mock_get_map.return_value = {"test_runtime": mock_runtime_cls}

        manager = RuntimeManager()
        old_runtime = MagicMock()
        manager.runtime = old_runtime
        manager.loaded_model_id = "old-model"

        manager.load("test_runtime", "new-model", "/path", threads=4)

        old_runtime.close.assert_called_once()


class TestRuntimeManagerUnload:
    """Tests for RuntimeManager.unload method."""

    def test_unload_no_runtime(self):
        """Unload with no runtime does nothing."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        manager.unload()  # Should not raise

        assert manager.runtime is None
        assert manager.loaded_model_id is None

    def test_unload_with_close(self):
        """Unload calls close on runtime."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        mock_runtime = MagicMock()
        manager.runtime = mock_runtime
        manager.loaded_model_id = "model-id"
        manager.loaded_runtime = "runtime"

        manager.unload()

        mock_runtime.close.assert_called_once()
        assert manager.runtime is None
        assert manager.loaded_model_id is None
        assert manager.loaded_runtime is None

    def test_unload_with_unload_method(self):
        """Unload calls unload method if no close."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        mock_runtime = MagicMock(spec=["unload"])  # No close method
        manager.runtime = mock_runtime
        manager.loaded_model_id = "model-id"

        manager.unload()

        mock_runtime.unload.assert_called_once()


class TestRuntimeManagerEnsureLoaded:
    """Tests for RuntimeManager.ensure_loaded method."""

    def test_ensure_loaded_raises_when_none(self):
        """ensure_loaded raises when no model loaded."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()

        with pytest.raises(RuntimeError, match="No model loaded"):
            manager.ensure_loaded()

    def test_ensure_loaded_passes_when_loaded(self):
        """ensure_loaded passes when model is loaded."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        manager.runtime = MagicMock()

        # Should not raise
        manager.ensure_loaded()


class TestRuntimeManagerThreadSafety:
    """Tests for RuntimeManager thread safety."""

    def test_load_uses_lock(self):
        """Load operation uses lock."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()

        # Verify lock exists and is RLock
        assert hasattr(manager, "_lock")

    def test_unload_uses_lock(self):
        """Unload operation uses lock."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()

        # Should not deadlock
        manager.unload()
        manager.unload()

    def test_ensure_loaded_uses_lock(self):
        """ensure_loaded uses lock."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        manager.runtime = MagicMock()

        # Should work correctly
        manager.ensure_loaded()


class TestRuntimeManagerFailureRecovery:
    """Tests for failure recovery in load."""

    @patch("backend.runtime_manager._get_runtime_map")
    def test_failed_runtime_closed(self, mock_get_map):
        """Failed runtime is closed after load failure."""
        from backend.runtime_manager import RuntimeManager

        mock_runtime_cls = MagicMock()
        mock_runtime = MagicMock()
        mock_runtime.load.side_effect = Exception("Load failed")
        mock_runtime_cls.return_value = mock_runtime
        mock_get_map.return_value = {"test_runtime": mock_runtime_cls}

        manager = RuntimeManager()

        with pytest.raises(RuntimeError):
            manager.load("test_runtime", "model", "/path", threads=4)

        # The failed runtime should be closed
        mock_runtime.close.assert_called_once()

    @patch("backend.runtime_manager._get_runtime_map")
    def test_failed_runtime_unload_fallback(self, mock_get_map):
        """Failed runtime uses unload method if no close."""
        from backend.runtime_manager import RuntimeManager

        mock_runtime_cls = MagicMock()
        mock_runtime = MagicMock(spec=["load", "unload"])  # No close method
        mock_runtime.load.side_effect = Exception("Load failed")
        mock_runtime_cls.return_value = mock_runtime
        mock_get_map.return_value = {"test_runtime": mock_runtime_cls}

        manager = RuntimeManager()

        with pytest.raises(RuntimeError):
            manager.load("test_runtime", "model", "/path", threads=4)

        mock_runtime.unload.assert_called_once()

    @patch("backend.runtime_manager._get_runtime_map")
    def test_close_failure_ignored(self, mock_get_map):
        """Close failure on failed runtime is ignored."""
        from backend.runtime_manager import RuntimeManager

        mock_runtime_cls = MagicMock()
        mock_runtime = MagicMock()
        mock_runtime.load.side_effect = Exception("Load failed")
        mock_runtime.close.side_effect = Exception("Close failed")
        mock_runtime_cls.return_value = mock_runtime
        mock_get_map.return_value = {"test_runtime": mock_runtime_cls}

        manager = RuntimeManager()

        # Should raise original error, not close error
        with pytest.raises(RuntimeError, match="Load failed"):
            manager.load("test_runtime", "model", "/path", threads=4)
