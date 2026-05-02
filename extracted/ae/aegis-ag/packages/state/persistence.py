"""Persist canonical personal-AI records with ledger tracking."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from uuid import uuid4

from .canonical import CanonicalProfileStateBundle
from packages.storage import (
    RuntimeStorageRepository,
    StoredIdentityLedgerEntry,
    StoredRelationshipLedgerEntry,
    StoredUserCardLedgerEntry,
)


@dataclass(frozen=True, slots=True)
class PersistedCanonicalState:
    clone_identity: object | None
    user_card: object | None
    relationship_memory: object | None


def load_persisted_canonical_state(repository: RuntimeStorageRepository, profile_id: str) -> PersistedCanonicalState:
    return PersistedCanonicalState(
        clone_identity=repository.load_clone_identity_for_profile(profile_id),
        user_card=repository.load_user_card_for_profile(profile_id),
        relationship_memory=repository.load_relationship_memory_for_profile(profile_id),
    )


def sync_canonical_profile_state(
    repository: RuntimeStorageRepository,
    bundle: CanonicalProfileStateBundle,
    *,
    previous: PersistedCanonicalState,
    sync_source: str,
) -> PersistedCanonicalState:
    synced_at = datetime.now(timezone.utc)
    profile_id = bundle.clone_identity.profile_id
    repository.upsert_clone_identity(bundle.clone_identity, updated_at=synced_at)
    repository.upsert_user_card(bundle.user_card, updated_at=synced_at)
    repository.upsert_relationship_memory(bundle.relationship_memory, updated_at=synced_at)
    metadata = {
        "profile_id": profile_id,
        "sync_source": sync_source,
    }
    if bundle.clone_identity.source_manifest_path is not None:
        metadata["manifest_path"] = bundle.clone_identity.source_manifest_path
    if bundle.clone_identity.source_clone_path is not None:
        metadata["clone_path"] = bundle.clone_identity.source_clone_path
    if bundle.user_card.source_user_profile_path is not None:
        metadata["user_profile_path"] = bundle.user_card.source_user_profile_path
    if _record_changed(previous.clone_identity, bundle.clone_identity):
        repository.append_identity_ledger(
            StoredIdentityLedgerEntry(
                entry_id=f"identity:{uuid4().hex}",
                clone_id=bundle.clone_identity.clone_id,
                profile_id=profile_id,
                action="canonical_sync",
                summary=f"synchronized canonical clone identity from {sync_source}",
                metadata={**metadata, "owner": "clone"},
                created_at=synced_at,
            )
        )
    if _record_changed(previous.user_card, bundle.user_card):
        repository.append_user_card_ledger(
            StoredUserCardLedgerEntry(
                entry_id=f"user-card:{uuid4().hex}",
                user_card_id=bundle.user_card.user_card_id,
                profile_id=profile_id,
                action="canonical_sync",
                summary=f"synchronized canonical user card from {sync_source}",
                metadata={**metadata, "owner": "user"},
                created_at=synced_at,
            )
        )
    if _record_changed(previous.relationship_memory, bundle.relationship_memory):
        repository.append_relationship_ledger(
            StoredRelationshipLedgerEntry(
                entry_id=f"relationship:{uuid4().hex}",
                relationship_id=bundle.relationship_memory.relationship_id,
                profile_id=profile_id,
                action="canonical_sync",
                summary=f"synchronized canonical relationship memory from {sync_source}",
                metadata={**metadata, "owner": "relationship"},
                created_at=synced_at,
            )
        )
    return load_persisted_canonical_state(repository, profile_id)


def _record_changed(previous, current) -> bool:
    if previous is None:
        return True
    return replace(previous, created_at=None, updated_at=None) != replace(
        current,
        created_at=None,
        updated_at=None,
    )
