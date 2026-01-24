from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from tabpfn_common_utils.telemetry.core.state import (
    _DEFAULT_STATE,
    _HAS_FILELOCK,
    APP,
    FILENAME,
    VENDOR,
    _write_with_lock,
    _cleanup_temp_file,
    _ensure_dir,
    _read,
    _set_file_permissions,
    _state_path,
    get_property,
    load_state,
    save_state,
    set_property,
)


class TestStateConstants:
    def test_app_constant(self):
        assert APP == ".tabpfn"

    def test_vendor_constant(self):
        assert VENDOR == "priorlabs"

    def test_filename_constant(self):
        assert FILENAME == "state.json"

    def test_filelock_availability(self):
        assert isinstance(_HAS_FILELOCK, bool)

    def test_default_state_schema(self):
        assert isinstance(_DEFAULT_STATE, dict)
        assert "created_at" in _DEFAULT_STATE
        assert "user_id" in _DEFAULT_STATE
        assert "email" in _DEFAULT_STATE
        assert "nr_prompts" in _DEFAULT_STATE
        assert "last_prompted_at" in _DEFAULT_STATE


class TestStatePath:
    def test_state_path_with_tabpfn_state_path_env(self):
        test_path = "/custom/state/path"

        with patch.dict(os.environ, {"TABPFN_STATE_PATH": test_path}):
            result = _state_path()
            assert result == Path(test_path).expanduser()

    def test_state_path_with_tabpfn_state_dir_env(self):
        test_dir = "/custom/state/dir"

        with patch.dict(os.environ, {"TABPFN_STATE_DIR": test_dir}):
            result = _state_path()
            expected = Path(test_dir).expanduser() / FILENAME
            assert result == expected

    def test_state_path_with_both_env_vars(self):
        state_path = "/custom/state/path"
        state_dir = "/custom/state/dir"

        environ_patch = {
            "TABPFN_STATE_PATH": state_path,
            "TABPFN_STATE_DIR": state_dir,
        }
        with patch.dict(os.environ, environ_patch):
            result = _state_path()
            assert result == Path(state_path).expanduser()

    def test_state_path_default(self):
        module = "tabpfn_common_utils.telemetry.core.state"
        with (
            patch.dict(os.environ, {}, clear=True),
            patch(f"{module}.user_config_dir") as mock_user_config_dir,
        ):
            mock_user_config_dir.return_value = "/default/state/dir"
            result = _state_path()
            expected = Path("/default/state/dir") / FILENAME
            assert result == expected
            mock_user_config_dir.assert_called_once_with(APP, VENDOR)

    def test_state_path_expands_user_home(self):
        test_path = "~/custom/state"

        with patch.dict(os.environ, {"TABPFN_STATE_PATH": test_path}):
            result = _state_path()
            assert result == Path(test_path).expanduser()


class TestEnsureDir:
    def test_ensure_dir_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "subdir" / "config.json"

            # Directory should not exist initially
            assert not test_path.parent.exists()

            _ensure_dir(test_path)

            # Directory should exist after calling _ensure_dir
            assert test_path.parent.exists()
            assert test_path.parent.is_dir()

    def test_ensure_dir_handles_existing_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "config.json"

            # Directory already exists
            assert test_path.parent.exists()

            # Should not raise an exception
            _ensure_dir(test_path)
            assert test_path.parent.exists()

    def test_ensure_dir_sets_permissions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "subdir" / "state.json"

            with patch("pathlib.Path.chmod") as mock_chmod:
                _ensure_dir(test_path)
                mock_chmod.assert_called_once_with(0o700)

    def test_ensure_dir_handles_chmod_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "subdir" / "state.json"

            with patch("pathlib.Path.chmod", side_effect=OSError):
                # Should not raise an exception
                _ensure_dir(test_path)
                assert test_path.parent.exists()


class TestSetFilePermissions:
    def test_set_file_permissions_success(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = Path(temp_file.name)

            with patch("pathlib.Path.chmod") as mock_chmod:
                _set_file_permissions(temp_path)
                mock_chmod.assert_called_once_with(0o600)

            temp_path.unlink()

    def test_set_file_permissions_handles_error(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = Path(temp_file.name)

            with patch("pathlib.Path.chmod", side_effect=OSError):
                # Should not raise an exception
                _set_file_permissions(temp_path)

            temp_path.unlink()


class TestCleanupTempFile:
    def test_cleanup_temp_file_exists(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            assert Path(temp_path).exists()

            _cleanup_temp_file(temp_path)

            assert not Path(temp_path).exists()

    def test_cleanup_temp_file_handles_error(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            with patch("pathlib.Path.unlink", side_effect=OSError):
                _cleanup_temp_file(temp_path)
            temp_file.close()
            Path(temp_path).unlink()


class TestRead:
    def test_read_existing_valid_file(self):
        test_data = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = Path(temp_file.name)

        try:
            result = _read(temp_path)
            assert result == test_data
        finally:
            temp_path.unlink()

    def test_read_non_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            non_existent_path = Path(temp_file.name)
            result = _read(non_existent_path)
            assert result == {}

    def test_read_corrupt_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            temp_file.write("invalid json content")
            temp_path = Path(temp_file.name)

        try:
            result = _read(temp_path)
            assert result == {}
        finally:
            temp_path.unlink()

    def test_read_empty_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            result = _read(temp_path)
            assert result == {}
        finally:
            temp_path.unlink()


class TestAtomicWrite:
    def test_write_with_lock_success(self):
        test_data = {"user_id": "test-123", "created_at": "2024-01-01"}

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"

            _write_with_lock(config_path, test_data)

            # File should exist and contain correct data
            assert config_path.exists()
            with config_path.open("r") as f:
                result = json.load(f)
            assert result == test_data

    def test_write_with_lock_creates_directory(self):
        test_data = {"key": "value"}

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "subdir" / "config.json"

            # Parent directory should not exist
            assert not config_path.parent.exists()

            _write_with_lock(config_path, test_data)

            # Parent directory should be created
            assert config_path.parent.exists()
            assert config_path.exists()

    def test_write_with_lock_cleans_up_temp_file(self):
        test_data = {"key": "value"}

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            module = "tabpfn_common_utils.telemetry.core.state"
            with patch(f"{module}._cleanup_temp_file") as mock_cleanup:
                _write_with_lock(state_path, test_data)
                mock_cleanup.assert_called_once()

    def test_write_with_lock_json_formatting(self):
        test_data = {"key": "value", "number": 42}

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            _write_with_lock(state_path, test_data)

            # Read the file and check formatting
            with state_path.open("r") as f:
                content = f.read()

            # Should be compact JSON (no spaces after separators)
            assert '":' in content  # No space after colon
            assert '","' in content  # No space after comma


class TestLoadState:
    def test_load_state_existing_file(self):
        test_data = {"user_id": True, "email": "test@example.com"}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = Path(temp_file.name)

        try:
            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=temp_path):
                result = load_state()
                assert result["user_id"] is True
                assert result["email"] == "test@example.com"
                assert "created_at" in result  # migrated
        finally:
            temp_path.unlink()

    def test_load_state_non_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            non_existent_path = Path(temp_file.name)
            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=non_existent_path):
                result = load_state()
                assert "created_at" in result
                assert result["user_id"] is None


class TestSaveState:
    def test_save_state_success(self):
        test_data = {"user_id": True, "email": "test@example.com"}

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                save_state(test_data)

                assert state_path.exists()
                with state_path.open("r") as f:
                    result = json.load(f)
                assert result["user_id"] is True
                assert result["email"] == "test@example.com"
                assert "created_at" in result  # migrated

    def test_save_state_handles_complex_data(self):
        test_data = {
            "user_id": True,
            "email": "test@example.com",
            "email_prompt_count": 2,
            "last_prompted_at": "2024-01-01T00:00:00Z",
            "custom": {"key": "value", "list": [1, 2, 3]},
            "unicode": "测试数据",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                save_state(test_data)

                assert state_path.exists()
                with state_path.open("r", encoding="utf-8") as f:
                    result = json.load(f)
                assert result["user_id"] is True
                assert result["email"] == "test@example.com"
                assert result["custom"]["key"] == "value"
                assert result["unicode"] == "测试数据"


class TestStateIntegration:
    def test_save_and_load_state_roundtrip(self):
        original_data = {
            "user_id": True,
            "email": "test@example.com",
            "email_prompt_count": 1,
            "last_prompted_at": "2024-01-01T00:00:00Z",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                # Save state
                save_state(original_data)

                # Load state
                loaded_data = load_state()

                # Should have all original data plus migrated fields
                assert loaded_data["user_id"] is True
                assert loaded_data["email"] == "test@example.com"
                assert loaded_data["email_prompt_count"] == 1
                assert loaded_data["last_prompted_at"] == "2024-01-01T00:00:00Z"
                assert "created_at" in loaded_data

    def test_multiple_saves_preserve_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                # Initial save
                save_state({"user_id": False, "email_prompt_count": 0})

                # Update with additional data
                state = {
                    "user_id": True,
                    "email": "test@example.com",
                    "email_prompt_count": 1,
                }
                save_state(state)

                # Load and verify
                loaded_data = load_state()
                assert loaded_data["user_id"] is True
                assert loaded_data["email"] == "test@example.com"
                assert loaded_data["email_prompt_count"] == 1

    def test_state_path_environment_priority(self):
        environ_patch = {
            "TABPFN_STATE_PATH": "/env/path/state.json",
            "TABPFN_STATE_DIR": "/env/dir",
        }
        with patch.dict(os.environ, environ_patch):
            path = _state_path()
            assert path == Path("/env/path/state.json").expanduser()

    def test_state_handles_unicode_data(self):
        unicode_data = {
            "user_id": True,
            "email": "测试@example.com",
            "description": "这是一个测试状态",
            "emoji": "🚀",
            "mixed": "Test 测试 🎉",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                save_state(unicode_data)
                loaded_data = load_state()
                assert loaded_data["email"] == "测试@example.com"
                assert loaded_data["description"] == "这是一个测试状态"
                assert loaded_data["emoji"] == "🚀"
                assert loaded_data["mixed"] == "Test 测试 🎉"


class TestPropertyAccess:
    def test_get_property_existing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                # Set up initial state
                save_state({"user_id": True, "email": "test@example.com"})

                # Test getting existing properties
                assert get_property("user_id") is True
                assert get_property("email") == "test@example.com"

    def test_set_property(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"

            name = "tabpfn_common_utils.telemetry.core.state._state_path"
            with patch(name, return_value=state_path):
                # Set properties
                set_property("user_id", value=True)
                set_property("email", "test@example.com")
                set_property("email_prompt_count", 2)

                # Verify they were set
                loaded_data = load_state()
                assert loaded_data["user_id"] is True
                assert loaded_data["email"] == "test@example.com"
                assert loaded_data["email_prompt_count"] == 2
