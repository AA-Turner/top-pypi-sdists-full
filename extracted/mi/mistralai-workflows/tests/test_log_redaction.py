import base64
import json
import logging
import sys
from urllib.parse import quote

import pytest
from pydantic import SecretStr

from mistralai.workflows.core.logging import (
    _PATTERN_SCAN_MAX_CHARS,
    LogFormat,
    LogLevel,
    _redact_log_event,
    build_json_log_formatter,
    setup_logging,
)


@pytest.mark.parametrize("log_format", [LogFormat.JSON, LogFormat.CONSOLE])
def test_console_and_otlp_logs_mask_credentials_and_exceptions(monkeypatch, log_format):
    secret = "FAKE-logging-secret/with-special-characters"
    monkeypatch.setenv("MISTRAL_API_KEY", secret)
    setup_logging(log_level=LogLevel.INFO, log_format=log_format)
    console = logging.getLogger().handlers[0].formatter
    assert console is not None
    try:
        raise RuntimeError(f"failure {secret}")
    except RuntimeError:
        info = sys.exc_info()
    record = logging.LogRecord("sdk", logging.ERROR, __file__, 1, f"credential={quote(secret, safe='')}", (), info)
    for formatter in (console, build_json_log_formatter()):
        text = formatter.format(record)
        assert secret not in text and quote(secret, safe="") not in text
        assert "[REDACTED]" in text and "RuntimeError" in text


def test_recursive_fields_unknown_auth_and_usage_are_safe():
    event = {
        "headers": {"x-private-access": "fake-private", "X-Custom": "safe"},
        "event": "Authorization: Basic ZmFrZTpwYXNzd29yZA==",
        "input_tokens": 42,
        "output_tokens": 3,
        "http_status": 403,
        "finding": "FLAG{synthetic}",
        "object": SecretStr("fake-object-secret"),
    }
    out = _redact_log_event(None, "info", event)
    assert out["headers"] == {"x-private-access": "[REDACTED]", "X-Custom": "safe"}
    assert "ZmFrZTpwYXNzd29yZA==" not in json.dumps(out)
    assert "fake-object-secret" not in json.dumps(out)
    assert out["input_tokens"] == 42 and out["finding"] == "FLAG{synthetic}"
    assert event["headers"]["x-private-access"] == "fake-private"


def test_header_credential_is_redacted_when_echoed_in_free_text(monkeypatch):
    monkeypatch.setenv("MISTRAL_API_HEADERS", '{"x-private-access":"FAKE-access-value"}')
    text = base64.b64encode(b"FAKE-access-value").decode()
    assert _redact_log_event(None, "info", {"event": f"error {text}"})["event"] == "error [REDACTED]"


def test_redaction_fails_closed_without_echoing_exception(monkeypatch):
    class Unsafe:
        def __str__(self):
            raise RuntimeError("fake-secret-in-error")

    assert _redact_log_event(None, "info", {"event": Unsafe()}) == {
        "event": "Log redaction failed; event omitted",
        "level": "error",
    }


def test_tokenizer_switches_do_not_erase_log_text(monkeypatch):
    monkeypatch.setenv("TOKENIZERS_PARALLELISM", "true")
    monkeypatch.setenv("HF_HUB_DISABLE_IMPLICIT_TOKEN", "1")
    event = {"latest": "tokenizer parallelism is true", "event": "latest test failed: true != 1"}
    assert _redact_log_event(None, "info", event) == event


@pytest.mark.parametrize(
    "flag",
    ["BUILDKITE_USE_GITHUB_APP_GIT_CREDENTIALS", "BUILDKITE_USE_REPOSITORY_PROVIDER_GIT_CREDENTIALS"],
)
@pytest.mark.parametrize("value", ["true", "false"])
def test_ci_credential_mode_flags_do_not_erase_log_text(monkeypatch, flag, value):
    monkeypatch.setenv(flag, value)
    event = {"event": f"credential mode is {value}", "access_token": "fake-credential"}
    assert _redact_log_event(None, "info", event) == {
        "event": f"credential mode is {value}",
        "access_token": "[REDACTED]",
    }


def test_usage_fields_stay_visible_without_weakening_token_redaction(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "FAKE-github-token-value")
    monkeypatch.setenv("MAX_TOKENS", "4096")
    event = {
        "event": "limit 4096 leaked FAKE-github-token-value",
        "token_workflow_usage": {
            "input_tokens": 7,
            "output_tokens": 1,
            "token_usage_source": "reported",
            "api_key": "nested-secret",
        },
        "token_usage_source": "reported",
        "max_tokens": 4096,
        "cached_tokens": 12,
        "access_token": "fake-access-token",
        "refresh_token": "fake-refresh-token",
        "customToken": "fake-custom-token",
        "TOKEN": "fake-uppercase-token",
    }
    out = _redact_log_event(None, "info", event)
    assert out["token_workflow_usage"] == {
        "input_tokens": 7,
        "output_tokens": 1,
        "token_usage_source": "reported",
        "api_key": "[REDACTED]",
    }
    assert out["token_usage_source"] == "reported"
    assert out["max_tokens"] == 4096 and out["cached_tokens"] == 12
    for key in ("access_token", "refresh_token", "customToken", "TOKEN"):
        assert out[key] == "[REDACTED]"
    assert out["event"] == "limit 4096 leaked [REDACTED]"


@pytest.mark.parametrize("secret", ["1", "test", "true", "none", "secret", "token12"])
def test_short_credentials_remain_masked_without_erasing_words(monkeypatch, secret):
    monkeypatch.setenv("MISTRAL_API_KEY", secret)
    event = {
        "latest": f"latest testable trueish nonevent step1 secretive token123: credential={secret}",
        "api_key": secret,
    }
    out = _redact_log_event(None, "info", event)
    assert out == {
        "latest": "latest testable trueish nonevent step1 secretive token123: credential=[REDACTED]",
        "api_key": "[REDACTED]",
    }


def test_oversized_values_still_mask_known_credentials(monkeypatch):
    monkeypatch.setenv("MISTRAL_API_KEY", "FAKE-oversized-secret")
    padding = "x" * _PATTERN_SCAN_MAX_CHARS
    out = _redact_log_event(None, "info", {"event": f"{padding} FAKE-oversized-secret"})
    assert out["event"] == f"{padding} [REDACTED]"
