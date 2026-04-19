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
    elif action == "pin":
        _handle_pin(db, args)
    elif action == "unpin":
        _handle_unpin(db, args)
    elif action == "retention":
        _handle_retention(config, db, args)
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
    """Propose a new memory candidate.

    Emits ``memory.proposed`` via the lineage layer so proposals are
    captured in the tamper-evident chain alongside approve/reject
    (#925).
    """
    from ..services import lineage, memory_promotion
    from ._audit_helper import get_cli_audit_writer

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

    proposer_id = (
        getattr(args, "proposer_id", None)
        or getattr(getattr(config, "identity", None), "user_id", None)
        or "cli-proposer"
    )
    lineage.emit_memory_promotion(
        get_cli_audit_writer(config),
        "proposed",
        fqn=mem["fqn"],
        reviewer_id=proposer_id,
        details={"proposer": args.proposer},
    )
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
    """Approve a candidate / pending-review memory.

    Routes through the local server's HTTP endpoint when reachable so the
    server's chain-safe audit writer is the sole writer for this durable
    action. Falls back to the local chain-safe writer only when the OS
    attests absence of the loopback server (#925 v7).
    """
    from ..services import lineage, memory_promotion
    from ._audit_helper import get_cli_audit_writer
    from ._decision_routing import (
        ServerHttpError,
        ServerNotRunningError,
        call_decision_endpoint,
    )

    edits: dict[str, Any] = {}
    if getattr(args, "edit_content", None):
        edits["content"] = args.edit_content
    if getattr(args, "edit_category", None):
        edits["category"] = args.edit_category

    reviewer_id = getattr(getattr(config, "identity", None), "user_id", None) or "cli-reviewer"
    reviewer_display = getattr(getattr(config, "identity", None), "display_name", None)

    body: dict[str, Any] = {}
    if reviewer_display is not None:
        body["reviewer_display"] = reviewer_display
    if edits:
        body["edits"] = edits

    try:
        mem = call_decision_endpoint(
            config,
            "POST",
            f"/api/memory/{args.fqn}/approve",
            json_body=body or None,
        )
        console.print(
            f"[green]Approved via server:[/green] {mem['fqn']} [dim]({mem['metadata']['memory_status']})[/dim]"
        )
        return
    except ServerNotRunningError:
        pass  # Fall through to local chain-safe path below.
    except ServerHttpError as exc:
        console.print(f"[red]Server error — declining to write audit locally.[/red] {exc}")
        sys.exit(2)

    # Local fallback: loopback + kernel-attested absence. Use a chain-safe
    # writer so the log resumes the prior chain via _load_last_hmac.
    audit_writer = get_cli_audit_writer(config)
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

    lineage.emit_memory_promotion(
        audit_writer,
        "approved",
        fqn=mem["fqn"],
        reviewer_id=reviewer_id,
        details={"edits_applied": bool(edits)},
    )
    console.print(f"[green]Approved:[/green] {mem['fqn']} [dim]({mem['metadata']['memory_status']})[/dim]")


def _handle_reject(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Reject a candidate / pending-review memory with a bounded reason.

    Same routing pattern as ``_handle_approve``: HTTPS-as-probe with
    loopback-gated ECONNREFUSED fallback (#925 v7).
    """
    from ..services import lineage, memory_promotion
    from ._audit_helper import get_cli_audit_writer
    from ._decision_routing import (
        ServerHttpError,
        ServerNotRunningError,
        call_decision_endpoint,
    )

    reviewer_id = getattr(getattr(config, "identity", None), "user_id", None) or "cli-reviewer"
    reviewer_display = getattr(getattr(config, "identity", None), "display_name", None)

    body: dict[str, Any] = {"reason": args.reason}
    if reviewer_display is not None:
        body["reviewer_display"] = reviewer_display

    try:
        mem = call_decision_endpoint(
            config,
            "POST",
            f"/api/memory/{args.fqn}/reject",
            json_body=body,
        )
        console.print(
            f"[yellow]Rejected via server:[/yellow] {mem['fqn']} "
            f"[dim](reason: {mem['metadata']['rejected_reason']})[/dim]"
        )
        return
    except ServerNotRunningError:
        pass
    except ServerHttpError as exc:
        console.print(f"[red]Server error — declining to write audit locally.[/red] {exc}")
        sys.exit(2)

    audit_writer = get_cli_audit_writer(config)
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

    lineage.emit_memory_promotion(
        audit_writer,
        "rejected",
        fqn=mem["fqn"],
        reviewer_id=reviewer_id,
        details={"reason_length": len(args.reason)},
    )
    console.print(f"[yellow]Rejected:[/yellow] {mem['fqn']} [dim](reason: {mem['metadata']['rejected_reason']})[/dim]")


# ---------------------------------------------------------------------------
# Retention / pin handlers (#625)
# ---------------------------------------------------------------------------


def _handle_pin(db: Any, args: argparse.Namespace) -> None:
    """Pin a memory so retention workers skip it by default."""
    from ..services import memory_service

    updated = memory_service.pin_memory(db, args.fqn)
    if updated is None:
        console.print(f"[red]Not found:[/red] {args.fqn}")
        sys.exit(1)
    console.print(f"[green]Pinned:[/green] {args.fqn}")


def _handle_unpin(db: Any, args: argparse.Namespace) -> None:
    """Remove the pin flag from a memory."""
    from ..services import memory_service

    updated = memory_service.unpin_memory(db, args.fqn)
    if updated is None:
        console.print(f"[red]Not found:[/red] {args.fqn}")
        sys.exit(1)
    console.print(f"[green]Unpinned:[/green] {args.fqn}")


def _handle_retention(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Dispatch ``aroom memory retention preview|purge``."""
    sub_action = getattr(args, "memory_retention_action", None)
    if sub_action == "preview":
        _handle_retention_preview(config, db, args)
    elif sub_action == "purge":
        _handle_retention_purge(config, db, args)
    else:
        console.print("Usage: aroom memory retention {preview,purge}")
        sys.exit(1)


def _render_retention_result(result: Any, *, title: str) -> None:
    if not result.items:
        console.print(f"[dim]{title}: no matching memories.[/dim]")
        return
    table = Table(title=title, show_header=True)
    table.add_column("FQN", style="bold")
    table.add_column("Reason")
    table.add_column("Age (days)", justify="right")
    table.add_column("Last recalled", style="dim")
    table.add_column("Status")
    table.add_column("Pinned", justify="center")
    for item in result.items:
        table.add_row(
            item.fqn,
            item.reason,
            str(item.age_days),
            (item.last_recalled_at or "-")[:19],
            item.status or "-",
            "yes" if item.pinned else "-",
        )
    console.print(table)
    if result.skipped_pinned_count:
        console.print(f"[dim]Skipped {result.skipped_pinned_count} pinned memory(ies).[/dim]")


def _handle_retention_preview(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Dry-run the retention policy and render the would-be-purged set."""
    from ..services import memory_retention

    result = memory_retention.purge_memories(
        db,
        config.memory.retention,
        dry_run=True,
    )
    if not config.memory.retention.enabled:
        console.print(
            "[dim]Memory retention is disabled (memory.retention.enabled=false). Nothing would be purged.[/dim]"
        )
        return
    _render_retention_result(result, title="Memories that would be purged")


def _handle_retention_purge(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Actually run the retention policy. Requires ``--confirm``.

    Routes through ``POST /api/memory/retention-purge`` when the local
    server is reachable so audit entries land on the server's chain-safe
    writer. Falls back to a local chain-safe writer only when the OS
    attests the loopback server is absent (#925 v7).
    """
    from ..services import memory_retention
    from ._audit_helper import get_cli_audit_writer
    from ._decision_routing import (
        ServerHttpError,
        ServerNotRunningError,
        call_decision_endpoint,
    )

    if not getattr(args, "confirm", False):
        console.print(
            "[red]Refusing to purge:[/red] pass --confirm to actually delete "
            "(use `aroom memory retention preview` first)."
        )
        sys.exit(1)
    if not config.memory.retention.enabled:
        console.print("[dim]Memory retention is disabled. Nothing to do.[/dim]")
        return

    try:
        payload = call_decision_endpoint(
            config,
            "POST",
            "/api/memory/retention-purge",
            json_body={"confirm": True},
        )
        console.print(f"[green]Purged via server:[/green] {payload.get('purged_count', 0)} memory(ies)")
        return
    except ServerNotRunningError:
        pass
    except ServerHttpError as exc:
        console.print(f"[red]Server error — declining to write audit locally.[/red] {exc}")
        sys.exit(2)

    # Local fallback path: use a chain-safe writer so the audit log
    # continues from the prior chain rather than creating an unkeyed
    # segment.
    audit_writer = get_cli_audit_writer(config)
    reviewer_id = getattr(getattr(config, "identity", None), "user_id", None) or "cli-reviewer"
    result = memory_retention.purge_memories(
        db,
        config.memory.retention,
        dry_run=False,
        audit_writer=audit_writer,
        reviewer_id=reviewer_id,
    )
    _render_retention_result(result, title=f"Purged {result.purged_count} memory(ies)")
