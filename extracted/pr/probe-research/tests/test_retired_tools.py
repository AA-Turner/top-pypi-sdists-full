"""A retired tool name answers with instructions, not `Unknown tool`.

THE FAILURE THIS EXISTS FOR (2026-09-02). The rename to browse/entity/metrics
deployed as a hard cutover, and the session that deployed it discovered the cost
by calling `browse_research` a minute later: `Unknown tool: browse_research`.

The cause is not a stale INSTALL, which is what an agent reading that error
assumes and what "upgrade the package" would tell it to fix. A client fetches
`tools/list` once at `initialize` and holds that snapshot for the life of the
session, so a session that connected before the deploy cannot see `browse` no
matter how current its package is. Its recovery is to RECONNECT. An agent cannot
work that out from `Unknown tool`, and its usual next move -- guess a
neighbouring name, or give up and tell the user the server is broken -- is wrong
in both directions.

Two properties are load-bearing here and each has a test:

  * the retired names must NOT be registered, or every new session pays context
    for six dead tools in `tools/list` forever;
  * calling one anyway must still be intercepted, which is the whole point --
    an unregistered name is exactly the one FastMCP would 404.

Those pull against each other, which is why this is a call-layer override rather
than six stubs, and why "it is not in the list" must never be read as "it is not
handled".
"""

from __future__ import annotations

import asyncio

import pytest

from probe.mcp.server import _RETIRED_TOOLS, create_server


def test_no_retired_name_is_registered() -> None:
    """The list an agent pays for holds only tools it can call."""
    tools = asyncio.run(create_server().list_tools())
    names = {t.name for t in tools}
    leaked = sorted(names & set(_RETIRED_TOOLS))
    assert not leaked, (
        f"retired names reached tools/list: {leaked} -- every new session now "
        "carries their descriptions as context to reach a refusal"
    )


@pytest.mark.parametrize("name", sorted(_RETIRED_TOOLS))
def test_a_retired_name_is_refused_with_the_replacement(name: str) -> None:
    """The refusal names the call to make, so recovery costs one turn."""
    with pytest.raises(Exception) as excinfo:
        asyncio.run(create_server().call_tool(name, {}))
    message = str(excinfo.value)
    assert name in message, "the refusal must name what was called"
    assert _RETIRED_TOOLS[name] in message, (
        f"{name} refused without naming its replacement -- that is the one fact "
        "that makes this better than Unknown tool"
    )


@pytest.mark.parametrize("name", sorted(_RETIRED_TOOLS))
def test_the_refusal_sends_a_stale_session_to_reconnect(name: str) -> None:
    """Not to upgrade. Upgrading is the wrong fix for the common case, and a
    message that leads with it sends a correctly-installed caller to reinstall a
    package that was never the problem."""
    with pytest.raises(Exception) as excinfo:
        asyncio.run(create_server().call_tool(name, {}))
    message = str(excinfo.value).lower()
    assert "reconnect" in message
    assert message.index("call `") < message.index("reconnect"), (
        "the replacement must come before the reconnect instruction: it is the "
        "only line an agent needs to recover inside the same turn"
    )


def test_a_live_tool_is_untouched() -> None:
    """The override must intercept retired names and nothing else."""
    tools = {t.name for t in asyncio.run(create_server().list_tools())}
    assert "browse" in tools and "entity" in tools and "metrics" in tools
