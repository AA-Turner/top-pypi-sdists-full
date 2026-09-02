"""Human-readable plan formatting for the nest command.

Produces terminal-friendly output showing source → target moves,
hierarchy.yml previews, specs that remain flat, cross-reference updates,
and warnings.
"""

from __future__ import annotations

from .plan import MigrationPlan


def render_warnings(warnings: list[str]) -> str:
    """Render warning messages as a labeled block.

    Args:
        warnings: Warning messages to render.

    Returns:
        A newline-joined block with one labeled line per warning, or an empty
        string when there are no warnings.
    """
    if not warnings:
        return ""

    lines = ["Warnings:", "-" * 40]
    lines.extend(f"  ⚠ {warning}" for warning in warnings)
    return "\n".join(lines)


def format_migration_plan(plan: MigrationPlan) -> str:
    """Format a migration plan for terminal display.

    Args:
        plan: The computed migration plan.

    Returns:
        Human-readable string representation of the plan.
    """
    lines: list[str] = []

    lines.append("=" * 72)
    lines.append("SPECKIT NEST — Migration Plan")
    lines.append("=" * 72)
    lines.append("")

    if plan.moves:
        lines.append(f"Directory Moves ({len(plan.moves)}):")
        lines.append("-" * 40)
        for move in plan.moves:
            lines.append(f"  {move.source.name}/ → {move.target}/")
        lines.append("")
    else:
        lines.append("No directory moves needed.")
        lines.append("")

    if plan.hierarchy_files:
        lines.append(f"hierarchy.yml Files to Create ({len(plan.hierarchy_files)}):")
        lines.append("-" * 40)
        for path, children in sorted(plan.hierarchy_files.items()):
            lines.append(f"  {path}/hierarchy.yml:")
            for child in children:
                lines.append(f"    - #{child.number} {child.title}")
        lines.append("")

    if plan.remaining_flat:
        lines.append(f"Specs Remaining Flat ({len(plan.remaining_flat)}):")
        lines.append("-" * 40)
        for spec in plan.remaining_flat:
            lines.append(f"  {spec.path.name}/ (stays in place)")
        lines.append("")

    if plan.multi_parent_selections:
        lines.append("Multi-Parent Selections:")
        lines.append("-" * 40)
        for issue, parent in sorted(plan.multi_parent_selections.items()):
            candidates = plan.multi_parent_candidates.get(issue, [parent])
            candidate_text = ", ".join(f"#{candidate}" for candidate in candidates)
            lines.append(f"  Issue #{issue} candidates: {candidate_text} → selected #{parent} (lowest-numbered)")
        lines.append("")

    if plan.excluded_cycles:
        lines.append("Excluded Cyclic Groups:")
        lines.append("-" * 40)
        for cycle in plan.excluded_cycles:
            lines.append(f"  ⚠ Cycle detected: {sorted(cycle)}")
        lines.append("")

    warning_block = render_warnings(plan.warnings)
    if warning_block:
        lines.append(warning_block)
        lines.append("")

    lines.append("=" * 72)
    return "\n".join(lines)
