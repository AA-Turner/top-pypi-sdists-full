"""What a researcher reads when a plan cap refuses them.

The RENDERER, not the gate. `main()`'s `LimitReachedError` branch is the only
place the CLI turns a 402 into human copy, and it hangs on one `not in` check:
the server's message already ends with the booking link so that clients which
do not special-case 402 still get a CTA, which means a second CLI-rendered copy
puts the same URL on screen twice. That bug shipped once and was caught by the
end-to-end CLI smoke.

That smoke now asserts the UN-refused path, because capture is free and there is
no cap left to walk into (see tests/integration/test_smoke_plan_limits_cli.py).
These tests keep the refusal copy covered without needing a live budget to exist
anywhere -- so the first metered budget inherits a renderer that is already
pinned, rather than one that spent a release untested.
"""

from __future__ import annotations

import asyncio

import pytest

from probe import cli
from probe.sdk import errors

BOOKING = "https://research.prbe.ai/demo-meeting"
SERVER_MESSAGE = (
    f"The free plan includes 3 projects. Book 30 minutes with us to lift the limit: {BOOKING}"
)


def _detail(**overrides: object) -> dict:
    detail = {
        "message": SERVER_MESSAGE,
        "code": "limit_reached",
        "limit": "projects_per_team",
        "current": 3,
        "maximum": 3,
        "plan": "free",
        "booking_url": BOOKING,
    }
    detail.update(overrides)
    return detail


@pytest.fixture
def refuse(monkeypatch):
    """Make any command refuse with a 402, so only the renderer is under test.

    The error is raised from the `Client` factory rather than from a specific
    command: every command builds a client inside the same `try`, so this
    exercises the one branch that matters without tying the test to whichever
    verb happens to create something today.
    """

    def factory(message: str = SERVER_MESSAGE, **detail_overrides: object):
        def _raise(**_kw):
            raise errors.LimitReachedError(message, detail=_detail(**detail_overrides))

        monkeypatch.setattr(cli, "Client", _raise)

    return factory


def test_the_refusal_says_the_ceiling_and_that_nothing_was_lost(refuse, capsys) -> None:
    """A refusal is not a failure, and the copy has to say so. Someone who just
    hit a wall needs to know the work they already did is still there."""
    refuse()
    rc = cli.main(["project", "create", "--kind", "general", "over-the-line"])
    err = capsys.readouterr().err

    assert rc == 1
    assert "The free plan includes 3 projects" in err
    assert "at 3 of 3." in err
    assert "Nothing was deleted and everything already recorded stays readable." in err


def test_the_booking_link_lands_on_screen_exactly_once(refuse, capsys) -> None:
    """THE regression. The server's message already ends with the link so that a
    client with no 402 branch still shows a CTA; the CLI adding its own copy
    underneath printed the same URL twice, which reads as a bug, not emphasis."""
    refuse()
    cli.main(["project", "create", "--kind", "general", "over-the-line"])
    err = capsys.readouterr().err

    assert err.count(BOOKING) == 1, err


def test_the_link_is_added_when_the_message_somehow_lacks_it(refuse, capsys) -> None:
    """The other half of the same condition. If the server copy is ever reworded
    so it no longer carries the URL, the CTA must not silently disappear."""
    refuse(message="The free plan includes 3 projects.")
    cli.main(["project", "create", "--kind", "general", "over-the-line"])
    err = capsys.readouterr().err

    assert f"Book 30 minutes: {BOOKING}" in err
    assert err.count(BOOKING) == 1, err


def test_a_deployment_with_no_booking_url_shows_no_dead_link(refuse, capsys) -> None:
    """Self-host configures no booking destination. A refusal there should read
    as a refusal, not as an invitation to a calendar that does not exist."""
    refuse(message="The free plan includes 3 projects.", booking_url=None)
    cli.main(["project", "create", "--kind", "general", "over-the-line"])
    err = capsys.readouterr().err

    assert "Book 30 minutes" not in err
    assert "http" not in err


def test_a_refusal_without_counts_still_renders(refuse, capsys) -> None:
    """`current`/`maximum` are optional on the wire. A body missing them must
    drop the ceiling line rather than print 'at None of None'."""
    refuse(current=None, maximum=None)
    rc = cli.main(["project", "create", "--kind", "general", "over-the-line"])
    err = capsys.readouterr().err

    assert rc == 1
    assert "None" not in err
    assert "Nothing was deleted and everything already recorded stays readable." in err


@pytest.mark.parametrize("raises", [False, True])
def test_a_temporary_cli_client_does_not_leak_into_later_commands(monkeypatch, raises):
    import sys

    implementation = sys.modules["probe.cli.main"]
    original = implementation.Client
    temporary = object()
    monkeypatch.setattr(cli, "Client", temporary)

    def invoke(_argv):
        assert implementation.Client is temporary
        if raises:
            raise RuntimeError("command failed")
        return 0

    monkeypatch.setattr(implementation, "main", invoke)
    if raises:
        with pytest.raises(RuntimeError, match="command failed"):
            cli.main([])
    else:
        assert cli.main([]) == 0
    assert implementation.Client is original


# --- the MCP surface ---------------------------------------------------------
def test_mcp_renders_a_refusal_as_one_friendly_line() -> None:
    """Inside Cursor / Claude Code, the agent is the one reading this.

    A raw 402 reads to a model as a broken tool: it retries, spends what is left
    of an allowance that is already gone, and finally tells the researcher Probe
    is down. One sentence, and it has to be the SERVER's sentence -- appending a
    locally-worded second line is the drift the CLI printer already had once.
    """
    from mcp.server.fastmcp.exceptions import ToolError

    from probe.mcp import server as mcp_server

    @mcp_server._tool
    def refusing_tool() -> str:
        raise errors.LimitReachedError(SERVER_MESSAGE, detail=_detail())

    # Driven with asyncio.run rather than an async test: this package configures
    # no asyncio plugin, and `_tool` returns a coroutine function whatever the
    # wrapped body is.
    with pytest.raises(ToolError) as caught:
        asyncio.run(refusing_tool())

    rendered = str(caught.value)
    assert rendered == SERVER_MESSAGE
    assert rendered.count(BOOKING) == 1
    # Not dressed up as a crash: the words that would send an agent into a
    # retry loop must not appear.
    assert "error" not in rendered.lower()
    assert "failed" not in rendered.lower()
