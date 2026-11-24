"""A line the person reads about a changed request is said once, wherever the run happens, and
saved with the answer it decorates.

Review findings (chat night, 2026-11-09):

1. the once-per-request guard lived only in ``AppContext.metadata``: with no app context, or with
   metadata that is not a dict, every loop iteration said the trim line again;
2. ``send_client_warning`` with no emitter (a headless or batch run) dropped the line silently;
3. a long chat left on a small model re-trims every turn, and every answer said the same line again
   (and saved it, so a reload showed it under every answer): once per conversation until the model or
   the depth of the trim changes, read off the saved line (``metadata.warnings[].metadata.once_key``);
4. a warning sent after the last provider call's take stayed live-only: it is stamped on the newest
   unsaved answer before the turn barrier writes it;
5. an image converted on an EARLIER turn kept its conversion only in memory: the saved row is
   updated, so a fresh server load does not convert and announce it again.
"""

from __future__ import annotations

import contextvars
import logging
from types import SimpleNamespace

import pytest
from matrx_connect.context.events import WarningPayload
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.config import TextContent, UnifiedMessage, input_fit
from matrx_ai.config.input_fit import HISTORY_TRIMMED_CODE, _announce_history_trimmed
from matrx_ai.config.media_config import ImageContent
from matrx_ai.context import app_context
from matrx_ai.orchestrator import executor
from matrx_ai.processing.media_fallback import handler as media_handler
from matrx_ai.providers import outbound_params

TRIMMED = {"fits": True, "passes": [{"pass": "forced_trim_2_4", "blocks_rewritten": 3}]}
DEEPER = {"fits": True, "passes": [{"pass": "forced_trim_2_4", "blocks_rewritten": 3}, {"pass": "stub_history", "stubbed_blocks": 2}]}


def _config(model: str = "qwen-3-4b", messages: list | None = None):
    return SimpleNamespace(model=model, matrx_model_name=model, messages=messages or [])


@pytest.fixture
def sent(monkeypatch):
    lines: list[WarningPayload] = []
    monkeypatch.setattr(outbound_params, "send_client_warning", lambda payload, *, name: lines.append(payload))
    return lines


def _three_iterations(config) -> None:
    for _ in range(3):
        _announce_history_trimmed(TRIMMED, config, stage="loop", conversation_id="c-1")


def test_with_no_app_context_the_trim_line_is_said_once_per_request(sent, monkeypatch) -> None:
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: None)
    contextvars.copy_context().run(_three_iterations, _config())
    assert len(sent) == 1, f"said {len(sent)} times in one request"


def test_with_metadata_that_is_not_a_dict_the_trim_line_is_said_once(sent, monkeypatch) -> None:
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: SimpleNamespace(metadata="not a dict", emitter=None))
    contextvars.copy_context().run(_three_iterations, _config())
    assert len(sent) == 1


def test_a_new_request_says_it_again(sent, monkeypatch) -> None:
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: None)
    contextvars.copy_context().run(_three_iterations, _config())
    contextvars.copy_context().run(_three_iterations, _config())
    assert len(sent) == 2


def test_with_no_emitter_the_line_is_logged_never_dropped(monkeypatch, caplog) -> None:
    import matrx_connect

    monkeypatch.setattr(matrx_connect, "get_app_context", lambda: SimpleNamespace(emitter=None))
    with caplog.at_level(logging.WARNING):
        outbound_params.send_client_warning(
            WarningPayload(code=HISTORY_TRIMMED_CODE, user_message="Earlier messages were shortened to fit this model.", system_message="s", level="medium", recoverable=True),
            name="input_fit_history_trimmed",
        )
    assert any("not streamed" in r.getMessage() and HISTORY_TRIMMED_CODE in r.getMessage() for r in caplog.records)


def _answer_saying(key: str) -> UnifiedMessage:
    return UnifiedMessage(
        role="assistant",
        content=[TextContent(text="ok")],
        metadata={"warnings": [{"code": HISTORY_TRIMMED_CODE, "user_message": "x", "count": 1, "metadata": {"once_key": key}}]},
    )


def test_a_long_chat_on_a_small_model_says_the_trim_once_per_conversation(sent, monkeypatch) -> None:
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: None)
    said = input_fit.trim_line_key("qwen-3-4b", TRIMMED)
    history = [UnifiedMessage(role="user", content=[TextContent(text="hi")]), _answer_saying(said), UnifiedMessage(role="user", content=[TextContent(text="more")])]
    contextvars.copy_context().run(_three_iterations, _config(messages=history))
    assert sent == [], "the next turn said the same trim again"
    # A different model, or a deeper trim, is new: said once.
    contextvars.copy_context().run(_three_iterations, _config(model="llama-3-8b", messages=history))
    contextvars.copy_context().run(lambda: _announce_history_trimmed(DEEPER, _config(messages=history), stage="loop", conversation_id="c-1"))
    assert len(sent) == 2


def test_the_saved_line_carries_what_it_stands_for() -> None:
    emitter = StreamEmitter()
    emitter._remember_warning(
        WarningPayload(code=HISTORY_TRIMMED_CODE, user_message="x", system_message="s", level="medium", recoverable=True, metadata={"once_key": "m|forced_trim_2_4"})
    )
    (saved,) = emitter.take_warnings()
    assert saved["metadata"] == {"once_key": "m|forced_trim_2_4"}


@pytest.mark.asyncio
async def test_a_warning_after_the_last_take_is_saved_with_the_answer() -> None:
    emitter = StreamEmitter()
    emitter._remember_warning(WarningPayload(code="media_converted", user_message="x", system_message="s", level="medium", recoverable=True))
    answer = UnifiedMessage(role="assistant", content=[TextContent(text="done")], metadata={"provider_iteration": 3})
    request = SimpleNamespace(config=SimpleNamespace(messages=[UnifiedMessage(role="user", content=[TextContent(text="q")]), answer]))
    await executor._stamp_leftover_warnings(request, 0, emitter)
    assert [w["code"] for w in answer.metadata["warnings"]] == ["media_converted"]
    assert answer.metadata["provider_iteration"] == 3


@pytest.mark.asyncio
async def test_an_earlier_turns_converted_image_is_written_to_its_saved_row(monkeypatch) -> None:
    from matrx_ai.persistence import queue_helpers, sealed

    updates: list[tuple[str, dict]] = []
    monkeypatch.setattr(queue_helpers, "queue_message_update", lambda id, **fields: updates.append((id, fields)) or "q")

    async def same(parts, ctx=None):
        return list(parts)

    monkeypatch.setattr(sealed, "stored_message_content", same)
    image = ImageContent(base64_data="AAAA", mime_type="image/png")
    image.metadata[media_handler.CONVERSION_CACHE_KEY] = {"text": "TOTAL 12.00", "metadata": {"conversion": "ocr"}}
    image.metadata[media_handler.CONVERSION_SAID_KEY] = True
    saved = UnifiedMessage(role="user", content=[TextContent(text="total?"), image], id="m-earlier")
    saved.position = 2
    await media_handler._persist_conversion_on_saved_message(saved)
    assert len(updates) == 1 and updates[0][0] == "m-earlier"
    stored_image = [p for p in updates[0][1]["content"] if isinstance(p, dict) and p.get("kind") == "image"]
    assert stored_image and stored_image[0]["metadata"][media_handler.CONVERSION_CACHE_KEY]["text"] == "TOTAL 12.00"
    assert stored_image[0]["metadata"][media_handler.CONVERSION_SAID_KEY] is True

    new_this_turn = UnifiedMessage(role="user", content=[image])
    await media_handler._persist_conversion_on_saved_message(new_this_turn)
    assert len(updates) == 1, "a message new this turn is written by the barrier, not here"
