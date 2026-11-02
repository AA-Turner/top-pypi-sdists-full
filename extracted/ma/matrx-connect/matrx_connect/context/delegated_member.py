"""The delegated member boundary — a worker acting FOR a proved member.

THE HOLE THIS FILLS. Until now the platform had exactly two tenant origins: a
live HTTP request whose membership was verified (``organization_admission ==
"verified"``), and non-HTTP work that names a member but proves nothing
(``system_app_context`` → ``"none"``). A Personal Staff turn is neither. The
person texted; the carrier proved the number; a worker — not a browser — runs
the turn on their behalf. Under ``system_app_context`` that turn could not text
them back (``services/notifications/staff_text.py``), could not notify them
(``services/notifications/self_service.py``), and could not drive their browser
(``services/cloud_browser/tools.py``): every one of those gates wants a VERIFIED
membership or refuses a ``system`` origin, and all three were right to.

THE BOUNDARY. ``delegated_member_context`` proves the membership LIVE, for this
turn, through a host resolver that reads ``iam.memberships`` (the same resolver
the auth middleware uses), and only then mints a context admitted as a member.
Four properties make it safe to hand a worker:

1. **It cannot be minted without a proof.** The provenance requires a typed
   ``MembershipProof``; a ``MembershipProof`` requires this module's private
   mint token; this function is the only holder. No proof, no context — and no
   way to fake one from outside.
2. **It says what it is.** ``origin_class="delegated_member"`` — never
   ``human``. Every reader downstream can tell a delegated turn from a person
   at a keyboard, and the persistence witness records the audit (reason,
   channel, proof id) on the rows the turn writes.
3. **It is not a session.** No token, no JWT claims, never an admin tier. Gates
   that require an interactive human — recent-auth on a reveal, a consent click
   — fail CLOSED here by construction, not by anyone remembering to check;
   ``require_interactive_human`` states the same refusal in words.
4. **It opens no credential door.** Filling a person's password into a page is
   its own named capability with its own consent; asking for it here is
   refused, loudly, with where to go instead.

WHAT IT IS NOT. It is not a way to run as somebody. The member is named by the
CHANNEL that proved them (a verified phone number, an admitted call), never by
a request body, never by an agent's argument, and the membership is re-proved
on every turn — a person removed from an organization loses the delegated turn
on their next text, not at some cache's convenience.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Awaitable, Callable, Iterable
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from matrx_connect.context.app_context import (
    DelegatedMemberAppContext,
    TenantAppContext,
    _mint_tenant_context,
    clear_app_context,
    set_app_context,
    try_get_app_context,
)
from matrx_connect.context.provenance import ORIGIN_CLASS_DELEGATED_MEMBER
from matrx_connect.context.tenant_provenance import (
    VERIFIED_DELEGATION_CHANNELS,
    DelegatedMemberTenantProvenance,
    MembershipProof,
    _PROOF_MINT,
    _require_principal,
)

#: The host's live membership check. ``(user_id, organization_id)`` → the
#: verified organization id (truthy) when ``iam.memberships`` holds an ACTIVE,
#: undeleted membership, or ``None`` for a proved non-member. It MUST RAISE when
#: it cannot tell: an outage that returns None would silently downgrade a member
#: to a stranger, which is the exact failure ``organization_admission
#: ="unverifiable"`` exists to make visible on the HTTP side.
#:
#: aidream supplies ``aidream.api.middleware.auth._resolve_active_organization``,
#: which is the resolver the auth middleware itself uses — one membership truth,
#: two doors.
MembershipProver = Callable[[str, str], Awaitable[Any]]

#: Capabilities a delegated turn may NEVER be minted with. Filling or revealing
#: a person's credentials is not a tenant-reach question at all — it is its own
#: consented capability with its own door, and it is deliberately NOT reachable
#: by widening this one.
FORBIDDEN_DELEGATED_CAPABILITIES: frozenset[str] = frozenset(
    {"credential_fill", "credential_login", "credential_reveal", "vault_reveal"}
)


class DelegatedMemberAdmissionError(PermissionError):
    """A delegated member turn could not be admitted. Never silent, never vague."""


class DelegatedMembershipDenied(DelegatedMemberAdmissionError):
    """Proved NOT a member. Permanent until the membership changes."""


class DelegatedMembershipUnverifiable(DelegatedMemberAdmissionError):
    """The platform could not tell. Transient, and NOT demoted to 'no org'."""


def _canonical_uuid(value: object, field_name: str) -> str:
    try:
        return str(UUID(str(value).strip()))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError(f"{field_name} must be a valid UUID") from exc


def is_delegated_member_context(ctx: object) -> bool:
    """True for a turn a worker is running FOR a proved member."""
    return isinstance(ctx, DelegatedMemberAppContext)


def delegated_member_admission(ctx: object) -> dict[str, Any] | None:
    """The audit record of the proof that admitted this turn, or None."""
    metadata = getattr(ctx, "metadata", None)
    if not isinstance(metadata, dict):
        return None
    record = metadata.get("delegated_member_admission")
    return dict(record) if isinstance(record, dict) else None


def require_interactive_human(ctx: object, action: str) -> None:
    """Refuse ``action`` when nobody is actually at a keyboard.

    A delegated turn carries a real member's reach, and deliberately not their
    PRESENCE. Anything whose whole point is that a person is here right now —
    revealing a secret, re-authenticating, accepting terms — calls this and
    gets a sentence that says what to do instead.
    """
    if not is_delegated_member_context(ctx):
        return
    record = delegated_member_admission(ctx) or {}
    channel = record.get("channel") or "a delegated channel"
    raise DelegatedMemberAdmissionError(
        f"{action} needs the person themselves, and this turn is being run for "
        f"them by AI Matrx over {channel} — nobody is at a keyboard to confirm "
        "it. Send them a link to do this in the app, and continue when they have."
    )


@asynccontextmanager
async def delegated_member_context(
    user_id: str,
    organization_id: str,
    *,
    reason: str,
    channel: str,
    prove_membership: MembershipProver,
    prover_id: str,
    feature: str | None = None,
    capabilities: Iterable[str] = (),
    source_app: str | None = None,
    label: str | None = None,
    **overrides: Any,
) -> AsyncGenerator[DelegatedMemberAppContext]:
    """Install a context admitted as a MEMBER, for a worker acting on their behalf.

    Parameters
    ----------
    user_id, organization_id
        Who the turn acts for, and where. Both are proved together — a
        membership is the pair, never either half.
    reason
        Why a worker is acting for this person, in words that will sit in the
        audit record forever ("answering an inbound SMS to the Personal Staff
        number"). A delegated turn always says why it ran.
    channel
        The channel that proved who is speaking — one of
        ``VERIFIED_DELEGATION_CHANNELS``. This is the evidence that the person
        on the other end IS ``user_id``; the membership proof only establishes
        what that person may reach.
    prove_membership
        The host's live ``iam.memberships`` check (see ``MembershipProver``).
        It is REQUIRED and has no default: a boundary that could be opened
        without a proof is not a boundary.
    prover_id
        Namespaced id of the resolver used, recorded in the proof so an audit
        can say WHAT proved this ("aidream.auth.active_organization").

    Raises
    ------
    DelegatedMembershipDenied
        The person is not an active member of that organization.
    DelegatedMembershipUnverifiable
        The membership could not be checked. The turn does NOT fall back to a
        system context — running one rung lower would silently be a different
        actor with different reach.
    """
    canonical_organization_id = _canonical_uuid(organization_id, "organization_id")
    _require_principal(user_id, "user_id")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a nonempty string — a delegated turn says why it ran")
    if channel not in VERIFIED_DELEGATION_CHANNELS:
        raise ValueError(
            f"channel must be one of {', '.join(VERIFIED_DELEGATION_CHANNELS)}; "
            f"{channel!r} has not been established as a channel that proves who is speaking"
        )
    if not callable(prove_membership):
        raise ValueError(
            "prove_membership is required: a delegated member context is minted ONLY "
            "from a live membership verification, never from a caller's assertion"
        )

    requested_capabilities = frozenset(str(item) for item in capabilities)
    forbidden = sorted(requested_capabilities & FORBIDDEN_DELEGATED_CAPABILITIES)
    if forbidden:
        raise ValueError(
            f"a delegated member turn may not carry {', '.join(forbidden)}: filling or "
            "revealing a person's credentials is its own consented capability with its "
            "own door, and widening this boundary is not that door"
        )

    for reserved in (
        "organization_admission",
        "claimed_organization_id",
        "user_id",
        "organization_id",
        "is_authenticated",
        "auth_type",
        "token",
        "is_admin",
        "admin_level",
        "origin_class",
        "_organization_admission_binding",
        "_organization_admission_provenance_binding",
        "_tenant_provenance",
        "_tenant_context_seal",
    ):
        if reserved in overrides:
            raise ValueError(f"{reserved} is not overrideable on a delegated member context")

    # ── The proof ────────────────────────────────────────────────────────────
    from matrx_connect.middleware.auth import OrganizationArchived, OrganizationNotFound

    try:
        verified = await prove_membership(user_id, canonical_organization_id)
    except OrganizationArchived as exc:
        # A definitive answer, not an outage: the organization is closed
        # (ACCESS LADDER T-33) and nothing runs in it until it is restored.
        raise DelegatedMembershipDenied(
            f"Organization {canonical_organization_id} is archived, so nothing may run in it "
            "for anyone until its owner restores it."
        ) from exc
    except OrganizationNotFound as exc:
        raise DelegatedMembershipDenied(
            f"Organization {canonical_organization_id} does not exist, so nothing may run in it."
        ) from exc
    except Exception as exc:  # noqa: BLE001 — an outage is an ANSWER we must name
        raise DelegatedMembershipUnverifiable(
            f"AI Matrx could not confirm that this person still belongs to organization "
            f"{canonical_organization_id}, so it did not act for them. This is on us, not "
            f"on them: {type(exc).__name__}. Retry the turn; if it persists, the membership "
            "resolver is failing."
        ) from exc
    if not verified:
        raise DelegatedMembershipDenied(
            f"This person is not an active member of organization "
            f"{canonical_organization_id}, so nothing may run for them in it. Membership is "
            "proved against iam.memberships on every delegated turn and is never inferred."
        )
    if _canonical_uuid(verified, "verified organization_id") != canonical_organization_id:
        raise DelegatedMembershipDenied(
            "The membership resolver verified a DIFFERENT organization than the one this "
            "turn named. Nothing is admitted on a disagreement — a delegated turn never "
            "silently moves tenants."
        )

    proof = MembershipProof(
        organization_id=canonical_organization_id,
        principal=user_id,
        proof_id=str(uuid4()),
        prover_id=prover_id,
        verified_at=datetime.now(UTC),
        mint=_PROOF_MINT,
    )
    provenance = DelegatedMemberTenantProvenance(proof=proof, reason=reason.strip(), channel=channel)

    # NOTHING IS INHERITED. A channel ingress often runs inside an ambient
    # context already — the carrier's inbound webhook is an HTTP request, and
    # that request is anonymous, belongs to the carrier, and has nothing to do
    # with the person being served. So this boundary always mints fresh and
    # never reuses (unlike ``tenant_system_context``, whose same-identity no-op
    # is right for re-entrant background work). The one thing it refuses is
    # being opened INSIDE another tenant's admitted work: that is not an
    # ingress, it is one person's turn nested in another's.
    ambient = try_get_app_context()
    if (
        isinstance(ambient, TenantAppContext)
        and (ambient.user_id, str(ambient.organization_id)) != (user_id, canonical_organization_id)
    ):
        raise DelegatedMemberAdmissionError(
            "a delegated member context is opened at the channel ingress, not inside "
            f"another tenant's admitted work (ambient: {ambient.user_id} in "
            f"{ambient.organization_id})"
        )

    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    resolved_feature = (feature or f"delegated_member.{channel}").strip()
    audit = {
        "reason": provenance.reason,
        "channel": channel,
        "membership_proof_id": proof.proof_id,
        "prover_id": proof.prover_id,
        "verified_at": proof.verified_at.isoformat(),
        "capabilities": sorted(requested_capabilities),
        "feature": resolved_feature,
    }
    metadata = dict(overrides.pop("metadata", None) or {})
    metadata.pop("jwt_claims", None)
    metadata["delegated_member_admission"] = audit

    fields: dict[str, Any] = {
        "emitter": ConsoleEmitter(label or resolved_feature, accumulate=False),
        "user_id": user_id,
        "email": None,
        "auth_type": "token",
        "is_authenticated": True,
        "is_admin": False,
        "admin_level": None,
        "token": None,
        "organization_id": canonical_organization_id,
        "organization_admission": "verified",
        "claimed_organization_id": None,
        "request_id": str(uuid4()),
        "operation_id": str(uuid4()),
        "origin_class": ORIGIN_CLASS_DELEGATED_MEMBER,
        "is_internal_agent": False,
        "system_run": False,
        "store": True,
        "source_app": source_app or "aidream",
        "source_feature": resolved_feature,
        "metadata": metadata,
    }
    fields.update(overrides)
    ctx = _mint_tenant_context(fields, provenance)

    try:
        from matrx_utils import vcprint

        vcprint(
            f"[DELEGATED] {resolved_feature} admitted {user_id} in "
            f"{canonical_organization_id} over {channel} — {provenance.reason} "
            f"(proof {proof.proof_id})",
            color="cyan",
        )
    except Exception:  # noqa: BLE001 — the audit log must never fail the turn
        pass

    token = set_app_context(ctx)
    try:
        yield ctx
    finally:
        clear_app_context(token)
