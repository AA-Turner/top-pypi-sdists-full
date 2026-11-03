"""Audit helpers for agent task execution."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from collections import Counter

from opentelemetry import trace

from plato.agents.mounts import AgentWorkspaceMount, AuditedMount
from plato.chronos.models import AuditEventInput, Operation
from plato.runtimes.base import RuntimeInfo
from plato.transports import GitTransport, NFSTransport, SSHFSTransport
from plato.utils.audit import (
    AuditScopeContext,
    audit_ignore_filter,
    build_audit_key,
    load_audit_ignore,
    new_audit_run_id,
    parse_audit_raw,
    write_audit_jsonl,
)
from plato.utils.audit_resolution import resolve_audit_events_for_scope
from plato.utils.subprocess import run_ssh
from plato.utils.tool_execution import (
    DEFAULT_TOOL_EXECUTION_CONTEXT_PATH,
    DEFAULT_TOOL_EXECUTION_SPOOL_PATH,
    DEFAULT_TOOL_START_SPOOL_PATH,
    ToolExecutionContext,
    ToolExecutionRecord,
    ToolExecutionScope,
    parse_tool_execution_records,
    write_tool_execution_records,
)

logger = logging.getLogger(__name__)


def default_agent_name(agent_image: str) -> str:
    return agent_image.split("/")[-1].split(":")[0]


def prepare_audited_mounts(
    mounts: list[AgentWorkspaceMount],
) -> tuple[list[AgentWorkspaceMount], list[AuditedMount]]:
    """Clone tracked mounts for per-run audit metadata and return audited wrappers."""
    run_mounts: list[AgentWorkspaceMount] = []
    audited_mounts: list[AuditedMount] = []

    for mount in mounts:
        run_mount = mount
        transport = mount.transport

        if mount.tracked and isinstance(transport, (NFSTransport, SSHFSTransport, GitTransport)):
            # Mounts are already cloned by the caller (AgentExecutionManager,
            # _run_with_warm_pool, or _run_impl) before reaching here, so we
            # just attach audit metadata without cloning again.  A second
            # clone_for_run() would create a new transport instance, breaking
            # the published_ref reference chain for git transports.
            audit_run_id = new_audit_run_id()
            audit_key = build_audit_key(audit_run_id)
            run_mount.audit_run_id = audit_run_id
            run_mount.audit_key = audit_key
            audited_mounts.append(
                AuditedMount(
                    mount=run_mount,
                    audit_run_id=audit_run_id,
                    audit_key=audit_key,
                )
            )

        run_mounts.append(run_mount)

    return run_mounts, audited_mounts


def build_audit_context_payload(
    info: RuntimeInfo,
    audited_mounts: list[AuditedMount],
    *,
    agent_image: str,
    default_display_name: str | None,
    display_name: str | None,
) -> dict[str, object]:
    span = trace.get_current_span()
    ctx = span.get_span_context()
    trace_id = format(ctx.trace_id, "032x") if ctx.is_valid else ""
    span_id = format(ctx.span_id, "016x") if ctx.is_valid else ""
    agent_name = display_name or default_display_name or default_agent_name(agent_image)
    return {
        "session_id": os.environ.get("SESSION_ID", ""),
        "agent_id": info.runtime_id,
        "agent_name": agent_name,
        "display_name": display_name or default_display_name or agent_name,
        "trace_id": trace_id,
        "span_id": span_id,
        "scopes": [
            {
                "workspace_name": audited_mount.workspace_name,
                "mount_path": audited_mount.mount_path,
                "audit_run_id": audited_mount.audit_run_id,
                "audit_key": audited_mount.audit_key,
            }
            for audited_mount in audited_mounts
        ],
    }


def build_tool_execution_context_payload(
    info: RuntimeInfo,
    audited_mounts: list[AuditedMount],
    *,
    agent_image: str,
    default_display_name: str | None,
    display_name: str | None,
) -> ToolExecutionContext:
    audit_context = build_audit_context_payload(
        info,
        audited_mounts,
        agent_image=agent_image,
        default_display_name=default_display_name,
        display_name=display_name,
    )
    return ToolExecutionContext(
        session_id=str(audit_context.get("session_id", "")),
        agent_id=info.runtime_id,
        agent_name=str(audit_context.get("agent_name", "")),
        display_name=str(audit_context.get("display_name", "")),
        trace_id=str(audit_context.get("trace_id", "")),
        span_id=str(audit_context.get("span_id", "")),
        spool_path=str(DEFAULT_TOOL_EXECUTION_SPOOL_PATH),
        hook_spool_path=str(DEFAULT_TOOL_START_SPOOL_PATH),
        scopes=[
            ToolExecutionScope(
                workspace_name=audited_mount.workspace_name,
                mount_path=audited_mount.mount_path,
                audit_run_id=audited_mount.audit_run_id,
                audit_key=audited_mount.audit_key,
            )
            for audited_mount in audited_mounts
        ],
    )


async def write_audit_context(
    info: RuntimeInfo,
    audited_mounts: list[AuditedMount],
    *,
    agent_image: str,
    default_display_name: str | None,
    display_name: str | None,
    watch_paths: list[str],
    file_trigger_patterns: list[str] | None,
    trigger_server_url: str | None,
) -> None:
    """Write audit/tool context and optional file watcher config to the agent VM."""
    try:
        context_json = json.dumps(
            build_audit_context_payload(
                info,
                audited_mounts,
                agent_image=agent_image,
                default_display_name=default_display_name,
                display_name=display_name,
            )
        )
        tool_context_json = build_tool_execution_context_payload(
            info,
            audited_mounts,
            agent_image=agent_image,
            default_display_name=default_display_name,
            display_name=display_name,
        ).model_dump_json()

        ssh_key = info.ssh_key_path
        if ssh_key:
            await run_ssh(
                ssh_key,
                info.hostname,
                (
                    "cat > /tmp/plato-audit-context.json << 'AUDIT_EOF'\n"
                    f"{context_json}\n"
                    "AUDIT_EOF\n"
                    f"cat > {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH} << 'TOOL_EOF'\n"
                    f"{tool_context_json}\n"
                    "TOOL_EOF\n"
                    f": > {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}\n"
                    f": > {DEFAULT_TOOL_START_SPOOL_PATH}"
                ),
                timeout=10,
            )
            logger.debug("Wrote audit and tool execution context to agent VM")

            if file_trigger_patterns and trigger_server_url and watch_paths:
                watcher_config = json.dumps(
                    {
                        "server_url": trigger_server_url,
                        "patterns": file_trigger_patterns,
                        "watch_paths": watch_paths,
                        "poll_interval_s": 2.0,
                    }
                )
                await run_ssh(
                    ssh_key,
                    info.hostname,
                    (
                        f"cat > /tmp/plato-file-watcher-config.json << 'WATCHER_EOF'\n"
                        f"{watcher_config}\n"
                        "WATCHER_EOF\n"
                        "nohup python3 -m plato.utils.file_watcher "
                        "/tmp/plato-file-watcher-config.json "
                        "> /tmp/plato-file-watcher.log 2>&1 &\n"
                        "echo $! > /tmp/plato-file-watcher.pid"
                    ),
                    timeout=10,
                )
                logger.info(
                    "Started file watcher sidecar on %s (patterns=%s, server=%s)",
                    info.hostname,
                    file_trigger_patterns,
                    trigger_server_url,
                )
    except Exception:
        logger.warning("Failed to write audit context to agent VM", exc_info=True)


async def read_tool_execution_records(info: RuntimeInfo) -> list[ToolExecutionRecord]:
    ssh_key = info.ssh_key_path
    if not ssh_key:
        return []

    context_exit_code, context_stdout, context_stderr = await run_ssh(
        ssh_key,
        info.hostname,
        (
            f"echo '=== context ==='; "
            f"if [ -f {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH} ]; then cat {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH}; else echo '<missing>'; fi; "
            f"echo; echo '=== spool-meta ==='; "
            f"if [ -f {DEFAULT_TOOL_EXECUTION_SPOOL_PATH} ]; then ls -l {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}; wc -l {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}; else echo '<missing>'; fi"
        ),
        timeout=10,
    )
    if context_exit_code == 0:
        logger.debug(
            "Tool execution VM state for agent %s:%s%s",
            info.runtime_id,
            "\n",
            context_stdout,
        )
    else:
        logger.warning(
            "Failed to inspect tool execution VM state for agent %s: %s",
            info.runtime_id,
            context_stderr,
        )

    exit_code, stdout, stderr = await run_ssh(
        ssh_key,
        info.hostname,
        (f"if [ -f {DEFAULT_TOOL_EXECUTION_SPOOL_PATH} ]; then cat {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}; fi"),
        timeout=10,
    )
    if exit_code != 0:
        logger.warning(
            "Failed to read tool execution spool from agent VM %s: %s",
            info.runtime_id,
            stderr,
        )
        return []

    records = parse_tool_execution_records(stdout)
    tool_counts = Counter(record.tool_name for record in records)
    logger.info(
        "Read %d tool execution records from agent VM %s: %s",
        len(records),
        info.runtime_id,
        dict(tool_counts),
    )
    return records


async def collect_and_store_audit_results(
    info: RuntimeInfo,
    audited_mounts: list[AuditedMount],
    *,
    agent_image: str,
    default_display_name: str | None,
    display_name: str | None,
) -> None:
    """Collect audit logs from tracked workspace scopes into scoped JSONL spools."""
    try:
        if not audited_mounts:
            return

        context = build_audit_context_payload(
            info,
            audited_mounts,
            agent_image=agent_image,
            default_display_name=default_display_name,
            display_name=display_name,
        )
        tool_records = await read_tool_execution_records(info)
        if tool_records:
            logger.debug(
                "Read %d tool execution records from agent VM %s: %s",
                len(tool_records),
                info.runtime_id,
                [
                    {
                        "tool_name": record.tool_name,
                        "trace_id": record.trace_id,
                        "span_id": record.span_id,
                        "started_at": record.started_at.isoformat(),
                        "ended_at": record.ended_at.isoformat(),
                        "path_hints": record.path_hints,
                        "working_directory": record.working_directory,
                        "pid": record.pid,
                        "child_pids": record.child_pids,
                    }
                    for record in tool_records
                ],
            )
        else:
            logger.debug(
                "No tool execution records were collected from agent VM %s",
                info.runtime_id,
            )
        for audited_mount in audited_mounts:
            await asyncio.to_thread(write_tool_execution_records, audited_mount.tool_spool_path, tool_records)
            logger.debug(
                "Stored %d tool execution records in %s",
                len(tool_records),
                audited_mount.tool_spool_path,
            )
            raw_log = await audited_mount.transport.collect_audit_log(
                info.hostname,
                audit_key=audited_mount.audit_key,
            )
            if not raw_log:
                logger.debug(
                    "No audit log data collected from agent VM for scope %s",
                    audited_mount.audit_key,
                )
                continue

            ignore_spec = await asyncio.to_thread(load_audit_ignore, audited_mount.transport.path)

            def _parse_and_filter(raw: str) -> list[AuditEventInput]:
                parsed = parse_audit_raw(raw)
                filtered = audit_ignore_filter(parsed, ignore_spec, workspace_prefix=audited_mount.mount_path)
                return [
                    event
                    for event in filtered
                    if not (
                        event.path in (audited_mount.mount_path, audited_mount.mount_path + "/.")
                        and event.operation == Operation.opened_file
                    )
                ]

            events = await asyncio.to_thread(_parse_and_filter, raw_log)
            if not events:
                logger.debug(
                    "No audit events after parsing and filtering for scope %s",
                    audited_mount.audit_key,
                )
                continue
            logger.info(
                "Parsed %d audit events for scope %s (agent=%s), time range: %s .. %s",
                len(events),
                audited_mount.audit_key,
                info.runtime_id,
                min(event.timestamp for event in events).isoformat(),
                max(event.timestamp for event in events).isoformat(),
            )

            scope_context = AuditScopeContext(
                session_id=str(context.get("session_id", "")),
                agent_id=info.runtime_id,
                agent_name=str(context.get("agent_name", "")),
                display_name=str(context.get("display_name", "")),
                workspace_name=audited_mount.workspace_name,
                audit_run_id=audited_mount.audit_run_id,
                audit_key=audited_mount.audit_key,
                trace_id=str(context.get("trace_id", "")),
                span_id=str(context.get("span_id", "")),
            )
            resolved_events = await asyncio.to_thread(
                resolve_audit_events_for_scope,
                events,
                scope_context=scope_context,
                tool_records=tool_records,
            )
            resolved_tools = Counter(event.tool_name for event in resolved_events)
            logger.info(
                "Resolved %d audit events for scope %s (agent=%s): tool_attribution=%s",
                len(resolved_events),
                audited_mount.audit_key,
                info.runtime_id,
                dict(resolved_tools),
            )
            await asyncio.to_thread(write_audit_jsonl, audited_mount.spool_path, resolved_events, scope_context)
            logger.debug(
                "Stored %d audit events in %s",
                len(resolved_events),
                audited_mount.spool_path,
            )
    except Exception:
        logger.warning("Failed to collect and store audit log", exc_info=True)
