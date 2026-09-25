"""Spawn-level proof that a ``runlayer run`` stdio child sees a minimal environment.

``test_main_stdio_env.py`` covers ``_build_stdio_env`` in isolation. This module
drives the real ``StdioTransport`` -> ``mcp.client.stdio.stdio_client`` path
``runlayer run`` uses, so an mcp/fastmcp upgrade that stopped merging the
platform base set (every launch breaks) or started passing the parent's full
environment through (secrets leak) fails here rather than in the field.
"""

import sys
import textwrap
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from runlayer_cli.main import _build_stdio_env

PARENT_SECRET = "RUNLAYER_TEST_PARENT_SECRET"
CONFIGURED_KEY = "RUNLAYER_TEST_CONFIGURED"

# A minimal MCP server whose only tool reports which env keys the child received.
_ENV_PROBE_SERVER = textwrap.dedent(
    """
    import os

    from fastmcp import FastMCP

    mcp = FastMCP("env-probe")


    @mcp.tool
    def env_keys(keys: list[str]) -> dict[str, bool]:
        return {key: key in os.environ for key in keys}


    mcp.run()
    """
)


@pytest.fixture
def env_probe_script(tmp_path: Path) -> Path:
    script = tmp_path / "env_probe_server.py"
    script.write_text(_ENV_PROBE_SERVER)
    return script


@pytest.mark.asyncio
async def test_spawned_child_gets_path_but_not_parent_secret(
    env_probe_script: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(PARENT_SECRET, "leaked-if-visible")
    transport_config: dict[str, object] = {"env": {CONFIGURED_KEY: "yes"}}

    transport = StdioTransport(
        command=sys.executable,
        args=[str(env_probe_script)],
        env=_build_stdio_env(transport_config),
    )
    async with Client(transport) as client:
        result = await client.call_tool(
            "env_keys", {"keys": ["PATH", PARENT_SECRET, CONFIGURED_KEY]}
        )

    seen = result.data
    assert seen["PATH"] is True, "mcp stopped merging its platform base env"
    assert seen[CONFIGURED_KEY] is True
    assert seen[PARENT_SECRET] is False, "parent env leaked into the stdio child"
