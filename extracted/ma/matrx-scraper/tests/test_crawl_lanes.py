"""Crawl lanes (MKT-150): background crawls never starve a person's initialization."""

from __future__ import annotations

import asyncio
import threading

import pytest

from matrx_scraper import cpu_lane
from matrx_scraper.cpu_lane import LANE_BULK, LANE_INTERACTIVE, bulk_page_slots, reset_lane, run_cpu, set_lane
from matrx_scraper.crawler import SiteCrawlerConfig
from matrx_scraper.parser.knobs import configure_parser_knobs


@pytest.fixture(autouse=True)
def _knobs():
    values: dict[str, int] = {}

    def reader(key: str):
        if key in values:
            return values[key]
        raise KeyError(key)

    configure_parser_knobs(reader)
    yield values
    configure_parser_knobs(None)


def _thread_name() -> str:
    return threading.current_thread().name


async def test_bulk_cpu_runs_on_its_own_pool_and_interactive_does_not():
    token = set_lane(LANE_BULK)
    try:
        bulk_thread = await run_cpu(_thread_name)
    finally:
        reset_lane(token)
    interactive_thread = await run_cpu(_thread_name)
    assert bulk_thread.startswith("crawl-bulk-cpu")
    assert not interactive_thread.startswith("crawl-bulk-cpu")


async def test_interactive_parse_finishes_while_bulk_pool_is_full(_knobs):
    _knobs["crawl.bulk_cpu_threads"] = 1
    release = threading.Event()
    token = set_lane(LANE_BULK)
    try:
        # Fill the bulk pool (and queue more behind it) with work that blocks.
        stuck = [asyncio.ensure_future(run_cpu(release.wait, 5)) for _ in range(6)]
    finally:
        reset_lane(token)
    try:
        await asyncio.sleep(0.05)
        # An interactive parse must not wait for any of it.
        assert await asyncio.wait_for(run_cpu(lambda: "parsed"), timeout=1.0) == "parsed"
    finally:
        release.set()
        await asyncio.gather(*stuck)


async def test_bulk_page_slots_follow_the_knob(_knobs):
    assert bulk_page_slots()._value == cpu_lane.BULK_PAGE_SLOTS_MIRROR
    _knobs["crawl.bulk_page_slots"] = 2
    slots = bulk_page_slots()
    assert slots._value == 2
    await slots.acquire()
    await slots.acquire()
    assert slots.locked()
    slots.release()
    slots.release()


def test_lane_defaults_to_interactive():
    assert SiteCrawlerConfig(base_url="https://example.com").lane == LANE_INTERACTIVE
    assert cpu_lane.current_lane() == LANE_INTERACTIVE


def test_site_initialization_runs_interactive_and_full_crawls_bulk():
    import inspect

    from matrx_scraper.web_crawl import service

    source = inspect.getsource(service)
    assert "lane=LANE_INTERACTIVE if short_homepage_run else LANE_BULK" in source
