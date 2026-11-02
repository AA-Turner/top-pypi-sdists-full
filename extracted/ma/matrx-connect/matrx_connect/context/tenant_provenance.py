"""Typed tenant-origin evidence owned by matrx-connect."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

ResourceOperation = Literal["read", "write", "rename", "delete"]
# Mirrors ``matrx_orm.platform_access.PERMISSION_LEVELS``. matrx-connect does
# NOT depend on matrx-orm, so the ladder is restated here rather than imported —
# and the restatement is proven, not trusted: the guard in
# aidream/api/tests/test_permission_level_ladder.py fails if the two disagree.
RESOURCE_ACCESS_LEVELS: tuple[str, ...] = ("viewer", "commenter", "editor", "admin")
ResourceAccessLevel = Literal["viewer", "commenter", "editor", "admin"]

_RESOURCE_TOKEN_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_ADAPTER_ID_RE = re.compile(r"^[a-z][a-z0-9_.:-]*$")
_ACCESS_FOR_OPERATION: dict[ResourceOperation, ResourceAccessLevel] = {
    "read": "viewer",
    "write": "editor",
    "rename": "editor",
    "delete": "admin",
}


def _canonical_uuid(value: object, field_name: str) -> str:
    try:
        return str(UUID(str(value).strip()))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError(f"{field_name} must be a valid UUID") from exc


def _require_principal(value: object, field_name: str = "principal") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")
    return value


@dataclass(frozen=True)
class MembershipTenantProvenance:
    """Verified membership evidence minted only by tenant promotion."""

    organization_id: str
    principal: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "organization_id", _canonical_uuid(self.organization_id, "organization_id"))
        _require_principal(self.principal)


@dataclass(frozen=True)
class ExplicitSystemTenantProvenance:
    """An explicitly initiated non-HTTP tenant operation."""

    organization_id: str
    principal: str
    initiating_feature: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "organization_id", _canonical_uuid(self.organization_id, "organization_id"))
        _require_principal(self.principal)
        if not isinstance(self.initiating_feature, str) or not self.initiating_feature.strip():
            raise ValueError("initiating_feature must be a nonempty string")


#: The channels on which a person's identity is proved BEFORE a staff turn runs
#: (the carrier verified the number / the call was admitted against the party
#: register). A delegated member turn may be opened only on one of these. Adding
#: a channel here is a claim that the channel itself proves WHO is speaking —
#: never a convenience.
VERIFIED_DELEGATION_CHANNELS: tuple[str, ...] = ("sms", "voice")

_PROOF_MINT = object()


@dataclass(frozen=True)
class MembershipProof:
    """One LIVE membership verification event, minted only by the boundary.

    It is evidence, not a claim: ``delegated_member_context`` builds it after a
    host resolver has answered against ``iam.memberships`` for THIS turn, and
    nothing else may build one — ``mint`` is the module-private token the
    boundary holds. ``proof_id`` identifies the verification EVENT (what the
    audit line points at), not the membership row.
    """

    organization_id: str
    principal: str
    proof_id: str
    prover_id: str
    verified_at: datetime
    mint: object = None

    def __post_init__(self) -> None:
        if self.mint is not _PROOF_MINT:
            raise ValueError(
                "a membership proof may only be minted by the delegated member "
                "boundary after a live membership verification"
            )
        object.__setattr__(self, "organization_id", _canonical_uuid(self.organization_id, "organization_id"))
        object.__setattr__(self, "proof_id", _canonical_uuid(self.proof_id, "proof_id"))
        _require_principal(self.principal)
        if not isinstance(self.prover_id, str) or not _ADAPTER_ID_RE.fullmatch(self.prover_id):
            raise ValueError("prover_id must be a nonempty namespaced identifier")
        if not isinstance(self.verified_at, datetime) or self.verified_at.tzinfo is None:
            raise ValueError("verified_at must be a timezone-aware datetime")


@dataclass(frozen=True)
class DelegatedMemberTenantProvenance:
    """A system worker acting FOR a member, on a channel that proved them.

    This is the third tenant origin. It is not a signed-in session (no browser,
    no token, no interactive human behind it) and it is not
    ``ExplicitSystemTenantProvenance`` either (that one names no member and
    proves nothing) — it is the honest middle the SMS/voice staff turn needed:
    the membership WAS proved live, so the turn is admitted "verified", while
    ``origin_class`` keeps saying out loud that a worker, not a person at a
    keyboard, is driving.
    """

    proof: MembershipProof
    reason: str
    channel: str

    def __post_init__(self) -> None:
        if type(self.proof) is not MembershipProof:
            raise ValueError("delegated member provenance requires a typed membership proof")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a nonempty string — a delegated turn says why it ran")
        if self.channel not in VERIFIED_DELEGATION_CHANNELS:
            raise ValueError(
                "channel must be one of "
                f"{', '.join(VERIFIED_DELEGATION_CHANNELS)} — a delegated member turn "
                "may only open on a channel that proved who is speaking"
            )

    @property
    def organization_id(self) -> str:
        return self.proof.organization_id

    @property
    def principal(self) -> str:
        return self.proof.principal


@dataclass(frozen=True)
class AuthorizedResourceAdmission:
    """Trusted host authorization evidence for one already-authorized resource."""

    principal: str
    organization_id: str
    resource_token: str
    resource_id: str
    operation: ResourceOperation
    access_level: ResourceAccessLevel
    adapter_id: str

    def __post_init__(self) -> None:
        _require_principal(self.principal)
        object.__setattr__(self, "organization_id", _canonical_uuid(self.organization_id, "organization_id"))
        object.__setattr__(self, "resource_id", _canonical_uuid(self.resource_id, "resource_id"))
        if not isinstance(self.resource_token, str) or not _RESOURCE_TOKEN_RE.fullmatch(self.resource_token):
            raise ValueError("resource_token must be a lowercase ASCII identifier")
        if self.operation not in _ACCESS_FOR_OPERATION:
            raise ValueError("operation must be read, write, rename, or delete")
        if self.access_level not in RESOURCE_ACCESS_LEVELS:
            raise ValueError(f"access_level must be one of {', '.join(RESOURCE_ACCESS_LEVELS)}")
        if _ACCESS_FOR_OPERATION[self.operation] != self.access_level:
            raise ValueError("access_level does not match operation")
        if not isinstance(self.adapter_id, str) or not _ADAPTER_ID_RE.fullmatch(self.adapter_id):
            raise ValueError("adapter_id must be a nonempty namespaced identifier")


@dataclass(frozen=True)
class AuthorizedResourceTenantProvenance:
    """Tenant origin copied from a trusted resource admission."""

    admission: AuthorizedResourceAdmission

    def __post_init__(self) -> None:
        if type(self.admission) is not AuthorizedResourceAdmission:
            raise ValueError("resource provenance requires typed authorized resource admission")

    @property
    def organization_id(self) -> str:
        return self.admission.organization_id

    @property
    def principal(self) -> str:
        return self.admission.principal


TenantProvenance = (
    MembershipTenantProvenance
    | ExplicitSystemTenantProvenance
    | AuthorizedResourceTenantProvenance
    | DelegatedMemberTenantProvenance
)


@dataclass(frozen=True)
class _TenantContextSeal:
    """Private structural binding against accidental tenant identity replacement."""

    organization_id: str
    principal: str
    provenance: TenantProvenance
