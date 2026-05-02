"""Method group extracted from packages/storage/repository.py."""


from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Iterator, Mapping

from packages.auth.runtime import AuthProfile, EncryptedSecretValue, ProviderAuthState, SecretReference
from packages.contracts.runtime import (
    AgentRunState,
    AgentRunStep,
    ArtifactRecord,
    CloneIdentityRecord,
    EvidenceGraph,
    ExperienceRecord,
    GoalNode,
    MemoryRecord,
    ProcedureLibrary,
    ProcedureRecord,
    ProcedureStep,
    ProfileGraph,
    ProfileGrowthState,
    ProfileState,
    RelationshipMemoryRecord,
    SessionState,
    UserCardRecord,
    VerificationBundle,
    ActivityGraph,
)
from packages.planning import GoalGraph, goal_graph_to_activity_graph

MIGRATION_VERSION = 16
MIGRATIONS = {
    1: Path(__file__).with_name("migrations") / "0001_initial.sql",
    2: Path(__file__).with_name("migrations") / "0002_auth_profiles.sql",
    3: Path(__file__).with_name("migrations") / "0003_goal_graph.sql",
    4: Path(__file__).with_name("migrations") / "0004_memory_substrate.sql",
    5: Path(__file__).with_name("migrations") / "0005_agent_runs.sql",
    6: Path(__file__).with_name("migrations") / "0006_experiences.sql",
    7: Path(__file__).with_name("migrations") / "0007_profile_growth.sql",
    8: Path(__file__).with_name("migrations") / "0008_profiles_clone_path.sql",
    9: Path(__file__).with_name("migrations") / "0009_auth_secret_values.sql",
    10: Path(__file__).with_name("migrations") / "0010_provider_auth_states.sql",
    11: Path(__file__).with_name("migrations") / "0011_canonical_personal_ai_state.sql",
    12: Path(__file__).with_name("migrations") / "0012_evidence_and_procedure_graphs.sql",
    13: Path(__file__).with_name("migrations") / "0013_learning_verification_bundles.sql",
    14: Path(__file__).with_name("migrations") / "0014_structured_turn_memory_metadata.sql",
    15: Path(__file__).with_name("migrations") / "0015_activity_graph_cutover.sql",
    16: Path(__file__).with_name("migrations") / "0016_user_profile_source_column_rename.sql",
}



from .repository_support import (
    CanonicalRowFamily,
    LegacyOwnerCutover,
    MIGRATIONS,
    MIGRATION_VERSION,
    StorageBootstrapState,
    StorageCutoverManifest,
    StoredIdentityLedgerEntry,
    StoredMemoryLedgerEntry,
    StoredMemoryRecord,
    StoredRelationshipLedgerEntry,
    StoredUserCardLedgerEntry,
    _agent_run_from_row,
    _agent_run_step_from_row,
    _artifact_from_row,
    _clone_identity_from_row,
    _experience_from_row,
    _growth_from_row,
    _identity_ledger_from_row,
    _iso,
    _json_dict_text,
    _json_mapping,
    _json_text,
    _ledger_entry_from_row,
    _mapping_object,
    _mapping_text,
    _memory_contract_from_record,
    _parse_datetime,
    _record_from_row,
    _relationship_ledger_from_row,
    _relationship_memory_from_row,
    _tuple_text,
    _user_card_from_row,
    _user_card_ledger_from_row,
    _utc_now,
)


_AGENT_LOG_FILENAME = "agent.log"
_AGENT_LOG_PREVIEW_LIMIT = 500


def _compact_agent_log_value(value: str | None, *, limit: int = _AGENT_LOG_PREVIEW_LIMIT) -> str | None:
    if value is None:
        return None
    compacted = " ".join(value.split())
    if len(compacted) <= limit:
        return compacted
    return f"{compacted[: max(0, limit - 15)].rstrip()} ... [truncated]"


def _append_agent_log(self, payload: Mapping[str, object]) -> None:
    log_path = self.database_path.parent / _AGENT_LOG_FILENAME
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str))
            handle.write("\n")
    except OSError:
        return


def _record_agent_run_log(self, run: AgentRunState) -> None:
    payload: dict[str, object] = {
        "event": "agent.run",
        "timestamp": _iso(run.updated_at),
        "runId": run.run_id,
        "sessionId": run.session_id,
        "sourceEventId": run.source_event_id,
        "status": run.status,
        "phase": run.phase,
        "stepCount": run.step_count,
        "modelTurnCount": run.model_turn_count,
        "toolCallCount": run.tool_call_count,
    }
    if run.waiting_reason:
        payload["waitingReason"] = run.waiting_reason
    summary = _compact_agent_log_value(run.last_summary)
    if summary:
        payload["summary"] = summary
    _append_agent_log(self, payload)


def _record_agent_step_log(self, step: AgentRunStep) -> None:
    payload: dict[str, object] = {
        "event": "agent.step",
        "timestamp": _iso(step.created_at),
        "runId": step.run_id,
        "sessionId": step.session_id,
        "stepId": step.step_id,
        "stepIndex": step.step_index,
        "kind": step.kind,
        "title": step.title,
    }
    if step.outcome:
        payload["outcome"] = step.outcome
    if step.tool_name:
        payload["toolName"] = step.tool_name
    if step.kind != "context_prompt":
        preview = _compact_agent_log_value(step.content)
        if preview:
            payload["contentPreview"] = preview
    _append_agent_log(self, payload)


def upsert_agent_run(self, run: AgentRunState) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO agent_runs (
                run_id,
                session_id,
                source_event_id,
                prompt,
                status,
                phase,
                step_count,
                model_turn_count,
                tool_call_count,
                max_model_turns,
                max_wall_time_seconds,
                waiting_reason,
                continuation_prompt,
                last_summary,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id) DO UPDATE SET
                session_id = excluded.session_id,
                source_event_id = excluded.source_event_id,
                prompt = excluded.prompt,
                status = excluded.status,
                phase = excluded.phase,
                step_count = excluded.step_count,
                model_turn_count = excluded.model_turn_count,
                tool_call_count = excluded.tool_call_count,
                max_model_turns = excluded.max_model_turns,
                max_wall_time_seconds = excluded.max_wall_time_seconds,
                waiting_reason = excluded.waiting_reason,
                continuation_prompt = excluded.continuation_prompt,
                last_summary = excluded.last_summary,
                created_at = excluded.created_at,
                updated_at = excluded.updated_at
            """,
            (
                run.run_id,
                run.session_id,
                run.source_event_id,
                run.prompt,
                run.status,
                run.phase,
                run.step_count,
                run.model_turn_count,
                run.tool_call_count,
                run.max_model_turns,
                run.max_wall_time_seconds,
                run.waiting_reason,
                run.continuation_prompt,
                run.last_summary,
                _iso(run.created_at),
                _iso(run.updated_at),
            ),
        )
        connection.commit()
    _record_agent_run_log(self, run)

def load_agent_run(self, run_id: str) -> AgentRunState | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT run_id, session_id, source_event_id, prompt, status, phase,
                   step_count, model_turn_count, tool_call_count, max_model_turns,
                   max_wall_time_seconds, waiting_reason, continuation_prompt,
                   last_summary, created_at, updated_at
            FROM agent_runs
            WHERE run_id = ?
            """,
            (run_id,),
        ).fetchone()
    return _agent_run_from_row(row) if row is not None else None

def load_latest_open_agent_run(self, session_id: str) -> AgentRunState | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT run_id, session_id, source_event_id, prompt, status, phase,
                   step_count, model_turn_count, tool_call_count, max_model_turns,
                   max_wall_time_seconds, waiting_reason, continuation_prompt,
                   last_summary, created_at, updated_at
            FROM agent_runs
            WHERE session_id = ? AND status IN ('active', 'pending')
            ORDER BY updated_at DESC, created_at DESC
            LIMIT 1
            """,
            (session_id,),
        ).fetchone()
    return _agent_run_from_row(row) if row is not None else None

def list_agent_runs(
    self,
    session_id: str | None = None,
    *,
    statuses: tuple[str, ...] = (),
) -> tuple[AgentRunState, ...]:
    filters: list[str] = []
    parameters: list[object] = []
    if session_id is not None:
        filters.append("session_id = ?")
        parameters.append(session_id)
    if statuses:
        placeholders = ", ".join("?" for _ in statuses)
        filters.append(f"status IN ({placeholders})")
        parameters.extend(statuses)
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    with self.connection() as connection:
        rows = connection.execute(
            f"""
            SELECT run_id, session_id, source_event_id, prompt, status, phase,
                   step_count, model_turn_count, tool_call_count, max_model_turns,
                   max_wall_time_seconds, waiting_reason, continuation_prompt,
                   last_summary, created_at, updated_at
            FROM agent_runs
            {where_clause}
            ORDER BY updated_at DESC, created_at DESC
            """,
            tuple(parameters),
        ).fetchall()
    return tuple(_agent_run_from_row(row) for row in rows)

def append_agent_run_step(self, step: AgentRunStep) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO agent_run_steps (
                step_id,
                run_id,
                session_id,
                step_index,
                kind,
                title,
                content,
                outcome,
                tool_name,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                step.step_id,
                step.run_id,
                step.session_id,
                step.step_index,
                step.kind,
                step.title,
                step.content,
                step.outcome,
                step.tool_name,
                _iso(step.created_at),
            ),
        )
        connection.commit()
    _record_agent_step_log(self, step)

def list_agent_run_steps(self, run_id: str, *, limit: int | None = None) -> tuple[AgentRunStep, ...]:
    limit_clause = "LIMIT ?" if limit is not None else ""
    parameters: tuple[object, ...]
    if limit is None:
        parameters = (run_id,)
    else:
        parameters = (run_id, limit)
    with self.connection() as connection:
        rows = connection.execute(
            f"""
            SELECT step_id, run_id, session_id, step_index, kind, title, content,
                   outcome, tool_name, created_at
            FROM agent_run_steps
            WHERE run_id = ?
            ORDER BY step_index DESC
            {limit_clause}
            """,
            parameters,
        ).fetchall()
    steps = tuple(_agent_run_step_from_row(row) for row in rows)
    return tuple(reversed(steps))

def upsert_experience(self, experience: ExperienceRecord) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO experiences (
                experience_id,
                session_id,
                profile_id,
                workspace_id,
                run_id,
                source_event_id,
                kind,
                title,
                summary,
                status,
                goal_id,
                tool_call_count,
                model_turn_count,
                related_skill_ids_json,
                produced_artifact_ids_json,
                tags_json,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(experience_id) DO UPDATE SET
                session_id = excluded.session_id,
                profile_id = excluded.profile_id,
                workspace_id = excluded.workspace_id,
                run_id = excluded.run_id,
                source_event_id = excluded.source_event_id,
                kind = excluded.kind,
                title = excluded.title,
                summary = excluded.summary,
                status = excluded.status,
                goal_id = excluded.goal_id,
                tool_call_count = excluded.tool_call_count,
                model_turn_count = excluded.model_turn_count,
                related_skill_ids_json = excluded.related_skill_ids_json,
                produced_artifact_ids_json = excluded.produced_artifact_ids_json,
                tags_json = excluded.tags_json,
                created_at = excluded.created_at,
                updated_at = excluded.updated_at
            """,
            (
                experience.experience_id,
                experience.session_id,
                experience.profile_id,
                experience.workspace_id,
                experience.run_id,
                experience.source_event_id,
                experience.kind,
                experience.title,
                experience.summary,
                experience.status,
                experience.goal_id,
                experience.tool_call_count,
                experience.model_turn_count,
                _json_text(experience.related_skill_ids),
                _json_text(experience.produced_artifact_ids),
                _json_text(experience.tags),
                _iso(experience.created_at),
                _iso(experience.updated_at),
            ),
        )
        connection.commit()

def load_experience(self, experience_id: str) -> ExperienceRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT experience_id, session_id, profile_id, workspace_id, run_id,
                   source_event_id, kind, title, summary, status, goal_id,
                   tool_call_count, model_turn_count, related_skill_ids_json,
                   produced_artifact_ids_json, tags_json, created_at, updated_at
            FROM experiences
            WHERE experience_id = ?
            """,
            (experience_id,),
        ).fetchone()
    return _experience_from_row(row) if row is not None else None

def load_profile_growth(self, profile_id: str) -> ProfileGrowthState | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT profile_id, growth_score, total_dialogues, total_tokens,
                   total_experiences, promoted_experiences, active_days,
                   streak_days, first_dialogue_at, last_dialogue_at,
                   last_active_day, created_at, updated_at
            FROM profile_growth
            WHERE profile_id = ?
            """,
            (profile_id,),
        ).fetchone()
    return _growth_from_row(row) if row is not None else None

def upsert_profile_growth(self, growth: ProfileGrowthState) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO profile_growth (
                profile_id,
                growth_score,
                total_dialogues,
                total_tokens,
                total_experiences,
                promoted_experiences,
                active_days,
                streak_days,
                first_dialogue_at,
                last_dialogue_at,
                last_active_day,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                growth_score = excluded.growth_score,
                total_dialogues = excluded.total_dialogues,
                total_tokens = excluded.total_tokens,
                total_experiences = excluded.total_experiences,
                promoted_experiences = excluded.promoted_experiences,
                active_days = excluded.active_days,
                streak_days = excluded.streak_days,
                first_dialogue_at = excluded.first_dialogue_at,
                last_dialogue_at = excluded.last_dialogue_at,
                last_active_day = excluded.last_active_day,
                created_at = excluded.created_at,
                updated_at = excluded.updated_at
            """,
            (
                growth.profile_id,
                growth.growth_score,
                growth.total_dialogues,
                growth.total_tokens,
                growth.total_experiences,
                growth.promoted_experiences,
                growth.active_days,
                growth.streak_days,
                _iso(growth.first_dialogue_at) if growth.first_dialogue_at is not None else None,
                _iso(growth.last_dialogue_at) if growth.last_dialogue_at is not None else None,
                growth.last_active_day,
                _iso(growth.created_at),
                _iso(growth.updated_at),
            ),
        )
        connection.commit()

def list_experiences(
    self,
    session_id: str | None = None,
    *,
    profile_id: str | None = None,
    statuses: tuple[str, ...] = (),
    limit: int | None = None,
) -> tuple[ExperienceRecord, ...]:
    if limit is not None and limit <= 0:
        return ()
    filters: list[str] = []
    parameters: list[object] = []
    if session_id is not None:
        filters.append("session_id = ?")
        parameters.append(session_id)
    if profile_id is not None:
        filters.append("profile_id = ?")
        parameters.append(profile_id)
    if statuses:
        placeholders = ", ".join("?" for _ in statuses)
        filters.append(f"status IN ({placeholders})")
        parameters.extend(statuses)
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    limit_clause = ""
    if limit is not None:
        limit_clause = "LIMIT ?"
        parameters.append(limit)
    with self.connection() as connection:
        rows = connection.execute(
            f"""
            SELECT experience_id, session_id, profile_id, workspace_id, run_id,
                   source_event_id, kind, title, summary, status, goal_id,
                   tool_call_count, model_turn_count, related_skill_ids_json,
                   produced_artifact_ids_json, tags_json, created_at, updated_at
            FROM experiences
            {where_clause}
            ORDER BY updated_at DESC, created_at DESC
            {limit_clause}
            """,
            tuple(parameters),
        ).fetchall()
    return tuple(_experience_from_row(row) for row in rows)
