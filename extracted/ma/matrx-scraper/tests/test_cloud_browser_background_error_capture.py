"""Detached worker cleanup errors remain visible without launching Chromium."""

from __future__ import annotations

import asyncio
from collections import OrderedDict
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_utils import configure_error_capture
import matrx_utils.error_capture as error_capture_module
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker, _AgentTab, _TrackedPage


@pytest.mark.asyncio
async def test_evicted_page_close_failure_is_captured() -> None:
    captured: list[tuple[BaseException, dict[str, Any]]] = []
    recorded = asyncio.Event()

    async def _sink(exc: BaseException, **kwargs: Any) -> None:
        captured.append((exc, kwargs))
        recorded.set()

    old_sink = error_capture_module._sink
    old_allow = error_capture_module._allow_in_tests
    configure_error_capture(_sink, allow_in_tests=True)

    class _FailingPage:
        async def close(self) -> None:
            raise RuntimeError("page close failed")

    try:
        worker = object.__new__(BrowserWorker)
        entry = _AgentTab("agent-conv", "run#agent:agent-conv")
        entry.page_id = "page-7"
        entry.last_url = "https://site.test/"
        worker._agent_owned = {entry.agent_ref: entry}
        worker._session_mgr = SimpleNamespace(_sessions={entry.session_id: object()})
        worker._focused_agent_ref = entry.agent_ref
        worker._evicted_agent_urls = OrderedDict()
        worker._pages = {
            "page-7": _TrackedPage(
                "page-7",
                _FailingPage(),
                opener_page_id=None,
                kind="agent",
                opened_by=entry.agent_ref,
            )
        }

        worker._forget_agent(entry, close_tab=True)
        await asyncio.wait_for(recorded.wait(), timeout=1)
    finally:
        configure_error_capture(old_sink, allow_in_tests=old_allow)

    assert len(captured) == 1
    exc, fields = captured[0]
    assert str(exc) == "page close failed"
    assert fields["kind"] == "cloud_browser_evicted_agent_tab_close_failed"
    assert fields["context"] == {
        "source_app": "matrx-scraper",
        "source_feature": "cloud_browser.worker",
        "agent_ref": "agent-conv",
        "page_id": "page-7",
    }
