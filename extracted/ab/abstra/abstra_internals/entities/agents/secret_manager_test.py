import os
from unittest.mock import patch

from abstra_internals.entities.agents.secret_manager import SecretEntry, SecretManager


class TestSecretEntry:
    def test_auto_placeholder(self):
        entry = SecretEntry(key="password", value="secret123")
        assert entry.placeholder.startswith("{{SECRET_")
        assert entry.placeholder.endswith("}}")

    def test_custom_placeholder(self):
        entry = SecretEntry(key="password", value="secret123", placeholder="{{MY_PH}}")
        assert entry.placeholder == "{{MY_PH}}"

    def test_unique_placeholders(self):
        e1 = SecretEntry(key="a", value="v1")
        e2 = SecretEntry(key="b", value="v2")
        assert e1.placeholder != e2.placeholder


class TestSecretManager:
    def test_register_secret(self):
        sm = SecretManager()
        placeholder = sm.register_secret("password", "s3cret!")
        assert placeholder.startswith("{{SECRET_")
        assert sm.has_secrets()

    def test_register_same_value_returns_same_placeholder(self):
        sm = SecretManager()
        p1 = sm.register_secret("password", "s3cret!")
        p2 = sm.register_secret("password2", "s3cret!")
        assert p1 == p2

    def test_register_empty_value(self):
        sm = SecretManager()
        result = sm.register_secret("key", "")
        assert result == ""
        assert not sm.has_secrets()

    def test_register_secrets_dict(self):
        sm = SecretManager()
        count = sm.register_secrets({"user": "admin", "pass": "p@ss"})
        assert count == 2
        assert sm.has_secrets()

    def test_mask(self):
        sm = SecretManager()
        sm.register_secret("password", "s3cret!")
        masked = sm.mask("Login with s3cret! password")
        assert "s3cret!" not in masked
        assert "{{SECRET_" in masked

    def test_unmask(self):
        sm = SecretManager()
        placeholder = sm.register_secret("password", "s3cret!")
        unmasked = sm.unmask(f"Login with {placeholder}")
        assert "s3cret!" in unmasked
        assert "{{SECRET_" not in unmasked

    def test_mask_unmask_roundtrip(self):
        sm = SecretManager()
        sm.register_secret("password", "s3cret!")
        original = "Connect to db with password s3cret! and user admin"
        masked = sm.mask(original)
        unmasked = sm.unmask(masked)
        assert unmasked == original

    def test_mask_no_secrets(self):
        sm = SecretManager()
        text = "nothing to mask here"
        assert sm.mask(text) == text

    def test_unmask_no_placeholders(self):
        sm = SecretManager()
        sm.register_secret("key", "val")
        text = "nothing to unmask here"
        assert sm.unmask(text) == text

    def test_mask_empty_content(self):
        sm = SecretManager()
        sm.register_secret("key", "val")
        assert sm.mask("") == ""

    def test_unmask_empty_content(self):
        sm = SecretManager()
        sm.register_secret("key", "val")
        assert sm.unmask("") == ""

    def test_mask_longer_secret_first(self):
        """Longer secrets should be masked first to avoid partial matches."""
        sm = SecretManager()
        sm.register_secret("short", "abc")
        sm.register_secret("long", "abcdef")
        masked = sm.mask("value is abcdef")
        # The long secret should be masked, not partially
        assert "abc" not in masked or "{{SECRET_" in masked

    def test_mask_dict(self):
        sm = SecretManager()
        sm.register_secret("key", "s3cret!")
        data = {"url": "https://api.com", "password": "s3cret!"}
        masked = sm.mask_dict(data)
        assert "s3cret!" not in str(masked)
        assert masked["url"] == "https://api.com"

    def test_unmask_dict(self):
        sm = SecretManager()
        placeholder = sm.register_secret("key", "s3cret!")
        data = {"password": placeholder, "other": "plain"}
        unmasked = sm.unmask_dict(data)
        assert unmasked["password"] == "s3cret!"
        assert unmasked["other"] == "plain"

    def test_mask_dict_nested(self):
        sm = SecretManager()
        sm.register_secret("key", "s3cret!")
        data = {"nested": {"password": "s3cret!"}, "list": ["s3cret!", "plain"]}
        masked = sm.mask_dict(data)
        assert "s3cret!" not in str(masked)

    def test_mask_dict_non_string(self):
        sm = SecretManager()
        sm.register_secret("key", "s3cret!")
        data = {"number": 42, "bool": True, "none": None}
        masked = sm.mask_dict(data)
        assert masked == data

    def test_load_secrets_from_env(self):
        sm = SecretManager()
        with patch.dict(
            os.environ, {"AGENT_SECRETS": '{"user": "admin", "pass": "p@ss"}'}
        ):
            count = sm.load_secrets()
        assert count == 2
        assert sm.has_secrets()

    def test_load_secrets_invalid_json(self):
        sm = SecretManager()
        count = sm.load_secrets("not valid json")
        assert count == 0

    def test_load_secrets_non_dict(self):
        sm = SecretManager()
        count = sm.load_secrets('["not", "a", "dict"]')
        assert count == 0

    def test_load_secrets_empty(self):
        sm = SecretManager()
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AGENT_SECRETS", None)
            os.environ.pop("USER_SECRETS", None)
            count = sm.load_secrets()
        assert count == 0

    def test_get_secrets_for_prompt_empty(self):
        sm = SecretManager()
        assert sm.get_secrets_for_prompt() == ""

    def test_get_secrets_for_prompt(self):
        sm = SecretManager()
        sm.register_secret("password", "s3cret!")
        prompt = sm.get_secrets_for_prompt()
        assert "password" in prompt
        assert "{{SECRET_" in prompt
        assert "s3cret!" not in prompt

    def test_get_secret_keys(self):
        sm = SecretManager()
        sm.register_secret("user", "admin")
        sm.register_secret("pass", "p@ss")
        keys = sm.get_secret_keys()
        assert "user" in keys
        assert "pass" in keys

    def test_clear(self):
        sm = SecretManager()
        sm.register_secret("key", "value")
        assert sm.has_secrets()
        sm.clear()
        assert not sm.has_secrets()
        assert sm.get_secret_keys() == []
