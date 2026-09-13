"""Regression guards for completed-turn block detection in async graph nodes."""

from __future__ import annotations

import asyncio
import threading
from types import SimpleNamespace

import pytest


@pytest.mark.asyncio
async def test_completed_graph_normalization_leaves_the_event_loop_responsive(monkeypatch) -> None:
    from matrx_ai.graph_nodes import shared
    from matrx_ai.processing.blocks import content_view

    started = asyncio.Event()
    def blocking_content_view(_text: str) -> list[dict]:
        started_loop.call_soon_threadsafe(started.set)
        assert release_thread.wait(1), "test worker was not released"
        return []

    started_loop = asyncio.get_running_loop()
    release_thread = threading.Event()
    monkeypatch.setattr(content_view, "content_from_text", blocking_content_view)
    completed = SimpleNamespace(
        request=SimpleNamespace(
            conversation_id="conversation",
            request_id="request",
            config=SimpleNamespace(messages=[], response_format=None),
        ),
        final_response=SimpleNamespace(text="<large_xml", finish_reason="stop"),
        total_usage=None,
        timing_stats={},
        tool_call_stats={},
        iterations=1,
        metadata={},
    )

    normalization = asyncio.create_task(asyncio.to_thread(shared.normalize_completed, completed))
    await asyncio.wait_for(started.wait(), timeout=1)

    progressed = asyncio.Event()
    asyncio.get_running_loop().call_soon(progressed.set)
    await asyncio.wait_for(progressed.wait(), timeout=0.1)

    release_thread.set()
    assert (await normalization).content == []


def test_every_async_graph_action_offloads_completed_normalization() -> None:
    """No async action may reintroduce content-view detection onto its loop."""
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "matrx_ai" / "graph_nodes"
    expected = {
        "agent_action.py": "normalize_completed_result",
        "conversation_action.py": "normalize_completed_result",
        "llm_action.py": "normalize_completed_result",
        "extract_action.py": "normalize_completed_result",
        "agent_produce_action.py": "normalize_completed_result",
        "agent_loop_actions.py": "normalize_completed_result",
        "_strict_json.py": "normalize_completed",
        "chat_action.py": "normalize_completed_result",
        "mandate_action.py": "normalize_completed_result",
        "agent_assignment_action.py": "normalize_completed",
    }
    for filename, normalizer in expected.items():
        source = (root / filename).read_text()
        assert f"await asyncio.to_thread({normalizer}, completed" in source, filename
