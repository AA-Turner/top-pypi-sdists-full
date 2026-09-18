"""No entrypoint of matrx-scraper may serve traffic with a Block Ledger that is a no-op.

🚨 THE DEFECT THESE GUARD (board row H7). `matrx_utils.block_sink.announce_block()` is a
documented no-op until a host calls `configure_block_sink()`. That call lived in exactly one
place — `aidream/package_integration.py` — and the hosted scraper service
(`scraper.app.matrxserver.com`) runs an image built from `packages/matrx-scraper/Dockerfile`,
which installs `packages/` and deliberately NOT aidream. So the service that the live
`/scraper/batch` screen actually calls could not make that call, and every wall it hit was
discarded in silence: two real login-walled URLs produced zero rows in
`platform.acquisition_block` while the identical failure inside aidream produced one.

Each leg below was run RED against the pre-fix arrangement before it was written green — the
RED command is named on the leg it belongs to.
"""

from __future__ import annotations

import ast
import asyncio
from pathlib import Path

import pytest
import matrx_utils.block_sink as sink_module

from matrx_scraper.blocks import (
    BlockSinkNotConfigured,
    BlockSinkSelfTestFailed,
    assert_block_sink_ready,
    self_test_block_ledger,
)
from matrx_scraper.blocks.testing import FakeBlockStore

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "matrx_scraper"


@pytest.fixture(autouse=True)
def _no_inherited_sink():
    """Every leg starts from the unconfigured world the hosted service actually booted into."""
    original = sink_module._sink
    sink_module.configure_block_sink(None)
    try:
        yield
    finally:
        sink_module.configure_block_sink(original)


# ── Leg 1: binding the database is what wires the ledger ────────────────────────────────
# RED before the fix (and RED again if `_wire_block_ledger()` is ever removed from db/web.py):
#   pytest packages/matrx-scraper/tests/test_every_entrypoint_wires_the_block_sink.py -k binding


def test_the_standalone_binding_path_wires_a_sink(monkeypatch):
    """`bootstrap_web_db()` — what the hosted service's lifespan calls — leaves a live sink."""
    import matrx_orm

    from matrx_scraper.db import web

    monkeypatch.setattr(web, "_models_registered", True)
    monkeypatch.setattr(matrx_orm, "register_platform_db", lambda *a, **k: None)
    monkeypatch.setattr(
        "matrx_scraper.db.web.register_platform_db", lambda *a, **k: None, raising=False
    )

    assert not sink_module.block_sink_configured()
    web.bootstrap_web_db()
    assert sink_module.block_sink_configured(), (
        "the hosted scraper service binds its database and then serves traffic; if that path "
        "does not install a block sink, every wall it hits is discarded in silence"
    )


def test_the_hosted_binding_path_wires_a_sink(monkeypatch):
    """`bind_web_to_host()` — every in-process host, including aidream — does too."""
    from matrx_scraper.db import web

    monkeypatch.setattr(web, "_models_registered", True)
    monkeypatch.setattr("matrx_orm.is_database_registered", lambda *a, **k: True)

    assert not sink_module.block_sink_configured()
    web.bind_web_to_host("some_host_pool")
    assert sink_module.block_sink_configured()


def test_a_host_that_already_wired_its_own_sink_keeps_it(monkeypatch):
    """aidream writes through its generated manager; the package must never displace it."""
    from matrx_scraper.db import web

    async def host_sink(**_fields):
        return None

    sink_module.configure_block_sink(host_sink)
    monkeypatch.setattr(web, "_models_registered", True)
    monkeypatch.setattr("matrx_orm.is_database_registered", lambda *a, **k: True)

    web.bind_web_to_host("some_host_pool")
    assert sink_module._sink is host_sink


# ── Leg 2: no new entrypoint can bind the web database behind db/web.py's back ───────────


def test_nothing_binds_the_web_database_outside_db_web():
    """The wiring hangs off the binding functions, so binding elsewhere would bypass it.

    This is the part that makes the fix a CLASS fix rather than one more place somebody
    remembered: a future worker, CLI or second service cannot obtain the `matrx_web` pool
    without also obtaining a ledger, because there is exactly one way to obtain it.
    """
    offenders: list[str] = []
    for path in PACKAGE_ROOT.rglob("*.py"):
        if path.parts[-2:] == ("db", "web.py"):
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id not in {"register_platform_db", "register_database_alias"}:
                continue
            args = [a for a in node.args if isinstance(a, ast.Name)]
            if any(a.id == "WEB_DB_NAME" for a in args):
                offenders.append(f"{path.relative_to(PACKAGE_ROOT)}:{node.lineno}")
    assert not offenders, (
        "these bind the canonical web database without going through matrx_scraper.db.web, "
        "so the process they run in would have no Block Ledger: " + ", ".join(offenders)
    )


# ── Leg 3: the door refuses to open on a ledger that is a no-op ─────────────────────────
# RED before the fix: `assert_block_sink_ready` did not exist and the service booted happily.


def test_the_door_refuses_to_open_without_a_sink():
    with pytest.raises(BlockSinkNotConfigured):
        assert_block_sink_ready()


def test_the_hosted_service_lifespan_actually_runs_the_self_test():
    """A guard nobody calls is not a guard. The service's own lifespan must call it."""
    source = (PACKAGE_ROOT / "server" / "app.py").read_text()
    assert "self_test_block_ledger" in source, (
        "the standalone scraper server must prove its block ledger at boot; a boolean saying "
        "the sink is configured would have been just as silent if the table or grant were the "
        "thing that was wrong"
    )
    assert '"block_ledger"' in source, "readiness must refuse to call a ledger-less server ready"


# ── Leg 4: the self-test is a real round trip, not a wiring check ────────────────────────
# RED: swap `find_open` for one that always answers a row and this leg still passes; swap the
# sink for one that drops the block and it fails, which is the direction that matters.


def test_the_self_test_fails_when_an_announced_block_never_becomes_a_row():
    async def swallowing_sink(**_fields):
        return None

    sink_module.configure_block_sink(swallowing_sink)
    store = FakeBlockStore()

    with pytest.raises(BlockSinkSelfTestFailed):
        asyncio.run(self_test_block_ledger(store=store, timeout_seconds=1.0))


def test_the_self_test_passes_on_a_working_seam_and_leaves_no_row_behind():
    from matrx_scraper.blocks.sink import configure_block_ledger

    store = FakeBlockStore()
    configure_block_ledger(store=store, force=True)

    block_id = asyncio.run(self_test_block_ledger(store=store, timeout_seconds=5.0))

    assert block_id
    assert store.rows == {}, (
        "the probe is not a finding; an operator reading the ledger to decide what to go and "
        "get must never see one row per container boot"
    )
