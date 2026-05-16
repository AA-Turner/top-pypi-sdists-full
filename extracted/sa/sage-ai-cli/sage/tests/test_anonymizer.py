"""Pin the cloud-AI anonymizer contract.

These tests are the wire-format guarantee Sage AI's privacy posture relies on.
If any of them fail, a privacy regression has shipped — investigate before
adjusting the test.
"""

from __future__ import annotations

import pytest

from sage.providers.anonymizer import (
    FORBIDDEN_TOP_LEVEL_KEYS,
    LOCAL_PROVIDERS,
    anonymize_payload,
    is_local_provider,
    scrub_text,
)


# ── Local-provider passthrough ────────────────────────────────────────────────


class TestLocalProvidersPassthrough:
    """Ollama / llama-cpp inference never leaves the user's machine — the
    anonymizer must NOT touch their payloads. Touching them would silently
    rewrite local prompts in a way the user can't see, breaking trust."""

    @pytest.mark.parametrize("name", sorted(LOCAL_PROVIDERS))
    def test_local_provider_recognized(self, name):
        assert is_local_provider(name)

    def test_local_payload_untouched_even_with_forbidden_keys(self):
        payload = {
            "model": "qwen3-coder",
            "messages": [{"role": "user", "content": "email me at me@example.com"}],
            "user": "should-not-strip-for-local",  # local pass-through
        }
        result = anonymize_payload(payload, provider_name="ollama")
        # IDENTITY — same object back. We don't want to spend CPU on
        # something that never leaves the machine.
        assert result is payload

    def test_unknown_provider_treated_as_cloud(self):
        assert not is_local_provider("some-new-provider")


# ── Forbidden field stripping ────────────────────────────────────────────────


class TestForbiddenFieldStripping:
    """End-user identifiers must never reach a cloud provider."""

    @pytest.mark.parametrize("key", sorted(FORBIDDEN_TOP_LEVEL_KEYS))
    def test_field_stripped(self, key):
        payload = {"model": "x", "messages": [], key: "leaked-value"}
        result = anonymize_payload(payload, provider_name="openrouter")
        assert key not in result

    def test_case_insensitive_match(self):
        payload = {"model": "x", "messages": [], "USER": "leaked", "User": "also"}
        result = anonymize_payload(payload, provider_name="openrouter")
        assert "USER" not in result and "User" not in result

    def test_allowed_fields_preserved(self):
        payload = {
            "model": "gpt-x",
            "messages": [{"role": "user", "content": "hi"}],
            "temperature": 0.7,
            "max_tokens": 100,
            "stream": True,
        }
        result = anonymize_payload(payload, provider_name="openrouter")
        for key in ("model", "messages", "temperature", "max_tokens", "stream"):
            assert key in result

    def test_does_not_mutate_input(self):
        payload = {"model": "x", "messages": [], "user": "leaked"}
        anonymize_payload(payload, provider_name="openrouter")
        # Original dict must still have the forbidden field — we returned
        # a COPY without it, but the caller's dict is untouched.
        assert payload["user"] == "leaked"


# ── PII scrubbing ────────────────────────────────────────────────────────────


class TestPIIScrubbing:
    """Best-effort scrub. Strict formats only, to keep code-heavy
    prompts legible."""

    def test_email_in_string_content(self):
        payload = {
            "model": "x",
            "messages": [{"role": "user", "content": "ping me at jane@acme.com"}],
        }
        result = anonymize_payload(payload, provider_name="openrouter")
        text = result["messages"][0]["content"]
        assert "jane@acme.com" not in text
        assert "[email redacted]" in text

    def test_phone_with_separators(self):
        payload = {
            "model": "x",
            "messages": [{"role": "user", "content": "call (415) 555-1234"}],
        }
        result = anonymize_payload(payload, provider_name="openrouter")
        text = result["messages"][0]["content"]
        assert "555-1234" not in text
        assert "[phone redacted]" in text

    def test_bare_digits_NOT_scrubbed(self):
        """Strict heuristic — bare 10-digit strings (timestamps, ports,
        large constants) must pass through. Otherwise code prompts break."""
        payload = {
            "model": "x",
            "messages": [{"role": "user", "content": "timestamp=1234567890 port=8080"}],
        }
        result = anonymize_payload(payload, provider_name="openrouter")
        assert "1234567890" in result["messages"][0]["content"]
        assert "8080" in result["messages"][0]["content"]

    def test_structured_content_parts(self):
        """OpenAI vision/multimodal prompts use a list of parts."""
        payload = {
            "model": "x",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "hi at me@example.com"},
                    {"type": "image_url", "image_url": {"url": "https://..."}},
                ],
            }],
        }
        result = anonymize_payload(payload, provider_name="openrouter")
        parts = result["messages"][0]["content"]
        assert parts[0]["text"] == "hi at [email redacted]"
        assert parts[1] == {"type": "image_url", "image_url": {"url": "https://..."}}

    def test_gemini_contents_parts(self):
        """Gemini wire format: `contents[].parts[].text`."""
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": "email me at x@y.com"}]},
            ],
            "generationConfig": {"temperature": 0.7},
        }
        result = anonymize_payload(payload, provider_name="gemini")
        assert "x@y.com" not in result["contents"][0]["parts"][0]["text"]

    def test_gemini_system_instruction(self):
        payload = {
            "contents": [{"role": "user", "parts": [{"text": "hi"}]}],
            "systemInstruction": {"parts": [{"text": "user is alice@a.com"}]},
        }
        result = anonymize_payload(payload, provider_name="gemini")
        assert "alice@a.com" not in result["systemInstruction"]["parts"][0]["text"]

    def test_empty_string_safe(self):
        assert scrub_text("") == ""

    def test_assistant_messages_also_scrubbed(self):
        """Conversation history can include prior assistant turns that
        leaked PII. Scrub those too on retransmission."""
        payload = {
            "model": "x",
            "messages": [
                {"role": "user",      "content": "what's John's email?"},
                {"role": "assistant", "content": "It is john@acme.com"},
                {"role": "user",      "content": "thanks"},
            ],
        }
        result = anonymize_payload(payload, provider_name="openrouter")
        assert "john@acme.com" not in result["messages"][1]["content"]


# ── Defense-in-depth check ────────────────────────────────────────────────────


class TestKeyCoverage:
    """The forbidden-key set must include the obvious leakage vectors."""

    @pytest.mark.parametrize("key", ["user", "user_id", "email", "uid", "metadata"])
    def test_must_be_forbidden(self, key):
        assert key in FORBIDDEN_TOP_LEVEL_KEYS
