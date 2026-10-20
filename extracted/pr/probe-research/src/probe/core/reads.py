"""What `probe.core` reads rather than changes: the device's status snapshot.

`status()` is `probe status --json`'s object (the schema is
`probe.cli.status`'s docstring); `print_status()` writes it the way that
command does, and `probe status --json` and `python -m probe.core.run status`
both call it, so the two cannot drift. Local files only unless `refresh`.

The CLI is imported inside each call, never at module level.
"""

from __future__ import annotations

import json

from probe.core import events


def status(*, refresh: bool = False, timeout: float | None = None) -> dict:
    """The device's Probe install as one JSON-ready object. `refresh` adds the
    slow checks (the agents' CLIs, the server, the MCP token), all within
    `timeout` seconds (default `probe.cli.status.DEFAULT_TIMEOUT_S`)."""
    from probe.cli import status as status_impl

    limit = status_impl.DEFAULT_TIMEOUT_S if timeout is None else timeout
    return status_impl.snapshot(refresh=refresh, timeout=limit)


def print_status(*, refresh: bool = False, timeout: float | None = None) -> None:
    """`status()` as ONE object on the real stdout: indented on a terminal, one
    line otherwise. Whatever the readers print goes to stderr meanwhile."""
    with events.redirect_stdout() as out:
        state = status(refresh=refresh, timeout=timeout)
        pretty = False
        try:
            pretty = out.isatty()
        except (AttributeError, ValueError):
            pass
        out.write(json.dumps(state, indent=2 if pretty else None) + "\n")
