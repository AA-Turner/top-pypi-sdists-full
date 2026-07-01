"""
cvc.cli_skills — `cvc skills ...` subcommand group.

Provides lifecycle management for the skill substrate (Phase B, item 3.8):

    cvc skills list                 # active skills
    cvc skills list --archived      # also show archived
    cvc skills show <name>          # print SKILL.md
    cvc skills stats <name>         # show usage counters
    cvc skills archive <name>       # mark archived (hides from agent)
    cvc skills restore <name>       # un-archive
    cvc skills pin <name>           # protect from deletion
    cvc skills unpin <name>
    cvc skills list-archived

All operations route to the native CVC ``cvc.skills.usage`` substrate so
state matches what the agent loop observes at runtime.
"""

from __future__ import annotations

# Force vendored upstream to write under ~/.cvc/skills (mirrors hermes_bridge boot).
import os
from pathlib import Path

import click

os.environ.setdefault("HERMES_HOME", os.path.expanduser("~/.cvc"))


def _render_table(title: str, rows: list[tuple[str, ...]], headers: tuple[str, ...]) -> None:
    from rich import box
    from rich.console import Console
    from rich.table import Table
    console = Console()
    tbl = Table(title=title, box=box.ROUNDED, border_style="cyan")
    for h in headers:
        tbl.add_column(h, style="white")
    for r in rows:
        tbl.add_row(*[str(c) for c in r])
    console.print(tbl)


@click.group("skills")
def skills_group() -> None:
    """Manage CVC's skill substrate — list, archive, restore, pin."""
    pass


# Phase C (items 3.11+3.12): `cvc skills hub ...` subcommand for discovering,
# scanning, and installing skills from remote registries (GitHub + well-known + URL).
try:
    from cvc.cli_skills_hub import hub_group as _hub_group
    skills_group.add_command(_hub_group)
except Exception:
    # Hub is best-effort; never block `cvc skills list` if the import fails.
    pass


@skills_group.command("list")
@click.option("--archived", is_flag=True, help="Include archived skills.")
def skills_list(archived: bool) -> None:
    """List discoverable skills (active by default)."""
    from cvc.agent.skills import discover_skills
    from cvc.skills.usage import load_usage

    workspace = Path.cwd()
    skills = discover_skills(workspace, include_archived=archived)
    usage = load_usage()

    rows = []
    for s in sorted(skills, key=lambda x: x.name):
        rec = usage.get(s.name, {}) if isinstance(usage, dict) else {}
        state = rec.get("state", "active") if isinstance(rec, dict) else "active"
        pinned = "📌" if isinstance(rec, dict) and rec.get("pinned") else ""
        views = rec.get("view_count", 0) if isinstance(rec, dict) else 0
        uses = rec.get("use_count", 0) if isinstance(rec, dict) else 0
        rows.append((s.name, state, pinned, views, uses, s.description[:40]))

    if not rows:
        click.echo("No skills found.")
        return
    _render_table(
        f"Skills ({'all' if archived else 'active'}) — {len(rows)} total",
        rows,
        ("Name", "State", "Pin", "Views", "Uses", "Description"),
    )


@skills_group.command("show")
@click.argument("name")
def skills_show(name: str) -> None:
    """Print a skill's SKILL.md content."""
    from cvc.agent.skills import discover_skills

    skills = discover_skills(Path.cwd(), include_archived=True)
    target = next((s for s in skills if s.name == name), None)
    if not target:
        raise click.ClickException(f"Skill not found: {name}")
    click.echo(f"# {target.name}\n")
    if target.description:
        click.echo(f"_{target.description}_\n")
    if target.path:
        click.echo(f"_path: {target.path}_\n")
    click.echo(target.content)


@skills_group.command("stats")
@click.argument("name")
def skills_stats(name: str) -> None:
    """Show usage counters for a skill."""
    from cvc.skills.usage import get_record

    rec = get_record(name)
    if not rec:
        click.echo(f"No usage record for '{name}'.")
        return
    from rich import box
    from rich.console import Console
    from rich.table import Table
    console = Console()
    tbl = Table(title=f"Usage: {name}", box=box.ROUNDED, border_style="cyan")
    tbl.add_column("Field", style="dim")
    tbl.add_column("Value", style="white")
    for k in (
        "state", "pinned", "view_count", "use_count", "patch_count",
        "last_viewed_at", "last_used_at", "last_patched_at",
        "created_at", "archived_at", "agent_created",
    ):
        if k in rec:
            tbl.add_row(k, str(rec.get(k)))
    console.print(tbl)


@skills_group.command("archive")
@click.argument("name")
def skills_archive(name: str) -> None:
    """Mark a skill as archived — hidden from the active set."""
    from cvc.skills.usage import archive_skill
    ok, msg = archive_skill(name)
    if ok:
        click.echo(f"✅ Archived: {name}  ({msg})")
    else:
        raise click.ClickException(f"archive failed: {msg}")


@skills_group.command("restore")
@click.argument("name")
def skills_restore(name: str) -> None:
    """Restore an archived skill back to active."""
    from cvc.skills.usage import restore_skill
    ok, msg = restore_skill(name)
    if ok:
        click.echo(f"✅ Restored: {name}  ({msg})")
    else:
        raise click.ClickException(f"restore failed: {msg}")


@skills_group.command("pin")
@click.argument("name")
def skills_pin(name: str) -> None:
    """Pin a skill — protects it from accidental deletion."""
    from cvc.skills.usage import set_pinned
    set_pinned(name, True)
    click.echo(f"📌 Pinned: {name}")


@skills_group.command("unpin")
@click.argument("name")
def skills_unpin(name: str) -> None:
    """Remove pin from a skill."""
    from cvc.skills.usage import set_pinned
    set_pinned(name, False)
    click.echo(f"Unpinned: {name}")


@skills_group.command("list-archived")
def skills_list_archived() -> None:
    """List skill names currently archived."""
    from cvc.skills.usage import list_archived_skill_names
    names = list_archived_skill_names()
    if not names:
        click.echo("No archived skills.")
        return
    for n in sorted(names):
        click.echo(n)


@skills_group.command("set-state")
@click.argument("name")
@click.argument("state", type=click.Choice(["active", "stale", "archived"]))
def skills_set_state(name: str, state: str) -> None:
    """Explicitly set a skill's lifecycle state."""
    from cvc.skills.usage import set_state
    set_state(name, state)
    click.echo(f"State '{name}' → {state}")


@skills_group.command("insights")
@click.option("--json", "as_json", is_flag=True, help="Emit JSON instead of the text table.")
@click.option(
    "--limit", default=8, show_default=True,
    help="Max rows per bucket in the text table.",
)
@click.option(
    "--no-actions", is_flag=True,
    help="Hide the RECOMMENDED ACTIONS section.",
)
@click.option(
    "--apply-archives", "apply_archives", is_flag=True,
    help="Actually archive every dead skill (skips pinned + bundled).",
)
def skills_insights(
    as_json: bool, limit: int, no_actions: bool, apply_archives: bool,
) -> None:
    """Show aggregate usage insights for the skill substrate.

    Reads the ``.usage.json`` sidecar and renders a bucketed summary
    of which skills are *hot*, *fading*, *dead* (shown to the agent but
    never used — wasted context), and *fresh*. The dashboard reads the
    same report via ``GET /api/skills/insights``.

    With ``--apply-archives`` the CLI will actually archive every skill
    that the report classifies as "dead" — except pinned or bundled
    ones, which require an explicit ``cvc skills unpin <name>`` first.
    This is the closest thing to "one-click cleanup" the insights
    command offers, and it always prints the dry-run preview first so
    you can Ctrl-C if the list surprises you.
    """
    from rich.console import Console

    from cvc.skills.insights import compute_insights, render_cli_summary, to_jsonable
    from cvc.skills.usage import archive_skill, load_usage

    usage = load_usage()
    report = compute_insights(usage)

    if as_json:
        import json as _json
        click.echo(_json.dumps(to_jsonable(report), indent=2, sort_keys=True))
        return

    console = Console()
    text = render_cli_summary(
        report, max_per_bucket=limit, include_actions=not no_actions,
    )
    console.print(text, highlight=False)

    if apply_archives:
        from cvc.skills.insights import recommend_actions
        actions = recommend_actions(report, max_actions=999)
        archives = [a for a in actions if a.kind == "archive"]
        if not archives:
            click.echo("\nNo archivable dead skills found.")
            return
        click.echo(f"\nApplying {len(archives)} archive action(s)...")
        ok = 0
        skipped = 0
        for a in archives:
            success, message = archive_skill(a.skill_name)
            if success:
                ok += 1
                click.echo(f"  archived {a.skill_name}")
            else:
                # archive_skill refuses bundled or hub skills — that is
                # the safety net catching us before we damage something.
                skipped += 1
                click.echo(f"  skipped {a.skill_name}: {message}")
        click.echo(f"\nDone. archived={ok} skipped={skipped}")
        click.echo(
            "Re-run `cvc skills insights` to see the post-cleanup report."
        )


# ── Auto-skill drafts subcommand ─────────────────────────────────────
#
# Surfaced as `cvc skills drafts list/show/approve/reject` so users
# can manage auto-generated drafts without the dashboard running.
# Mirrors the /api/skills/drafts endpoints for the same data.


@skills_group.group("drafts")
def drafts_group() -> None:
    """Manage auto-generated skill drafts (created by post-turn reflection)."""
    pass


@drafts_group.command("list")
@click.option("--state", default="draft",
              type=click.Choice(["draft", "approved", "rejected"]),
              help="Filter by state (default: pending drafts).")
def drafts_list(state: str) -> None:
    """List auto-generated skill drafts awaiting review."""
    from rich.console import Console
    from rich.table import Table
    from cvc.skills.drafts import list_drafts as _list_drafts

    records = _list_drafts(state=state)
    if not records:
        click.echo(f"No {state} drafts. (Auto-skill runs after every turn; "
                   "a draft is created when the turn produced a reusable "
                   "pattern with confidence ≥ 0.6.)")
        return

    console = Console()
    tbl = Table(title=f"Skill drafts ({state}) — {len(records)}", box=None)
    tbl.add_column("Name", style="cyan", no_wrap=True)
    tbl.add_column("Confidence", justify="right")
    tbl.add_column("Source turn", style="dim")
    tbl.add_column("Tools used", style="dim")
    for r in records:
        tbl.add_row(
            r.name,
            f"{r.confidence:.2f}",
            r.source_turn_id or r.source_session_id,
            ", ".join(sorted(set(r.tool_sequence))[:5]) + (
                " …" if len(set(r.tool_sequence)) > 5 else ""),
        )
    console.print(tbl)
    click.echo("\nReview with: cvc skills drafts show <name>")
    click.echo("Promote:     cvc skills drafts approve <name>")
    click.echo("Discard:     cvc skills drafts reject <name>")


@drafts_group.command("show")
@click.argument("name")
def drafts_show(name: str) -> None:
    """Print a draft SKILL.md for review."""
    from cvc.skills.drafts import DRAFTS_DIR, _read_description
    md = DRAFTS_DIR / name / "SKILL.md"
    if not md.exists():
        archived = DRAFTS_DIR / ".archive" / name / "SKILL.md"
        if archived.exists():
            md = archived
        else:
            raise click.ClickException(f"No draft named {name!r}")
    click.echo(md.read_text(encoding="utf-8"))


@drafts_group.command("approve")
@click.argument("name")
@click.option("--category", default=None,
              help="Override inferred category (e.g. 'software-development').")
def drafts_approve(name: str, category: str | None) -> None:
    """Promote a draft to the active skill tree."""
    from cvc.skills.drafts import approve_draft as _approve
    try:
        dest = _approve(name, category=category)
    except FileNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo(f"Promoted {name!r} → {dest}")
    click.echo("It will appear in `cvc skills list` on the next session.")


@drafts_group.command("reject")
@click.argument("name")
@click.option("--reason", default=None, help="Why you're rejecting (audit only).")
def drafts_reject(name: str, reason: str | None) -> None:
    """Reject a draft and archive it."""
    from cvc.skills.drafts import reject_draft as _reject
    try:
        _reject(name, reason=reason)
    except FileNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo(f"Rejected {name!r} (moved to .archive/).")
