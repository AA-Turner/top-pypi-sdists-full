"""Secret discovery commands.

Read-only wrapper around the user-secrets API so agents can enumerate
candidate values for ``--secret`` on commands like ``dn evaluation create``
and ``dn runtime start``. Mutation (create/delete/rotate) lives in the TUI
secrets screen and the platform web app — keeping the CLI surface narrow
avoids exposing raw secret values via prompts.
"""

import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformArgs
from dreadnode.app.cli.shared import (
    _fmt_timestamp,
    _jsonable,
    _print_json,
    _project_row,
    console,
)

cli = cyclopts.App(
    name="secret",
    help="Discover user secrets (read-only).",
)


# ---------------------------------------------------------------------------
# Summary + projection
# ---------------------------------------------------------------------------


def _summarize_secret(p: dict[str, t.Any]) -> str:
    name = p.get("name") or "[dim]unnamed[/dim]"
    provider = p.get("provider")
    masked = p.get("masked_value") or ""
    parts = [
        f"[cyan]{name}[/cyan]",
        f"[dim]{provider}[/dim]" if provider else "",
        f"[dim]{masked}[/dim]" if masked else "",
    ]
    return "  ".join(part for part in parts if part)


_SECRET_LIST_ROW_FIELDS: tuple[str, ...] = (
    "provider",
    "masked_value",
    "created_at",
    "updated_at",
)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """List configured user secrets.

    Names returned here are the values accepted by ``--secret`` selectors.
    Glob selectors (``*``, ``?``) are matched best-effort by the API; exact
    names are strict. Manage secret values via the TUI secrets screen or
    the platform web app.

    Args:
        as_json: Output as JSON (list-row projection).
    """
    api, _profile = platform.connect()
    response = api.list_secrets()

    raw_secrets = (
        response.get("secrets", [])
        if isinstance(response, dict)
        else getattr(response, "secrets", [])
    )
    items: list[dict[str, t.Any]] = [
        s if isinstance(s, dict) else _jsonable(s) for s in raw_secrets
    ]

    if as_json:
        rows = [_project_row(item, _SECRET_LIST_ROW_FIELDS) for item in items]
        _print_json(rows)
        return

    if not items:
        console.print("[dim]No secrets configured[/dim]")
        return

    for item in items:
        line = _summarize_secret(item)
        updated = item.get("updated_at") or item.get("created_at")
        if updated:
            line = f"{line}  [dim]{_fmt_timestamp(updated)}[/dim]"
        console.print(line)
