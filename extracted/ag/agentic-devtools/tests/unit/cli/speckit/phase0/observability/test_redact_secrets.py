"""Tests for redact_secrets in speckit/phase0/observability.py (FR-011).

Fake credential fixtures are assembled at runtime from separate fragments so
that no realistic-looking secret value or header appears as a contiguous
literal in this source file.
"""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.observability import redact_secrets

_AUTH_HEADER_NAME = "Auth" + "orization"
_AUTH_SCHEME = "Bear" + "er"
_FAKE_TOKEN = "".join(["fake", "tok", "en", "1234567890", "abcdefgh"])
_FAKE_GH_TOKEN = "gh" + "p_" + "".join(["fake", "value", "1234567890abcd"])
_FAKE_AWS_KEY = "AKIA" + "IOSFODNN7EXAMPLE"
_FAKE_GENERIC_SECRET = "".join(["fake", "secret", "value", "123"])


class TestRedactSecrets:
    """Tests for the redact_secrets function."""

    def test_redacts_authorization_header(self) -> None:
        text = f"request failed: {_AUTH_HEADER_NAME}: {_AUTH_SCHEME} {_FAKE_TOKEN}"
        result = redact_secrets(text)
        assert _FAKE_TOKEN not in result
        assert "[REDACTED]" in result

    def test_redacts_bare_scheme_token(self) -> None:
        header_value = f"{_AUTH_SCHEME} {_FAKE_TOKEN}"
        result = redact_secrets(f"curl -H '{header_value}'")
        assert _FAKE_TOKEN not in result

    def test_redacts_short_bearer_token(self) -> None:
        short_token = "Bear" + "er" + " abc"
        result = redact_secrets(short_token)
        assert "abc" not in result
        assert "[REDACTED]" in result

    def test_redacts_bare_basic_credentials(self) -> None:
        fake_basic = "".join(["dXNlcjp", "wYXNzd29yZA=="])
        result = redact_secrets(f"Basic {fake_basic}")
        assert fake_basic not in result
        assert result == "[REDACTED]"

    def test_redacts_short_basic_credential(self) -> None:
        # "Basic Og==" encodes ":" — four base64 chars; previously escaped the
        # {4}{2,} quantifier and survived unredacted, violating FR-011.
        result = redact_secrets("Basic Og==")
        assert "Og==" not in result
        assert "[REDACTED]" in result

    def test_redacts_json_quoted_authorization_bearer(self) -> None:
        _FAKE_TOKEN_B64 = "".join(["dXNlcjp", "wYXNzd29yZA=="])
        scheme = "Bear" + "er"
        text = f'"Authorization": "{scheme} {_FAKE_TOKEN_B64}"'
        result = redact_secrets(text)
        assert _FAKE_TOKEN_B64 not in result
        assert "[REDACTED]" in result

    def test_redacts_json_quoted_authorization_basic(self) -> None:
        _FAKE_B64 = "".join(["dXNlcjp", "wYXNzd29yZA=="])
        text = f'"Authorization": "Basic {_FAKE_B64}"'
        result = redact_secrets(text)
        assert _FAKE_B64 not in result
        assert "[REDACTED]" in result

    def test_redacts_json_quoted_authorization_token(self) -> None:
        _FAKE_VAL = "".join(["fake", "token", "val", "xyz123"])
        text = f'"Authorization": "token {_FAKE_VAL}"'
        result = redact_secrets(text)
        assert _FAKE_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_single_quoted_dict_authorization(self) -> None:
        fake_basic = "".join(["dXNlc", "jpwYXNz"])
        result = redact_secrets(f"'Authorization': 'Basic {fake_basic}'")
        assert fake_basic not in result
        assert result == "'Authorization': '[REDACTED]'"

    def test_redacts_authorization_header_for_nonstandard_scheme(self) -> None:
        api_key_token = "".join(["abc", "123", "secret"])
        result = redact_secrets(f"{_AUTH_HEADER_NAME}: ApiKey {api_key_token}")
        assert api_key_token not in result
        assert result == "Authorization: [REDACTED]"

    def test_redacts_json_quoted_authorization_for_nonstandard_scheme(self) -> None:
        api_key_token = "".join(["abc", "123", "secret"])
        result = redact_secrets(f'"Authorization": "ApiKey {api_key_token}"')
        assert api_key_token not in result
        assert result == '"Authorization": "[REDACTED]"'

    def test_redacts_json_quoted_authorization_with_literal_newline(self) -> None:
        api_key_token = "".join(["abc", "123", "secret"])
        value = f"ApiKey {api_key_token}\ncontinued"
        result = redact_secrets(f'"Authorization": "{value}"')
        assert api_key_token not in result
        assert result == '"Authorization": "[REDACTED]"'

    def test_redacts_mixed_quote_dict_authorization(self) -> None:
        fake_basic = "".join(["dXNlc", "jpwYXNz"])
        result = redact_secrets(f"\"Authorization\": 'Basic {fake_basic}'")
        assert fake_basic not in result
        assert result == "\"Authorization\": '[REDACTED]'"

    def test_redacts_github_personal_access_token(self) -> None:
        result = redact_secrets(f"token {_FAKE_GH_TOKEN} used")
        assert _FAKE_GH_TOKEN not in result
        assert "[REDACTED]" in result

    def test_redacts_aws_access_key(self) -> None:
        result = redact_secrets(f"key={_FAKE_AWS_KEY} leaked")
        assert _FAKE_AWS_KEY not in result

    def test_redacts_generic_key_value_secret(self) -> None:
        key_value_pair = f"secret={_FAKE_GENERIC_SECRET}"
        result = redact_secrets(key_value_pair)
        assert _FAKE_GENERIC_SECRET not in result

    def test_redacts_compound_pat_name_unquoted(self) -> None:
        pat_value = "".join(["fake", "pat", "value", "123"])
        result = redact_secrets(f"AZURE_DEVOPS_COPILOT_PAT={pat_value}")
        assert pat_value not in result
        assert "[REDACTED]" in result

    def test_redacts_bare_pat_name_quoted(self) -> None:
        pat_value = "".join(["fake", "pat", "value", "123"])
        result = redact_secrets(f'{{"pat": "{pat_value}"}}')
        assert pat_value not in result
        assert "[REDACTED]" in result

    def test_redacts_json_quoted_secret_keys(self) -> None:
        result = redact_secrets('{"password": "hunter2", "client_secret":"abc123"}')
        assert result == ('{"password": "[REDACTED]", "client_secret":"[REDACTED]"}')

    def test_redacts_json_quoted_value_with_whitespace(self) -> None:
        result = redact_secrets('{"password": "two words here"}')
        assert "two words here" not in result
        assert "[REDACTED]" in result

    def test_redacts_single_quoted_value_with_whitespace(self) -> None:
        result = redact_secrets("{'password': 'two words here'}")
        assert "two words here" not in result
        assert "[REDACTED]" in result

    def test_leaves_safe_text_unchanged(self) -> None:
        assert redact_secrets("branch created successfully") == "branch created successfully"

    def test_redacts_unquoted_multi_word_value(self) -> None:
        result = redact_secrets("password: two words here")
        assert "two words here" not in result
        assert "[REDACTED]" in result

    def test_redacts_unquoted_colon_value_to_delimiter(self) -> None:
        result = redact_secrets("token=abc123 & other=value")
        assert "abc123" not in result
        assert "[REDACTED]" in result

    def test_redacts_compound_token_name_unquoted(self) -> None:
        """Compound names ending in _token (e.g. refresh_token) must be redacted."""
        result = redact_secrets("refresh_token=abc123")
        assert "abc123" not in result
        assert "[REDACTED]" in result

    def test_redacts_compound_token_name_quoted(self) -> None:
        """Compound names ending in _token inside JSON must be redacted."""
        _FAKE_PAYLOAD = "".join(["payload", "xyz", "123"])
        result = redact_secrets(f'{{"id_token": "{_FAKE_PAYLOAD}"}}')
        assert _FAKE_PAYLOAD not in result
        assert "[REDACTED]" in result

    def test_redacts_compound_key_name_unquoted(self) -> None:
        """Compound names ending in _key (e.g. private_key) must be redacted."""
        _FAKE_KEY_VAL = "".join(["BEGINRSA", "FAKEVAL", "123"])
        result = redact_secrets(f"private_key={_FAKE_KEY_VAL}")
        assert _FAKE_KEY_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_aws_secret_access_key(self) -> None:
        """AWS_SECRET_ACCESS_KEY ends in _KEY and must be redacted."""
        fake_aws_secret = "".join(["wJalrXUtn", "FICTITIOUS", "KEY"])
        result = redact_secrets(f"AWS_SECRET_ACCESS_KEY={fake_aws_secret}")
        assert fake_aws_secret not in result
        assert "[REDACTED]" in result

    def test_redacts_compound_key_name_json_quoted(self) -> None:
        """Compound _key names in JSON must be redacted."""
        _FAKE_SECRET_VAL = "".join(["supersecret", "123", "xyz"])
        result = redact_secrets(f'{{"private_key": "{_FAKE_SECRET_VAL}"}}')
        assert _FAKE_SECRET_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_camel_case_access_token_unquoted(self) -> None:
        """camelCase accessToken (no separator) must be redacted like access_token."""
        _FAKE_VAL = "".join(["oauth", "fake", "token", "xyz123"])
        result = redact_secrets(f"accessToken={_FAKE_VAL}")
        assert _FAKE_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_camel_case_refresh_token_quoted(self) -> None:
        """camelCase refreshToken inside JSON must be redacted like refresh_token."""
        _FAKE_VAL = "".join(["refresh", "fake", "value", "abc"])
        result = redact_secrets(f'{{"refreshToken": "{_FAKE_VAL}"}}')
        assert _FAKE_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_camel_case_private_key_unquoted(self) -> None:
        """camelCase privateKey (no separator) must be redacted like private_key."""
        _FAKE_VAL = "".join(["BEGINRSA", "CAMEL", "FAKE123"])
        result = redact_secrets(f"privateKey={_FAKE_VAL}")
        assert _FAKE_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_camel_case_openai_api_key_unquoted(self) -> None:
        """openaiApiKey must be redacted — camelCase compound ending in Key."""
        _FAKE_VAL = "".join(["sk-fake", "openai", "key", "xyz123"])
        result = redact_secrets(f"openaiApiKey={_FAKE_VAL}")
        assert _FAKE_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_url_userinfo_credentials(self) -> None:
        """URL userinfo (user:pass@host) must be redacted per FR-011."""
        _FAKE_PASS = "".join(["s3cr3t", "pass", "word"])
        url = f"https://alice:{_FAKE_PASS}@example.invalid/x"
        result = redact_secrets(f"failed {url}")
        assert _FAKE_PASS not in result
        assert "[REDACTED]" in result

    def test_redacts_cli_flag_token_value(self) -> None:
        """--token VALUE on a CLI invocation must be redacted per FR-011."""
        _FAKE_VAL = "".join(["cli", "tok", "en", "abc123"])
        result = redact_secrets(f"tool --token {_FAKE_VAL}")
        assert _FAKE_VAL not in result
        assert "[REDACTED]" in result

    def test_redacts_cli_flag_password_value(self) -> None:
        """--password VALUE on a CLI invocation must be redacted per FR-011."""
        _FAKE_PASS = "".join(["hunter", "two", "pass"])
        result = redact_secrets(f"cmd --password {_FAKE_PASS} --verbose")
        assert _FAKE_PASS not in result
        assert "[REDACTED]" in result

    def test_redacts_cli_flag_double_quoted_value_with_spaces(self) -> None:
        """--token "secret value" must be fully redacted; the space-separated tail must not leak."""
        _FAKE_TOKEN = "".join(["secret", " ", "value"])
        result = redact_secrets(f'tool --token "{_FAKE_TOKEN}"')
        assert "secret" not in result
        assert "value" not in result
        assert "[REDACTED]" in result

    def test_redacts_cli_flag_single_quoted_value_with_spaces(self) -> None:
        """--secret 'my pass phrase' must be fully redacted per FR-011."""
        _FAKE_SECRET = "".join(["my", " ", "pass", " ", "phrase"])
        result = redact_secrets(f"tool --secret '{_FAKE_SECRET}'")
        assert "my" not in result
        assert "pass" not in result
        assert "phrase" not in result
        assert "[REDACTED]" in result

    def test_redacts_kv_unterminated_double_quoted_value(self) -> None:
        """Truncated provider output with an unterminated double-quoted value MUST be redacted.

        When the closing quote of a key=value pair is missing (e.g. the error
        message was cut off mid-string), the pattern must still consume the
        exposed value — a conservative FR-011 fallback.
        """
        _FAKE_SECRET = "".join(["topsecret", "val", "123"])
        # truncated: no closing double-quote
        result = redact_secrets(f'password: "{_FAKE_SECRET}')
        assert _FAKE_SECRET not in result
        assert "[REDACTED]" in result

    def test_redacts_kv_unterminated_single_quoted_value(self) -> None:
        """key='value truncated without closing quote must still be redacted (FR-011)."""
        _FAKE_SECRET = "".join(["topsecret", "val", "456"])
        result = redact_secrets(f"secret='{_FAKE_SECRET}")
        assert _FAKE_SECRET not in result
        assert "[REDACTED]" in result
