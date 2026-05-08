"""Fixtures for Zoom webhook integration tests.

These tests require a running PostgreSQL instance. They are marked with
@pytest.mark.integration and can be skipped with::

    pytest -m "not integration"

To run them, export a test DSN or set ENV=production::

    ZOOM_WEBHOOK_TEST_DSN="postgres://user:pass@localhost:5432/testdb" \\
        pytest tests/integration/hooks/ -v -m integration

    # or using the project's configured environment:
    ENV=production pytest tests/integration/hooks/ -v -m integration
"""
import hashlib
import hmac
import json
import os
import time

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from asyncdb import AsyncDB

from flowtask.hooks.actions.zoom_event import PersistZoomEvent
from flowtask.hooks.types.zoom import ZoomWebHook

ZOOM_SECRET = "test-secret-do-not-use-in-prod"


def _resolve_dsn() -> str | None:
    if dsn := os.getenv("ZOOM_WEBHOOK_TEST_DSN"):
        return dsn
    if dsn := os.getenv("DATABASE_URL"):
        return dsn
    try:
        from flowtask.conf import default_dsn
        return default_dsn
    except Exception:
        return None


ZOOM_TEST_DSN = _resolve_dsn()

_CREATE_SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS navigator;
CREATE TABLE IF NOT EXISTS navigator.zoom_events_raw (
    id              BIGSERIAL PRIMARY KEY,
    event           TEXT NOT NULL,
    account_id      TEXT,
    event_ts        TIMESTAMPTZ NOT NULL,
    received_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    dedupe_hash     TEXT NOT NULL,
    headers         JSONB,
    raw             JSONB NOT NULL,
    CONSTRAINT zoom_events_raw_dedupe_uniq UNIQUE (dedupe_hash)
);
"""


def make_signed_request(
    payload: dict,
    secret: str = ZOOM_SECRET,
    ts: str | None = None,
) -> tuple[bytes, dict]:
    """Return (raw_body_bytes, headers_dict) with a valid x-zm-signature."""
    raw = json.dumps(payload).encode("utf-8")
    ts = ts or str(int(time.time()))
    msg = f"v0:{ts}:{raw.decode()}".encode()
    sig = "v0=" + hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
    return raw, {
        "x-zm-signature": sig,
        "x-zm-request-timestamp": ts,
        "content-type": "application/json",
    }


async def _make_db() -> AsyncDB:
    """Open a fresh AsyncDB connection to the test database."""
    if not ZOOM_TEST_DSN:
        pytest.skip("ZOOM_WEBHOOK_TEST_DSN not set — skipping integration tests")
    db = AsyncDB("pg", dsn=ZOOM_TEST_DSN)
    try:
        await db.connection()
    except Exception as exc:
        pytest.skip(f"Postgres unavailable: {exc}")
    return db


@pytest.fixture(autouse=True, scope="session")
def ensure_zoom_schema(request):
    """Create the zoom_events_raw table once per session via a sync subprocess."""
    import asyncio

    async def _setup():
        if not ZOOM_TEST_DSN:
            return
        db = AsyncDB("pg", dsn=ZOOM_TEST_DSN)
        try:
            await db.connection()
            await db.execute(_CREATE_SCHEMA_SQL)
        except Exception:
            pass
        finally:
            try:
                await db.close()
            except Exception:
                pass

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_setup())
    finally:
        loop.close()


@pytest.fixture
async def zoom_db():
    """Function-scoped Postgres connection for test assertions."""
    db = await _make_db()
    yield db
    await db.close()


@pytest.fixture
async def zoom_action():
    """Function-scoped PersistZoomEvent with its own DB connection."""
    action = PersistZoomEvent(dsn=ZOOM_TEST_DSN)
    await action.open()
    yield action
    await action.close()


@pytest.fixture
async def zoom_client(zoom_action):
    """aiohttp TestClient with ZoomWebHook + PersistZoomEvent wired directly."""
    app = web.Application()
    hook = ZoomWebHook(
        id="zoom-us-test",
        secret_token=ZOOM_SECRET,
        replay_window_seconds=300,
        actions=[],
    )
    hook.add_action(zoom_action)
    hook.setup(app)
    async with TestClient(TestServer(app)) as client:
        yield client
