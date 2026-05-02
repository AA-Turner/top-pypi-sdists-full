"""Personal-AI console projection for the private dashboard."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
import json
import sqlite3
import subprocess
import sys
from typing import Any

from packages.growth import unbounded_level_for_score
from packages.skills import operator_skill_catalog_entries
from packages.state import PROFILE_MANIFEST_FILENAME, write_profile_manifest
from packages.state.loader import profile_manifest_path
from packages.runtime_config import (
    global_config_path_for_database,
    global_config_schema,
    load_global_config,
    parse_global_config_text,
    read_global_config_text,
    write_global_config,
)

from .api_runtime_console_usage import (
    cache_usage_fields,
    normalize_token_usage_row,
    summarize_token_usage,
    token_usage_rows_for_session,
)


def _profile_dir_for_database(database_path: Path) -> Path:
    state_dir = database_path.parent
    if state_dir.name == "state":
        return state_dir.parent / "profile"
    return state_dir / "profile"


def _json_loads(value: object, fallback: Any) -> Any:
    if value is None:
        return fallback
    try:
        return json.loads(str(value))
    except (TypeError, ValueError, json.JSONDecodeError):
        return fallback


def _read_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _read_text_file(path: Path, *, max_chars: int = 20_000) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if len(text) <= max_chars:
        return text
    return text[-max_chars:]


def _tail_lines(path: Path, *, max_lines: int = 160) -> tuple[str, ...]:
    text = _read_text_file(path, max_chars=80_000)
    if not text:
        return ()
    return tuple(text.splitlines()[-max_lines:])


def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row is not None


def _query(
    connection: sqlite3.Connection,
    sql: str,
    params: tuple[object, ...] = (),
) -> list[dict[str, Any]]:
    try:
        rows = connection.execute(sql, params).fetchall()
    except sqlite3.Error:
        return []
    return [dict(row) for row in rows]


def _count(connection: sqlite3.Connection, table: str) -> int:
    if not _table_exists(connection, table):
        return 0
    try:
        row = connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()
    except sqlite3.Error:
        return 0
    return int(row["count"]) if row is not None else 0


def _latest_timestamp(connection: sqlite3.Connection, table: str, column: str = "updated_at") -> str | None:
    if not _table_exists(connection, table):
        return None
    try:
        row = connection.execute(f"SELECT MAX({column}) AS latest FROM {table}").fetchone()
    except sqlite3.Error:
        return None
    if row is None or row["latest"] is None:
        return None
    return str(row["latest"])


def _connection(database_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def _profiles(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    return _query(
        connection,
        """
        SELECT
            p.profile_id,
            p.display_name,
            p.mode,
            p.clone_path,
            p.preferences_json,
            p.enabled_capabilities_json,
            p.created_at,
            p.updated_at,
            c.clone_id,
            c.identity_mode,
            c.personality_preset,
            c.initiative,
            c.relational_stance,
            c.voice_contract,
            c.working_style_contract,
            c.charter_extension,
            c.source_clone_path,
            g.growth_score,
            g.total_dialogues,
            g.total_tokens,
            g.total_experiences,
            g.active_days,
            g.streak_days,
            g.last_dialogue_at
        FROM profiles AS p
        INNER JOIN (
            SELECT
                profile_id,
                MIN(started_at) AS first_session_started_at,
                MAX(updated_at) AS latest_session_updated_at
            FROM sessions
            GROUP BY profile_id
        ) AS active_sessions ON active_sessions.profile_id = p.profile_id
        LEFT JOIN clone_identities AS c ON c.profile_id = p.profile_id
        LEFT JOIN profile_growth AS g
          ON g.profile_id = p.profile_id
         AND (
            COALESCE(g.updated_at, g.created_at, g.last_dialogue_at, g.first_dialogue_at) IS NULL
            OR COALESCE(g.updated_at, g.created_at, g.last_dialogue_at, g.first_dialogue_at) >= active_sessions.first_session_started_at
         )
        ORDER BY active_sessions.latest_session_updated_at DESC, p.updated_at DESC
        LIMIT 100
        """,
    )


def _session_rows(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    sessions = _query(
        connection,
        """
        SELECT
            s.session_id,
            s.profile_id,
            s.workspace_id,
            s.status,
            s.started_at,
            s.updated_at,
            s.parent_session_id,
            s.interruption_state,
            s.resume_count,
            p.display_name,
            r.run_id,
            r.prompt AS latest_prompt,
            r.status AS latest_run_status,
            r.phase AS latest_phase,
            r.model_turn_count,
            r.tool_call_count,
            r.last_summary,
            r.waiting_reason
        FROM sessions AS s
        LEFT JOIN profiles AS p ON p.profile_id = s.profile_id
        LEFT JOIN agent_runs AS r
          ON r.run_id = (
            SELECT r2.run_id
            FROM agent_runs AS r2
            WHERE r2.session_id = s.session_id
            ORDER BY r2.updated_at DESC
            LIMIT 1
          )
        ORDER BY s.updated_at DESC
        LIMIT 100
        """,
    )
    for session in sessions:
        token_usage_rows = token_usage_rows_for_session(connection, session["session_id"])
        token_usage_by_run: dict[str, list[dict[str, Any]]] = {}
        for token_usage_row in token_usage_rows:
            run_id = str(token_usage_row.get("run_id") or "").strip()
            if run_id:
                token_usage_by_run.setdefault(run_id, []).append(token_usage_row)
        runs = _query(
            connection,
            """
            SELECT run_id, session_id, source_event_id, prompt, status, phase,
                   step_count, model_turn_count, tool_call_count, max_model_turns,
                   max_wall_time_seconds, waiting_reason, continuation_prompt,
                   last_summary, created_at, updated_at
            FROM agent_runs
            WHERE session_id = ?
            ORDER BY created_at ASC, updated_at ASC
            LIMIT 200
            """,
            (session["session_id"],),
        )
        for run in runs:
            run_token_usage_rows = token_usage_by_run.get(str(run.get("run_id") or ""), [])
            run["tokenUsageEvents"] = run_token_usage_rows
            run_token_usage = summarize_token_usage(run_token_usage_rows)
            if run_token_usage is not None:
                run["tokenUsage"] = run_token_usage
            run["steps"] = _query(
                connection,
                """
                SELECT step_id, step_index, kind, title, content, outcome, tool_name, created_at
                FROM agent_run_steps
                WHERE run_id = ?
                ORDER BY step_index ASC
                LIMIT 400
                """,
                (run["run_id"],),
            )
        run_id = session.get("run_id")
        latest_steps = []
        if run_id:
            latest_steps = _query(
                connection,
                """
                SELECT step_id, step_index, kind, title, content, outcome, tool_name, created_at
                FROM agent_run_steps
                WHERE run_id = ?
                ORDER BY step_index ASC
                LIMIT 200
                """,
                (run_id,),
            )
        session["runs"] = runs
        session["steps"] = latest_steps
        session["tokenUsageEvents"] = token_usage_rows
        session["conversation"] = _conversation_entries(session=session, runs=runs)
        session["recording"] = {
            "systemPrompt": "persisted" if any(
                step.get("kind") in {"system", "system_prompt", "context_prompt"}
                for run in runs
                for step in as_rows(run.get("steps"))
            ) else "not_persisted",
            "assistantResponse": "step_content_or_summary",
            "toolExecution": "persisted" if any(
                step.get("kind") == "tool"
                for run in runs
                for step in as_rows(run.get("steps"))
            ) else "not_present",
        }
    return sessions


def as_rows(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _conversation_entries(*, session: Mapping[str, Any], runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for run in runs:
        prompt = str(run.get("prompt") or "").strip()
        is_proactive_opening = _is_proactive_opening_prompt(prompt)
        run_cache_usage_fields = cache_usage_fields(run)
        model_entry_recorded = False
        if prompt and is_proactive_opening:
            entries.append(
                {
                    "type": "internal_query",
                    "role": "internal",
                    "label": "Proactive opening query",
                    "runId": run.get("run_id"),
                    "sessionId": session.get("session_id"),
                    "timestamp": run.get("created_at"),
                    "content": prompt,
                    "status": "persisted",
                }
            )
        elif prompt:
            entries.append(
                {
                    "type": "user_query",
                    "label": "User query",
                    "runId": run.get("run_id"),
                    "sessionId": session.get("session_id"),
                    "timestamp": run.get("created_at"),
                    "content": prompt,
                    "status": "persisted",
                }
            )
        system_steps = [
            step for step in as_rows(run.get("steps"))
            if step.get("kind") in {"system", "system_prompt", "context_prompt"}
        ]
        if system_steps:
            for step in system_steps:
                entries.append(
                    {
                        "type": "system_prompt",
                        "label": str(step.get("title") or "System prompt"),
                        "runId": run.get("run_id"),
                        "sessionId": session.get("session_id"),
                        "timestamp": step.get("created_at"),
                        "content": step.get("content") or "",
                        "status": "persisted",
                    }
                )
        else:
            entries.append(
                {
                    "type": "system_prompt",
                    "label": "Provider system prompt",
                    "runId": run.get("run_id"),
                    "sessionId": session.get("session_id"),
                    "timestamp": run.get("created_at"),
                    "content": "Provider system prompt was not persisted for this run.",
                    "status": "not_persisted",
                }
            )
        for step in as_rows(run.get("steps")):
            kind = str(step.get("kind") or "")
            if kind in {"system", "system_prompt", "context_prompt"}:
                continue
            if kind == "tool":
                entries.append(
                    {
                        "type": "tool_call",
                        "label": step.get("tool_name") or step.get("title") or "Tool call",
                        "runId": run.get("run_id"),
                        "sessionId": session.get("session_id"),
                        "timestamp": step.get("created_at"),
                        "content": _tool_call_content(str(step.get("content") or "")),
                        "outcome": "called",
                        "status": "called",
                    }
                )
                entries.append(
                    {
                        "type": "tool_execute",
                        "label": step.get("tool_name") or step.get("title") or "Tool execution",
                        "runId": run.get("run_id"),
                        "sessionId": session.get("session_id"),
                        "timestamp": step.get("created_at"),
                        "content": step.get("content") or "",
                        "outcome": step.get("outcome"),
                        "status": "persisted",
                    }
                )
                continue
            entries.append(
                {
                    "type": "assistant_response" if kind == "model" else kind or "step",
                    "label": "Proactive opening" if is_proactive_opening and kind == "model" else step.get("title") or kind or "Run step",
                    "runId": run.get("run_id"),
                    "sessionId": session.get("session_id"),
                    "timestamp": step.get("created_at"),
                    "content": step.get("content") or "",
                    "outcome": step.get("outcome"),
                    "status": "persisted",
                    **(run_cache_usage_fields if kind == "model" else {}),
                }
            )
            if kind == "model":
                model_entry_recorded = True
        if run.get("last_summary") and (not as_rows(run.get("steps")) or (is_proactive_opening and not model_entry_recorded)):
            entries.append(
                {
                    "type": "assistant_response",
                    "label": "Proactive opening" if is_proactive_opening else "Run summary",
                    "runId": run.get("run_id"),
                    "sessionId": session.get("session_id"),
                    "timestamp": run.get("updated_at"),
                    "content": run.get("last_summary"),
                    "status": "summary_only",
                    **run_cache_usage_fields,
                }
            )
    return entries


def _is_proactive_opening_prompt(prompt: str) -> bool:
    return prompt.startswith("Open the wake surface proactively before the user sends a new message.")


def _tool_call_content(content: str) -> str:
    for line in content.splitlines():
        if line.startswith("arguments:"):
            return line
    return content


def _memory_rows(connection: sqlite3.Connection) -> dict[str, Any]:
    return {
        "memories": _query(
            connection,
            """
            SELECT memory_id, session_id, kind, content, source_event_id, goal_refs_json,
                   tags_json, lifecycle_state, metadata_json, created_at, updated_at
            FROM memories
            ORDER BY updated_at DESC
            LIMIT 200
            """,
        ),
        "memoryLedger": _query(
            connection,
            """
            SELECT entry_id, session_id, event_type, content, kind, goal_refs_json,
                   tags_json, metadata_json, created_at
            FROM memory_ledger_entries
            ORDER BY created_at DESC
            LIMIT 200
            """,
        ),
        "userCards": _query(
            connection,
            """
            SELECT user_card_id, profile_id, preferred_name, locale, timezone,
                   communication_preferences_json, boundaries_json, biography_fragments_json,
                   shared_preferences_json, durable_notes_json, source_user_profile_path,
                   created_at, updated_at
            FROM user_cards
            ORDER BY updated_at DESC
            LIMIT 100
            """,
        ),
        "relationships": _query(
            connection,
            """
            SELECT relationship_id, profile_id, clone_id, user_card_id,
                   interaction_preferences_json, repair_history_json, trust_markers_json,
                   expectations_json, local_corrections_json, continuity_notes_json,
                   created_at, updated_at
            FROM relationship_memories
            ORDER BY updated_at DESC
            LIMIT 100
            """,
        ),
        "identityLedger": _query(
            connection,
            """
            SELECT entry_id, clone_id, profile_id, action, summary, metadata_json, created_at
            FROM identity_ledger_entries
            ORDER BY created_at DESC
            LIMIT 100
            """,
        ),
    }


def _usage(connection: sqlite3.Connection) -> dict[str, Any]:
    growth = _query(
        connection,
        """
        SELECT profile_id, growth_score, total_dialogues, total_tokens, total_experiences,
               promoted_experiences, active_days, streak_days, last_active_day,
               first_dialogue_at, last_dialogue_at, updated_at
        FROM profile_growth
        ORDER BY updated_at DESC
        LIMIT 100
        """,
    )
    runs = _query(
        connection,
        """
        SELECT run_id, session_id, status, phase, model_turn_count, tool_call_count,
               step_count, last_summary, waiting_reason, created_at, updated_at
        FROM agent_runs
        ORDER BY updated_at DESC
        LIMIT 200
        """,
    )
    total_tokens = sum(int(row.get("total_tokens") or 0) for row in growth)
    total_dialogues = sum(int(row.get("total_dialogues") or 0) for row in growth)
    total_tools = sum(int(row.get("tool_call_count") or 0) for row in runs)
    token_events = [
        normalize_token_usage_row(row)
        for row in _query(
            connection,
            """
            SELECT usage_id, session_id, profile_id, run_id, source_event_id,
                   provider_id, model_id, prompt_tokens, completion_tokens,
                   total_tokens, unit, metadata_json, created_at
            FROM token_usage_events
            ORDER BY created_at DESC
            LIMIT 500
            """,
        )
    ] if _table_exists(connection, "token_usage_events") else []
    token_trend = _query(
        connection,
        """
        SELECT substr(created_at, 1, 10) AS day,
               SUM(prompt_tokens) AS prompt_tokens,
               SUM(completion_tokens) AS completion_tokens,
               SUM(total_tokens) AS total_tokens,
               COUNT(*) AS turns
        FROM token_usage_events
        GROUP BY substr(created_at, 1, 10)
        ORDER BY day DESC
        LIMIT 90
        """,
    ) if _table_exists(connection, "token_usage_events") else []
    ledger_total_tokens = sum(int(row.get("total_tokens") or 0) for row in token_events)
    return {
        "summary": {
            "totalTokens": ledger_total_tokens or total_tokens,
            "profileGrowthTokens": total_tokens,
            "totalDialogues": total_dialogues,
            "totalToolCalls": total_tools,
            "tokenLedgerEvents": len(token_events),
            "recordingLevel": "per-turn token ledger" if token_events else "profile_growth totals; token ledger has no rows yet",
        },
        "growth": growth,
        "runs": runs,
        "tokenEvents": token_events,
        "tokenTrend": token_trend,
    }


def _skills(app: Any, *, skill_overrides: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in operator_skill_catalog_entries(install_root=app.config.install_root):
        enabled = _override_enabled(skill_overrides, entry.skill_id, bool(entry.default_enabled))
        rows.append(
            {
                "skillId": entry.skill_id,
                "displayName": entry.display_name,
                "source": entry.source_label,
                "sourceId": entry.source_id,
                "summary": entry.summary,
                "version": entry.version,
                "enabled": enabled,
                "defaultEnabled": bool(entry.default_enabled),
                "override": skill_overrides.get(entry.skill_id),
                "reference": entry.reference,
                "metadata": dict(entry.metadata),
            }
        )
    return rows


def _tools(app: Any, *, tool_overrides: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tool in app.tool_runtime.list_tools(audience="operator"):
        enabled = _override_enabled(tool_overrides, tool.tool_id, bool(tool.enabled))
        rows.append(
            {
                "toolId": tool.tool_id,
                "displayName": tool.display_name,
                "description": tool.description,
                "family": tool.family,
                "enabled": enabled,
                "defaultEnabled": bool(tool.enabled),
                "override": tool_overrides.get(tool.tool_id),
                "available": tool.available,
                "availabilityReason": tool.availability.reason,
                "riskClass": tool.side_effects.risk_class,
                "approvalClass": tool.side_effects.approval_class,
                "readsState": tool.side_effects.reads_state,
                "writesState": tool.side_effects.writes_state,
                "touchesNetwork": tool.side_effects.touches_network,
                "touchesSecrets": tool.side_effects.touches_secrets,
                "requiredFields": tool.required_fields,
                "schema": dict(tool.schema),
                "provenance": tool.provenance,
                "backend": tool.backend,
                "metadata": dict(tool.metadata),
            }
        )
    return rows


def _logs(state_dir: Path) -> list[dict[str, Any]]:
    candidates = [
        *state_dir.glob("*.log"),
        *state_dir.glob("gateway/*.log"),
        *state_dir.glob("gateway/**/*.log"),
    ]
    seen: set[Path] = set()
    rows: list[dict[str, Any]] = []
    for path in sorted(candidates):
        resolved = path.resolve()
        if resolved in seen or not path.is_file():
            continue
        seen.add(resolved)
        rows.append(
            {
                "name": path.name,
                "path": str(path),
                "size": path.stat().st_size,
                "updatedAt": datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat(),
                "tail": _tail_lines(path),
            }
        )
    return rows


def _gateway(state_dir: Path) -> dict[str, Any]:
    gateway_dir = state_dir / "gateway"
    runtime_files = []
    for path in sorted((*gateway_dir.glob("*.runtime.json"), *gateway_dir.glob("*.pid"))):
        if not path.is_file():
            continue
        runtime_files.append(
            {
                "name": path.name,
                "path": str(path),
                "updatedAt": datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat(),
                "content": _read_json_file(path) if path.suffix == ".json" else _read_text_file(path, max_chars=4_000),
            }
        )
    return {
        "stateDir": str(gateway_dir),
        "exists": gateway_dir.exists(),
        "runtimeFiles": runtime_files,
        "logs": _logs(gateway_dir) if gateway_dir.exists() else [],
    }


def gateway_action(self, payload: Mapping[str, Any]) -> dict[str, Any]:
    action = str(payload.get("action") or "status").strip()
    service = str(payload.get("service") or "feishu").strip()
    if action not in {"status", "doctor", "start", "stop", "restart"}:
        raise ValueError("gateway action must be status, doctor, start, stop, or restart")
    if service not in {"feishu", "discord"}:
        raise ValueError("gateway service must be feishu or discord")
    database_path = self.repository.database_path
    state_dir = database_path.parent
    profile_dir = _profile_dir_for_database(database_path)
    command = [
        sys.executable,
        "-m",
        "apps.gateway",
        service,
        action,
        "--state-dir",
        str(state_dir / "gateway"),
        "--cli-state-dir",
        str(state_dir),
        "--cli-profile-dir",
        str(profile_dir),
    ]
    if action in {"start", "restart"}:
        command.append("--detach")
    if action in {"stop", "restart"} and bool(payload.get("force")):
        command.append("--force")
    result = subprocess.run(
        command,
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    return {
        "status": "ok" if result.returncode == 0 else "failed",
        "service": service,
        "action": action,
        "returnCode": result.returncode,
        "stdout": result.stdout[-8_000:],
        "stderr": result.stderr[-8_000:],
        "gateway": _gateway(state_dir),
    }


def _clone_memory_layers(
    *,
    clones: list[dict[str, Any]],
    memory: Mapping[str, Any],
    sessions: list[dict[str, Any]],
    settings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    sessions_by_profile: dict[str, set[str]] = {}
    for session in sessions:
        profile_id = str(session.get("profile_id") or "")
        session_id = str(session.get("session_id") or "")
        if profile_id and session_id:
            sessions_by_profile.setdefault(profile_id, set()).add(session_id)

    memory_rows = as_rows(memory.get("memories"))
    ledger_rows = as_rows(memory.get("memoryLedger"))
    user_cards = as_rows(memory.get("userCards"))
    relationships = as_rows(memory.get("relationships"))
    identity_ledger = as_rows(memory.get("identityLedger"))

    enriched: list[dict[str, Any]] = []
    for clone in clones:
        profile_id = str(clone.get("profile_id") or "")
        clone_id = str(clone.get("clone_id") or "")
        session_ids = sessions_by_profile.get(profile_id, set())
        power_score = max(0, int(clone.get("growth_score") or 0))
        ascension_level = unbounded_level_for_score(power_score)
        layer_payload = {
            "profileConfig": {
                "profileId": profile_id,
                "displayName": clone.get("display_name"),
                "mode": clone.get("mode"),
                "clonePath": clone.get("clone_path"),
                "preferences": _json_loads(clone.get("preferences_json"), []),
                "enabledCapabilities": _json_loads(clone.get("enabled_capabilities_json"), []),
            },
            "aegisMd": {
                "path": settings.get("aegisPath"),
                "content": settings.get("aegisText"),
            },
            "identity": {
                "cloneId": clone_id,
                "identityMode": clone.get("identity_mode"),
                "personalityPreset": clone.get("personality_preset"),
                "initiative": clone.get("initiative"),
                "relationalStance": clone.get("relational_stance"),
                "voiceContract": clone.get("voice_contract"),
                "workingStyleContract": clone.get("working_style_contract"),
                "charterExtension": clone.get("charter_extension"),
            },
            "level": {
                "ascensionLevel": ascension_level,
                "powerScore": power_score,
                "growthScore": clone.get("growth_score"),
                "totalDialogues": clone.get("total_dialogues"),
                "totalTokens": clone.get("total_tokens"),
                "totalExperiences": clone.get("total_experiences"),
                "activeDays": clone.get("active_days"),
                "streakDays": clone.get("streak_days"),
                "lastDialogueAt": clone.get("last_dialogue_at"),
            },
            "userProfile": [row for row in user_cards if row.get("profile_id") == profile_id],
            "relationshipMemory": [
                row for row in relationships
                if row.get("profile_id") == profile_id or (clone_id and row.get("clone_id") == clone_id)
            ],
            "durableMemories": [row for row in memory_rows if row.get("session_id") in session_ids],
            "memoryLedger": [row for row in ledger_rows if row.get("session_id") in session_ids],
            "identityLedger": [
                row for row in identity_ledger
                if row.get("profile_id") == profile_id or (clone_id and row.get("clone_id") == clone_id)
            ],
            "sessionIds": sorted(session_ids),
        }
        next_clone = dict(clone)
        next_clone["memoryLayers"] = layer_payload
        enriched.append(next_clone)
    return enriched


def _settings(profile_dir: Path, state_dir: Path, database_path: Path) -> dict[str, Any]:
    manifest_path = profile_manifest_path(profile_dir)
    aegis_md = profile_dir / "AEGIS.md"
    profile_json = _read_json_file(manifest_path)
    config_path = global_config_path_for_database(database_path)
    global_config = load_global_config(config_path, state_dir=state_dir, profile_dir=profile_dir)
    return {
        "profileDir": str(profile_dir),
        "stateDir": str(state_dir),
        "profileManifestPath": str(manifest_path),
        "profileManifest": profile_json if isinstance(profile_json, Mapping) else {},
        "aegisPath": str(aegis_md),
        "aegisText": _read_text_file(aegis_md) if aegis_md.exists() else None,
        "globalConfigPath": str(config_path),
        "globalConfigExists": config_path.exists(),
        "globalConfig": global_config,
        "globalConfigYaml": read_global_config_text(config_path, fallback=global_config),
        "globalConfigSchema": global_config_schema(),
    }


def _profile_overrides(profile_dir: Path, key: str) -> Mapping[str, Any]:
    manifest = _read_json_file(profile_manifest_path(profile_dir))
    if not isinstance(manifest, Mapping):
        return {}
    value = manifest.get(key)
    return value if isinstance(value, Mapping) else {}


def _override_enabled(overrides: Mapping[str, Any], item_id: str, default: bool) -> bool:
    value = overrides.get(item_id)
    if isinstance(value, Mapping) and isinstance(value.get("enabled"), bool):
        return bool(value["enabled"])
    return default


def _cron_jobs(app: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for job in app.cron_runtime.list_jobs():
        rows.append(
            {
                "jobId": job.job_id,
                "name": job.name,
                "schedule": job.schedule_text,
                "scheduleKind": job.schedule_kind,
                "jobKind": job.action_kind,
                "status": job.status,
                "profileId": job.profile_id,
                "cloneId": job.clone_id,
                "payload": dict(job.payload),
                "skills": list(_cron_skill_ids(job.payload.get("skills"))),
                "createdAt": job.created_at.isoformat(),
                "updatedAt": job.updated_at.isoformat(),
                "nextRunAt": job.next_run_at.isoformat() if job.next_run_at is not None else None,
                "lastRunAt": job.last_run_at.isoformat() if job.last_run_at is not None else None,
                "runCount": job.run_count,
                "lastSummary": job.last_summary,
            }
        )
    return rows


def _cron_skill_ids(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").split(",")
    elif isinstance(value, (list, tuple)):
        raw_items = [str(item) for item in value]
    else:
        raw_items = [str(value)]
    return tuple(dict.fromkeys(item.strip() for item in raw_items if item.strip()))


def inspect_operator_console(self) -> dict[str, Any]:
    database_path = self.repository.database_path
    state_dir = database_path.parent
    profile_dir = _profile_dir_for_database(database_path)
    skill_overrides = _profile_overrides(profile_dir, "skill_overrides")
    tool_overrides = _profile_overrides(profile_dir, "tool_overrides")
    skills = _skills(self, skill_overrides=skill_overrides)
    tools = _tools(self, tool_overrides=tool_overrides)
    cron_jobs = _cron_jobs(self)
    with _connection(database_path) as connection:
        profiles = _profiles(connection)
        memories = _memory_rows(connection)
        sessions = _session_rows(connection)
        usage = _usage(connection)
        settings = _settings(profile_dir, state_dir, database_path)
        clones = _clone_memory_layers(clones=profiles, memory=memories, sessions=sessions, settings=settings)
        return {
            "meta": {
                "generatedAt": datetime.now(UTC).isoformat(),
                "databasePath": str(database_path),
                "stateDir": str(state_dir),
                "profileDir": str(profile_dir),
            },
            "system": {
                "counts": {
                    "profiles": _count(connection, "profiles"),
                    "sessions": _count(connection, "sessions"),
                    "memories": _count(connection, "memories"),
                    "agentRuns": _count(connection, "agent_runs"),
                    "cronJobs": len(cron_jobs),
                    "tools": len(tools),
                    "skills": len(skills),
                },
                "latest": {
                    "session": _latest_timestamp(connection, "sessions"),
                    "memory": _latest_timestamp(connection, "memories"),
                    "run": _latest_timestamp(connection, "agent_runs"),
                    "cron": max((str(job.get("updatedAt")) for job in cron_jobs), default=None),
                },
                "activeProvider": self.model_provider.describe(),
            },
            "clones": clones,
            "memory": memories,
            "sessions": sessions,
            "usage": usage,
            "models": {
                "activeProvider": self.model_provider.describe(),
                "providers": self.list_providers().get("providers", []),
                "doctor": self.doctor_provider(),
                "keys": self.list_provider_keys().get("keys", []),
            },
            "logs": _logs(state_dir),
            "skills": skills,
            "tools": tools,
            "cron": {
                "jobs": cron_jobs,
            },
            "gateway": _gateway(state_dir),
            "settings": settings,
        }


def patch_operator_settings(self, payload: Mapping[str, Any]) -> dict[str, Any]:
    database_path = self.repository.database_path
    profile_dir = _profile_dir_for_database(database_path)
    manifest = payload.get("profileManifest")
    if not isinstance(manifest, Mapping):
        raise ValueError("profileManifest must be an object")
    if not str(manifest.get("profile_id") or "").strip():
        raise ValueError("profileManifest.profile_id is required")
    write_profile_manifest(profile_dir, manifest)
    return {
        "status": "ok",
        "profileManifestPath": str(profile_dir / PROFILE_MANIFEST_FILENAME),
        "settings": _settings(profile_dir, database_path.parent, database_path),
    }


def patch_operator_global_config(self, payload: Mapping[str, Any]) -> dict[str, Any]:
    database_path = self.repository.database_path
    profile_dir = _profile_dir_for_database(database_path)
    state_dir = database_path.parent
    config_path = global_config_path_for_database(database_path)
    raw_text = payload.get("yamlText")
    if isinstance(raw_text, str):
        config = parse_global_config_text(raw_text)
    else:
        config = payload.get("config")
    if not isinstance(config, Mapping):
        raise ValueError("config must be an object or yamlText must parse to an object")
    write_global_config(config_path, config)
    next_settings = _settings(profile_dir, state_dir, database_path)
    return {
        "status": "ok",
        "globalConfigPath": str(config_path),
        "settings": next_settings,
    }


def set_console_item_enabled(self, *, kind: str, item_id: str, enabled: bool) -> dict[str, Any]:
    database_path = self.repository.database_path
    profile_dir = _profile_dir_for_database(database_path)
    manifest_path = profile_manifest_path(profile_dir)
    manifest = _read_json_file(manifest_path)
    if not isinstance(manifest, Mapping):
        manifest = {}
    section = "skill_overrides" if kind == "skill" else "tool_overrides"
    overrides = dict(manifest.get(section, {})) if isinstance(manifest.get(section), Mapping) else {}
    overrides[item_id] = {"enabled": bool(enabled)}
    next_manifest = dict(manifest)
    next_manifest[section] = overrides
    write_profile_manifest(profile_dir, next_manifest)
    runtime_status = "profile_override_written"
    if kind == "tool":
        try:
            self.tool_runtime.set_enabled(item_id, bool(enabled))
            runtime_status = "runtime_reloaded"
        except KeyError:
            runtime_status = "profile_override_written_tool_not_loaded"
    elif hasattr(self, "skill_runtime"):
        skill_runtime = getattr(self, "skill_runtime")
        try:
            skill_runtime.set_enabled(item_id, bool(enabled))
            runtime_status = "runtime_reloaded"
        except Exception:
            runtime_status = "profile_override_written_skill_not_loaded"
    return {
        "status": "ok",
        "kind": kind,
        "itemId": item_id,
        "enabled": bool(enabled),
        "runtimeStatus": runtime_status,
        "profileManifestPath": str(manifest_path),
    }


__all__ = [
    "inspect_operator_console",
    "patch_operator_settings",
    "patch_operator_global_config",
    "set_console_item_enabled",
    "gateway_action",
]
