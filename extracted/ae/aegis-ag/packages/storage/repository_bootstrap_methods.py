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

def bootstrap(self) -> StorageBootstrapState:
    self.database_path.parent.mkdir(parents=True, exist_ok=True)
    with self.connection() as connection:
        version = self.schema_version(connection)
        if version > MIGRATION_VERSION:
            raise RuntimeError(
                f"database schema version {version} is newer than supported "
                f"migration version {MIGRATION_VERSION}"
            )
        for target_version in range(version + 1, MIGRATION_VERSION + 1):
            migration_file = MIGRATIONS[target_version]
            migration_sql = migration_file.read_text(encoding="utf-8")
            connection.executescript(migration_sql)
            connection.execute(
                "INSERT OR REPLACE INTO schema_migrations(version, applied_at) VALUES(?, ?)",
                (target_version, _iso(None)),
            )
            connection.commit()
    return StorageBootstrapState(
        database_path=str(self.database_path),
        schema_version=MIGRATION_VERSION,
    )

@contextmanager
def connection(self) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(self.database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
    finally:
        connection.close()

def schema_version(self, connection: sqlite3.Connection | None = None) -> int:
    owns_connection = connection is None
    if owns_connection:
        with self.connection() as owned_connection:
            return self.schema_version(owned_connection)

    assert connection is not None
    try:
        row = connection.execute(
            "SELECT MAX(version) AS version FROM schema_migrations"
        ).fetchone()
    except sqlite3.OperationalError:
        return 0
    if row is None or row["version"] is None:
        return 0
    return int(row["version"])
