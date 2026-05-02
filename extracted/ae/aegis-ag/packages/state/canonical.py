"""Canonical identity, user, and relationship builders for loaded profiles."""

from __future__ import annotations

from dataclasses import dataclass

from packages.contracts import CloneIdentityRecord, ProfileGraph, RelationshipMemoryRecord, UserCardRecord

from .governance import (
    build_companion_identity_state,
    parse_user_profile_content,
    resolved_companion_settings,
    user_biography_field_ids,
)
from .loader import LoadedProfile


@dataclass(frozen=True, slots=True)
class CanonicalProfileIds:
    clone_id: str
    user_card_id: str
    relationship_id: str


@dataclass(frozen=True, slots=True)
class CanonicalProfileStateBundle:
    profile_graph: ProfileGraph
    clone_identity: CloneIdentityRecord
    user_card: UserCardRecord
    relationship_memory: RelationshipMemoryRecord


def canonical_profile_ids(profile_id: str) -> CanonicalProfileIds:
    normalized = profile_id.strip() or "default"
    return CanonicalProfileIds(
        clone_id=f"{normalized}:clone",
        user_card_id=f"{normalized}:user-card",
        relationship_id=f"{normalized}:relationship",
    )


def build_canonical_profile_state(
    profile: LoadedProfile,
    *,
    clone_id: str | None = None,
    user_card_id: str | None = None,
    relationship_id: str | None = None,
) -> CanonicalProfileStateBundle:
    ids = canonical_profile_ids(profile.state.profile_id)
    resolved_clone_id = clone_id or ids.clone_id
    resolved_user_card_id = user_card_id or ids.user_card_id
    resolved_relationship_id = relationship_id or ids.relationship_id
    clone_identity = build_clone_identity_record(profile, clone_id=resolved_clone_id)
    user_card = build_user_card_record(profile, user_card_id=resolved_user_card_id)
    relationship_memory = build_relationship_memory_record(
        profile,
        clone_id=resolved_clone_id,
        user_card_id=resolved_user_card_id,
        relationship_id=resolved_relationship_id,
    )
    return CanonicalProfileStateBundle(
        profile_graph=build_profile_graph(
            profile,
            clone_identity=clone_identity,
            user_card=user_card,
            relationship_memory=relationship_memory,
        ),
        clone_identity=clone_identity,
        user_card=user_card,
        relationship_memory=relationship_memory,
    )


def build_profile_graph(
    profile: LoadedProfile,
    *,
    clone_identity: CloneIdentityRecord | None = None,
    user_card: UserCardRecord | None = None,
    relationship_memory: RelationshipMemoryRecord | None = None,
) -> ProfileGraph:
    resolved_clone_identity = clone_identity or build_clone_identity_record(profile)
    resolved_user_card = user_card or build_user_card_record(profile)
    resolved_relationship_memory = relationship_memory or build_relationship_memory_record(
        profile,
        clone_id=resolved_clone_identity.clone_id,
        user_card_id=resolved_user_card.user_card_id,
    )
    return ProfileGraph(
        profile=profile.state,
        clone_identity=resolved_clone_identity,
        user_card=resolved_user_card,
        relationship_memory=resolved_relationship_memory,
    )


def build_clone_identity_record(
    profile: LoadedProfile,
    *,
    clone_id: str | None = None,
) -> CloneIdentityRecord:
    identity = build_companion_identity_state(profile)
    companion = resolved_companion_settings(profile)
    ids = canonical_profile_ids(profile.state.profile_id)
    return CloneIdentityRecord(
        clone_id=clone_id or ids.clone_id,
        profile_id=profile.state.profile_id,
        display_name=identity.display_name,
        identity_mode=identity.mode,
        personality_preset=identity.personality_preset,
        initiative=identity.initiative,
        relational_stance=identity.relational_stance,
        voice_contract=identity.voice_identity_summary,
        working_style_contract=identity.personality_summary,
        charter_extension=_strip_or_none(profile.clone_text),
        governance_flags=_governance_flags(companion),
        source_manifest_path=profile.manifest_path,
        source_clone_path=profile.state.clone_path,
    )


def build_user_card_record(
    profile: LoadedProfile,
    *,
    user_card_id: str | None = None,
) -> UserCardRecord:
    parsed_profile = parse_user_profile_content(profile.user_profile_text or "")
    fields = dict(parsed_profile.field_values)
    locale = _strip_or_none(str(profile.manifest.get("locale") or ""))
    timezone = _strip_or_none(str(profile.manifest.get("timezone") or ""))
    communication_preferences, shared_preferences = _split_profile_preferences(profile.state.preferences)
    biography_fragments = _biography_fragments(fields)
    boundaries = _maybe_singleton(fields.get("boundaries"))
    ids = canonical_profile_ids(profile.state.profile_id)
    return UserCardRecord(
        user_card_id=user_card_id or ids.user_card_id,
        profile_id=profile.state.profile_id,
        preferred_name=_strip_or_none(fields.get("preferred_name")),
        locale=locale,
        timezone=timezone,
        communication_preferences=communication_preferences,
        boundaries=boundaries,
        biography_fragments=biography_fragments,
        durable_notes=parsed_profile.durable_notes,
        shared_preferences=shared_preferences,
        source_user_profile_path=profile.user_profile_path,
    )


def build_relationship_memory_record(
    profile: LoadedProfile,
    *,
    clone_id: str | None = None,
    user_card_id: str | None = None,
    relationship_id: str | None = None,
) -> RelationshipMemoryRecord:
    ids = canonical_profile_ids(profile.state.profile_id)
    companion = resolved_companion_settings(profile)
    identity = build_companion_identity_state(profile)
    return RelationshipMemoryRecord(
        relationship_id=relationship_id or ids.relationship_id,
        profile_id=profile.state.profile_id,
        clone_id=clone_id or ids.clone_id,
        user_card_id=user_card_id or ids.user_card_id,
        interaction_preferences=_interaction_preferences(companion),
        expectations=(
            f"initiative:{companion.initiative}",
            f"relational_stance:{identity.relational_stance}",
            f"personality_label:{identity.personality_label}",
        ),
        continuity_notes=tuple(note.strip() for note in companion.notes if note.strip()),
    )


def _governance_flags(companion) -> tuple[str, ...]:
    flags = [
        "text-first" if companion.text_first else "voice-capable",
        "preserve-relationship-timeline" if companion.preserve_relationship_timeline else "limit-relationship-timeline",
        "preserve-preferences" if companion.preserve_preferences else "limit-preferences",
        "preserve-corrections" if companion.preserve_corrections else "limit-corrections",
        "preserve-emotional-context" if companion.preserve_emotional_context else "limit-emotional-context",
        "allow-voice-extension" if companion.allow_voice_extension else "block-voice-extension",
    ]
    return tuple(flags)


def _interaction_preferences(companion) -> tuple[str, ...]:
    return _governance_flags(companion)


def _split_profile_preferences(values: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    communication: list[str] = []
    shared: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        if normalized.startswith(("tone:", "verbosity:", "language:", "response-style:")):
            communication.append(normalized)
        else:
            shared.append(normalized)
    return tuple(communication), tuple(shared)


def _biography_fragments(fields: dict[str, str]) -> tuple[str, ...]:
    fragments: list[str] = []
    for key in user_biography_field_ids(fields):
        value = _strip_or_none(fields.get(key))
        if value is not None:
            fragments.append(f"{key}:{value}")
    return tuple(fragments)


def _maybe_singleton(value: str | None) -> tuple[str, ...]:
    cleaned = _strip_or_none(value)
    if cleaned is None:
        return ()
    return (cleaned,)


def _strip_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


__all__ = [
    "CanonicalProfileIds",
    "CanonicalProfileStateBundle",
    "build_canonical_profile_state",
    "build_clone_identity_record",
    "build_relationship_memory_record",
    "build_user_card_record",
    "canonical_profile_ids",
]
