"""Rich renderer for the ``/attribution`` slash command (#923).

Emits five compact tables covering the five attribution sections plus a
header line of section counts. All rendering goes through ``textContent``-
equivalent paths (Rich's built-in escaping) — user-derived values are
already scanner-processed by ``services.attribution.build_attribution``.
"""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.table import Table


def _fmt_distance(d: Any) -> str:
    try:
        return f"{float(d):.3f}"
    except (TypeError, ValueError):
        return "-"


def _section_table(title: str, columns: list[str], rows: list[list[str]]) -> Table:
    t = Table(title=title, title_style="bold", show_header=True, show_edge=False, pad_edge=False)
    for col in columns:
        t.add_column(col, overflow="fold")
    for r in rows:
        t.add_row(*r)
    return t


def render_attribution_detail(console: Console, snapshot: Any) -> None:
    """Render the full per-turn attribution detail to *console*.

    Accepts either an ``AttributionSnapshot`` dataclass instance or a
    dict (from persisted ``messages.metadata["attribution"]``). Each
    section is its own Rich table; empty sections render as ``(none)``.
    """
    if snapshot is None:
        console.print("[dim]No attribution recorded for this turn.[/dim]")
        return

    def _get(key: str) -> list[dict[str, Any]]:
        if hasattr(snapshot, key):
            return list(getattr(snapshot, key) or [])
        if isinstance(snapshot, dict):
            return list(snapshot.get(key) or [])
        return []

    dlp = getattr(snapshot, "dlp_match_count", None)
    if dlp is None and isinstance(snapshot, dict):
        dlp = snapshot.get("dlp_match_count", 0)
    of = getattr(snapshot, "output_filter_match_count", None)
    if of is None and isinstance(snapshot, dict):
        of = snapshot.get("output_filter_match_count", 0)

    turns = _get("turns")
    memory = _get("memory")
    sources = _get("sources")
    tools = _get("tools")
    packs = _get("packs")

    console.print()
    header_parts = [
        f"{len(turns)} turns",
        f"{len(memory)} memories",
        f"{len(sources)} sources",
        f"{len(tools)} tools",
        f"{len(packs)} packs",
    ]
    if dlp:
        header_parts.append(f"DLP:{dlp}")
    if of:
        header_parts.append(f"OF:{of}")
    console.print(f"[bold]Context attribution[/bold] — {' · '.join(header_parts)}")
    console.print()

    _render_section_turns(console, turns)
    _render_section_memory(console, memory)
    _render_section_sources(console, sources)
    _render_section_tools(console, tools)
    _render_section_packs(console, packs)


def _truncated_marker_row(items: list[dict[str, Any]], width: int) -> list[str] | None:
    if items and isinstance(items[-1], dict) and "truncated" in items[-1]:
        return [f"+{items[-1]['truncated']} more"] + ([""] * (width - 1))
    return None


def _real_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [i for i in items if isinstance(i, dict) and "truncated" not in i]


def _render_section_turns(console: Console, items: list[dict[str, Any]]) -> None:
    console.print("[bold]Recent turns[/bold]")
    if not items:
        console.print("  (none)")
        console.print()
        return
    rows: list[list[str]] = []
    for m in _real_rows(items):
        rows.append([str(m.get("message_id", ""))[:8], str(m.get("role", ""))])
    trunc = _truncated_marker_row(items, 2)
    if trunc:
        rows.append(trunc)
    console.print(_section_table("", ["Message", "Role"], rows))
    console.print()


def _render_section_memory(console: Console, items: list[dict[str, Any]]) -> None:
    console.print("[bold]Recalled memories[/bold]")
    if not items:
        console.print("  (none)")
        console.print()
        return
    rows: list[list[str]] = []
    for m in _real_rows(items):
        rows.append(
            [
                str(m.get("fqn", "")),
                str(m.get("scope", "")),
                str(m.get("category", "")),
                _fmt_distance(m.get("distance")),
            ]
        )
    trunc = _truncated_marker_row(items, 4)
    if trunc:
        rows.append(trunc)
    console.print(_section_table("", ["FQN", "Scope", "Category", "Distance"], rows))
    console.print()


def _render_section_sources(console: Console, items: list[dict[str, Any]]) -> None:
    console.print("[bold]RAG sources[/bold]")
    if not items:
        console.print("  (none)")
        console.print()
        return
    rows: list[list[str]] = []
    for s in _real_rows(items):
        rows.append([str(s.get("label", "")), str(s.get("type", ""))])
    trunc = _truncated_marker_row(items, 2)
    if trunc:
        rows.append(trunc)
    console.print(_section_table("", ["Label", "Type"], rows))
    console.print()


def _render_section_tools(console: Console, items: list[dict[str, Any]]) -> None:
    console.print("[bold]Tool calls[/bold]")
    if not items:
        console.print("  (none)")
        console.print()
        return
    rows: list[list[str]] = []
    for t in _real_rows(items):
        rows.append([str(t.get("id", ""))[:8], str(t.get("name", ""))])
    trunc = _truncated_marker_row(items, 2)
    if trunc:
        rows.append(trunc)
    console.print(_section_table("", ["Call ID", "Tool"], rows))
    console.print()


def _render_section_packs(console: Console, items: list[dict[str, Any]]) -> None:
    console.print("[bold]Attached packs[/bold]")
    if not items:
        console.print("  (none)")
        console.print()
        return
    rows: list[list[str]] = []
    for p in _real_rows(items):
        rows.append(
            [
                str(p.get("namespace", "")),
                str(p.get("name", "")),
                str(p.get("scope", "")),
            ]
        )
    trunc = _truncated_marker_row(items, 3)
    if trunc:
        rows.append(trunc)
    console.print(_section_table("", ["Namespace", "Name", "Scope"], rows))
    console.print()
