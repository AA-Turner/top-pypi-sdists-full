"""Tests for the advertised-tools startup log.

Operators occasionally rename a handler method and silently drop it
from ``tools/list`` — discovering that during incident review is the
wrong time. ``_log_advertised_tools`` turns a silent drop into a
searchable INFO log on server boot. These tests verify the message is
emitted with the right transport + counts on both MCP and A2A paths.
"""

from __future__ import annotations

import logging
import re
import sys

import pytest

from adcp.server import ADCPHandler, create_mcp_server
from adcp.server.a2a_server import create_a2a_server

_ADVERTISING_PATTERN = re.compile(r"advertising (\d+) of (\d+) tools")


class _MinimalHandler(ADCPHandler):
    """Overrides a few tools; rest stay at the ``not_supported`` default."""

    async def get_adcp_capabilities(self, params, context=None):
        return {"adcp": {"major_versions": [3]}}

    async def get_products(self, params, context=None):
        return {"products": []}


def test_mcp_startup_log_emits_count(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="adcp.server")
    create_mcp_server(_MinimalHandler(), name="log-test")
    messages = [r.message for r in caplog.records if r.name == "adcp.server"]
    assert any(
        "mcp server advertising" in m and "of" in m and "tools" in m for m in messages
    ), f"expected MCP startup log in {messages}"


def test_mcp_startup_log_advertises_only_overridden_tools(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO, logger="adcp.server")
    create_mcp_server(_MinimalHandler(), name="log-test")
    log_line = next(r.message for r in caplog.records if "mcp server advertising" in r.message)
    match = _ADVERTISING_PATTERN.search(log_line)
    assert match is not None, f"log line did not match expected shape: {log_line!r}"
    advertised = int(match.group(1))
    total = int(match.group(2))
    assert advertised == 2, f"expected 2 advertised, got {advertised} in: {log_line}"
    assert total > advertised, (
        f"expected total > advertised; got {total} vs {advertised}. "
        f"Full handler surface should exceed the 2 overridden methods."
    )


def test_mcp_startup_log_notes_advertise_all_flag(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO, logger="adcp.server")
    create_mcp_server(_MinimalHandler(), name="log-test", advertise_all=True)
    log_line = next(r.message for r in caplog.records if "mcp server advertising" in r.message)
    assert "advertise_all=True" in log_line


@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="a2a-sdk starlette integration requires Python 3.11+",
)
def test_a2a_startup_log_emits_count(caplog: pytest.LogCaptureFixture) -> None:
    """A2A startup log fires from ``create_a2a_server`` (symmetric with
    MCP's placement). Per-test executor constructions don't pollute
    caplog, which keeps this test reliable alongside a large test suite
    that instantiates executors."""
    caplog.set_level(logging.INFO, logger="adcp.server")
    create_a2a_server(_MinimalHandler(), name="log-test")
    messages = [r.message for r in caplog.records if r.name == "adcp.server"]
    assert any(
        "a2a server advertising" in m for m in messages
    ), f"expected A2A startup log in {messages}"


def test_unadvertised_tools_at_debug_level(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """The list of unadvertised tool names logs at DEBUG — INFO would
    be noisy on fully-implemented handlers. Pin both the level and the
    existence of the message so operators know where to look."""
    caplog.set_level(logging.DEBUG, logger="adcp.server")
    create_mcp_server(_MinimalHandler(), name="log-test")
    debug_lines = [r.message for r in caplog.records if r.levelno == logging.DEBUG]
    assert any(
        "unadvertised" in m for m in debug_lines
    ), f"expected a DEBUG log listing unadvertised tools, got: {debug_lines}"
