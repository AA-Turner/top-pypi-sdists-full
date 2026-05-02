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

def upsert_procedure_library(self, library: ProcedureLibrary, *, updated_at: datetime | None = None) -> None:
    timestamp = _iso(updated_at)
    with self.connection() as connection:
        existing_library = connection.execute(
            "SELECT created_at FROM procedure_libraries WHERE profile_id = ?",
            (library.profile_id,),
        ).fetchone()
        created_at = str(existing_library["created_at"]) if existing_library is not None else timestamp
        connection.execute(
            """
            INSERT INTO procedure_libraries (profile_id, created_at, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                updated_at = excluded.updated_at
            """,
            (library.profile_id, created_at, timestamp),
        )

        existing_procedure_rows = connection.execute(
            "SELECT procedure_id, created_at FROM procedures WHERE profile_id = ?",
            (library.profile_id,),
        ).fetchall()
        existing_procedure_ids = {str(row["procedure_id"]) for row in existing_procedure_rows}
        created_by_procedure = {
            str(row["procedure_id"]): str(row["created_at"])
            for row in existing_procedure_rows
        }
        retained_procedure_ids = {procedure.procedure_id for procedure in library.procedures}

        for procedure in library.procedures:
            procedure_created_at = created_by_procedure.get(procedure.procedure_id, timestamp)
            connection.execute(
                """
                INSERT INTO procedures (
                    procedure_id,
                    profile_id,
                    title,
                    summary,
                    status,
                    trigger_refs_json,
                    evidence_refs_json,
                    verification_bundle_id,
                    skill_id,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(procedure_id) DO UPDATE SET
                    profile_id = excluded.profile_id,
                    title = excluded.title,
                    summary = excluded.summary,
                    status = excluded.status,
                    trigger_refs_json = excluded.trigger_refs_json,
                    evidence_refs_json = excluded.evidence_refs_json,
                    verification_bundle_id = excluded.verification_bundle_id,
                    skill_id = excluded.skill_id,
                    updated_at = excluded.updated_at
                """,
                (
                    procedure.procedure_id,
                    library.profile_id,
                    procedure.title,
                    procedure.summary,
                    procedure.status,
                    _json_text(procedure.trigger_refs),
                    _json_text(procedure.evidence_refs),
                    procedure.verification_bundle_id,
                    procedure.skill_id,
                    procedure_created_at,
                    timestamp,
                ),
            )
            existing_step_ids = {
                str(row["step_id"])
                for row in connection.execute(
                    "SELECT step_id FROM procedure_steps WHERE procedure_id = ?",
                    (procedure.procedure_id,),
                ).fetchall()
            }
            retained_step_ids = {step.step_id for step in procedure.steps}
            for step_order, step in enumerate(procedure.steps):
                connection.execute(
                    """
                    INSERT INTO procedure_steps (
                        step_id,
                        procedure_id,
                        step_order,
                        title,
                        instruction,
                        tool_name
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(step_id) DO UPDATE SET
                        procedure_id = excluded.procedure_id,
                        step_order = excluded.step_order,
                        title = excluded.title,
                        instruction = excluded.instruction,
                        tool_name = excluded.tool_name
                    """,
                    (
                        step.step_id,
                        procedure.procedure_id,
                        step_order,
                        step.title,
                        step.instruction,
                        step.tool_name,
                    ),
                )
            stale_step_ids = existing_step_ids - retained_step_ids
            if stale_step_ids:
                placeholders = ", ".join("?" for _ in stale_step_ids)
                connection.execute(
                    f"DELETE FROM procedure_steps WHERE step_id IN ({placeholders})",
                    tuple(sorted(stale_step_ids)),
                )

        stale_procedure_ids = existing_procedure_ids - retained_procedure_ids
        if stale_procedure_ids:
            placeholders = ", ".join("?" for _ in stale_procedure_ids)
            connection.execute(
                f"DELETE FROM procedures WHERE procedure_id IN ({placeholders})",
                tuple(sorted(stale_procedure_ids)),
            )
        connection.commit()

def load_procedure_library(self, profile_id: str) -> ProcedureLibrary | None:
    with self.connection() as connection:
        library_row = connection.execute(
            "SELECT profile_id FROM procedure_libraries WHERE profile_id = ?",
            (profile_id,),
        ).fetchone()
        procedure_rows = connection.execute(
            """
            SELECT procedure_id, title, summary, status, trigger_refs_json, evidence_refs_json,
                   verification_bundle_id, skill_id
            FROM procedures
            WHERE profile_id = ?
            ORDER BY updated_at DESC, created_at DESC, procedure_id ASC
            """,
            (profile_id,),
        ).fetchall()
        step_rows = connection.execute(
            """
            SELECT steps.step_id, steps.procedure_id, steps.step_order, steps.title,
                   steps.instruction, steps.tool_name
            FROM procedure_steps AS steps
            JOIN procedures ON procedures.procedure_id = steps.procedure_id
            WHERE procedures.profile_id = ?
            ORDER BY steps.procedure_id ASC, steps.step_order ASC, steps.step_id ASC
            """,
            (profile_id,),
        ).fetchall()
    if library_row is None and not procedure_rows:
        return None
    steps_by_procedure: dict[str, list[ProcedureStep]] = {}
    for row in step_rows:
        procedure_id = str(row["procedure_id"])
        steps_by_procedure.setdefault(procedure_id, []).append(
            ProcedureStep(
                step_id=str(row["step_id"]),
                title=str(row["title"]),
                instruction=str(row["instruction"]),
                tool_name=str(row["tool_name"]) if row["tool_name"] is not None else None,
            )
        )
    return ProcedureLibrary(
        profile_id=profile_id,
        procedures=tuple(
            ProcedureRecord(
                procedure_id=str(row["procedure_id"]),
                title=str(row["title"]),
                summary=str(row["summary"]),
                status=str(row["status"]),
                trigger_refs=_tuple_text(str(row["trigger_refs_json"])),
                evidence_refs=_tuple_text(str(row["evidence_refs_json"])),
                verification_bundle_id=(
                    str(row["verification_bundle_id"])
                    if row["verification_bundle_id"] is not None
                    else None
                ),
                skill_id=str(row["skill_id"]) if row["skill_id"] is not None else None,
                steps=tuple(steps_by_procedure.get(str(row["procedure_id"]), [])),
            )
            for row in procedure_rows
        ),
    )

def upsert_verification_bundle(self, bundle: VerificationBundle) -> None:
    timestamp = _iso(bundle.updated_at or _utc_now())
    created_at = _iso(bundle.created_at or bundle.verified_at or _utc_now())
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO verification_bundles (
                bundle_id,
                profile_id,
                candidate_id,
                method,
                status,
                notes,
                evidence_ids_json,
                scenario_ids_json,
                verified_at,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(bundle_id) DO UPDATE SET
                profile_id = excluded.profile_id,
                candidate_id = excluded.candidate_id,
                method = excluded.method,
                status = excluded.status,
                notes = excluded.notes,
                evidence_ids_json = excluded.evidence_ids_json,
                scenario_ids_json = excluded.scenario_ids_json,
                verified_at = excluded.verified_at,
                updated_at = excluded.updated_at
            """,
            (
                bundle.bundle_id,
                bundle.profile_id,
                bundle.candidate_id,
                bundle.method,
                bundle.status,
                bundle.notes,
                _json_text(bundle.evidence_ids),
                _json_text(bundle.scenario_ids),
                _iso(bundle.verified_at),
                created_at,
                timestamp,
            ),
        )
        connection.commit()

def load_verification_bundle(self, bundle_id: str) -> VerificationBundle | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT bundle_id, profile_id, candidate_id, method, status, notes,
                   evidence_ids_json, scenario_ids_json, verified_at, created_at, updated_at
            FROM verification_bundles
            WHERE bundle_id = ?
            """,
            (bundle_id,),
        ).fetchone()
    if row is None:
        return None
    return VerificationBundle(
        bundle_id=str(row["bundle_id"]),
        profile_id=str(row["profile_id"]),
        candidate_id=str(row["candidate_id"]),
        method=str(row["method"]),
        status=str(row["status"]),
        notes=str(row["notes"]),
        evidence_ids=_tuple_text(str(row["evidence_ids_json"])),
        scenario_ids=_tuple_text(str(row["scenario_ids_json"])),
        verified_at=_parse_datetime(str(row["verified_at"])) if row["verified_at"] is not None else None,
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )
