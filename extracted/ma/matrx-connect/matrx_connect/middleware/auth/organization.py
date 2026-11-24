"""Organization pinning: membership resolve, the admin lane, the record-grant lane."""

from __future__ import annotations


from matrx_utils import vcprint
from starlette.requests import HTTPConnection, Request

from matrx_connect.context.app_context import AppContext
from ..authority_retry import call_authority

from .types import (
    _is_uuid,
    _unsafe_encoded_path,
    OrganizationNotFound,
    OrganizationArchived,
    ADMIN_LANE_HEADER,
    AdminLaneAuditUnavailable,
    ADMISSION_FAILURE_KEY,
    ADMIN_LANE_AUDIT_UNAVAILABLE,
    ADMIN_LANE_UNVERIFIABLE,
)


class OrganizationLane:
    """Mixin on ``AuthMiddleware``: pins a verified ``organization_id`` onto an authenticated context."""

    async def _admin_lane_verdict(
        self, request: Request | HTTPConnection, ctx: AppContext, claimed: str
    ) -> bool | str:
        """True only when the request rides the admin lane AND the host's
        admission hook verifies it. The header alone never admits anything.

        False is a REFUSAL (not on the lane, not an admin, not the tenant). A
        string is a check that could not be DECIDED — the hook raised or timed
        out — naming why (``ADMIN_LANE_AUDIT_UNAVAILABLE`` /
        ``ADMIN_LANE_UNVERIFIABLE``). Never an admission, and never reported as
        "not a member"."""
        if self._admin_lane_admission is None or not ctx.user_id:
            return False
        if (ctx.auth_type == "token" and self._resolve_current_session is not None
                and not ctx.is_admin):
            # A host's role-only tenant hook cannot restore administrator power
            # that this request's fresh session/MFA authority has withheld.
            return False
        if (request.headers.get(ADMIN_LANE_HEADER) or "").strip() != "1":
            return False
        try:
            admission = self._admin_lane_admission
            admitted = await call_authority(
                lambda: admission(str(ctx.user_id), claimed),
                attempt_timeout=self._organization_resolve_timeout,
                label="Admin-lane authority",
                decisions=(AdminLaneAuditUnavailable,),
            )
        except Exception as exc:  # noqa: BLE001 — a failed check is a refusal, never an admission
            failure = (
                ADMIN_LANE_AUDIT_UNAVAILABLE
                if isinstance(exc, AdminLaneAuditUnavailable)
                else ADMIN_LANE_UNVERIFIABLE
            )
            vcprint(
                f"[AUTH][ERROR] admin-lane admission check FAILED for org={claimed} "
                f"user={ctx.user_id}: {type(exc).__name__}: {exc} — refused ({failure}).",
                color="red",
                log_level="ERROR",
            )
            return failure
        if admitted:
            vcprint(
                f"[AUTH][INFO] organization admitted by the ADMIN LANE: org={claimed} user={ctx.user_id}",
                color="green",
                log_level="INFO",
            )
        return bool(admitted)

    async def _record_grant_verdict(
        self, request: Request | HTTPConnection, ctx: AppContext, claimed: str
    ) -> bool | None:
        """True when the host's record-grant hook admits this exact request.

        False is a refusal (no hook, not HTTP, unsafe path, or the host said
        no). None is a check that could not be DECIDED (the hook raised or
        timed out) — never an admission, and never reported as "not a member".
        """
        if self._record_grant_admission is None or not ctx.user_id:
            return False
        if not isinstance(request, Request):
            return False
        if _unsafe_encoded_path(request.scope.get("raw_path")):
            return False
        try:
            grant = self._record_grant_admission
            admitted = await call_authority(
                lambda: grant(str(ctx.user_id), claimed, request.method.upper(), request.url.path),
                attempt_timeout=self._organization_resolve_timeout,
                label="Record-grant authority",
            )
        except Exception as exc:  # noqa: BLE001 — a failed check is never an admission
            vcprint(
                f"[AUTH][ERROR] record-grant admission check FAILED for org={claimed} "
                f"user={ctx.user_id} {request.method} {request.url.path}: "
                f"{type(exc).__name__}: {exc} — refused (unverifiable).",
                color="red",
                log_level="ERROR",
            )
            return None
        if admitted:
            vcprint(
                f"[AUTH][INFO] organization admitted by a RECORD GRANT: org={claimed} "
                f"user={ctx.user_id} {request.method} {request.url.path}",
                color="green",
                log_level="INFO",
            )
        return bool(admitted)

    async def _resolve_organization(self, request: Request | HTTPConnection, ctx: AppContext) -> AppContext:
        """Pin a verified organization_id onto an authenticated AppContext.

        Resolution order:
          1. ``X-Organization-Id`` header (explicit user choice).
          2. JWT claim ``organization_id`` or ``org_id`` (stashed on
             ``ctx.metadata['jwt_claims']`` by ``_validate_token``).
        If a resolver was injected, it is the source of truth: it returns
        the verified org_id (or None to deny). Without a resolver, the
        claim is trusted as-is — acceptable in dev, never in production.
        """
        if not ctx.is_authenticated or not ctx.user_id:
            return ctx

        claimed: str | None = request.headers.get("x-organization-id") or None
        if not claimed:
            claims = ctx.metadata.get("jwt_claims") if isinstance(ctx.metadata, dict) else None
            if isinstance(claims, dict):
                raw = claims.get("organization_id") or claims.get("org_id")
                if isinstance(raw, str) and raw:
                    claimed = raw

        if claimed is None and self._resolve_active_organization is None:
            return ctx

        # A value that is not an organization id at all is answered HERE, before
        # any lookup: sending it to the resolver produces a database type error,
        # which the handler below would honestly but uselessly report as
        # "could not verify — try again" for something that will never verify.
        if claimed is not None:
            if not _is_uuid(str(claimed).strip()):
                vcprint(
                    f"[AUTH][REJECT] organization admission MALFORMED: {claimed!r} is "
                    f"not an organization id (user={ctx.user_id})",
                    color="yellow",
                    log_level="WARNING",
                )
                return ctx.with_overrides(
                    organization_admission="malformed",
                    claimed_organization_id=str(claimed),
                )

        if self._resolve_active_organization is not None:
            try:
                # Bounded: the singleflight task is shielded, so a timeout here
                # stops only THIS caller waiting; a TimeoutError is a failure to
                # verify ("unverifiable", 503 below), never a quiet no-org.
                # Transient misses are retried within a bounded budget (authority_retry);
                # not-found / archived are DECISIONS and raise at once.
                verified = await call_authority(
                    lambda: self._org_flights.do(
                        (ctx.user_id, claimed),
                        lambda: self._resolve_active_organization(ctx.user_id, claimed),
                    ),
                    attempt_timeout=self._organization_resolve_timeout,
                    label="Organization membership authority",
                    decisions=(OrganizationNotFound, OrganizationArchived),
                )
            except OrganizationNotFound:
                # A well-formed id for an organization that does not exist. As
                # permanent as a denial and as un-retryable, but a DIFFERENT
                # repair — telling this caller "ask an admin to add you" would
                # send them to fix the wrong thing.
                vcprint(
                    f"[AUTH][REJECT] organization admission UNKNOWN: no organization "
                    f"{claimed} (user={ctx.user_id})",
                    color="yellow",
                    log_level="WARNING",
                )
                return ctx.with_overrides(
                    organization_admission="unknown",
                    claimed_organization_id=claimed,
                )
            except OrganizationArchived:
                # The organization exists and is closed. Refused for everyone —
                # member, owner and platform admin alike — exactly as the
                # database refuses it (iam.has_org_access_for).
                vcprint(
                    f"[AUTH][REJECT] organization admission ARCHIVED: organization "
                    f"{claimed} is archived (user={ctx.user_id})",
                    color="yellow",
                    log_level="WARNING",
                )
                return ctx.with_overrides(
                    organization_admission="archived",
                    claimed_organization_id=claimed,
                )
            except Exception as exc:  # noqa: BLE001 — resolver failures must never 500 the request
                # 🚨 NOT A SILENT NO-ORG. The request DID name an organization and
                # the platform could not tell whether the caller belongs to it.
                # Downstream, "no org" is not a smaller answer — it is a
                # DIFFERENT one (the mandate ladder resolves user -> ACTIVE org
                # -> system, so a swallowed failure here changes which agent
                # runs). The context now carries the difference; consumers that
                # scope by organization refuse on it.
                vcprint(
                    f"[AUTH][ERROR] organization admission UNVERIFIABLE for "
                    f"org={claimed} user={ctx.user_id}: {type(exc).__name__}: {exc} — "
                    "the request is NOT demoted to no-org; organization-scoped "
                    "features will refuse until the resolver answers again.",
                    color="red",
                    log_level="ERROR",
                )
                return ctx.with_overrides(
                    organization_admission="unverifiable",
                    claimed_organization_id=claimed,
                )
        else:
            verified = claimed

        if not verified:
            lane = await self._admin_lane_verdict(request, ctx, str(claimed)) if claimed else False
            if isinstance(lane, str):
                # The admin lane could not DECIDE. Retryable server-side
                # failure ("unverifiable", 503), with the real cause named —
                # an admin whose audit log is down is not "not a member".
                metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                metadata[ADMISSION_FAILURE_KEY] = lane
                return ctx.with_overrides(
                    organization_admission="unverifiable",
                    claimed_organization_id=claimed,
                    metadata=metadata,
                )
            if lane is True:
                # THE ADMIN LANE: the host verified a platform admin, on the
                # admin lane, naming its platform tenant. The tenant is VERIFIED
                # (every tenant-scoped consumer reads "verified"); the lane that
                # admitted it rides on metadata so it is never mistaken for a
                # membership.
                metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                metadata["organization_admitted_by"] = "admin_lane"
                return ctx.with_overrides(
                    organization_id=str(claimed),
                    organization_admission="verified",
                    claimed_organization_id=claimed,
                    metadata=metadata,
                )
            if claimed:
                grant = await self._record_grant_verdict(request, ctx, str(claimed))
                if grant is None:
                    return ctx.with_overrides(
                        organization_admission="unverifiable",
                        claimed_organization_id=claimed,
                    )
                if grant is True:
                    # THE RECORD-GRANT LANE: the host verified a share grant on
                    # the exact record this route acts on, whose own
                    # organization is the claimed one. The tenant is VERIFIED;
                    # how it was admitted rides on metadata so it is never
                    # mistaken for a membership.
                    metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                    metadata["organization_admitted_by"] = "record_grant"
                    return ctx.with_overrides(
                        organization_id=str(claimed),
                        organization_admission="verified",
                        claimed_organization_id=claimed,
                        metadata=metadata,
                    )
                # A proved non-member. An ANSWER, not a failure — and still not
                # the same thing as naming no organization at all.
                vcprint(
                    f"[AUTH][INFO] organization admission DENIED for org={claimed} "
                    f"user={ctx.user_id} (not an active member)",
                    color="yellow",
                    log_level="INFO",
                )
                return ctx.with_overrides(
                    organization_admission="denied",
                    claimed_organization_id=claimed,
                )
            return ctx

        if (request.headers.get(ADMIN_LANE_HEADER) or "").strip() == "1":
            # A MEMBER of the platform tenant who is also a platform admin, on the
            # admin lane: membership already admitted the org, but the request is
            # still ADMIN work and must read as the lane (admin-reach doors ask
            # ``organization_admitted_by == "admin_lane"``). The host hook
            # re-verifies tenant + admin registry and audits, exactly as for a
            # non-member. A refusal or an undecided check leaves the plain
            # membership admission untouched — never a demotion.
            lane = await self._admin_lane_verdict(request, ctx, str(verified))
            if lane is True:
                metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                metadata["organization_admitted_by"] = "admin_lane"
                return ctx.with_overrides(
                    organization_id=verified,
                    organization_admission="verified",
                    claimed_organization_id=claimed,
                    metadata=metadata,
                )

        return ctx.with_overrides(
            organization_id=verified,
            organization_admission="verified",
            claimed_organization_id=claimed,
        )
