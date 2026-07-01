"""Session subcommands — browse, inspect, and export agent session trajectories."""

import json
import typing as t
from pathlib import Path
from uuid import UUID

import cyclopts
from rich.text import Text

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_SEARCH,
    _collect_pages,
    _fmt_id,
    _fmt_timestamp,
    _hint,
    _label,
    _print_json,
    _project_row,
    _relative_time,
    _short_id,
    confirm_destructive,
    console,
    print_link,
    print_success,
)

cli = cyclopts.App(
    name="session",
    help=(
        "Browse, inspect, and export agent session trajectories — the "
        "record of what an agent did during a run."
    ),
)

TrajectoryFormat = t.Literal["atif", "openai", "native"]
SessionOrigin = t.Literal["user", "eval", "worker"]

_SESSION_LIST_ROW_FIELDS: tuple[str, ...] = (
    "id",
    "title",
    "model",
    "agent",
    "origin",
    "visibility",
    "message_count",
    "usage",
    "project_name",
    "labels",
    "archived_at",
    "frozen_at",
    "last_message_at",
    "updated_at",
)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def _fmt_compact(value: int | None) -> str:
    """Compact integer rendering — ``1.2k``, ``3.4M``. Mirrors TUI/web."""
    if not value:
        return "0"
    n = int(value)
    if n < 1_000:
        return str(n)
    if n < 1_000_000:
        return f"{n / 1_000:.1f}k".replace(".0k", "k")
    return f"{n / 1_000_000:.1f}M".replace(".0M", "M")


def _origin_token(origin: str | None) -> str:
    """Render origin as a parenthesized token; empty for the default ``user``."""
    if not origin or origin == "user":
        return ""
    return f"[dim]({origin})[/dim]"


def _status_tokens(payload: dict[str, t.Any]) -> list[str]:
    """Lifecycle status tokens that match the TUI's inline title decorations.

    Returns an ordered list of rich-formatted tokens (or an empty list when
    the session is in the unmarked baseline state — active, private, unfrozen,
    user-origin).
    """
    tokens: list[str] = []
    origin = payload.get("origin")
    if origin and origin != "user":
        tokens.append(f"[dim]({origin})[/dim]")
    if payload.get("frozen_at"):
        tokens.append("[yellow]frozen[/yellow]")
    if payload.get("archived_at"):
        tokens.append("[dim]archived[/dim]")
    if payload.get("visibility") == "workspace":
        tokens.append("[dim]shared[/dim]")
    return tokens


def _format_labels(labels: dict[str, list[str]] | None, *, max_pairs: int = 3) -> str:
    """Render labels as ``key=value`` chips, truncated past ``max_pairs``."""
    if not labels:
        return ""
    pairs: list[str] = []
    for key, values in sorted(labels.items()):
        for v in values:
            pairs.append(f"[cyan]{key}[/cyan]=[dim]{v}[/dim]")
    if len(pairs) > max_pairs:
        rest = len(pairs) - max_pairs
        return "  ".join(pairs[:max_pairs]) + f"  [dim]+{rest}[/dim]"
    return "  ".join(pairs)


def _format_tokens(usage: dict[str, t.Any] | None) -> str:
    """Render token usage as ``↑in · ↓out`` (matches web SessionHeader)."""
    if not usage:
        return ""
    in_tok = usage.get("total_input_tokens") or 0
    out_tok = usage.get("total_output_tokens") or 0
    if not in_tok and not out_tok:
        return ""
    return f"[dim]↑[/dim]{_fmt_compact(in_tok)} [dim]↓[/dim]{_fmt_compact(out_tok)}"


def _format_cost(usage: dict[str, t.Any] | None) -> str:
    """Render cost in USD. Blank when unknown or zero (no inference happened)."""
    if not usage:
        return ""
    cost = usage.get("total_cost_usd")
    if not cost:
        return ""
    return f"${cost:.2f}"


def _print_session_link(profile: t.Any, session_id: str) -> None:
    org = getattr(profile, "org_key", None)
    ws = getattr(profile, "workspace_key", None)
    if not org or not ws:
        return
    print_link(profile.url, f"{org}/analysis", workspace=ws, session=session_id)


def _resolve_project_id(api: t.Any, profile: t.Any, project: str | None) -> str | None:
    """Resolve ``project`` (slug or UUID) to a UUID string, or ``None``.

    Looks at the explicit ``project`` argument first, then falls back to the
    profile's active project key. Slugs are resolved via the projects API.
    UUID-shaped strings are returned as-is so scripts that already have an
    id don't pay for a lookup.
    """
    candidate = project or getattr(profile, "project_key", None)
    if not candidate:
        return None
    try:
        UUID(str(candidate))
    except ValueError:
        pass
    else:
        return str(candidate)
    resolved = api.get_project(profile.org_key, profile.workspace_key, str(candidate))
    return str(resolved.id)


_ROW_INDENT = "          "  # matches "{8-char id}  " on the head line


def _truncate(text: str, max_len: int) -> str:
    """Right-truncate to ``max_len`` characters with an ellipsis."""
    if max_len <= 0 or len(text) <= max_len:
        return text
    return text[: max(1, max_len - 1)] + "…"


def _append_separator(text: Text) -> None:
    text.append(" · ", style="dim")


def _render_session_block(item: dict[str, t.Any], *, width: int) -> list[Text]:
    """Render one session as a two-line block.

    The list is the scanner; ``dn session get`` is the detail view. Anything
    that doesn't help the eye pick a session out of a crowd belongs in
    ``get``, not here. The two lines we render are:

    - Head: short id, title (or first-message preview when title is missing),
      lifecycle status badges, and a right-aligned relative timestamp.
    - Secondary: agent · model · msg count · tool calls · token total · cost.
      Tool calls and tokens are omitted on sessions that haven't run inference.
      Project, labels, compaction count, and the input/output split live in
      ``get``.

    Visual hierarchy:

    - **Bold** is the title only — the focal point.
    - *Italic* (no bold) marks a derived preview that's standing in for an
      explicit title, so the user can tell at a glance which sessions have
      been deliberately named.
    - Color carries meaning: agent is cyan (matches ``dn evaluation`` and
      ``dn capability``), cost is green when non-zero, ``frozen`` is yellow.
    - Dim is reserved for things that should fade: short id, separators,
      units (``msgs``), the right-aligned relative time, the placeholder.
    """
    short = _short_id(str(item.get("id", "")))
    raw_title = item.get("title")
    preview = item.get("preview_text")
    status_tokens = _status_tokens(item)

    # ---- Line 1: head row (id + title + status, right-pad with updated)
    updated = item.get("last_message_at") or item.get("updated_at")
    updated_text = _relative_time(updated) if updated else "-"
    right = Text(updated_text, style="dim")

    # Reserve space on the head row for: id+gap (10), status badges (each
    # token + 2-char gap), updated timestamp + at least 2 cols of breathing
    # room before it. Whatever is left is the title's budget.
    badges_width = sum(Text.from_markup(tok).cell_len + 2 for tok in status_tokens)
    title_budget = max(20, width - 10 - badges_width - right.cell_len - 2)

    head = Text()
    head.append(short, style="dim")
    head.append("  ")
    if raw_title:
        head.append(_truncate(raw_title, title_budget), style="bold")
    elif preview:
        # First-user-message snippet — italic so it reads as a derived stand-in
        # for the title rather than the explicit one the user (or model) set.
        snippet = " ".join(str(preview).split())  # collapse whitespace/newlines
        head.append(_truncate(snippet, title_budget), style="italic")
    else:
        head.append("(no messages yet)", style="dim italic")
    for tok in status_tokens:
        head.append("  ")
        head.append_text(Text.from_markup(tok))

    pad_width = max(1, width - head.cell_len - right.cell_len)
    head.append(" " * pad_width)
    head.append_text(right)

    # ---- Line 2: secondary metadata. Default foreground for content,
    # dim only for separators and unit suffixes.
    secondary = Text(_ROW_INDENT)
    has_part = False
    if agent := item.get("agent"):
        secondary.append(_truncate(str(agent), 20), style="cyan")
        has_part = True
    if model := item.get("model"):
        if has_part:
            _append_separator(secondary)
        secondary.append(_truncate(str(model), 22))
        has_part = True

    if has_part:
        _append_separator(secondary)
    msg_count = int(item.get("message_count", 0) or 0)
    secondary.append(str(msg_count))
    secondary.append(" msg" if msg_count == 1 else " msgs", style="dim")

    usage = item.get("usage") or {}
    tool_calls = usage.get("total_tool_call_count") or 0
    if tool_calls:
        _append_separator(secondary)
        secondary.append(str(tool_calls))
        secondary.append(" tool" if tool_calls == 1 else " tools", style="dim")

    total_tokens = (usage.get("total_input_tokens") or 0) + (usage.get("total_output_tokens") or 0)
    if total_tokens:
        _append_separator(secondary)
        secondary.append(_fmt_compact(total_tokens))
        secondary.append(" tokens", style="dim")

    cost = usage.get("total_cost_usd")
    if cost:
        _append_separator(secondary)
        secondary.append(f"${cost:.2f}", style="green")

    return [head, secondary]


def _render_session_list(items: list[dict[str, t.Any]], *, width: int) -> None:
    """Print sessions as 2-3 line blocks separated by a blank line."""
    for i, item in enumerate(items):
        if i:
            console.print()
        for line in _render_session_block(item, width=width):
            console.print(line)


# ---------------------------------------------------------------------------
# list / ls
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    search: t.Annotated[str | None, cyclopts.Parameter(name=_FLAG_SEARCH)] = None,
    origin: t.Annotated[
        list[SessionOrigin] | None,
        cyclopts.Parameter(name="--origin", negative_iterable=()),
    ] = None,
    label: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(name="--label", negative_iterable=()),
    ] = None,
    include_archived: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show sessions in your workspace.

    Args:
        search: Free-text match across title, model, agent, and label values.
        origin: Filter by session origin (``user``, ``eval``, ``worker``).
            Repeatable.
        label: ``key:value`` filter, repeatable. Same key combines with OR;
            different keys combine with AND.
        include_archived: Include archived sessions. Default hides them.
        limit: Maximum results to show.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    project_id = _resolve_project_id(api, profile, None)
    items = _collect_pages(
        lambda page, page_size: api.list_sessions(
            profile.org_key,
            profile.workspace_key,
            page=page,
            limit=page_size,
            search=search,
            project_id=project_id,
            origin=list(origin) if origin else None,
            label=label,
            archived="any" if include_archived else "active",
        ),
        limit=limit,
        page_size=50,
        items_key="sessions",
    )

    if as_json:
        rows = [_project_row(item, _SESSION_LIST_ROW_FIELDS) for item in items]
        _print_json(rows)
        return

    if not items:
        console.print("[dim]No sessions found[/dim]")
        return

    _render_session_list(items, width=console.width)


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


@cli.command()
def get(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show session metadata, identity, and rollup usage in a single panel.

    For the actual trajectory data (messages, tool calls, observations) use
    ``dn session export``.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.get_session(profile.org_key, profile.workspace_key, session_id)

    detail = payload.get("session", payload)

    if as_json:
        _print_json(detail)
        return

    sid = str(detail.get("id", "-"))
    raw_title = detail.get("title")
    title_line = f"[bold]{raw_title}[/bold]" if raw_title else "[dim](untitled)[/dim]"
    tokens = _status_tokens(detail)
    if tokens:
        title_line = f"{title_line}  {'  '.join(tokens)}"
    console.print(title_line)
    console.print(f"{_label('ID')}{_fmt_id(sid)}")

    if model := detail.get("model"):
        console.print(f"{_label('Model')}{model}")
    if agent := detail.get("agent"):
        console.print(f"{_label('Agent')}[cyan]{agent}[/cyan]")
    if project := detail.get("project_name"):
        console.print(f"{_label('Project')}{project}")

    creator = detail.get("created_by") or {}
    if email := creator.get("email"):
        console.print(f"{_label('Created by')}[dim]{email}[/dim]")

    console.print()
    console.print(f"{_label('Created')}[dim]{_fmt_timestamp(detail.get('created_at'))}[/dim]")
    if last := detail.get("last_message_at"):
        console.print(f"{_label('Updated')}[dim]{_fmt_timestamp(last)}[/dim]")
    if archived_at := detail.get("archived_at"):
        console.print(f"{_label('Archived')}[dim]{_fmt_timestamp(archived_at)}[/dim]")
    if frozen_at := detail.get("frozen_at"):
        frozen_by = detail.get("frozen_by") or "unknown"
        console.print(
            f"{_label('Frozen')}[yellow]{_fmt_timestamp(frozen_at)}[/yellow]"
            f"  [dim]by {frozen_by}[/dim]"
        )

    usage = detail.get("usage") or {}
    msgs = detail.get("message_count", 0)
    tool_calls = usage.get("total_tool_call_count") or 0
    msg_line = f"{msgs} msgs"
    if tool_calls:
        msg_line += f"  [dim]· {tool_calls} tool calls[/dim]"
    console.print()
    console.print(f"{_label('Messages')}{msg_line}")

    tokens_part = _format_tokens(usage)
    if tokens_part:
        console.print(f"{_label('Tokens')}{tokens_part}")

    cost_part = _format_cost(usage)
    if cost_part:
        console.print(f"{_label('Cost')}{cost_part}")

    compactions = usage.get("compaction_count") or 0
    if compactions:
        console.print(f"{_label('Compacted')}[dim]×{compactions}[/dim]")  # noqa: RUF001

    if labels := detail.get("labels"):
        console.print(f"{_label('Labels')}{_format_labels(labels, max_pairs=10)}")

    console.print()
    _hint(f"dn session export {sid}")
    _print_session_link(profile, sid)


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------


@cli.command()
def export(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    format: TrajectoryFormat = "atif",
    output: t.Annotated[
        Path | None,
        cyclopts.Parameter(name="--output", alias="-o", allow_leading_hyphen=True),
    ] = None,
    include_compacted: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Export the session's trajectory in a portable format.

    By default writes an ATIF v1.7 JSON document to
    ``./session-<id>.<format>.json``. Pass ``--format openai`` for a Chat
    Completions ``messages`` array, ``--format native`` for a
    Dreadnode-native bundle that includes session metadata, transcript
    messages, and ClickHouse events, ``--output -`` (or ``--json``) to
    stream to stdout.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        format: Export format. ``atif`` (default), ``openai``, or ``native``.
        output: Output path. ``-`` writes to stdout.
        include_compacted: Include compacted history. Default excludes it.
        as_json: Stream the result to stdout as JSON.
    """
    api, profile = platform.connect()
    payload = api.get_session_trajectory(
        profile.org_key,
        profile.workspace_key,
        session_id,
        format=format,
        include_compacted=include_compacted,
    )

    if as_json or (output is not None and str(output) == "-"):
        _print_json(payload)
        return

    target = output or Path(f"session-{session_id}.{format}.json")
    target.write_text(json.dumps(payload, indent=2, default=str))
    console.print(f"  Exported to [bold]{target}[/bold]  [dim]({format})[/dim]")


# ---------------------------------------------------------------------------
# archive / unarchive / freeze / share / rename
# ---------------------------------------------------------------------------


@cli.command()
def archive(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Archive a session. Idempotent — re-archiving is a no-op.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.archive_session(profile.org_key, profile.workspace_key, session_id)
    if as_json:
        _print_json(payload)
        return
    console.print(f"  {_short_id(str(payload.get('id', session_id)))}  [yellow]archived[/yellow]")


@cli.command()
def unarchive(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Restore an archived session. Idempotent.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.unarchive_session(profile.org_key, profile.workspace_key, session_id)
    if as_json:
        _print_json(payload)
        return
    console.print(f"  {_short_id(str(payload.get('id', session_id)))}  [green]unarchived[/green]")


@cli.command()
def freeze(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Freeze a session. No new messages can be appended; there is no thaw.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        yes: Skip the confirmation prompt.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    short = _short_id(session_id)
    if not confirm_destructive(
        f"Freeze session [cyan]{short}[/cyan]? Freezing is permanent — no new "
        "messages can be appended and there is no way to thaw it.",
        yes=yes,
    ):
        console.print("[dim]Aborted[/dim]")
        return
    payload = api.freeze_session(profile.org_key, profile.workspace_key, session_id)
    if as_json:
        _print_json(payload)
        return
    console.print(f"  {short}  [yellow]frozen[/yellow]")


@cli.command()
def share(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Share a private session with the workspace. Cannot be undone.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        yes: Skip the confirmation prompt.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    short = _short_id(session_id)
    if not confirm_destructive(
        f"Share session [cyan]{short}[/cyan] with the workspace? Everyone in "
        "the workspace will be able to see this session and its transcript. "
        "This cannot be undone.",
        yes=yes,
    ):
        console.print("[dim]Aborted[/dim]")
        return
    payload = api.update_session(
        profile.org_key, profile.workspace_key, session_id, visibility="workspace"
    )
    if as_json:
        _print_json(payload)
        return
    console.print(f"  {short}  [green]shared[/green]")


@cli.command()
def rename(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    title: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Rename a session.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        title: New session title (max 255 chars).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.update_session(profile.org_key, profile.workspace_key, session_id, title=title)
    if as_json:
        _print_json(payload)
        return
    print_success(f"Renamed to “{title}”")


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


@cli.command(alias="rm")
def delete(
    session_id: t.Annotated[str, cyclopts.Parameter(name="session-id")],
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Permanently delete a session and its transcript.

    Sessions referenced by evaluations cannot be deleted.

    Args:
        session_id: Session UUID, or a unique prefix (e.g. the 8-char id shown by `dn session list`).
        yes: Skip the confirmation prompt.
    """
    from dreadnode.app.api.client import ConflictError, NotFoundError

    api, profile = platform.connect()
    short = _short_id(session_id)

    try:
        payload = api.get_session(profile.org_key, profile.workspace_key, session_id)
    except NotFoundError as exc:
        raise NotFoundError(f"Session {short} not found.") from exc
    detail = payload.get("session", payload)

    title = (detail or {}).get("title") if detail else None
    label = f"“{title}”" if title else f"[cyan]{short}[/cyan]"
    if not confirm_destructive(
        f"Delete session {label}? This is permanent and removes the transcript.",
        yes=yes,
    ):
        console.print("[dim]Aborted[/dim]")
        return
    try:
        api.delete_session(profile.org_key, profile.workspace_key, session_id)
    except ConflictError as exc:
        raise ConflictError("Cannot delete a session referenced by an evaluation.") from exc
    console.print(f"  {short}  [red]deleted[/red]")
