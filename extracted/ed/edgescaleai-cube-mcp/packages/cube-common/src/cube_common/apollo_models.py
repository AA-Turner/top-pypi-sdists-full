"""Pydantic models and formatting helpers for Apollo entities and plans."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from cube_common import entity_config


# ---------------------------------------------------------------------------
# Status icon maps
# ---------------------------------------------------------------------------

# Icons for `reportedStatus`'s three enums, one map because their values never
# collide in meaning (UP_TO_DATE is good in both rollout and config). Every key is a
# member verified by introspection (2026-09-30) — the previous map was guessed, and
# apart from HEALTHY none of its keys existed, so every Rollout and Config rendered
# "?" and ERROR/WARNING had no icon. An unlisted value still renders "?".
STATUS_ICONS = {
    # ApolloEntityHealthStatus. Meanings of the Witchcraft states are from its
    # HealthState docs; the last five are Apollo's own roll-ups and undocumented.
    "HEALTHY": "✓", "DEFERRING": "✓",
    "WARNING": "!", "REPAIRING": "⟳",
    "ERROR": "✗", "TERMINAL": "✗",
    "SUSPENDED": "-",
    "ACTIVE_PLAN": "⟳",
    "OUT_OF_DATE": "?", "NO_DATA": "?", "UNKNOWN_HEALTH": "?", "INDETERMINATE": "?",
    # ApolloEntityRolloutStatus.
    "UP_TO_DATE": "✓",
    "IN_GRACE_PERIOD": "⟳", "ONGOING_BLUE_GREEN": "⟳",
    "STALE_BLOCKED": "✗", "STALE_BLOCKED_TRANSIENT": "⟳",
    "STALE_BLUE_GREEN": "✗", "STALE_OTHER": "✗", "RECALLED": "✗",
    "NOT_AVAILABLE": "-",
    # ApolloEntityConfigStatus (UP_TO_DATE / NOT_AVAILABLE above).
    "PENDING": "⟳", "BLOCKED": "✗",
}

PLAN_STATUS_ICONS = {
    "SUCCESSFUL": "✓", "SUCCESS": "✓",
    "UNSUCCESSFUL": "✗", "FAILURE": "✗",
    "ACTIVE": "⟳", "PENDING_INTERRUPTION": "⏸",
    "ABORTED": "✗", "TIMEOUT": "✗", "INTERRUPTED": "✗",
}

TASK_STATUS_ICONS = {
    "SUCCEEDED": "✓", "ACTIVE": "⟳", "FAILED": "✗",
    "ABANDONED": "—", "INTERRUPTED": "✗",
}


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_duration(start_str: str, end_str: str | None = None) -> str:
    """Format duration between two ISO timestamps, or elapsed since start."""
    if not start_str:
        return ""
    try:
        start = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        if end_str:
            end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        else:
            end = datetime.now(timezone.utc)
        total_secs = int((end - start).total_seconds())
        if total_secs < 60:
            return f"{total_secs}s"
        elif total_secs < 3600:
            return f"{total_secs // 60}m {total_secs % 60}s"
        else:
            hours = total_secs // 3600
            mins = (total_secs % 3600) // 60
            return f"{hours}h {mins}m"
    except Exception:
        return ""


def module_manager(entity: dict) -> dict | None:
    """The module installation that manages ``entity`` (`installedByModuleV2`), or None."""
    module = entity.get("installedByModuleV2")
    return module if isinstance(module, dict) and module else None


def module_label(module: dict) -> str:
    """How a managing module is named in tool output: its coordinate, display name if set."""
    coordinate = module.get("moduleMavenCoordinate") or module.get("rid") or "unknown module"
    display = module.get("displayName")
    return f"{coordinate} ({display})" if display and display != coordinate else coordinate


# Shown instead of an entity's config when the caller may not read it. Today that is
# a Teleport app service's config for a scoped caller: its `apps` key lists every
# company's apps on the cube (cube-cloud `tools/environments.py::withholds_config`).
CONFIG_WITHHELD = (
    "(withheld: this app service's config lists every company's apps on the cube; "
    "use list_exposed for the apps you can reach)"
)


def format_entity_health(
    entity: dict, health_check_lines: list[str] | None = None,
    *, withhold_config: bool = False,
) -> list[str]:
    """Format a single entity's health data into readable lines.

    `health_check_lines` (cube-cloud's `tools/health_checks.py` rendering) goes
    directly under the Health line it explains, rather than after the plan history.
    ``withhold_config`` prints `CONFIG_WITHHELD` in place of the declared config.
    """
    lines: list[str] = []
    name = entity.get("displayName") or entity.get("id", "unknown")
    entity_id = entity.get("id", "unknown")
    entity_name = (entity.get("entityLocator") or {}).get("entityName", "")
    product_id = (entity.get("product") or {}).get("productId", "")
    lifecycle = entity.get("lifecycleStatus", "")

    lines.append(f"  {name} ({entity_id})")
    if entity_name or product_id:
        lines.append(f"    Entity: {entity_name}  Product: {product_id}")
    if lifecycle:
        lines.append(f"    Lifecycle: {lifecycle}")

    reported = entity.get("reportedStatus")
    if reported:
        version = reported.get("version", "unknown")
        rollout = reported.get("rolloutStatus", "unknown")
        config = reported.get("configStatus", "unknown")
        health = reported.get("healthStatus", "unknown")

        lines.append(f"    Version:  {version}")
        lines.append(
            f"    Health:   {STATUS_ICONS.get(health, '?')} {health}  |  "
            f"Rollout: {STATUS_ICONS.get(rollout, '?')} {rollout}  |  "
            f"Config: {STATUS_ICONS.get(config, '?')} {config}"
        )

        blockers = reported.get("upgradeBlockerTypes")
        if blockers:
            lines.append(f"    Blockers: {', '.join(blockers)}")
    else:
        lines.append("    Status: No reported status")
    lines.extend(health_check_lines or [])

    status_label = ""
    plan_status = entity.get("planStatus")
    if plan_status:
        typename = plan_status.get("__typename", "")
        status_label = typename.replace("ApolloEntityPlanStatus_", "") if typename else "Unknown"
        blocked_count = plan_status.get("blockedChangesCount")
        if blocked_count:
            lines.append(f"    Plan:     {status_label} ({blocked_count} blocking constraint{'s' if blocked_count > 1 else ''})")
        else:
            lines.append(f"    Plan:     {status_label}")

    # Say who owns this entity's config BEFORE showing it. A module-managed entity's
    # declared config is the module's render; editing it here instead of through the
    # module is what broke jacanda-orin-agx-nanocube's `cube` label for six weeks.
    module = module_manager(entity)
    if module:
        lines.append(f"    Managed by module: {module_label(module)}")
        lines.append(
            "       Change its config with update_module_variables on that module. "
            "update_entity_config refuses this entity unless force=true (break-glass only)."
        )

    # Surface config override details from declared state. Parsed as YAML: a module
    # render and the Apollo UI both write block YAML, which the old JSON-only reader
    # skipped, so a configured entity read as having no overrides. Values go through
    # `entity_config.display_lines`, which masks secret-named entries.
    declared_config = (entity.get("declaredState") or {}).get("config") or []
    if declared_config and withhold_config:
        lines.append(f"    Current overrides: {CONFIG_WITHHELD}")
    elif declared_config and isinstance(declared_config, list):
        for cfg_str in declared_config:
            blocks = entity_config.parse_config(cfg_str)
            if not blocks:
                continue
            for block in blocks:
                lines.append(f"    Config override version: {block.version}")
                if status_label == "Blocked" and block.version == "0.0.0":
                    lines.append("    ** Config issue: override block uses version 0.0.0 — Apollo needs a version matching the target release (e.g. 4.x.x)")
                    lines.append("       Use update_entity_config with version param to fix")
                if not block.readable:
                    lines.append("    Current overrides: (could not be parsed; not shown)")
                elif block.overrides in ({}, []):
                    lines.append("    Current overrides: (none)")
                else:
                    lines.append("    Current overrides (secret-named values hidden):")
                    lines.extend(f"      {ol}" for ol in entity_config.display_lines(block.overrides))
            break

    plans_conn = entity.get("nonGenericPlans")
    if plans_conn:
        plans = plans_conn.get("plans", [])
        if plans:
            lines.append(f"    Recent Plans ({len(plans)}):")
            for plan in plans:
                ps = plan.get("status", {}) or {}
                status_type = ps.get("type", "unknown")
                icon = PLAN_STATUS_ICONS.get(status_type, "?")

                tasks = plan.get("tasks", [])
                plan_desc = ""
                for t in tasks:
                    tdesc = (t.get("description") or {}).get("summary", "")
                    if "target state" in tdesc.lower() or "install" in tdesc.lower():
                        plan_desc = "Install"
                        break
                    elif "enforce" in tdesc.lower() or "config" in tdesc.lower():
                        plan_desc = "Enforce config"
                        break

                start = plan.get("startTime", "")
                end = plan.get("endTime")
                duration = format_duration(start, end)
                start_display = start[:19].replace("T", " ") if start else ""

                result_summary = (ps.get("result") or {}).get("summary", "")
                reason_summary = (ps.get("reason") or {}).get("summary", "")
                detail = result_summary or reason_summary

                plan_line = f"      {icon} {status_type}"
                if plan_desc:
                    plan_line += f" ({plan_desc})"
                if duration:
                    plan_line += f" [{duration}]"
                if start_display:
                    plan_line += f" {start_display}"
                lines.append(plan_line)

                if detail:
                    if len(detail) > 120:
                        detail = detail[:117] + "..."
                    lines.append(f"        {detail}")

                for task in tasks:
                    desc = (task.get("description") or {}).get("summary", "") or (
                        task.get("description") or {}
                    ).get("type", "")
                    ts = task.get("status") or {}
                    ttype = ts.get("type", "") if isinstance(ts, dict) else str(ts)
                    ticon = TASK_STATUS_ICONS.get(ttype, "?")
                    lines.append(f"        {ticon} {desc}: {ttype}")
        else:
            lines.append("    Recent Plans: (none)")

    lines.append("    (Use plan_details for full plan info with events and error logs)")
    return lines


def format_plan_task(task: dict, lines: list[str], indent: int = 2) -> None:
    """Format a single plan task with its events into readable lines."""
    prefix = " " * indent
    desc = task.get("description") or {}
    task_name = desc.get("summary") or desc.get("type", "unknown task")
    origin = task.get("origin", "")
    ts = task.get("status") or {}
    status_type = ts.get("type", "unknown")
    status_icon = TASK_STATUS_ICONS.get(status_type, "?")
    created = task.get("createdAt", "")
    updated = ts.get("updatedAt") or ""
    duration = format_duration(created, updated if updated else None)

    task_line = f"{prefix}{status_icon} {task_name}"
    if origin:
        task_line += f" ({origin})"
    task_line += f" {status_type}"
    if duration:
        task_line += f" {duration}"
    lines.append(task_line)

    task_status_desc = ts.get("description")
    if task_status_desc:
        summary = task_status_desc.get("summary", "")
        if summary:
            lines.append(f"{prefix}  └ {summary}")
        metadata = task_status_desc.get("metadataMap")
        if metadata and isinstance(metadata, dict):
            details = metadata.get("details") or metadata.get("message")
            if details and isinstance(details, str):
                detail_lines = details.strip().split("\n")
                for dl in detail_lines[:10]:
                    lines.append(f"{prefix}    {dl}")
                if len(detail_lines) > 10:
                    lines.append(f"{prefix}    ... ({len(detail_lines) - 10} more lines)")

    events = task.get("events", [])
    if events:
        show_events = events[-8:] if len(events) > 8 else events
        if len(events) > 8:
            lines.append(f"{prefix}  ({len(events)} events, showing last 8)")
        for event in show_events:
            ts_str = event.get("timestamp", "")
            time_display = ts_str[11:19] if len(ts_str) >= 19 else ts_str
            event_desc = (event.get("description") or {}).get("summary", "")
            if event_desc:
                lines.append(f"{prefix}  {time_display} {event_desc}")
    elif not task_status_desc:
        latest = task.get("latestEvent")
        if latest:
            event_desc = (latest.get("description") or {}).get("summary", "")
            if event_desc:
                lines.append(f"{prefix}  └ {event_desc}")

    for subtask in task.get("subtasks", []):
        format_plan_task(subtask, lines, indent=indent + 2)


def format_plan_details(entity: dict, env_name: str, plan_index: int = 0) -> str:
    """Format full plan details for an entity. Returns formatted string."""
    ename = entity.get("displayName") or entity.get("id", "unknown")
    product_id = (entity.get("product") or {}).get("productId", "")
    lifecycle = entity.get("lifecycleStatus", "")
    version = (entity.get("reportedStatus") or {}).get("version", "")

    plans = (entity.get("nonGenericPlans") or {}).get("plans", [])
    if not plans:
        return f"No plans found for entity '{ename}' in {env_name}."

    if plan_index >= len(plans):
        return (
            f"Plan index {plan_index} out of range. "
            f"Entity '{ename}' has {len(plans)} plan(s) (use 0-{len(plans)-1})."
        )

    plan = plans[plan_index]
    ps = plan.get("status", {}) or {}
    status_type = ps.get("type", "unknown")
    status_icon = PLAN_STATUS_ICONS.get(status_type, "?")
    agent_id = plan.get("agentId", "unknown")
    start = plan.get("startTime", "")
    end = plan.get("endTime")
    duration = format_duration(start, end)
    start_display = start[:19].replace("T", " ") if start else ""
    end_display = end[:19].replace("T", " ") if end else ""

    changes = plan.get("stateChanges", [])
    change_types = [c.get("changeType", "") for c in changes]
    plan_type = "Install" if "INSTALL" in " ".join(change_types).upper() else "Plan"
    if any("ENFORCE" in ct.upper() or "CONFIG" in ct.upper() for ct in change_types):
        plan_type = "Enforce config"
    elif any("UPGRADE" in ct.upper() for ct in change_types):
        plan_type = "Upgrade"
    elif any("UNINSTALL" in ct.upper() for ct in change_types):
        plan_type = "Uninstall"

    lines = [
        f"Plan Details: {ename} on {env_name}",
        "=" * 60,
        "",
        f"  {status_icon} {plan_type} {version or ''}",
        f"  Status:     {status_type}",
        f"  Agent:      {agent_id}",
        f"  Product:    {product_id}",
        f"  Lifecycle:  {lifecycle}",
    ]
    if start_display:
        lines.append(f"  Started:    {start_display}")
    if end_display:
        lines.append(f"  Ended:      {end_display}")
    if duration:
        lines.append(f"  Duration:   {duration}")

    result = ps.get("result")
    reason = ps.get("reason")
    if result:
        lines.append("")
        lines.append(f"  Result: {result.get('summary', '')}")
        metadata = result.get("metadataMap")
        if metadata and isinstance(metadata, dict):
            details = metadata.get("details") or metadata.get("resultDetails") or metadata.get("message")
            if details:
                lines.append("")
                lines.append("  Result Details:")
                lines.append("  " + "-" * 56)
                if isinstance(details, str):
                    for dl in details.split("\n"):
                        lines.append(f"  {dl}")
                else:
                    lines.append(f"  {json.dumps(details, indent=2)}")
                lines.append("  " + "-" * 56)
            else:
                for k, v in metadata.items():
                    if isinstance(v, str) and len(v) > 200:
                        lines.append(f"  {k}: {v[:200]}...")
                    else:
                        lines.append(f"  {k}: {v}")

    if reason and reason.get("summary"):
        lines.append(f"  Reason: {reason.get('summary', '')}")

    tasks = plan.get("tasks", [])
    if tasks:
        lines.append("")
        lines.append("Tasks:")
        lines.append("-" * 60)
        for task in tasks:
            format_plan_task(task, lines, indent=2)

    lines.append("")
    if plan_index == 0 and len(plans) > 1:
        lines.append(f"This is the most recent plan. Use plan_index=1..{len(plans)-1} to see older plans.")

    return "\n".join(lines)
