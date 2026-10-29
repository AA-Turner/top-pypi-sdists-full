"""matrx-ai limits read through the ONE package knob seam (``matrx_ai.knobs``), never module constants.

2026-10-28: the chat-title retry delay, memory call retries, the structured-answer size, the device-relay
waits, the default music length and the desktop research text budget were constants. Each is now a
``platform.feature_knob`` row read through the host's ``(feature, key)`` reader: turning the row changes
the behavior, and with no host (or the row at its seeded value) the behavior is exactly as before.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import knobs


def _bind(monkeypatch: pytest.MonkeyPatch, values: dict[tuple[str, str], Any]) -> list[tuple[str, str]]:
    asked: list[tuple[str, str]] = []

    def reader(feature: str, key: str) -> Any:
        asked.append((feature, key))
        return values[(feature, key)]

    monkeypatch.setattr(knobs, "_reader", reader)
    return asked


def test_unbound_answers_the_mirror_and_bound_answers_the_row(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(knobs, "_reader", None)
    assert knobs.package_knob_number("f", "k", 5, low=0, high=10) == 5
    _bind(monkeypatch, {("f", "k"): 7})
    assert knobs.package_knob_number("f", "k", 5, low=0, high=10) == 7
    _bind(monkeypatch, {("f", "k"): 70})
    assert knobs.package_knob_number("f", "k", 5, low=0, high=10) == 10, "clamped to the row's range"
    _bind(monkeypatch, {("f", "k"): "x"})
    assert knobs.package_knob_number("f", "k", 5, low=0, high=10) == 5, "not a number: the mirror"


def test_a_failing_reader_answers_the_mirror(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(_f: str, _k: str) -> Any:
        raise RuntimeError("not primed")

    monkeypatch.setattr(knobs, "_reader", broken)
    assert knobs.package_knob_number("f", "k2", 2.5, low=0.0, high=10.0) == 2.5


def test_the_chat_title_retry_delay_is_the_knob(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agents.services import conversation_labeler as cl

    monkeypatch.setattr(knobs, "_reader", None)
    assert cl.label_retry_delay_seconds() == 180.0
    _bind(monkeypatch, {("agents.conversations", "label_retry_delay_seconds"): 600})
    assert cl.label_retry_delay_seconds() == 600.0


def test_memory_retries_are_the_knob(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.memory import llm_adapter

    monkeypatch.setattr(knobs, "_reader", None)
    assert llm_adapter.memory_transient_retries() == 2
    _bind(monkeypatch, {("agents.memory", "llm_transient_retries"): 5})
    assert llm_adapter.memory_transient_retries() == 5


def test_the_structured_answer_size_is_the_knob(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.orchestrator import answer_checks

    answer = '{"__kind": "x", "pad": "' + "a" * 2_000 + '"}'
    monkeypatch.setattr(knobs, "_reader", None)
    assert answer_checks.answer_text_max_chars() == 400_000
    assert answer_checks.structured_answer(answer) is not None
    _bind(monkeypatch, {("agents.answer_checks", "answer_text_max_chars"): 1_000})
    assert answer_checks.structured_answer(answer) is None, "longer than the knob: not parsed"


def test_the_device_relay_waits_are_the_knobs_unless_pinned(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.providers.device import relay_transport as rt

    monkeypatch.setattr(rt, "_seam", rt._RelaySeam())
    monkeypatch.setattr(knobs, "_reader", None)
    assert (rt.first_byte_timeout_ms(), rt.idle_timeout_ms()) == (300_000, 120_000)
    _bind(monkeypatch, {("ai.device_relay", "first_byte_timeout_ms"): 60_000,
                        ("ai.device_relay", "idle_timeout_ms"): 950_000})
    assert (rt.first_byte_timeout_ms(), rt.idle_timeout_ms()) == (60_000, 900_000), "the relay caps at 900 000"
    monkeypatch.setattr(rt, "_seam", rt._RelaySeam(first_byte_timeout_ms=1_234))
    assert rt.first_byte_timeout_ms() == 1_234, "a host-pinned value wins"


def test_the_default_music_length_is_the_knob(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace

    from matrx_ai.providers.eleven_labs import music_api

    monkeypatch.setattr(knobs, "_reader", None)
    assert music_api.music_length_seconds(SimpleNamespace(duration_seconds=None)) == 30
    _bind(monkeypatch, {("ai.music", "default_length_seconds"): 90})
    assert music_api.music_length_seconds(SimpleNamespace(duration_seconds=None)) == 90
    assert music_api.music_length_seconds(SimpleNamespace(duration_seconds=12)) == 12, "an asked length wins"
