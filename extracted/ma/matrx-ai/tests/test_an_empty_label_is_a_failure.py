"""The conversation labeler: an empty label is a failure, and its five input bounds are knobs.

Breaks this guards:
* E2 — a held call that came back blank was ``LabelResult(success=True, output="")``; valid JSON
  with no label, description or keywords was ``skipped:empty_label``. Neither is retried, so the
  conversation stayed unnamed for good. Both are now failures (the inline retry and the durable
  retry key on ``failed:``).
* F — the five ``*_MAX_CHARS`` bounds were constants an admin could not turn. They are now
  ``agents.conversations`` knobs read through the one package knob seam (``matrx_ai.knobs``).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.agent_runners.conversation_labeler as runner
import matrx_ai.agents.services.conversation_labeler as service
import matrx_ai.mandates as mandates
from matrx_ai.code_call_mandate_keys import CONVERSATION_LABEL_CHAT_MANDATE
from matrx_ai.knobs import configure_package_knobs


def _held_answer(monkeypatch: pytest.MonkeyPatch, final_text: str) -> list[BaseException]:
    async def hold(*_a: Any, **_k: Any) -> Any:
        return SimpleNamespace(model="m")

    async def run(_held: Any, **_k: Any) -> Any:
        return SimpleNamespace(final_text=final_text)

    captured: list[BaseException] = []

    async def capture(exc: BaseException, **_k: Any) -> None:
        captured.append(exc)

    monkeypatch.setattr(mandates, "hold_code_call", hold)
    monkeypatch.setattr(mandates, "run_held_call", run)
    monkeypatch.setattr(runner, "_capture_labeler_failure", capture)
    return captured


@pytest.mark.parametrize("blank", ["", "  \n "])
async def test_a_blank_answer_is_a_captured_failure(monkeypatch, blank) -> None:
    captured = _held_answer(monkeypatch, blank)
    result = await runner._run_labeler(CONVERSATION_LABEL_CHAT_MANDATE, {}, conversation_id=None)
    assert (result.success, result.error) == (False, "empty_output")
    assert [str(e) for e in captured] == [f"{CONVERSATION_LABEL_CHAT_MANDATE} returned an empty label"]


async def test_a_real_answer_still_succeeds(monkeypatch) -> None:
    captured = _held_answer(monkeypatch, '{"label": "Tide tables"}')
    result = await runner._run_labeler(CONVERSATION_LABEL_CHAT_MANDATE, {}, conversation_id=None)
    assert (result.success, result.output) == (True, '{"label": "Tide tables"}')
    assert captured == []


async def test_valid_json_with_nothing_in_it_is_a_failed_label(monkeypatch) -> None:
    async def label(**_k: Any) -> Any:
        return runner.LabelResult(success=True, output='{"label": "", "description": " ", "keywords": []}')

    async def no_titles(_user_id: str) -> list:
        return []

    monkeypatch.setattr(service, "label_chat_conversation", label)
    monkeypatch.setattr(service, "_fetch_recent_titles", no_titles)
    outcome, parsed = await service._label_and_apply(
        conversation_id="c1", user_id="u1", conversation_content="User:\nhi",
        agent_name=None, agent_description=None, user_variables=None, user_prompt=None,
    )
    assert (outcome, parsed) == ("failed:empty_label", None)


def test_the_five_bounds_are_read_from_their_knobs() -> None:
    asked: list[tuple[str, str]] = []
    values = {
        "label_recent_titles_max_chars": 300,
        "label_agent_name_max_chars": 150,
        "label_agent_description_max_chars": 400,
        "label_user_variables_max_chars": 500,
        "label_user_prompt_max_chars": 250,
    }

    def reader(feature: str, key: str) -> Any:
        asked.append((feature, key))
        return values[key]

    configure_package_knobs(reader)
    try:
        chat = runner._chat_variables("User:\nhi", "t" * 5_000)
        agent = runner._agent_variables("n" * 5_000, "d" * 5_000, "v" * 50_000, "p" * 5_000)
    finally:
        configure_package_knobs(None)
    # The trim keeps head and tail around a marker; it lands within a character of the bound.
    got = [len(chat["recent_titles"])] + [
        len(agent[k]) for k in ("agent_name", "agent_description", "user_variables", "user_prompt")
    ]
    for size, bound in zip(got, [300, 150, 400, 500, 250], strict=True):
        assert bound - 1 <= size <= bound, (got, bound)
    assert {key for _feature, key in asked} == set(values)
    assert {feature for feature, _key in asked} == {"agents.conversations"}
