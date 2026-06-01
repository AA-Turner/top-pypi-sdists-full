"""Tests for lifespan_stack."""

import warnings
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI

from csrd.lifespan.lifespan_stack import lifespan_stack


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.state.db = "connected"
    yield {"db": "connected"}
    app.state.db = None


@asynccontextmanager
async def cache_lifespan(app: FastAPI):
    yield {"cache": "ready"}


@asynccontextmanager
async def void_lifespan(app: FastAPI):
    yield  # yields None — no state to merge


@asynccontextmanager
async def bad_lifespan(app: FastAPI):
    yield "not_a_mapping"  # should trigger warning


class TestLifespanStack:
    @pytest.mark.asyncio
    async def test_single_lifespan(self):
        app = FastAPI()
        stack = lifespan_stack(db_lifespan)
        async with stack(app) as state:
            assert state == {"db": "connected"}

    @pytest.mark.asyncio
    async def test_multiple_lifespans(self):
        app = FastAPI()
        stack = lifespan_stack(db_lifespan, cache_lifespan)
        async with stack(app) as state:
            assert state == {"db": "connected", "cache": "ready"}

    @pytest.mark.asyncio
    async def test_void_lifespan_skipped(self):
        app = FastAPI()
        stack = lifespan_stack(void_lifespan, db_lifespan)
        async with stack(app) as state:
            assert state == {"db": "connected"}

    @pytest.mark.asyncio
    async def test_bad_lifespan_warns(self):
        app = FastAPI()
        stack = lifespan_stack(bad_lifespan)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            async with stack(app) as state:
                assert state == {}
            assert len(w) == 1
            assert "Unexpected value" in str(w[0].message)

    @pytest.mark.asyncio
    async def test_nested_list_flattening(self):
        app = FastAPI()
        stack = lifespan_stack([db_lifespan, cache_lifespan])
        async with stack(app) as state:
            assert state == {"db": "connected", "cache": "ready"}

    @pytest.mark.asyncio
    async def test_empty_stack(self):
        app = FastAPI()
        stack = lifespan_stack()
        async with stack(app) as state:
            assert state == {}

    @pytest.mark.asyncio
    async def test_cleanup_runs_on_exit(self):
        app = FastAPI()
        stack = lifespan_stack(db_lifespan)
        async with stack(app):
            assert app.state.db == "connected"
        assert app.state.db is None

    @pytest.mark.asyncio
    async def test_state_mirrored_to_app_state(self):
        """Lifespan state is mirrored onto app.state for auto-discovery."""
        app = FastAPI()
        stack = lifespan_stack(cache_lifespan)
        async with stack(app) as state:
            assert state == {"cache": "ready"}
            # cache_lifespan doesn't set app.state directly,
            # but lifespan_stack mirrors it automatically
            assert app.state.cache == "ready"
