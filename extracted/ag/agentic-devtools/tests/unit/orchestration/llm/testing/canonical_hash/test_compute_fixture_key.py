"""Tests for compute_fixture_key."""

from agentic_devtools.orchestration.llm.testing.canonical_hash import compute_fixture_key
from agentic_devtools.orchestration.llm.types import LLMMessage


class TestComputeFixtureKey:
    """Tests for compute_fixture_key."""

    def test_deterministic_output(self):
        key1 = compute_fixture_key(
            node_type="analysis",
            model="gpt-4o",
            messages=[LLMMessage(role="user", content="Hello")],
        )
        key2 = compute_fixture_key(
            node_type="analysis",
            model="gpt-4o",
            messages=[LLMMessage(role="user", content="Hello")],
        )
        assert key1 == key2

    def test_different_messages_produce_different_keys(self):
        key1 = compute_fixture_key(
            node_type="analysis",
            model="gpt-4o",
            messages=[LLMMessage(role="user", content="Hello")],
        )
        key2 = compute_fixture_key(
            node_type="analysis",
            model="gpt-4o",
            messages=[LLMMessage(role="user", content="World")],
        )
        assert key1 != key2

    def test_different_models_produce_different_keys(self):
        msgs = [LLMMessage(role="user", content="Hi")]
        key1 = compute_fixture_key(node_type="n", model="gpt-4o", messages=msgs)
        key2 = compute_fixture_key(node_type="n", model="gpt-4o-mini", messages=msgs)
        assert key1 != key2

    def test_is_valid_sha256_hex(self):
        key = compute_fixture_key(node_type="n", model="m", messages=[])
        assert len(key) == 64
        assert all(c in "0123456789abcdef" for c in key)

    def test_optional_params_affect_key(self):
        msgs = [LLMMessage(role="user", content="Hi")]
        key1 = compute_fixture_key(node_type="n", model="m", messages=msgs)
        key2 = compute_fixture_key(node_type="n", model="m", messages=msgs, temperature=0.5)
        assert key1 != key2

    def test_max_tokens_affects_key(self):
        msgs = [LLMMessage(role="user", content="Hi")]
        key1 = compute_fixture_key(node_type="n", model="m", messages=msgs)
        key2 = compute_fixture_key(node_type="n", model="m", messages=msgs, max_tokens=100)
        assert key1 != key2

    def test_response_format_affects_key(self):
        msgs = [LLMMessage(role="user", content="Hi")]
        key1 = compute_fixture_key(node_type="n", model="m", messages=msgs)
        key2 = compute_fixture_key(node_type="n", model="m", messages=msgs, response_format={"type": "json_object"})
        assert key1 != key2

    def test_additional_params_affect_key(self):
        msgs = [LLMMessage(role="user", content="Hi")]
        key1 = compute_fixture_key(node_type="n", model="m", messages=msgs, additional_params={"top_p": 0.9})
        key2 = compute_fixture_key(node_type="n", model="m", messages=msgs, additional_params={"top_p": 0.8})
        assert key1 != key2
