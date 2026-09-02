"""Client-host pricing: no error spam, one-time INFO degrade, and catalog-fed
pricing when the host supplies it."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


def _clean_env() -> dict[str, str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }
    if "VIRTUAL_ENV" in os.environ:
        env["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV"]
    return env


def _run(code: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=_clean_env(),
        timeout=120,
    )


def test_dbless_host_degrades_once_no_error_spam():
    """In a CLIENT host with no catalog, warm_pricing_lookup must decide ONCE
    (warm-empty cache + a single INFO notice), never a DBNotConfiguredError or
    red error per request."""
    code = """
import asyncio

async def main():
    from matrx_ai.config import usage_config as uc
    notices = []
    import matrx_utils
    for _ in range(5):  # simulate five requests
        result = await uc.warm_pricing_lookup()
        assert result == {}
    assert uc.is_pricing_lookup_warm() is True   # decided, not retried forever
    assert uc._client_host_pricing_mode is True
    assert uc._client_host_pricing_notice_shown is True

    # Cost calc on a miss stays quiet (no per-request red error).
    usage = uc.TokenUsage(input_tokens=10, output_tokens=5, matrx_model_name="whatever")
    assert usage.calculate_cost() is None

asyncio.run(main())
"""
    proc = _run(code)
    assert proc.returncode == 0, proc.stderr
    combined = proc.stdout + proc.stderr
    assert "DBNotConfiguredError" not in combined
    assert combined.count("Cost tracking unavailable in this client host") == 1, combined


def test_catalog_pricing_computes_costs():
    """When the host catalog carries pricing tiers, costs ARE computed."""
    code = """
import asyncio
import matrx_ai

MODEL = {
    "id": "1", "name": "mock-model", "api_class": "mock_standard",
    "wire_format": "mock_chat", "provider": "mock",
    "pricing": [{"max_tokens": None, "input_price": 1.0, "output_price": 2.0,
                 "cached_input_price": 0.5}],
}

class Catalog:
    async def list_models(self):
        return [MODEL]
    async def get_model(self, id_or_name):
        return MODEL if id_or_name in ("1", "mock-model") else None

matrx_ai.configure(model_catalog=Catalog())

async def main():
    from matrx_ai.config import usage_config as uc
    lookup = await uc.warm_pricing_lookup()
    assert "mock-model" in lookup, lookup
    assert "catalog:mock-model" in lookup, lookup
    usage = uc.TokenUsage(input_tokens=1_000_000, output_tokens=1_000_000,
                          matrx_model_name="mock-model",
                          offering_id="catalog:mock-model")
    cost = usage.calculate_cost()
    assert cost is not None and abs(cost - 3.0) < 1e-9, cost

asyncio.run(main())
"""
    proc = _run(code)
    assert proc.returncode == 0, proc.stderr


def test_catalog_without_pricing_is_quiet():
    """A host catalog with NO pricing data → warm-empty + one INFO, quiet misses."""
    code = """
import asyncio
import matrx_ai

MODEL = {"id": "1", "name": "mock-model", "api_class": "mock_standard",
         "wire_format": "mock_chat", "provider": "mock"}

class Catalog:
    async def list_models(self):
        return [MODEL]
    async def get_model(self, id_or_name):
        return MODEL if id_or_name in ("1", "mock-model") else None

matrx_ai.configure(model_catalog=Catalog())

async def main():
    from matrx_ai.config import usage_config as uc
    for _ in range(3):
        assert await uc.warm_pricing_lookup() == {}
    usage = uc.TokenUsage(input_tokens=10, output_tokens=5,
                          matrx_model_name="mock-model")
    assert usage.calculate_cost() is None

asyncio.run(main())
"""
    proc = _run(code)
    assert proc.returncode == 0, proc.stderr
    combined = proc.stdout + proc.stderr
    assert "PRICING LOOKUP MISS" not in combined
    assert combined.count("Cost tracking unavailable in this client host") == 1, combined
