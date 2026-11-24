"""A stream warning the person saw is part of the answer (CGU-M3 W4, lead's ruling 2026-11-04).

Live on 237036cb5: a chat bound to a retired box ran on Cloud and the stream said "This chat's old sandbox is retired,
so it now runs on Cloud…" — it showed while the reply was written, then went when the saved reply took over, and a
reload never said it: no stream warning was saved anywhere. The stream emitter now keeps the warnings it sent (repeats
collapsed by code), and the executor saves them on the first answer of the provider call (``metadata.warnings``).
"""

from __future__ import annotations

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.context.events import WarningPayload
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.config import TextContent, UnifiedMessage
from matrx_ai.orchestrator.executor import _stamp_answer_notes

RETIRED = (
    "This chat's old sandbox is retired, so it now runs on Cloud. Its files are archived and can be restored to your "
    "Cloud files."
)


def _answer(text: str) -> UnifiedMessage:
    return UnifiedMessage(role="assistant", content=[TextContent(text=text)])


@pytest.mark.asyncio
async def test_a_warning_sent_before_the_answer_is_saved_on_it() -> None:
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        await emitter.send_warning(
            WarningPayload(code="sandbox_retired_ran_on_cloud", system_message="retired tier", user_message=RETIRED, level="high")
        )
        await emitter.send_warning(WarningPayload(code="tools_missing", system_message="x", user_message="Some tools are missing."))
        await emitter.send_warning(WarningPayload(code="tools_missing", system_message="x", user_message="Some tools are missing."))

        first, second = _answer("ok"), _answer("and more")
        _stamp_answer_notes([first, second], 1, emitter)

        saved = first.metadata["warnings"]
        assert [w["code"] for w in saved] == ["sandbox_retired_ran_on_cloud", "tools_missing"]
        assert saved[0]["user_message"] == RETIRED and saved[0]["level"] == "high" and saved[0]["count"] == 1
        assert saved[1]["count"] == 2, "a repeat is one entry with its count (P-176's rule)"
        assert "warnings" not in second.metadata, "a call's warnings ride its FIRST answer only"
        assert first.metadata["provider_iteration"] == 1

        # Taken once: the next call's answer carries only what was sent after.
        later = _answer("next turn")
        _stamp_answer_notes([later], 2, emitter)
        assert "warnings" not in later.metadata
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_warnings_metadata_is_not_copied_and_a_take_empties_it() -> None:
    emitter = StreamEmitter()
    await emitter.send_warning(
        WarningPayload(code="request_context_changed", system_message="y" * 5000, metadata={"big": "z" * 5000})
    )
    (entry,) = emitter.take_warnings()
    assert entry["system_message"] == "y" * 5000
    assert "metadata" not in entry
    assert emitter.take_warnings() == []
