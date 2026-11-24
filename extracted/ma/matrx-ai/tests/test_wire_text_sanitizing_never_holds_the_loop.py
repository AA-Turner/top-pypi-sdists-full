"""The send boundary's lone-surrogate step never holds the event loop (2026-11-11).

Live: ops.system_error event_loop_stall ``aidream-api:004bd02ae7555485`` - the loop froze 1.3-4.6s with its stack in
``replace_lone_surrogates`` (``LONE_SURROGATE.subn``) called from ``sanitize_wire_text`` inside ``prepare_for_send``:
the alternation-with-lookarounds pattern ran over every field of every wire part, on the loop, for every send. Two
fixes, each pinned here: (1) the step runs in a worker thread (``_run_step_off_loop``); (2) a string with no surrogate
at all skips the slow pattern (O(1) for ASCII, a fast charset scan otherwise). Red proof: before this, the step ran
via ``_run_step`` on the loop thread and a 10M-char ASCII field cost ~270ms of regex per send.
"""

from __future__ import annotations

import asyncio
import threading
import time
from types import SimpleNamespace

from matrx_ai.config import send_boundary
from matrx_ai.config.send_boundary import SendPrep, _run_step_off_loop, sanitize_wire_text
from matrx_ai.persistence import postgres_text
from matrx_ai.persistence.postgres_text import replace_lone_surrogates, sanitize_postgres_text


def test_the_step_runs_on_a_worker_thread_not_the_loop() -> None:
    seen: dict[str, object] = {}

    async def main() -> None:
        loop_thread = threading.get_ident()
        prep = SendPrep(stage="loop")

        def step() -> None:
            seen["thread"] = threading.get_ident()

        await _run_step_off_loop(prep, "lone_surrogates", step)
        seen["loop_thread"] = loop_thread
        seen["steps"] = list(prep.steps)

    asyncio.run(main())
    assert seen["thread"] != seen["loop_thread"]
    assert seen["steps"] == ["lone_surrogates"]


def test_prepare_for_send_routes_the_lone_surrogate_step_off_the_loop() -> None:
    from matrx_utils.source_guard import stable_source

    source = stable_source(send_boundary.prepare_for_send)
    block = source[source.index("sanitize_wire_text(") - 400 : source.index("sanitize_wire_text(")]
    assert "await _run_step_off_loop(" in block, "the lone-surrogate step must not run via the sync _run_step"


def test_a_failing_off_loop_step_is_announced_and_skipped() -> None:
    async def main() -> list[str]:
        prep = SendPrep(stage="loop")

        def boom() -> None:
            raise RuntimeError("x")

        await _run_step_off_loop(prep, "lone_surrogates", boom)
        return list(prep.steps)

    assert asyncio.run(main()) == []


def test_text_without_a_surrogate_never_reaches_the_slow_pattern(monkeypatch) -> None:
    class Exploding:
        def subn(self, *_a, **_k):  # pragma: no cover - reaching it is the failure
            raise AssertionError("slow pattern ran on text with no surrogate")

    monkeypatch.setattr(postgres_text, "LONE_SURROGATE", Exploding())
    monkeypatch.setattr(postgres_text, "_POSTGRES_ILLEGAL_TEXT", Exploding())
    for text in ("A" * 1000, "é中😀 plain", ""):
        assert replace_lone_surrogates(text) == (text, 0)
        assert sanitize_postgres_text({"k": text}).replacements == 0


def test_lone_halves_and_nul_are_still_replaced() -> None:
    assert replace_lone_surrogates("a\ud800b") == ("a�b", 1)
    assert replace_lone_surrogates("ascii\x00") == ("ascii\x00", 0)  # the wire step leaves NUL alone, as before
    result = sanitize_postgres_text({"a": "x\x00", "b": "é\udc80"})
    assert result.replacements == 2
    assert result.value == {"a": "x�", "b": "é�"}


def test_a_huge_clean_wire_is_cheap() -> None:
    from matrx_ai.config import UnifiedMessage
    from matrx_ai.config.message_config import MessageList
    from matrx_ai.config.unified_content import TextContent

    big_ascii = "A" * 10_000_000
    big_cjk = "中" * 2_000_000
    msgs = MessageList(
        _messages=[UnifiedMessage(role="user", content=[TextContent(text=big_ascii), TextContent(text=big_cjk)])]
    )
    cfg = SimpleNamespace(messages=msgs, system_instruction=big_ascii)
    started = time.perf_counter()
    assert sanitize_wire_text(cfg) == 0
    assert time.perf_counter() - started < 0.1
