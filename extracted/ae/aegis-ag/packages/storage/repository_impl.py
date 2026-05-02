"""Runtime storage repository implementation assembled from smaller method groups."""


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

MIGRATION_VERSION = 20
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
    17: Path(__file__).with_name("migrations") / "0017_user_card_durable_notes.sql",
    18: Path(__file__).with_name("migrations") / "0018_token_usage_events.sql",
    19: Path(__file__).with_name("migrations") / "0019_activity_node_projection_identity.sql",
    20: Path(__file__).with_name("migrations") / "0020_agent_run_wall_time_budget.sql",
}



from .repository_support import (
    CanonicalRowFamily,
    LegacyOwnerCutover,
    StorageBootstrapState,
    StorageCutoverManifest,
    StoredIdentityLedgerEntry,
    StoredMemoryLedgerEntry,
    StoredMemoryRecord,
    StoredRelationshipLedgerEntry,
    StoredUserCardLedgerEntry,
)
from . import repository_auth_methods as _auth_methods
from . import repository_bootstrap_methods as _bootstrap_methods
from . import repository_memory_methods as _memory_methods
from . import repository_procedure_methods as _procedure_methods
from . import repository_profile_methods as _profile_methods
from . import repository_run_methods as _run_methods
from . import repository_session_methods as _session_methods
from . import repository_usage_methods as _usage_methods

class RuntimeStorageRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)

RuntimeStorageRepository.bootstrap = _bootstrap_methods.bootstrap
RuntimeStorageRepository.connection = _bootstrap_methods.connection
RuntimeStorageRepository.schema_version = _bootstrap_methods.schema_version

RuntimeStorageRepository.upsert_profile = _profile_methods.upsert_profile
RuntimeStorageRepository.load_profile = _profile_methods.load_profile
RuntimeStorageRepository.upsert_clone_identity = _profile_methods.upsert_clone_identity
RuntimeStorageRepository.load_clone_identity = _profile_methods.load_clone_identity
RuntimeStorageRepository.load_clone_identity_for_profile = _profile_methods.load_clone_identity_for_profile
RuntimeStorageRepository.upsert_user_card = _profile_methods.upsert_user_card
RuntimeStorageRepository.load_user_card = _profile_methods.load_user_card
RuntimeStorageRepository.load_user_card_for_profile = _profile_methods.load_user_card_for_profile
RuntimeStorageRepository.upsert_relationship_memory = _profile_methods.upsert_relationship_memory
RuntimeStorageRepository.load_relationship_memory = _profile_methods.load_relationship_memory
RuntimeStorageRepository.load_relationship_memory_for_profile = _profile_methods.load_relationship_memory_for_profile
RuntimeStorageRepository.load_profile_graph = _profile_methods.load_profile_graph
RuntimeStorageRepository.canonical_cutover_manifest = _profile_methods.canonical_cutover_manifest
RuntimeStorageRepository.append_identity_ledger = _profile_methods.append_identity_ledger
RuntimeStorageRepository.list_identity_ledger = _profile_methods.list_identity_ledger
RuntimeStorageRepository.append_user_card_ledger = _profile_methods.append_user_card_ledger
RuntimeStorageRepository.list_user_card_ledger = _profile_methods.list_user_card_ledger
RuntimeStorageRepository.append_relationship_ledger = _profile_methods.append_relationship_ledger
RuntimeStorageRepository.list_relationship_ledger = _profile_methods.list_relationship_ledger

RuntimeStorageRepository.upsert_session = _session_methods.upsert_session
RuntimeStorageRepository.load_session = _session_methods.load_session
RuntimeStorageRepository.upsert_activity_graph = _session_methods.upsert_activity_graph
RuntimeStorageRepository.load_activity_graph = _session_methods.load_activity_graph
RuntimeStorageRepository.record_resume = _session_methods.record_resume
RuntimeStorageRepository.lineage = _session_methods.lineage
RuntimeStorageRepository.refresh_session = _session_methods.refresh_session
RuntimeStorageRepository.delete_sessions = _session_methods.delete_sessions
RuntimeStorageRepository.delete_orphaned_profiles = _session_methods.delete_orphaned_profiles

RuntimeStorageRepository.upsert_agent_run = _run_methods.upsert_agent_run
RuntimeStorageRepository.load_agent_run = _run_methods.load_agent_run
RuntimeStorageRepository.load_latest_open_agent_run = _run_methods.load_latest_open_agent_run
RuntimeStorageRepository.list_agent_runs = _run_methods.list_agent_runs
RuntimeStorageRepository.append_agent_run_step = _run_methods.append_agent_run_step
RuntimeStorageRepository.list_agent_run_steps = _run_methods.list_agent_run_steps
RuntimeStorageRepository.upsert_experience = _run_methods.upsert_experience
RuntimeStorageRepository.load_experience = _run_methods.load_experience
RuntimeStorageRepository.load_profile_growth = _run_methods.load_profile_growth
RuntimeStorageRepository.upsert_profile_growth = _run_methods.upsert_profile_growth
RuntimeStorageRepository.list_experiences = _run_methods.list_experiences
RuntimeStorageRepository.record_token_usage = _usage_methods.record_token_usage
RuntimeStorageRepository.list_token_usage_events = _usage_methods.list_token_usage_events

RuntimeStorageRepository.upsert_procedure_library = _procedure_methods.upsert_procedure_library
RuntimeStorageRepository.load_procedure_library = _procedure_methods.load_procedure_library
RuntimeStorageRepository.upsert_verification_bundle = _procedure_methods.upsert_verification_bundle
RuntimeStorageRepository.load_verification_bundle = _procedure_methods.load_verification_bundle

RuntimeStorageRepository.append_memory_ledger = _memory_methods.append_memory_ledger
RuntimeStorageRepository.list_memory_ledger = _memory_methods.list_memory_ledger
RuntimeStorageRepository.upsert_memory_record = _memory_methods.upsert_memory_record
RuntimeStorageRepository.load_memory_record = _memory_methods.load_memory_record
RuntimeStorageRepository.list_memory_records = _memory_methods.list_memory_records
RuntimeStorageRepository.upsert_artifact_record = _memory_methods.upsert_artifact_record
RuntimeStorageRepository.load_artifact_record = _memory_methods.load_artifact_record
RuntimeStorageRepository.list_artifact_records = _memory_methods.list_artifact_records
RuntimeStorageRepository.upsert_evidence_graph = _memory_methods.upsert_evidence_graph
RuntimeStorageRepository.load_evidence_graph = _memory_methods.load_evidence_graph
RuntimeStorageRepository.mark_memory_consolidated = _memory_methods.mark_memory_consolidated
RuntimeStorageRepository.mark_memory_superseded = _memory_methods.mark_memory_superseded
RuntimeStorageRepository.mark_memory_deleted = _memory_methods.mark_memory_deleted
RuntimeStorageRepository.memory_state = _memory_methods.memory_state
RuntimeStorageRepository.memory_lineage = _memory_methods.memory_lineage

RuntimeStorageRepository.upsert_auth_profile = _auth_methods.upsert_auth_profile
RuntimeStorageRepository.upsert_auth_secret_value = _auth_methods.upsert_auth_secret_value
RuntimeStorageRepository.load_auth_secret_value = _auth_methods.load_auth_secret_value
RuntimeStorageRepository.has_auth_secret_value = _auth_methods.has_auth_secret_value
RuntimeStorageRepository.delete_auth_secret_value = _auth_methods.delete_auth_secret_value
RuntimeStorageRepository.load_auth_profile = _auth_methods.load_auth_profile
RuntimeStorageRepository.list_auth_profiles = _auth_methods.list_auth_profiles
RuntimeStorageRepository.select_auth_profile = _auth_methods.select_auth_profile
RuntimeStorageRepository.upsert_provider_auth_state = _auth_methods.upsert_provider_auth_state
RuntimeStorageRepository.load_provider_auth_state = _auth_methods.load_provider_auth_state
RuntimeStorageRepository.list_provider_auth_states = _auth_methods.list_provider_auth_states

__all__ = [
    "CanonicalRowFamily",
    "LegacyOwnerCutover",
    "RuntimeStorageRepository",
    "StorageBootstrapState",
    "StorageCutoverManifest",
    "StoredIdentityLedgerEntry",
    "StoredMemoryLedgerEntry",
    "StoredMemoryRecord",
    "StoredRelationshipLedgerEntry",
    "StoredUserCardLedgerEntry",
]
