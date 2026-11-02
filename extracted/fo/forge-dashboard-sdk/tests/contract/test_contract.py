"""Runs the client against a Prism mock server generated from
forge-dashboard's own pinned spec (see .github/workflows/ci.yml's
"contract" job) — never a hand-rolled stub. See
rules/sdk-generation.md's "Testing against the spec, not a hand-written
stub": this proves the client's requests/responses conform to the spec,
nothing more.
"""

from __future__ import annotations

import asyncio
import os

import pytest

from forge_dashboard import ForgeDashboardClient

pytestmark = pytest.mark.contract


@pytest.fixture
def client() -> ForgeDashboardClient:
    base_url = os.environ.get("FORGE_DASHBOARD_BASE_URL")
    if not base_url:
        pytest.fail("FORGE_DASHBOARD_BASE_URL must point at a running Prism mock (see ci.yml's contract job)")
    return ForgeDashboardClient(base_url, api_token="prism-does-not-check-this")  # noqa: S106 -- not a real secret, Prism doesn't check auth


def test_health(client: ForgeDashboardClient) -> None:
    client.health()


def test_ahealth(client: ForgeDashboardClient) -> None:
    asyncio.run(client.ahealth())


def test_get_version(client: ForgeDashboardClient) -> None:
    client.get_version()


def test_aget_version(client: ForgeDashboardClient) -> None:
    asyncio.run(client.aget_version())
