"""Tests for redact_sensitive_keys blocklist matching."""

from agentic_devtools.orchestration.execution.tracing import redact_sensitive_keys


class TestRedactSensitiveKeys:
    def test_redacts_token_key(self) -> None:
        data = {"token": "abc123", "name": "test"}
        result = redact_sensitive_keys(data)
        assert result["token"] == "[REDACTED]"
        assert result["name"] == "test"

    def test_redacts_case_insensitive(self) -> None:
        data = {"TOKEN": "secret", "API_KEY": "key123"}
        result = redact_sensitive_keys(data)
        assert result["TOKEN"] == "[REDACTED]"
        assert result["API_KEY"] == "[REDACTED]"

    def test_redacts_nested_dicts(self) -> None:
        data = {"config": {"password": "secret", "host": "localhost"}}
        result = redact_sensitive_keys(data)
        assert result["config"]["password"] == "[REDACTED]"
        assert result["config"]["host"] == "localhost"

    def test_redacts_sensitive_keys_in_list_of_dicts(self) -> None:
        data = {"messages": [{"role": "system", "token": "secret-token"}]}
        result = redact_sensitive_keys(data)
        assert result["messages"][0]["token"] == "[REDACTED]"

    def test_preserves_non_sensitive(self) -> None:
        data = {"name": "Alice", "count": 42, "active": True}
        result = redact_sensitive_keys(data)
        assert result == data

    def test_custom_blocklist(self) -> None:
        data = {"custom_field": "value", "name": "test"}
        result = redact_sensitive_keys(data, blocklist=frozenset({"custom_field"}))
        assert result["custom_field"] == "[REDACTED]"
        assert result["name"] == "test"

    def test_empty_dict(self) -> None:
        result = redact_sensitive_keys({})
        assert result == {}

    def test_does_not_mutate_input(self) -> None:
        data = {"token": "secret"}
        redact_sensitive_keys(data)
        assert data["token"] == "secret"

    def test_redacts_sensitive_keys_in_nested_list_of_lists(self) -> None:
        """Lists inside lists must be traversed recursively."""
        data = {"items": [[{"token": "secret"}]]}
        result = redact_sensitive_keys(data)
        assert result["items"][0][0]["token"] == "[REDACTED]"

    def test_redacts_sensitive_keys_in_mixed_nested_list(self) -> None:
        """Mixed list of plain dict and nested list must both be redacted."""
        data = {"items": [{"token": "t1"}, [{"password": "p2"}]]}
        result = redact_sensitive_keys(data)
        assert result["items"][0]["token"] == "[REDACTED]"
        assert result["items"][1][0]["password"] == "[REDACTED]"

    def test_preserves_scalar_items_in_nested_list(self) -> None:
        """Scalar values inside nested lists must be returned unchanged."""
        data = {"nums": [1, [2, 3], "text"]}
        result = redact_sensitive_keys(data)
        assert result["nums"] == [1, [2, 3], "text"]
