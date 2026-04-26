"""Tests for deterministic explicit memory-save intent detection."""

from anteroom.services.memory_intent import ExplicitMemoryIntent, detect_explicit_memory_intent


def test_detects_save_my_name_typo_memory() -> None:
    assert detect_explicit_memory_intent("save my name Troy Larson as a memorry") == ExplicitMemoryIntent(
        content="User's name is Troy Larson."
    )


def test_detects_remember_my_name_is() -> None:
    assert detect_explicit_memory_intent("remember that my name is Troy Larson") == ExplicitMemoryIntent(
        content="User's name is Troy Larson."
    )


def test_detects_explicit_memory_fact() -> None:
    assert detect_explicit_memory_intent("remember that I prefer terse answers as a memory") == ExplicitMemoryIntent(
        content="I prefer terse answers."
    )


def test_rejects_memory_question() -> None:
    assert detect_explicit_memory_intent("what do you remember about me?") is None


def test_rejects_slash_commands() -> None:
    assert detect_explicit_memory_intent("/memory list") is None


def test_rejects_ambiguous_remember() -> None:
    assert detect_explicit_memory_intent("remember to check the logs later") is None


def test_rejects_code_blocks() -> None:
    assert detect_explicit_memory_intent("remember this as a memory\n```python\nprint('x')\n```") is None
