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

def upsert_auth_profile(self, profile: AuthProfile, *, updated_at: datetime | None = None) -> None:
    timestamp = _iso(updated_at)
    created_at = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM auth_profiles WHERE profile_id = ?",
            (profile.profile_id,),
        ).fetchone()
        if existing is not None:
            created_at = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO auth_profiles (
                profile_id,
                provider_id,
                transport_id,
                base_url,
                default_model,
                auth_method,
                provider_kind,
                extra_headers_json,
                priority,
                session_pin,
                cooldown_until,
                metadata_json,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                provider_id = excluded.provider_id,
                transport_id = excluded.transport_id,
                base_url = excluded.base_url,
                default_model = excluded.default_model,
                auth_method = excluded.auth_method,
                provider_kind = excluded.provider_kind,
                extra_headers_json = excluded.extra_headers_json,
                priority = excluded.priority,
                session_pin = excluded.session_pin,
                cooldown_until = excluded.cooldown_until,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at
            """,
            (
                profile.profile_id,
                profile.provider_id,
                profile.transport_id,
                profile.base_url,
                profile.default_model,
                profile.auth_method,
                profile.provider_kind,
                _json_mapping(dict(profile.extra_headers)),
                profile.priority,
                profile.session_pin,
                _iso(profile.cooldown_until) if profile.cooldown_until is not None else None,
                _json_mapping(dict(profile.metadata)),
                created_at,
                timestamp,
            ),
        )
        existing_reference_rows = connection.execute(
            "SELECT reference_id FROM auth_secret_references WHERE profile_id = ?",
            (profile.profile_id,),
        ).fetchall()
        existing_reference_ids = {
            str(row["reference_id"])
            for row in existing_reference_rows
        }
        desired_reference_ids = {reference.reference_id for reference in profile.secret_references}
        for order_index, reference in enumerate(profile.secret_references):
            connection.execute(
                """
                INSERT INTO auth_secret_references (
                    reference_id,
                    profile_id,
                    provider_id,
                    secret_name,
                    secret_key,
                    source,
                    reference_order,
                    metadata_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(reference_id) DO UPDATE SET
                    profile_id = excluded.profile_id,
                    provider_id = excluded.provider_id,
                    secret_name = excluded.secret_name,
                    secret_key = excluded.secret_key,
                    source = excluded.source,
                    reference_order = excluded.reference_order,
                    metadata_json = excluded.metadata_json
                """,
                (
                    reference.reference_id,
                    profile.profile_id,
                    reference.provider_id,
                    reference.secret_name,
                    reference.secret_key,
                    reference.source,
                    order_index,
                    _json_mapping(dict(reference.metadata)),
                    created_at,
                ),
            )
        stale_reference_ids = tuple(sorted(existing_reference_ids - desired_reference_ids))
        if stale_reference_ids:
            placeholders = ", ".join("?" for _ in stale_reference_ids)
            connection.execute(
                f"DELETE FROM auth_secret_references WHERE reference_id IN ({placeholders})",
                stale_reference_ids,
            )
        connection.commit()

def upsert_auth_secret_value(
    self,
    value: EncryptedSecretValue,
    *,
    updated_at: datetime | None = None,
) -> None:
    timestamp = _iso(updated_at)
    created_at = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM auth_secret_values WHERE reference_id = ?",
            (value.reference_id,),
        ).fetchone()
        if existing is not None:
            created_at = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO auth_secret_values (
                reference_id,
                key_id,
                nonce_b64,
                ciphertext_b64,
                mac_hex,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(reference_id) DO UPDATE SET
                key_id = excluded.key_id,
                nonce_b64 = excluded.nonce_b64,
                ciphertext_b64 = excluded.ciphertext_b64,
                mac_hex = excluded.mac_hex,
                updated_at = excluded.updated_at
            """,
            (
                value.reference_id,
                value.key_id,
                value.nonce_b64,
                value.ciphertext_b64,
                value.mac_hex,
                created_at,
                timestamp,
            ),
        )
        connection.commit()

def load_auth_secret_value(self, reference_id: str) -> EncryptedSecretValue | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT reference_id, key_id, nonce_b64, ciphertext_b64, mac_hex
            FROM auth_secret_values
            WHERE reference_id = ?
            """,
            (reference_id,),
        ).fetchone()
    if row is None:
        return None
    return EncryptedSecretValue(
        reference_id=str(row["reference_id"]),
        key_id=str(row["key_id"]),
        nonce_b64=str(row["nonce_b64"]),
        ciphertext_b64=str(row["ciphertext_b64"]),
        mac_hex=str(row["mac_hex"]),
    )

def has_auth_secret_value(self, reference_id: str) -> bool:
    with self.connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM auth_secret_values WHERE reference_id = ?",
            (reference_id,),
        ).fetchone()
    return row is not None

def delete_auth_secret_value(self, reference_id: str) -> None:
    with self.connection() as connection:
        connection.execute(
            "DELETE FROM auth_secret_values WHERE reference_id = ?",
            (reference_id,),
        )
        connection.commit()

def load_auth_profile(self, profile_id: str) -> AuthProfile | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT profile_id, provider_id, transport_id, base_url, default_model,
                   auth_method, provider_kind, extra_headers_json, priority,
                   session_pin, cooldown_until, metadata_json
            FROM auth_profiles
            WHERE profile_id = ?
            """,
            (profile_id,),
        ).fetchone()
        if row is None:
            return None
        references = connection.execute(
            """
            SELECT reference_id, provider_id, secret_name, secret_key, source, metadata_json
            FROM auth_secret_references
            WHERE profile_id = ?
            ORDER BY reference_order ASC, reference_id ASC
            """,
            (profile_id,),
        ).fetchall()
    return AuthProfile(
        profile_id=str(row["profile_id"]),
        provider_id=str(row["provider_id"]),
        transport_id=str(row["transport_id"]),
        base_url=str(row["base_url"]) if row["base_url"] is not None else None,
        default_model=str(row["default_model"]) if row["default_model"] is not None else None,
        auth_method=str(row["auth_method"]),
        provider_kind=str(row["provider_kind"]),
        extra_headers=_mapping_text(str(row["extra_headers_json"])),
        secret_references=tuple(
            SecretReference(
                reference_id=str(reference["reference_id"]),
                provider_id=str(reference["provider_id"]),
                secret_name=str(reference["secret_name"]),
                secret_key=str(reference["secret_key"]),
                source=str(reference["source"]),
                metadata=_mapping_text(str(reference["metadata_json"])),
            )
            for reference in references
        ),
        priority=int(row["priority"]),
        session_pin=str(row["session_pin"]) if row["session_pin"] is not None else None,
        cooldown_until=_parse_datetime(str(row["cooldown_until"])) if row["cooldown_until"] is not None else None,
        metadata=_mapping_text(str(row["metadata_json"])),
    )

def list_auth_profiles(self, provider_id: str | None = None) -> tuple[AuthProfile, ...]:
    with self.connection() as connection:
        if provider_id is None:
            rows = connection.execute(
                """
                SELECT profile_id
                FROM auth_profiles
                ORDER BY provider_id ASC, priority DESC, profile_id ASC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT profile_id
                FROM auth_profiles
                WHERE provider_id = ?
                ORDER BY priority DESC, profile_id ASC
                """,
                (provider_id,),
            ).fetchall()
    profiles = []
    for row in rows:
        profile = self.load_auth_profile(str(row["profile_id"]))
        if profile is not None:
            profiles.append(profile)
    return tuple(profiles)

def select_auth_profile(self, provider_id: str) -> AuthProfile:
    profiles = sorted(
        self.list_auth_profiles(provider_id),
        key=lambda profile: (-profile.priority, profile.profile_id),
    )
    if not profiles:
        raise LookupError(f"no auth profile registered for provider: {provider_id}")
    return profiles[0]

def upsert_provider_auth_state(
    self,
    state: ProviderAuthState,
    *,
    updated_at: datetime | None = None,
) -> None:
    timestamp = _iso(updated_at)
    discovered_at = _iso(state.discovered_at) if state.discovered_at is not None else timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT discovered_at FROM provider_auth_states WHERE provider_id = ?",
            (state.provider_id,),
        ).fetchone()
        if existing is not None and existing["discovered_at"] is not None:
            discovered_at = str(existing["discovered_at"])
        connection.execute(
            """
            INSERT INTO provider_auth_states (
                provider_id,
                auth_type,
                status,
                source,
                profile_id,
                transport_id,
                provider_kind,
                base_url,
                default_model,
                runtime_enabled,
                summary,
                metadata_json,
                discovered_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(provider_id) DO UPDATE SET
                auth_type = excluded.auth_type,
                status = excluded.status,
                source = excluded.source,
                profile_id = excluded.profile_id,
                transport_id = excluded.transport_id,
                provider_kind = excluded.provider_kind,
                base_url = excluded.base_url,
                default_model = excluded.default_model,
                runtime_enabled = excluded.runtime_enabled,
                summary = excluded.summary,
                metadata_json = excluded.metadata_json,
                updated_at = excluded.updated_at
            """,
            (
                state.provider_id,
                state.auth_type,
                state.status,
                state.source,
                state.profile_id,
                state.transport_id,
                state.provider_kind,
                state.base_url,
                state.default_model,
                1 if state.runtime_enabled else 0,
                state.summary,
                _json_mapping(dict(state.metadata)),
                discovered_at,
                timestamp,
            ),
        )
        connection.commit()

def load_provider_auth_state(self, provider_id: str) -> ProviderAuthState | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT provider_id, auth_type, status, source, profile_id, transport_id,
                   provider_kind, base_url, default_model, runtime_enabled, summary,
                   metadata_json, discovered_at, updated_at
            FROM provider_auth_states
            WHERE provider_id = ?
            """,
            (provider_id,),
        ).fetchone()
    if row is None:
        return None
    return ProviderAuthState(
        provider_id=str(row["provider_id"]),
        auth_type=str(row["auth_type"]),
        status=str(row["status"]),
        source=str(row["source"]),
        profile_id=str(row["profile_id"]) if row["profile_id"] is not None else None,
        transport_id=str(row["transport_id"]) if row["transport_id"] is not None else None,
        provider_kind=str(row["provider_kind"]),
        base_url=str(row["base_url"]) if row["base_url"] is not None else None,
        default_model=str(row["default_model"]) if row["default_model"] is not None else None,
        runtime_enabled=bool(int(row["runtime_enabled"])),
        summary=str(row["summary"] or ""),
        metadata=_mapping_text(str(row["metadata_json"])),
        discovered_at=_parse_datetime(str(row["discovered_at"])) if row["discovered_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )

def list_provider_auth_states(self) -> tuple[ProviderAuthState, ...]:
    with self.connection() as connection:
        rows = connection.execute(
            """
            SELECT provider_id
            FROM provider_auth_states
            ORDER BY provider_id ASC
            """
        ).fetchall()
    states: list[ProviderAuthState] = []
    for row in rows:
        state = self.load_provider_auth_state(str(row["provider_id"]))
        if state is not None:
            states.append(state)
    return tuple(states)
