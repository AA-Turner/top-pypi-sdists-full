"""Tests for FixtureStore."""

import builtins
import json

import pytest

from agentic_devtools.orchestration.llm.errors import (
    FixtureVersionMismatchError,
    NoFixtureFoundError,
)
from agentic_devtools.orchestration.llm.testing import fixture_store as fixture_store_module
from agentic_devtools.orchestration.llm.testing.fixture_store import FixtureStore, load_fixture, save_fixture


class TestFixtureStore:
    """Tests for FixtureStore."""

    def test_save_and_load(self, tmp_path):
        store = FixtureStore(tmp_path)
        store.save("test-key", request={"model": "gpt-4o"}, response={"text": "Hello"})
        record = store.load("test-key")
        assert record["fixture_version"] == 1
        assert record["request"]["model"] == "gpt-4o"
        assert record["response"]["text"] == "Hello"

    def test_exists_returns_true(self, tmp_path):
        store = FixtureStore(tmp_path)
        store.save("my-key", request={}, response={})
        assert store.exists("my-key")

    def test_exists_returns_false(self, tmp_path):
        store = FixtureStore(tmp_path)
        assert not store.exists("missing-key")

    def test_override_takes_precedence(self, tmp_path):
        store = FixtureStore(tmp_path)
        # Save regular fixture
        store.save("key", request={}, response={"text": "original"})
        # Create override
        override_path = tmp_path / "key.override.json"
        override_path.write_text(
            json.dumps(
                {
                    "fixture_version": 1,
                    "request": {},
                    "response": {"text": "override"},
                }
            )
        )
        record = store.load("key")
        assert record["response"]["text"] == "override"

    def test_not_found_raises(self, tmp_path):
        store = FixtureStore(tmp_path)
        with pytest.raises(NoFixtureFoundError) as exc_info:
            store.load("nonexistent")
        assert exc_info.value.fixture_key == "nonexistent"

    def test_version_mismatch_raises(self, tmp_path):
        fixture_path = tmp_path / "old.json"
        fixture_path.write_text(
            json.dumps(
                {
                    "fixture_version": 99,
                    "request": {},
                    "response": {},
                }
            )
        )
        with pytest.raises(FixtureVersionMismatchError) as exc_info:
            load_fixture("old", fixture_dir=tmp_path)
        assert exc_info.value.expected_version == 1
        assert exc_info.value.actual_version == 99

    def test_load_uses_utf8_encoding(self, tmp_path, monkeypatch):
        fixture_path = tmp_path / "utf8.json"
        fixture_path.write_text(
            json.dumps({"fixture_version": 1, "request": {}, "response": {"text": "Grüezi"}}),
            encoding="utf-8",
        )
        encodings: list[str | None] = []

        def recording_open(*args, **kwargs):
            encodings.append(kwargs.get("encoding"))
            return builtins.open(*args, **kwargs)

        monkeypatch.setattr(fixture_store_module, "open", recording_open, raising=False)

        record = load_fixture("utf8", fixture_dir=tmp_path)

        assert record["response"]["text"] == "Grüezi"
        assert encodings == ["utf-8"]


class TestFixtureStoreProperty:
    """Tests for FixtureStore.fixture_dir property."""

    def test_fixture_dir_property(self, tmp_path):
        store = FixtureStore(tmp_path)
        assert store.fixture_dir == tmp_path


class TestFixtureStoreExistsOverride:
    """Tests for FixtureStore.exists with override files."""

    def test_exists_with_override_file(self, tmp_path):
        override_path = tmp_path / "my-key.override.json"
        override_path.write_text(json.dumps({"fixture_version": 1, "request": {}, "response": {}}))
        store = FixtureStore(tmp_path)
        assert store.exists("my-key")


class TestSaveFixture:
    """Tests for save_fixture."""

    def test_creates_directory(self, tmp_path):
        target = tmp_path / "nested" / "dir"
        path = save_fixture("k", request={}, response={}, fixture_dir=target)
        assert path.exists()

    def test_file_contains_valid_json(self, tmp_path):
        path = save_fixture("k", request={"a": 1}, response={"b": 2}, fixture_dir=tmp_path)
        with open(path) as f:
            data = json.load(f)
        assert data["fixture_version"] == 1
        assert data["request"] == {"a": 1}
        assert data["response"] == {"b": 2}

    def test_save_uses_utf8_encoding(self, tmp_path, monkeypatch):
        encodings: list[str | None] = []

        def recording_open(*args, **kwargs):
            encodings.append(kwargs.get("encoding"))
            return builtins.open(*args, **kwargs)

        monkeypatch.setattr(fixture_store_module, "open", recording_open, raising=False)

        path = save_fixture("k", request={}, response={"text": "Grüezi"}, fixture_dir=tmp_path)

        assert path.read_text(encoding="utf-8")
        assert encodings == ["utf-8"]


class TestFixtureKeyValidation:
    """Tests for _validate_fixture_key path-traversal protection."""

    def test_load_fixture_rejects_forward_slash(self, tmp_path):
        with pytest.raises(ValueError, match="path separators"):
            load_fixture("../secret", fixture_dir=tmp_path)

    def test_load_fixture_rejects_backslash(self, tmp_path):
        with pytest.raises(ValueError, match="path separators"):
            load_fixture("sub\\key", fixture_dir=tmp_path)

    def test_save_fixture_rejects_forward_slash(self, tmp_path):
        with pytest.raises(ValueError, match="path separators"):
            save_fixture("../evil", request={}, response={}, fixture_dir=tmp_path)

    def test_save_fixture_rejects_backslash(self, tmp_path):
        with pytest.raises(ValueError, match="path separators"):
            save_fixture("sub\\key", request={}, response={}, fixture_dir=tmp_path)

    def test_store_exists_rejects_path_traversal(self, tmp_path):
        store = FixtureStore(tmp_path)
        with pytest.raises(ValueError, match="path separators"):
            store.exists("../other")

    def test_store_load_rejects_path_traversal(self, tmp_path):
        store = FixtureStore(tmp_path)
        with pytest.raises(ValueError, match="path separators"):
            store.load("../other")

    def test_store_save_rejects_path_traversal(self, tmp_path):
        store = FixtureStore(tmp_path)
        with pytest.raises(ValueError, match="path separators"):
            store.save("../evil", request={}, response={})

    @pytest.mark.parametrize("invalid_char", [":", '"', "<", ">", "|", "?", "*"])
    def test_save_fixture_rejects_invalid_filename_characters(self, tmp_path, invalid_char):
        with pytest.raises(ValueError, match="invalid filename character"):
            save_fixture(f"bad{invalid_char}key", request={}, response={}, fixture_dir=tmp_path)

    @pytest.mark.parametrize("key", [" leading", "trailing ", "\tboth\t"])
    def test_save_fixture_rejects_leading_or_trailing_whitespace(self, tmp_path, key):
        with pytest.raises(ValueError, match="leading/trailing whitespace"):
            save_fixture(key, request={}, response={}, fixture_dir=tmp_path)

    @pytest.mark.parametrize("key", ["CON", "nul.json", "LPT1"])
    def test_save_fixture_rejects_windows_reserved_names(self, tmp_path, key):
        with pytest.raises(ValueError, match="reserved Windows filename"):
            save_fixture(key, request={}, response={}, fixture_dir=tmp_path)

    def test_save_fixture_rejects_empty_key(self, tmp_path):
        with pytest.raises(ValueError, match="must not be empty"):
            save_fixture("", request={}, response={}, fixture_dir=tmp_path)

    @pytest.mark.parametrize("key", [".", ".."])
    def test_save_fixture_rejects_reserved_relative_segments(self, tmp_path, key):
        with pytest.raises(ValueError, match="reserved relative path segment"):
            save_fixture(key, request={}, response={}, fixture_dir=tmp_path)

    def test_save_fixture_rejects_control_characters(self, tmp_path):
        with pytest.raises(ValueError, match="control characters"):
            save_fixture("bad\nkey", request={}, response={}, fixture_dir=tmp_path)

    def test_save_fixture_rejects_trailing_dot(self, tmp_path):
        with pytest.raises(ValueError, match="must not end with a dot"):
            save_fixture("bad.", request={}, response={}, fixture_dir=tmp_path)

    def test_valid_key_is_accepted(self, tmp_path):
        """Keys without path separators must not raise."""
        path = save_fixture("valid-key_01", request={}, response={"text": "ok"}, fixture_dir=tmp_path)
        assert path.exists()
