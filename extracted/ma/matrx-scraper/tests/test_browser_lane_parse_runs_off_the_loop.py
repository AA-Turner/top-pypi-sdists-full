"""A page rendered in the host's browser lane is parsed OFF the event loop.

RED before (live 2026-11-19, event_loop_stall in workflow_step:thin_rescue): ``_render_in_lane`` called the
BeautifulSoup/lxml parse (``_build_result_from_response``) directly on the loop, freezing the whole API process
~2.2 s on one page. Every other fetch path already parses through ``cpu_lane.run_cpu``.
"""

from __future__ import annotations

import threading
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper import browser_lane, orchestrator
from matrx_scraper.graph_nodes import scrape_actions
from matrx_scraper.graph_nodes.scrape_actions import ScrapeInput


@pytest.mark.asyncio
async def test_the_browser_lane_parse_runs_on_a_worker_thread(monkeypatch: pytest.MonkeyPatch) -> None:
    loop_thread = threading.get_ident()
    parsed_on: list[int] = []

    async def render(url: str, *, trigger: str) -> Any:
        return SimpleNamespace(url=url)

    def parse(response: Any, fast: bool = False) -> Any:
        parsed_on.append(threading.get_ident())
        return SimpleNamespace(engine=None, url=response.url)

    monkeypatch.setattr(browser_lane, "render_in_browser_lane", render)
    monkeypatch.setattr(orchestrator, "_build_result_from_response", parse)

    result = await scrape_actions._render_in_lane(ScrapeInput(url="https://news.example/tea"))

    assert result.engine == "browser_lane"
    assert parsed_on and parsed_on[0] != loop_thread, "the parse ran on the event-loop thread"
