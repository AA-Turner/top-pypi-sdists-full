"""Context selection, minimization, hashing, and injection (FR-005, FR-006, FR-011, FR-012).

Provides:

- ``ContextProvenance``: distinguishes verified, unavailable, and inferred
  context so that agent prompts and review records never present fabricated
  content as authoritative (NFR-005).
- Epic and Feature artifact selection, including the complete Feature
  artifact suite defined by
  ``agentic_devtools.hierarchy.artifact_profiles.get_artifact_profile``.
- Exact-byte SHA-256 hashing and immutable-locator validation for injected
  fields (FR-011, FR-012), plus optional protected (encrypted) snapshot
  handling for retained fields via ``protected_storage.py``.
- Injection that can never alter static permissions, tools, file
  boundaries, or review authority — injected content is always untrusted
  data (FR-011).
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.models import HierarchyLevel

from .protected_storage import ProtectedStorage
from .scopes import ScopeAgent

_SNAPSHOT_REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContextProvenance(StrEnum):
    """Provenance status for a piece of injected hierarchy context (NFR-005).

    - ``VERIFIED``: sourced directly from a resolved, existing artifact.
    - ``UNAVAILABLE``: the artifact/field could not be found; no content is
      substituted, and this status alone marks the field non-authoritative.
    - ``INFERRED``: derived rather than directly verified (for example, a
      sibling relationship inferred from hierarchy structure rather than an
      explicit artifact statement). Never promoted to authoritative.
    """

    VERIFIED = "verified"
    UNAVAILABLE = "unavailable"
    INFERRED = "inferred"

    @property
    def is_authoritative(self) -> bool:
        """Return True only for verified provenance."""
        return self is ContextProvenance.VERIFIED


@dataclass(frozen=True)
class RetentionMetadata:
    """Retention and deletion metadata for one retained context snapshot."""

    created_at: str
    expires_at: str
    incident_hold: bool = False

    def __post_init__(self) -> None:
        created = _parse_retention_timestamp(self.created_at)
        expires = _parse_retention_timestamp(self.expires_at)
        if expires < created:
            raise ValueError("expires_at must not precede created_at")
        if not self.incident_hold and expires > created + timedelta(days=30):
            raise ValueError("retention must not exceed 30 days without an incident hold")

    def to_dict(self) -> dict[str, object]:
        """Return the metadata shape persisted alongside a retained field."""
        return {
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "incident_hold": self.incident_hold,
        }


def _parse_retention_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid retention timestamp: {value!r}") from exc
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def retention_metadata(
    *,
    created_at: datetime | None = None,
    retention_days: int = 30,
    incident_hold: bool = False,
) -> RetentionMetadata:
    """Create retention metadata, enforcing the 30-day non-hold limit."""
    if retention_days < 0:
        raise ValueError("retention_days must be non-negative")
    if retention_days > 30 and not incident_hold:
        raise ValueError("retention must not exceed 30 days without an incident hold")
    created = created_at or datetime.now(UTC)
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return RetentionMetadata(
        created_at=created.isoformat(),
        expires_at=(created + timedelta(days=retention_days)).isoformat(),
        incident_hold=incident_hold,
    )


def is_retention_expired(metadata: RetentionMetadata, *, now: datetime | None = None) -> bool:
    """Return whether retained data is expired and not protected by an incident hold."""
    if metadata.incident_hold:
        return False
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return current >= _parse_retention_timestamp(metadata.expires_at)


def cleanup_retained_paths(paths: Iterable[Any]) -> tuple[Any, ...]:
    """Delete retained snapshot/trace paths and return paths actually removed."""
    removed: list[Any] = []
    for path in paths:
        delete_func = getattr(path, "delete", None)
        if callable(delete_func):
            if delete_func():
                removed.append(path)
            continue
        try:
            path.unlink()
        except FileNotFoundError:
            continue
        removed.append(path)
    return tuple(removed)


def sha256_hex(content: str) -> str:
    """Return the SHA-256 hex digest of ``content`` encoded as UTF-8."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ContentLocator:
    """An immutable locator to the exact bytes referenced by a hash (FR-012).

    ``artifact_path`` locators MUST be revision-pinned (repository revision
    plus path); ``issue_url`` locators MUST reference immutable resources.
    """

    locator_type: str  # "artifact_path" | "issue_url"
    locator_value: str
    revision: str | None = None

    def __post_init__(self) -> None:
        if self.locator_type not in ("artifact_path", "issue_url"):
            msg = f"Invalid locator_type: {self.locator_type!r}"
            raise ValueError(msg)
        if self.locator_type == "artifact_path" and not self.revision:
            msg = "artifact_path locators MUST be revision-pinned"
            raise ValueError(msg)


@dataclass(frozen=True)
class InjectedField:
    """A single field of hierarchy context prepared for injection into an agent prompt.

    Attributes:
        name: The field name (e.g. ``"epic_spec"``).
        content: The exact finalized bytes (as text) supplied to the agent,
            after minimization/redaction has already been applied.
        provenance: Whether this content is verified, unavailable, or inferred.
        locator: An immutable locator reproducing the exact ``content`` bytes,
            or ``None`` when a durable snapshot is used instead.
        snapshot_ref: A reference to a retained, content-addressed snapshot,
            or ``None`` when the locator alone is sufficient (only valid when
            ``locator`` reproduces the exact bytes without transformation).
        transformed: Whether minimization/redaction/synthesis altered the
            content relative to the raw source (forces snapshot retention).
    """

    name: str
    content: str
    provenance: ContextProvenance
    locator: ContentLocator | None = None
    snapshot_ref: str | None = None
    transformed: bool = False
    retention: RetentionMetadata | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.content, str):
            msg = f"Field '{self.name}' content must be a string, got {type(self.content).__name__!r}"
            raise ValueError(msg)
        if (
            self.snapshot_ref is not None
            and self.provenance is not ContextProvenance.UNAVAILABLE
            and not _SNAPSHOT_REF_RE.fullmatch(self.snapshot_ref)
        ):
            msg = f"Field '{self.name}' must use a sha256:<64 lowercase hex> snapshot_ref; got {self.snapshot_ref!r}"
            raise ValueError(msg)
        if (
            self.snapshot_ref is not None
            and self.provenance is not ContextProvenance.UNAVAILABLE
            and self.snapshot_ref != f"sha256:{sha256_hex(self.content)}"
        ):
            msg = (
                f"Field '{self.name}' snapshot_ref does not match the hash of its content; "
                "snapshot_ref must be content-addressed"
            )
            raise ValueError(msg)
        if self.snapshot_ref is None and self.locator is not None and self.locator.locator_type == "issue_url":
            msg = (
                f"Field '{self.name}' uses an issue_url locator; "
                "a durable snapshot_ref is required because issue resources are mutable"
            )
            raise ValueError(msg)
        if self.snapshot_ref is None and self.transformed:
            msg = (
                f"Field '{self.name}' is transformed relative to its source; "
                "a durable snapshot_ref is required when locator cannot reproduce exact bytes"
            )
            raise ValueError(msg)
        if self.snapshot_ref is None and self.locator is None:
            msg = f"Field '{self.name}' must have either a snapshot_ref or a locator"
            raise ValueError(msg)

    @property
    def content_sha256(self) -> str:
        return sha256_hex(self.content)

    def to_ref_dict(self) -> dict[str, Any]:
        """Serialize to the ``field_content_refs`` entry shape used by trace events."""
        return {
            "content_sha256": self.content_sha256,
            "snapshot_ref": self.snapshot_ref,
            "locator_type": self.locator.locator_type if self.locator else None,
            "locator_value": self.locator.locator_value if self.locator else None,
            "locator_revision": self.locator.revision if self.locator else None,
            "retention": self.retention.to_dict() if self.retention is not None else None,
        }


def minimize_and_redact(content: str, *, redact_patterns: tuple[str, ...] = ()) -> tuple[str, bool]:
    """Apply minimization/redaction before hashing and injection.

    Returns a tuple of ``(transformed_content, was_transformed)``. Even a
    no-op call returns ``was_transformed=False`` so that untransformed
    content may use a locator-only reference; any actual redaction forces
    ``was_transformed=True``, which requires a durable snapshot reference.
    """
    transformed = False
    result = content
    for pattern in redact_patterns:
        if pattern and pattern in result:
            result = result.replace(pattern, "[REDACTED]")
            transformed = True
    return result, transformed


def make_verified_field(
    name: str,
    raw_content: str,
    *,
    artifact_path: str,
    revision: str,
    redact_patterns: tuple[str, ...] = (),
    snapshot_ref: str | None = None,
    retention: RetentionMetadata | None = None,
    protected_storage: ProtectedStorage | None = None,
) -> InjectedField:
    """Build a ``VERIFIED`` injected field from raw artifact content.

    When ``redact_patterns`` transforms the content, ``snapshot_ref`` MUST
    either match the finalized content hash or be derived by persisting the
    finalized bytes via ``ProtectedStorage.write_snapshot``. A locator alone
    is insufficient for transformed content.
    """
    content, transformed = minimize_and_redact(raw_content, redact_patterns=redact_patterns)
    if transformed and protected_storage is not None:
        expected_snapshot_ref = f"sha256:{sha256_hex(content)}"
        if snapshot_ref is not None and snapshot_ref != expected_snapshot_ref:
            raise ValueError("snapshot_ref does not match the retained transformed content")
        derived_snapshot_ref = protected_storage.write_snapshot(content.encode("utf-8"))
        snapshot_ref = derived_snapshot_ref
    elif transformed and snapshot_ref is not None:
        expected_snapshot_ref = f"sha256:{sha256_hex(content)}"
        if snapshot_ref != expected_snapshot_ref:
            raise ValueError("snapshot_ref must be content-addressed and match the finalized transformed content")
    locator = (
        None
        if transformed
        else ContentLocator(locator_type="artifact_path", locator_value=artifact_path, revision=revision)
    )
    return InjectedField(
        name=name,
        content=content,
        provenance=ContextProvenance.VERIFIED,
        locator=locator,
        snapshot_ref=snapshot_ref,
        transformed=transformed,
        retention=retention,
    )


def make_unavailable_field(name: str) -> InjectedField:
    """Build an explicit ``UNAVAILABLE`` field marker (never fabricated content)."""
    return InjectedField(
        name=name,
        content="",
        provenance=ContextProvenance.UNAVAILABLE,
        locator=None,
        snapshot_ref="unavailable:no-content-retained",
        transformed=False,
    )


def make_inferred_field(name: str, content: str, *, snapshot_ref: str) -> InjectedField:
    """Build an ``INFERRED`` field (e.g. a derived sibling relationship)."""
    return InjectedField(
        name=name,
        content=content,
        provenance=ContextProvenance.INFERRED,
        locator=None,
        snapshot_ref=snapshot_ref,
        transformed=True,
    )


@dataclass(frozen=True)
class ArtifactAvailability:
    """Whether an artifact exists and is non-empty, plus its content when available."""

    path: str
    exists: bool
    content: str = ""


def select_epic_context(artifacts: dict[str, ArtifactAvailability], *, revision: str) -> list[InjectedField]:
    """Select Epic context: ``spec.md`` and ``plan.md`` when available (FR-005).

    Missing or empty artifacts never fabricate content; they are recorded
    as ``UNAVAILABLE`` fields so the Epic Agent reviews only verified input.
    """
    fields: list[InjectedField] = []
    for name in ("spec.md", "plan.md"):
        artifact = artifacts.get(name)
        if artifact is not None and artifact.exists and artifact.content.strip():
            fields.append(
                make_verified_field(
                    name.replace(".", "_"), artifact.content, artifact_path=artifact.path, revision=revision
                )
            )
        else:
            fields.append(make_unavailable_field(name.replace(".", "_")))
    return fields


def select_feature_context(artifacts: dict[str, ArtifactAvailability], *, revision: str) -> list[InjectedField]:
    """Select the complete Feature artifact suite (FR-006).

    Uses ``get_artifact_profile(HierarchyLevel.FEATURE)`` as the
    authoritative list of artifacts a Feature Agent must be offered; every
    entry in that profile is represented (verified or explicitly
    unavailable).
    """
    profile = get_artifact_profile(HierarchyLevel.FEATURE)
    fields: list[InjectedField] = []
    for artifact_name in profile.included_artifacts:
        artifact = artifacts.get(artifact_name)
        field_name = artifact_name.replace("/", "_").replace(".", "_")
        if artifact is not None and artifact.exists and artifact.content.strip():
            fields.append(
                make_verified_field(field_name, artifact.content, artifact_path=artifact.path, revision=revision)
            )
        else:
            fields.append(make_unavailable_field(field_name))
    return fields


@dataclass(frozen=True)
class ContextInjectionRecord:
    """The result of injecting context into a spawned agent (for trace + prompt use)."""

    agent_id: str
    fields: tuple[InjectedField, ...]

    @property
    def fields_injected(self) -> list[str]:
        return [f.name for f in self.fields]

    @property
    def field_content_refs(self) -> dict[str, Any]:
        return {f.name: f.to_ref_dict() for f in self.fields}

    def to_event_detail(self) -> dict[str, Any]:
        """Serialize to the ``context_injected`` trace event_detail shape."""
        return {
            "agent_id": self.agent_id,
            "fields_injected": self.fields_injected,
            "field_content_refs": self.field_content_refs,
            "trusted": False,
        }

    def to_prompt_context(self) -> dict[str, Any]:
        """Serialize fields for prompt use, distinguishing provenance (NFR-005)."""
        return {
            f.name: {
                "content": f.content,
                "provenance": f.provenance.value,
                "authoritative": f.provenance.is_authoritative,
            }
            for f in self.fields
        }


def inject_prompt_context(agent: ScopeAgent, fields: list[InjectedField]) -> ContextInjectionRecord:
    """Inject prepared fields into an agent's context.

    Injection is purely additive data; it can never widen ``agent``'s
    static file boundary, capabilities, or review authority (FR-011). The
    returned record is always marked ``trusted: false`` in its
    trace-facing representation.
    """
    return ContextInjectionRecord(agent_id=agent.agent_id, fields=tuple(fields))
