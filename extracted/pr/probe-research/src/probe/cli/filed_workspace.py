"""The stderr line that names the workspace a project was just created in.

`probe project create` and the folder import print `Filed in workspace <name>
(<slug>)` so the agent that made the project can check it landed where the
researcher meant (a project that went to a teammate's workspace, twice, is why).
stderr, like `_print_link`: stdout stays the JSON scripts parse. Naming it costs
one `GET /v1/workspaces/{id}` per workspace per client, bounded to a few seconds
so a hung API cannot hold back the create's output; when that read fails the line
names the id instead, and nothing here ever fails the create.
"""

from __future__ import annotations

import sys
import time
import weakref

from ..sdk.delivery.transport.deadlines import deadline_scope

#: The most the name read may add to a create that already succeeded.
LOOKUP_SECONDS = 5.0

#: Per client: workspace id -> its line. A client that cannot be weakly
#: referenced (a test double with slots) just reads again.
_LINES: "weakref.WeakKeyDictionary[object, dict[str, str]]" = weakref.WeakKeyDictionary()


def _printable(text: str) -> str:
    """A team member's workspace name, safe on a terminal (no escapes, no bidi)."""
    return "".join(ch if ch.isprintable() else "?" for ch in text)


def filed_line(client, project) -> str | None:
    """The line for `project` (the create's answer), or None when it names no workspace."""
    workspace_id = project.get("workspace_id") if isinstance(project, dict) else None
    if not workspace_id:
        return None
    workspace_id = str(workspace_id)
    try:
        lines = _LINES.setdefault(client, {})
    except TypeError:
        lines = {}
    if workspace_id not in lines:
        line = f"Filed in workspace {workspace_id}"
        try:
            with deadline_scope(time.monotonic() + LOOKUP_SECONDS):
                row = client.get_workspace(workspace_id)
            name, slug = row.get("name"), row.get("slug")
            if isinstance(name, str) and name and isinstance(slug, str) and slug:
                line = f"Filed in workspace {_printable(name)} ({_printable(slug)})"
        except Exception:  # noqa: BLE001 - naming the workspace never fails the create
            pass
        lines[workspace_id] = line
    return lines[workspace_id]


def say_filed(client, project) -> None:
    """Print `filed_line` to stderr, if there is one. A closed or missing stderr
    (a detached job, a broken pipe) loses the line, never the create."""
    line = filed_line(client, project)
    stream = sys.stderr
    if line and stream is not None:
        try:
            print(line, file=stream)
        except (OSError, ValueError):  # ValueError: a closed stream
            pass
