"""CLI subcommand handlers for `aroom memory`.

Follows the same dispatch pattern as ``mission_cli.py``. Integration layer
over :mod:`anteroom.services.memory_service` (CRUD from #1416) and
:mod:`anteroom.services.memory_promotion` (propose / approve / reject /
lineage from #920).
"""

from __future__ import annotations

import argparse
import logging
import sqlite3
import sys
from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

if TYPE_CHECKING:
    from ..config import AppConfig

logger = logging.getLogger(__name__)
console = Console()


def _run_memory(config: AppConfig, args: argparse.Namespace) -> None:
    """Top-level dispatcher for ``aroom memory`` subcommands."""
    action = getattr(args, "memory_action", None)
    if not action:
        console.print("Usage: aroom memory {list,show,create,edit,delete,propose,candidates,approve,reject}")
        return

    from ..db import get_db

    db = get_db(config.app.data_dir / "chat.db")

    if action == "list":
        _handle_list(db, args)
    elif action == "show":
        _handle_show(db, args)
    elif action == "create":
        _handle_create(db, args)
    elif action == "edit":
        _handle_edit(db, args)
    elif action == "delete":
        _handle_delete(db, args)
    elif action == "propose":
        _handle_propose(config, db, args)
    elif action == "candidates":
        _handle_candidates(db, args)
    elif action == "approve":
        _handle_approve(config, db, args)
    elif action == "reject":
        _handle_reject(config, db, args)
    else:
        console.print(f"Unknown memory action: {action}")


def _handle_list(db: Any, args: argparse.Namespace) -> None:
    """Render a Rich table of memories with optional filters."""
    from ..services import memory_service

    results = memory_service.list_memories(
        db,
        scope=getattr(args, "scope", None),
        category=getattr(args, "category", None),
        status=getattr(args, "status", None),
        namespace=getattr(args, "namespace", None),
    )

    if not results:
        console.print("[dim]No memories found.[/dim]")
        return

    table = Table(title="Memories", show_header=True)
    table.add_column("FQN", style="bold")
    table.add_column("Scope", justify="left")
    table.add_column("Category")
    table.add_column("Status")
    table.add_column("Created", style="dim")
    table.add_column("Provenance", style="dim")

    for mem in results:
        meta = mem.get("metadata") or {}
        prov = meta.get("provenance") or {}
        prov_hint = "-"
        for key in ("conversation_id", "message_id", "workflow_run_id", "source_artifact_id"):
            if prov.get(key):
                prov_hint = f"{key[:4]}:{prov[key][:8]}"
                break
        table.add_row(
            mem["fqn"],
            meta.get("memory_scope", "-"),
            meta.get("memory_category", "-"),
            meta.get("memory_status", "-"),
            (mem.get("created_at") or "")[:10],
            prov_hint,
        )
    console.print(table)


def _handle_show(db: Any, args: argparse.Namespace) -> None:
    """Render a single memory's full detail as a Rich panel."""
    from ..services import memory_service

    fqn = args.fqn
    mem = memory_service.get_memory(db, fqn)
    if mem is None:
        console.print(f"[red]Not found:[/red] {fqn}")
        sys.exit(1)

    meta = mem.get("metadata") or {}
    prov = meta.get("provenance") or {}
    prov_lines = "\n".join(f"  {k}: {v}" for k, v in prov.items() if v) or "  (none)"

    body = (
        f"[bold]Content:[/bold]\n{mem.get('content', '')}\n\n"
        f"[bold]Scope:[/bold] {meta.get('memory_scope', '-')}\n"
        f"[bold]Category:[/bold] {meta.get('memory_category', '-')}\n"
        f"[bold]Status:[/bold] {meta.get('memory_status', '-')}\n"
        f"[bold]Created by:[/bold] {meta.get('created_by', '-')}\n"
        f"[bold]Recall count:[/bold] {meta.get('recall_count', 0)}\n"
        f"[bold]Last recalled:[/bold] {meta.get('last_recalled_at') or '-'}\n"
        f"[bold]Promoted by:[/bold] {meta.get('promoted_by') or '-'}\n"
        f"[bold]Provenance:[/bold]\n{prov_lines}"
    )
    console.print(Panel(body, title=fqn, border_style="blue"))


def _handle_create(db: Any, args: argparse.Namespace) -> None:
    """Create a memory, taking content from --content or stdin if '-'."""
    from ..services import memory_service

    content = args.content
    if content == "-":
        content = sys.stdin.read().strip()
    if not content:
        console.print("[red]Error:[/red] content is empty")
        sys.exit(1)

    try:
        art = memory_service.create_memory(
            db,
            content=content,
            scope=args.scope,
            category=args.category,
            name=getattr(args, "name", None),
            project_slug=getattr(args, "project_slug", None),
            status=getattr(args, "status", "active") or "active",
        )
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    except sqlite3.IntegrityError:
        # Duplicate FQN — surface cleanly instead of a raw stack trace.
        console.print("[red]Error:[/red] A memory with that FQN already exists")
        sys.exit(1)

    console.print(f"[green]Created:[/green] {art['fqn']}")


def _handle_edit(db: Any, args: argparse.Namespace) -> None:
    """Edit content and/or a single metadata field."""
    from ..services import memory_service

    fqn = args.fqn
    content = getattr(args, "content", None)
    if content == "-":
        content = sys.stdin.read().strip()

    status = getattr(args, "status", None)
    category = getattr(args, "category", None)

    touched = False

    if content:
        updated = memory_service.update_memory_content(db, fqn, content)
        if updated is None:
            console.print(f"[red]Not found:[/red] {fqn}")
            sys.exit(1)
        touched = True

    metadata_updates: dict[str, Any] = {}
    if status:
        metadata_updates["memory_status"] = status
    if category:
        metadata_updates["memory_category"] = category

    if metadata_updates:
        try:
            updated = memory_service.update_memory_metadata(db, fqn, **metadata_updates)
        except ValueError as exc:
            console.print(f"[red]Error:[/red] {exc}")
            sys.exit(1)
        if updated is None:
            console.print(f"[red]Not found:[/red] {fqn}")
            sys.exit(1)
        touched = True

    if not touched:
        console.print("[red]Error:[/red] nothing to edit — supply --content, --status, or --category")
        sys.exit(1)

    console.print(f"[green]Updated:[/green] {fqn}")


def _handle_delete(db: Any, args: argparse.Namespace) -> None:
    """Delete a memory by FQN."""
    from ..services import memory_service

    fqn = args.fqn
    removed = memory_service.delete_memory(db, fqn)
    if not removed:
        console.print(f"[red]Not found:[/red] {fqn}")
        sys.exit(1)
    console.print(f"[green]Deleted:[/green] {fqn}")


# ---------------------------------------------------------------------------
# Promotion / review handlers (#920)
# ---------------------------------------------------------------------------


def _handle_propose(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Propose a new memory candidate."""
    from ..services import memory_promotion

    content = args.content
    if content == "-":
        content = sys.stdin.read().strip()
    if not content:
        console.print("[red]Error:[/red] content is empty")
        sys.exit(1)

    provenance: dict[str, Any] = {}
    if getattr(args, "conversation_id", None):
        provenance["conversation_id"] = args.conversation_id
    if getattr(args, "message_id", None):
        provenance["message_id"] = args.message_id

    try:
        mem = memory_promotion.propose_candidate(
            db,
            content=content,
            scope=args.scope,
            category=args.category,
            proposer=args.proposer,
            proposer_id=getattr(args, "proposer_id", None),
            provenance=provenance or None,
            project_slug=getattr(args, "project_slug", None),
            config=config.memory.promotion,
            name=getattr(args, "name", None),
        )
    except memory_promotion.PromotionAgentDisabledError as exc:
        console.print(f"[red]Blocked:[/red] {exc}")
        sys.exit(1)
    except memory_promotion.PromotionRateLimitError as exc:
        console.print(f"[red]Rate limit:[/red] {exc}")
        sys.exit(1)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    except sqlite3.IntegrityError:
        console.print("[red]Error:[/red] A memory with that FQN already exists")
        sys.exit(1)

    status = mem["metadata"]["memory_status"]
    console.print(f"[green]Proposed:[/green] {mem['fqn']} [dim]({status})[/dim]")


def _handle_candidates(db: Any, args: argparse.Namespace) -> None:
    """List memories in the review queue."""
    from ..services import memory_promotion

    try:
        results = memory_promotion.list_candidates(
            db,
            namespace=getattr(args, "namespace", None),
            status=getattr(args, "status", "candidate") or "candidate",
            limit=getattr(args, "limit", None),
        )
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if not results:
        console.print("[dim]No candidates.[/dim]")
        return

    table = Table(title="Memory candidates", show_header=True)
    table.add_column("FQN", style="bold")
    table.add_column("Category")
    table.add_column("Status")
    table.add_column("Proposer", style="dim")
    table.add_column("Proposed at", style="dim")

    for mem in results:
        meta = mem.get("metadata") or {}
        lineage = meta.get("lineage") or []
        first = lineage[0] if lineage else {}
        table.add_row(
            mem["fqn"],
            meta.get("memory_category", "-"),
            meta.get("memory_status", "-"),
            first.get("actor", meta.get("created_by", "-")),
            (first.get("at") or "")[:19],
        )
    console.print(table)


def _handle_approve(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Approve a candidate / pending-review memory."""
    from ..services import memory_promotion

    edits: dict[str, Any] = {}
    if getattr(args, "edit_content", None):
        edits["content"] = args.edit_content
    if getattr(args, "edit_category", None):
        edits["category"] = args.edit_category

    reviewer_id = getattr(getattr(config, "identity", None), "user_id", None) or "cli-reviewer"
    reviewer_display = getattr(getattr(config, "identity", None), "display_name", None)

    try:
        mem = memory_promotion.approve_candidate(
            db,
            args.fqn,
            reviewer_id=reviewer_id,
            reviewer_display=reviewer_display,
            edits=edits or None,
            config=config.memory.promotion,
        )
    except memory_promotion.PromotionStateError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    console.print(f"[green]Approved:[/green] {mem['fqn']} [dim]({mem['metadata']['memory_status']})[/dim]")


def _handle_reject(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Reject a candidate / pending-review memory with a bounded reason."""
    from ..services import memory_promotion

    reviewer_id = getattr(getattr(config, "identity", None), "user_id", None) or "cli-reviewer"
    reviewer_display = getattr(getattr(config, "identity", None), "display_name", None)

    try:
        mem = memory_promotion.reject_candidate(
            db,
            args.fqn,
            reviewer_id=reviewer_id,
            reviewer_display=reviewer_display,
            reason=args.reason,
            config=config.memory.promotion,
        )
    except memory_promotion.PromotionStateError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    console.print(f"[yellow]Rejected:[/yellow] {mem['fqn']} [dim](reason: {mem['metadata']['rejected_reason']})[/dim]")
