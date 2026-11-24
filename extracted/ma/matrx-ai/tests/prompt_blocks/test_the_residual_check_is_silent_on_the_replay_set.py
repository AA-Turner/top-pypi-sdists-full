"""FORCING GUARD — the residual check is silent on the fixed replay set (PLAN §5.4, §9 P1a).

Every replay case (wire shape × turn phase × the blocks matrx-ai owns) is built through the REAL
assembly; the residual check then runs on the exact request dict the translator built, with the
source the translator recorded (``BaseTranslator.messages_for_wire`` → ``note_wire_source``). A
known request leaves nothing unaccounted for. Self-test: the same request with one planted
sentence leaves exactly that sentence.
"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers import residual_check

# The replay set module, loaded once under the name the byte-identity guard gives it.
replay_set = sys.modules.get("prompt_blocks_replay_set")
if replay_set is None:
    _spec = importlib.util.spec_from_file_location("prompt_blocks_replay_set", Path(__file__).with_name("replay_set.py"))
    assert _spec and _spec.loader
    replay_set = importlib.util.module_from_spec(_spec)
    sys.modules[_spec.name] = replay_set
    _spec.loader.exec_module(replay_set)

SHAPE_OF = {
    "anthropic": fos.SHAPE_ANTHROPIC,
    "openai_responses": fos.SHAPE_RESPONSES,
    "chat_completions": fos.SHAPE_CHAT,
    "google": fos.SHAPE_GOOGLE,
}
PLANT = "Planted platform sentence that no registered block accounts for."


def _built(case: tuple[str, str, str], monkeypatch: pytest.MonkeyPatch) -> tuple[dict[str, Any], Any]:
    shape, phase, variant = case
    seen: list[Any] = []
    real = replay_set.canonical_bytes

    def keep(value: Any) -> bytes:
        seen.append(value)
        return real(value)

    monkeypatch.setattr(replay_set, "canonical_bytes", keep)
    # The replay set builds outside an agent loop with the seal off: record the source anyway.
    monkeypatch.setattr(residual_check, "_will_be_checked", lambda _provider: True)

    async def run() -> Any:
        await replay_set.build(shape, phase, variant)
        return residual_check.take_wire_source()

    source = asyncio.run(run())
    request = seen[-1]
    if shape == "google":  # replay_set flattens genai's config: put the system text where the wire has it
        request = {"contents": request["contents"], "systemInstruction": {"parts": [{"text": request["system"]}]}}
    return request, source


@pytest.mark.parametrize("case", replay_set.cases(), ids=lambda c: replay_set.key(*c))
def test_the_residual_check_is_silent_on_every_replay_case(
    case: tuple[str, str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    request, source = _built(case, monkeypatch)
    assert source is not None, "the translator recorded no source: the check would never run"
    texts = residual_check.wire_texts(SHAPE_OF[case[0]], request)
    assert texts, "no platform-writable text read: this guard would prove nothing"
    assert residual_check.residual_of(SHAPE_OF[case[0]], request, residual_check.known_texts(source)) == []


@pytest.mark.parametrize("case", replay_set.cases()[:: len(replay_set.PHASES) * len(replay_set.VARIANTS)])
def test_a_planted_sentence_is_the_whole_residual(case: tuple[str, str, str], monkeypatch: pytest.MonkeyPatch) -> None:
    request, source = _built(case, monkeypatch)
    shape = SHAPE_OF[case[0]]
    if shape == fos.SHAPE_GOOGLE:
        request["systemInstruction"]["parts"].append({"text": PLANT})
    elif shape == fos.SHAPE_RESPONSES and isinstance(request.get("instructions"), str):
        request["instructions"] = f"{request['instructions']}\n\n{PLANT}"
    elif shape == fos.SHAPE_RESPONSES:
        request["input"] = [{"role": "user", "content": PLANT}, *request["input"]]
    elif shape == fos.SHAPE_ANTHROPIC:
        system = request.get("system")
        request["system"] = [*system, {"type": "text", "text": PLANT}] if isinstance(system, list) else f"{system}\n\n{PLANT}"
    else:
        first = request["messages"][0]
        first["content"] = f"{first['content']}\n\n{PLANT}"
    residual = residual_check.residual_of(shape, request, residual_check.known_texts(source))
    assert [text for _, text in residual] == [PLANT], residual


# --- a carried history system message (Anthropic / Google wrap it as a <system_note>) ---

HISTORY_NOTE = "The person switched the chat to the billing desk."


def _with_history_system_message(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.config import TextContent, UnifiedMessage

    real = replay_set._messages

    def messages(phase: str) -> list[Any]:
        out = real(phase)
        note = UnifiedMessage(role="system", content=[TextContent(text=HISTORY_NOTE)])
        return [*out[:1], note, *out[1:]]

    monkeypatch.setattr(replay_set, "_messages", messages)


@pytest.mark.parametrize("shape", list(SHAPE_OF))
def test_a_carried_history_system_message_leaves_no_residual(shape: str, monkeypatch: pytest.MonkeyPatch) -> None:
    _with_history_system_message(monkeypatch)
    request, source = _built((shape, "t2_cache_miss", "every_block"), monkeypatch)
    texts = residual_check.wire_texts(SHAPE_OF[shape], request)
    assert any(HISTORY_NOTE in text for _, text in texts), "the history message never reached the check"
    assert residual_check.residual_of(SHAPE_OF[shape], request, residual_check.known_texts(source)) == []


@pytest.mark.parametrize("shape", ["anthropic", "google"])
def test_an_addition_inside_a_history_note_is_still_reported(shape: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """The <system_note> wrapper is subtracted only when nothing but known text was inside it."""
    _with_history_system_message(monkeypatch)
    request, source = _built((shape, "t2_cache_miss", "every_block"), monkeypatch)
    raw = str(request)
    assert "<system_note>" in raw, f"{shape} no longer wraps a history system message: update this guard"
    planted = residual_check.wire_texts  # find the note text and plant inside it
    for where, text in planted(SHAPE_OF[shape], request):
        if HISTORY_NOTE in text:
            break
    else:  # pragma: no cover
        raise AssertionError("no note")
    _replace_text(request, text, text.replace(HISTORY_NOTE, f"{HISTORY_NOTE} {PLANT}"))
    residual = residual_check.residual_of(SHAPE_OF[shape], request, residual_check.known_texts(source))
    assert len(residual) == 1 and PLANT in residual[0][1], residual


def _replace_text(node: Any, old: str, new: str) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if value == old:
                node[key] = new
            else:
                _replace_text(value, old, new)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            if value == old:
                node[index] = new
            else:
                _replace_text(value, old, new)


# --- the registered-frame subtraction matters: a registered frame added on the wire ---

LIVE_PLAN = '<your_plan source="platform">\n- [ ] Send the line.\n</your_plan>'


@pytest.mark.parametrize("shape", list(SHAPE_OF))
def test_a_registered_frame_added_on_the_wire_is_accounted_for(shape: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """The open-tasks block is attached inside the model client, after the translator: only the
    registry's frame (``without_platform_parts``) accounts for it."""
    request, source = _built((shape, "t1", "plain"), monkeypatch)
    sh = SHAPE_OF[shape]
    if sh == fos.SHAPE_GOOGLE:
        request["contents"].append({"role": "user", "parts": [{"text": LIVE_PLAN}]})
    elif sh == fos.SHAPE_RESPONSES:
        request["input"] = [*request["input"], {"role": "user", "content": LIVE_PLAN}]
    else:
        request["messages"] = [*request["messages"], {"role": "user", "content": LIVE_PLAN}]
    known = residual_check.known_texts(source)
    assert residual_check.residual_of(sh, request, known) == []
    # Self-test: without the registry's frames the same block is a residual.
    monkeypatch.setattr("matrx_ai.config.platform_parts.without_platform_parts", lambda text: text)
    assert [t for _, t in residual_check.residual_of(sh, request, known)] == [LIVE_PLAN]
