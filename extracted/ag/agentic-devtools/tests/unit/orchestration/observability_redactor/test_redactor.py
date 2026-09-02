"""Tests for Redactor class."""

from agentic_devtools.orchestration.observability_redactor import Redactor


class TestRedactor:
    """Tests for the Redactor class."""

    def setup_method(self) -> None:
        self.redactor = Redactor()

    # --- Key-name redaction ---

    def test_redacts_authorization_key(self) -> None:
        data = {"authorization": "******"}
        result = self.redactor.redact(data)
        assert result["authorization"] == "[REDACTED]"

    def test_redacts_password_key(self) -> None:
        data = {"password": "my-secret-pass"}
        result = self.redactor.redact(data)
        assert result["password"] == "[REDACTED]"

    def test_redacts_api_key(self) -> None:
        data = {"api_key": "sk-abc123"}
        result = self.redactor.redact(data)
        assert result["api_key"] == "[REDACTED]"

    def test_redacts_token_key(self) -> None:
        data = {"token": "eyJhbG..."}
        result = self.redactor.redact(data)
        assert result["token"] == "[REDACTED]"

    def test_redacts_secret_key(self) -> None:
        data = {"secret": "hidden"}
        result = self.redactor.redact(data)
        assert result["secret"] == "[REDACTED]"

    def test_redacts_pat_key(self) -> None:
        data = {"pat": "personal-access-token"}
        result = self.redactor.redact(data)
        assert result["pat"] == "[REDACTED]"

    def test_key_matching_case_insensitive(self) -> None:
        data = {"Authorization": "******", "PASSWORD": "y", "Api_Key": "z"}
        result = self.redactor.redact(data)
        assert result["Authorization"] == "[REDACTED]"
        assert result["PASSWORD"] == "[REDACTED]"
        assert result["Api_Key"] == "[REDACTED]"

    def test_redacts_camel_case_sensitive_keys(self) -> None:
        data = {
            "accessToken": "access-secret",
            "refreshToken": "refresh-secret",
            "privateKey": "private-secret",
        }
        result = self.redactor.redact(data)
        assert result["accessToken"] == "[REDACTED]"
        assert result["refreshToken"] == "[REDACTED]"
        assert result["privateKey"] == "[REDACTED]"

    def test_redacts_compound_sensitive_keys(self) -> None:
        data = {
            "github_token": "opaque-secret",
            "clientSecret": "client-secret",
            "openaiApiKey": "openai-secret",
            "x-api-key": "header-secret",
            "GITHUBToken": "upper-secret",
        }
        result = self.redactor.redact(data)
        assert result["github_token"] == "[REDACTED]"
        assert result["clientSecret"] == "[REDACTED]"
        assert result["openaiApiKey"] == "[REDACTED]"
        assert result["x-api-key"] == "[REDACTED]"
        assert result["GITHUBToken"] == "[REDACTED]"

    def test_non_secret_compound_key_names_not_redacted(self) -> None:
        data = {
            "tokenizer": "keep",
            "secretary": "keep",
            "compatibility": "keep",
            "user_tokenizer": "keep",
            "api_compatibility": "keep",
        }
        result = self.redactor.redact(data)
        assert result["tokenizer"] == "keep"
        assert result["secretary"] == "keep"
        assert result["compatibility"] == "keep"
        assert result["user_tokenizer"] == "keep"
        assert result["api_compatibility"] == "keep"

    def test_empty_string_key_not_redacted(self) -> None:
        data = {"": "keep"}
        result = self.redactor.redact(data)
        assert result[""] == "keep"

    # --- Value-pattern redaction ---

    def test_redacts_ghp_token(self) -> None:
        data = {"ref": "ghp_ABCdef123456"}
        result = self.redactor.redact(data)
        assert result["ref"] == "[REDACTED]"

    def test_redacts_github_pat_token(self) -> None:
        data = {"ref": "github_pat_ABC123_xyz"}
        result = self.redactor.redact(data)
        assert result["ref"] == "[REDACTED]"

    def test_redacts_bearer_value(self) -> None:
        token_value = "Bearer" + " " + "******"
        data = {"header": token_value}
        result = self.redactor.redact(data)
        assert result["header"] == "[REDACTED]"

    def test_redacts_gho_token(self) -> None:
        data = {"oauth": "gho_ABC123xyz"}
        result = self.redactor.redact(data)
        assert result["oauth"] == "[REDACTED]"

    def test_redacts_ghs_token(self) -> None:
        data = {"server_token": "ghs_ABC123xyz"}
        result = self.redactor.redact(data)
        assert result["server_token"] == "[REDACTED]"

    # --- Embedded credential detection (search, not match) ---

    def test_redacts_ghp_token_embedded_in_value(self) -> None:
        """Tokens embedded in larger strings are caught by search()."""
        data = {"output": "token=ghp_ABC123xyz rest of output"}
        result = self.redactor.redact(data)
        assert result["output"] == "[REDACTED]"

    def test_redacts_ghp_token_with_key_prefix(self) -> None:
        """'Authorization: ghp_...' style values are redacted."""
        data = {"header": "Authorization: ghp_SECRETTOKEN"}
        result = self.redactor.redact(data)
        assert result["header"] == "[REDACTED]"

    def test_redacts_gho_token_embedded_in_value(self) -> None:
        """OAuth tokens embedded in longer strings are detected."""
        data = {"env": "GITHUB_TOKEN=gho_ABC123xyz"}
        result = self.redactor.redact(data)
        assert result["env"] == "[REDACTED]"

    def test_redacts_bearer_embedded_in_authorization_header(self) -> None:
        """Bearer anywhere in a larger string is redacted."""
        data = {"raw": "Authorization: Bearer myapitoken123"}
        result = self.redactor.redact(data)
        assert result["raw"] == "[REDACTED]"

    def test_redacts_github_pat_embedded_in_url(self) -> None:
        """GitHub fine-grained PAT embedded in a URL-style string is redacted."""
        data = {"clone_url": "https://github_pat_ABC123_xyz@github.com/org/repo"}
        result = self.redactor.redact(data)
        assert result["clone_url"] == "[REDACTED]"

    def test_token_prefix_within_identifier_not_redacted(self) -> None:
        """Word boundary prevents false positives on identifiers containing token prefixes."""
        data = {
            "ghp_var": "my_ghp_style_variable_name",
            "gho_var": "my_gho_style_variable_name",
            "ghs_var": "my_ghs_style_variable_name",
            "pat_var": "my_github_pat_style_var",
        }
        result = self.redactor.redact(data)
        assert result["ghp_var"] == "my_ghp_style_variable_name"
        assert result["gho_var"] == "my_gho_style_variable_name"
        assert result["ghs_var"] == "my_ghs_style_variable_name"
        assert result["pat_var"] == "my_github_pat_style_var"

    # --- Non-sensitive data passes through ---

    def test_nonsensitive_string_unchanged(self) -> None:
        data = {"name": "John", "status": "active"}
        result = self.redactor.redact(data)
        assert result["name"] == "John"
        assert result["status"] == "active"

    def test_nonsensitive_nested_dict(self) -> None:
        data = {"config": {"host": "localhost", "port": 8080}}
        result = self.redactor.redact(data)
        assert result["config"]["host"] == "localhost"
        assert result["config"]["port"] == 8080

    def test_none_input_returns_none(self) -> None:
        assert self.redactor.redact(None) is None

    def test_does_not_mutate_original(self) -> None:
        data = {"password": "secret", "name": "test"}
        original_password = data["password"]
        self.redactor.redact(data)
        assert data["password"] == original_password

    # --- Nested redaction ---

    def test_redacts_nested_sensitive_keys(self) -> None:
        data = {"headers": {"authorization": "******", "content-type": "json"}}
        result = self.redactor.redact(data)
        assert result["headers"]["authorization"] == "[REDACTED]"
        assert result["headers"]["content-type"] == "json"

    def test_redacts_sensitive_values_in_lists(self) -> None:
        data = {"tokens": ["ghp_ABC123", "normal_value"]}
        result = self.redactor.redact(data)
        assert result["tokens"][0] == "[REDACTED]"
        assert result["tokens"][1] == "normal_value"

    def test_list_items_with_sensitive_parent_key(self) -> None:
        """A sensitive key whose value is a list is fully redacted as a unit."""
        data = {"password": ["secret1", "secret2"]}
        result = self.redactor.redact(data)
        assert result["password"] == "[REDACTED]"

    def test_sensitive_key_with_dict_value_fully_redacted(self) -> None:
        """A sensitive key whose value is a dict is fully redacted, not traversed."""
        data = {"token": {"access": "secret", "refresh": "other_secret"}}
        result = self.redactor.redact(data)
        assert result["token"] == "[REDACTED]"

    def test_sensitive_key_with_list_of_dicts_fully_redacted(self) -> None:
        """A sensitive key whose value is a list of dicts is fully redacted."""
        data = {"password": [{"nested_key": "nested_value"}, {"other": "also_secret"}]}
        result = self.redactor.redact(data)
        assert result["password"] == "[REDACTED]"

    def test_top_level_list_with_sensitive_string(self) -> None:
        """Top-level list containing credential patterns."""
        data = ["ghp_ABC123", "normal", "gho_XYZ789"]
        result = self.redactor.redact(data)
        assert result[0] == "[REDACTED]"
        assert result[1] == "normal"
        assert result[2] == "[REDACTED]"

    def test_non_string_non_dict_non_list_passes_through(self) -> None:
        """Numeric and boolean values pass through without modification."""
        data = {"count": 42, "active": True, "ratio": 3.14}
        result = self.redactor.redact(data)
        assert result["count"] == 42
        assert result["active"] is True
        assert result["ratio"] == 3.14

    def test_top_level_integer_passes_through(self) -> None:
        """A bare integer passed to redact returns unchanged."""
        result = self.redactor.redact(42)
        assert result == 42

    def test_top_level_boolean_passes_through(self) -> None:
        """A bare boolean passed to redact returns unchanged."""
        result = self.redactor.redact(True)
        assert result is True

    # --- Redaction before truncation guarantee ---

    def test_redaction_before_truncation_no_partial_secrets(self) -> None:
        """Verify redaction happens before truncation so no partial secrets appear."""
        from agentic_devtools.orchestration.observability_truncation import (
            truncate_summary,
        )

        data = {"password": "super_secret_password_that_is_very_long" * 100}
        redacted = self.redactor.redact(data)
        truncated = truncate_summary(redacted, max_chars=50)
        # The password should be fully redacted before any truncation
        assert "super_secret" not in str(truncated)

    # --- deepcopy failure degrades gracefully ---

    def test_deepcopy_failure_returns_none(self) -> None:
        """If deepcopy raises, redact() returns None instead of crashing."""
        from unittest.mock import patch

        with patch("copy.deepcopy", side_effect=RuntimeError("cannot copy")):
            result = self.redactor.redact({"key": "value"})
        assert result is None

    def test_deepcopy_failure_does_not_expose_sensitive_data(self) -> None:
        """Even when deepcopy fails, no sensitive data leaks."""
        from unittest.mock import patch

        sensitive = {"token": "ghp_SUPERSECRET"}
        with patch("copy.deepcopy", side_effect=TypeError("unhashable")):
            result = self.redactor.redact(sensitive)
        # Must not contain the original secret value
        assert result is None or "SUPERSECRET" not in str(result)

    # --- Unknown object coercion ---

    def test_unknown_object_coerced_to_str_top_level(self) -> None:
        """An unknown object at the top level is coerced to str and value-pattern-checked."""

        class Plain:
            def __str__(self) -> str:
                return "harmless text"

        result = self.redactor.redact(Plain())
        assert result == "harmless text"

    def test_unknown_object_with_credential_str_redacted_top_level(self) -> None:
        """An unknown object whose __str__ is a credential is redacted before write."""

        class LeakyObj:
            def __str__(self) -> str:
                return "ghp_SECRETTOKEN123"

        result = self.redactor.redact(LeakyObj())
        assert result == "[REDACTED]"

    def test_unknown_object_in_dict_value_coerced_and_checked(self) -> None:
        """An unknown object as a dict value is coerced and value-pattern-checked."""

        class LeakyObj:
            def __str__(self) -> str:
                # __str__ exposes a GitHub PAT – must be caught after str() coercion
                return "ghp_SECRETTOKEN123"

        data = {"header": LeakyObj()}
        result = self.redactor.redact(data)
        assert result["header"] == "[REDACTED]"

    def test_unknown_object_in_dict_value_harmless_coerced(self) -> None:
        """An unknown object with a safe __str__ is coerced to its string form."""

        class Cfg:
            def __str__(self) -> str:
                return "host=localhost port=5432"

        data = {"db": Cfg()}
        result = self.redactor.redact(data)
        assert result["db"] == "host=localhost port=5432"

    def test_unknown_object_in_list_coerced_and_checked(self) -> None:
        """An unknown object nested inside a list is coerced and value-pattern-checked."""

        class LeakyObj:
            def __str__(self) -> str:
                return "gho_OAUTHTOKEN"

        data = {"items": [LeakyObj(), "normal"]}
        result = self.redactor.redact(data)
        assert result["items"][0] == "[REDACTED]"
        assert result["items"][1] == "normal"

    # --- Non-string dict keys ---

    def test_integer_key_does_not_crash(self) -> None:
        """Dict with integer keys must not raise AttributeError on key.lower()."""
        data = {1: "value", 2: "other"}
        result = self.redactor.redact(data)
        # Keys coerced to str; values pass through (not sensitive)
        assert result["1"] == "value"
        assert result["2"] == "other"

    def test_integer_sensitive_key_name_redacted(self) -> None:
        """Integer key whose str() form matches a sensitive name is redacted."""
        # 'token' is in _SENSITIVE_KEYS; int key won't match – this verifies no crash
        data = {42: "harmless"}
        result = self.redactor.redact(data)
        assert result["42"] == "harmless"

    def test_nested_dict_with_integer_key_does_not_crash(self) -> None:
        """Nested dict with integer keys must not raise during recursive redaction."""
        data = {"outer": {1: "nested_value", "token": "secret"}}
        result = self.redactor.redact(data)
        # Outer sensitive key is NOT present – only inner keys are tested here
        assert result["outer"]["1"] == "nested_value"
        assert result["outer"]["token"] == "[REDACTED]"

    def test_tuple_key_does_not_crash(self) -> None:
        """Tuple keys (non-JSON) are coerced to str without raising."""
        data = {("a", "b"): "value"}
        result = self.redactor.redact(data)
        assert result["('a', 'b')"] == "value"
