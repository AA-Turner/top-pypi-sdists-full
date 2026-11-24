"""The ad-block lists come from ONE announced step per process, and no parse runs without it.

A host pre-warms the step at startup (``prewarm_filter_lists``); a parse that arrives
while it is still running waits for that same step instead of running unfiltered, and
the fetch happens once. When the fetch fails and nothing is saved, the parse blocks
nothing (as it always did) and the process reports the list as degraded
(``filter_list_status``, shown by the scraper server's /health/ready). An extractor
never keeps a filter older than the process's lists.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from matrx_scraper.parser import utils
from matrx_scraper.parser.core import ParserOrchestrator, _parse_html_sync

AD_LIST = "||ads.blocked-example.com^\n"
PAGE = (
    "<html><body><p>Story.</p><img src='https://ads.blocked-example.com/b.png' alt='ad'>"
    "<img src='https://cdn.example.test/photo.png' alt='photo'></body></html>"
)


@pytest.fixture
def lists(tmp_path, monkeypatch):
    class _Temp(utils.LocalTempFiles):
        @property
        def temp_dir(self) -> Path:
            return tmp_path

    fetches: list[str] = []
    state = {"delay": 0.0, "fail": False}

    def fetch(url, **_kwargs):
        fetches.append(url)
        time.sleep(state["delay"])
        if state["fail"]:
            raise OSError("list host unreachable")
        return type("R", (), {"status_code": 200, "text": AD_LIST})()

    monkeypatch.setattr(utils.DomainFilter, "_instances", {})
    monkeypatch.setattr(utils.AdblockConfigLoader, "_instance", None)
    monkeypatch.setattr(utils, "_FILTER_LIST_STATUS", {})
    monkeypatch.setattr(utils, "default_file_manager", lambda: _Temp("scraper"))
    monkeypatch.setattr(utils.httpx, "get", fetch)
    return fetches, state


def _images(result) -> str:
    return str(result.get("images"))


def test_a_parse_during_the_prewarm_waits_for_it_and_the_list_is_fetched_once(lists):
    fetches, state = lists
    state["delay"] = 0.5
    prewarm = threading.Thread(target=utils.ensure_filter_lists)
    prewarm.start()
    time.sleep(0.05)  # the pre-warm holds the step
    out = _parse_html_sync(PAGE, "https://example.test/a")
    prewarm.join()
    assert len(fetches) == 1
    assert "ads.blocked-example.com" not in _images(out)
    assert "cdn.example.test" in _images(out)


def test_a_process_that_never_prewarmed_gets_the_list_on_its_first_parse(lists):
    fetches, _state = lists
    out = _parse_html_sync(PAGE, "https://example.test/a")
    _parse_html_sync(PAGE, "https://example.test/b")
    assert len(fetches) == 1
    assert "ads.blocked-example.com" not in _images(out)
    assert utils.filter_list_status() == {"easylist": "fetched"}


def test_a_failed_fetch_blocks_nothing_and_reports_degraded(lists):
    fetches, state = lists
    state["fail"] = True
    out = _parse_html_sync(PAGE, "https://example.test/a")
    assert "ads.blocked-example.com" in _images(out)
    assert utils.filter_list_status()["easylist"].startswith("EMPTY")
    _parse_html_sync(PAGE, "https://example.test/b")
    assert len(fetches) == 1  # never one fetch per parse


def test_an_orchestrator_built_earlier_reads_the_current_lists(lists):
    fetches, state = lists
    state["fail"] = True
    held = ParserOrchestrator()  # built while the process has an empty list
    state["fail"] = False
    utils.DomainFilter._instances = {}  # the process's lists are replaced
    utils.AdblockConfigLoader._instance = None
    result = held.parse_content(PAGE, "https://example.test/a")
    from matrx_scraper.parser.extraction_rules import rules

    assert "ads.blocked-example.com" not in str(result["organized_data"].extract(rules=rules).get("images"))
