from agentic_devtools.ai_providers.serialization import redact_credentials


def test_redact_credentials():
    original = {
        "api_secret": "my_secret",
        "api-key": "hyphen_api_secret",
        "github_token": "fuzzy_token_secret",
        "service_api_key": "fuzzy_api_key_secret",
        "session-key": "hyphen_session_secret",
        "signing-key": "hyphen_signing_secret",
        "PASSWORD": "my_password",
        "normal": "value",
        "token_count": 42,
        "password_policy": "strong",
        "authorization_scheme": "Bearer",
        "tokenizer_settings": "keep_this",
        "tokenizer-settings": "keep_hyphenated_tokenizer",
        "items": [{"token": "t1"}, "plain_text"],
    }

    redacted = redact_credentials(original)
    assert redacted["api_secret"] == "<redacted>"
    assert redacted["api-key"] == "<redacted>"
    assert redacted["github_token"] == "<redacted>"
    assert redacted["service_api_key"] == "<redacted>"
    assert redacted["session-key"] == "<redacted>"
    assert redacted["signing-key"] == "<redacted>"
    assert redacted["PASSWORD"] == "<redacted>"
    assert redacted["normal"] == "value"
    assert redacted["token_count"] == 42
    assert redacted["password_policy"] == "strong"
    assert redacted["authorization_scheme"] == "Bearer"
    assert redacted["tokenizer_settings"] == "keep_this"
    assert redacted["tokenizer-settings"] == "keep_hyphenated_tokenizer"
    assert isinstance(redacted["items"], list)
    assert redacted["items"][0]["token"] == "<redacted>"
    assert redacted["items"][1] == "plain_text"

    # original should not be modified
    assert original["api_secret"] == "my_secret"


def test_redact_credentials_camel_case_keys():
    original = {
        "accessToken": "secret-value",
        "refreshToken": "another-secret",
        "clientSecret": "hidden",
        "apiKey": "key-value",
        "APIKey": "upper-camel-key",
        "tokenizerSettings": "keep_this",
    }

    redacted = redact_credentials(original)
    assert redacted["accessToken"] == "<redacted>"
    assert redacted["refreshToken"] == "<redacted>"
    assert redacted["clientSecret"] == "<redacted>"
    assert redacted["apiKey"] == "<redacted>"
    assert redacted["APIKey"] == "<redacted>"
    assert redacted["tokenizerSettings"] == "keep_this"
