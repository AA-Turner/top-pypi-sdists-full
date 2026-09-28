"""The hosted scraper server binds its own `knowledge.scraper` knob reader.

Crawls run in THIS process (``matrx_scraper.server.app``), not in aidream, and
aidream's binding in ``package_integration`` never reaches it — so until the
server bound one, every ``crawl.*`` / parser knob here silently answered with
the package's mirrored default and an admin turning the row changed nothing
(OPENSEO-TOOLS-SPEC §8.1).

Forcing function: remove the ``_bind_parser_knobs()`` call from ``_lifespan``
and the lifespan test reads the mirror instead of the row value; remove the
snapshot and the module fails to import its names.
"""

from __future__ import annotations

import time

import pytest
from test_startup_capability_gates import _app, _FakeQuery, _stub_prereqs

from matrx_scraper.parser.knobs import configure_parser_knobs, parser_knob
from matrx_scraper.server import app as server_app

MIRROR = 5_000_000


@pytest.fixture(autouse=True)
def _unbind():
    yield
    configure_parser_knobs(None)


@pytest.mark.asyncio
async def test_lifespan_binds_the_servers_knob_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_prereqs(monkeypatch)
    rows = {"crawl.html_max_bytes": 1234}

    async def fake_load(self) -> dict[str, object]:
        return dict(rows)

    monkeypatch.setattr(server_app._FeatureKnobSnapshot, "_load_from_db", fake_load)

    # Stop the boot at the first capability gate AFTER the binding: the binding
    # must already have happened by then.
    def exploding_filter(**kwargs: object) -> _FakeQuery:
        raise RuntimeError("stop after binding")

    monkeypatch.setattr("matrx_scraper.db.models_scraper.ScrapeParsedPage.filter", exploding_filter)
    configure_parser_knobs(None)

    with pytest.raises(server_app.ScraperStartupError):
        async with server_app._lifespan(_app()):
            pass

    assert parser_knob("crawl.html_max_bytes", MIRROR) == 1234


@pytest.mark.asyncio
async def test_the_crawler_sees_a_changed_crawl_knob(capsys: pytest.CaptureFixture[str]) -> None:
    rows: dict[str, object] = {"crawl.html_max_bytes": 1234, "crawl.link_first": False}

    async def loader() -> dict[str, object]:
        return dict(rows)

    snapshot = await server_app._bind_parser_knobs(loader)
    assert "parser/crawler knobs bound" in capsys.readouterr().err
    assert parser_knob("crawl.html_max_bytes", MIRROR) == 1234
    assert parser_knob("crawl.link_first", True) is False

    rows["crawl.html_max_bytes"] = 999
    snapshot._loaded_at = time.monotonic() - server_app.PARSER_KNOB_TTL_SECONDS - 1
    parser_knob("crawl.html_max_bytes", MIRROR)  # stale read schedules the refresh
    await snapshot._refresh_task
    assert parser_knob("crawl.html_max_bytes", MIRROR) == 999


@pytest.mark.asyncio
async def test_a_missing_row_falls_back_to_the_mirror_loudly(
    capsys: pytest.CaptureFixture[str],
) -> None:
    async def loader() -> dict[str, object]:
        return {}

    await server_app._bind_parser_knobs(loader)
    assert parser_knob("crawl.not_seeded", MIRROR) == MIRROR
    assert "crawl.not_seeded" in capsys.readouterr().err


@pytest.mark.asyncio
async def test_a_failed_first_load_is_announced_and_not_fatal(
    capsys: pytest.CaptureFixture[str],
) -> None:
    async def loader() -> dict[str, object]:
        raise OSError("db down")

    await server_app._bind_parser_knobs(loader)
    assert "FIRST LOAD FAILED" in capsys.readouterr().err
    assert parser_knob("crawl.html_max_bytes", MIRROR) == MIRROR
