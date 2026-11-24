"""The API-key lane (``Authorization: Bearer mx_...``, C16)."""

from __future__ import annotations


from matrx_utils import vcprint
from starlette.requests import HTTPConnection

from matrx_connect.context.app_context import AppContext
from ..session_authority import (
    CredentialAuthorityUnavailable,
)

from .types import (
    ApiKeyIdentity,
    ApiKeyRefused,
    API_KEY_BEARER_PREFIX,
    ApiKeyOrganizationMismatch,
)


class ApiKeyLane:
    """Mixin on ``AuthMiddleware``: service and personal API-key admission."""

    async def _admit_api_key(
        self,
        authorization: str,
        request: HTTPConnection,
        ctx: AppContext,
    ) -> AppContext | None:
        """The API-key admission lane (design: API-KEY-LANE-DESIGN.md, C16).

        Returns None when the request is not an API-key request (no resolver
        configured, non-bearer scheme, or the token lacks the ``mx_`` prefix) —
        the JWT lane then proceeds untouched. When the lane claims the request:

        * resolver success → authenticated context: ``user_id`` is the key's
          service identity, ``auth_type="api_key"``, and the key's organization
          is the admitted org. ``X-Organization-Id``, when present, must EQUAL
          it (409 via ``ApiKeyOrganizationMismatch``); when absent the key's
          org is admitted — fail-closed while sparing machine callers a
          redundant header.
        * typed current-authority outage → retryable HTTP503 / WebSocket1013.
        * resolver rejection/unexpected failure → the anonymous context, with the same
          compact INFO control-flow logging a rejected JWT gets (no token
          material ever logged). The route's own auth gate produces the 401.
        """
        if self._resolve_api_key is None:
            return None
        try:
            scheme, token_value = authorization.split(None, 1)
        except ValueError:
            return None
        if scheme.lower() != "bearer" or not token_value.startswith(API_KEY_BEARER_PREFIX):
            return None

        identity: ApiKeyIdentity | None
        try:
            identity = await self._resolve_api_key(token_value)
        except ApiKeyRefused as refused:
            vcprint("[AUTH][INFO] API key refused: " + refused.message, color="yellow", log_level="INFO")
            refused_metadata = dict(ctx.metadata)
            refused_metadata["credential_refused"] = refused.message
            return ctx.with_overrides(metadata=refused_metadata)
        except CredentialAuthorityUnavailable:
            raise
        except Exception as exc:  # noqa: BLE001 — unexpected resolver failure retains denial compatibility
            vcprint(
                f"[AUTH][WARN] API key resolver failed: {type(exc).__name__}",
                color="yellow",
                log_level="WARNING",
            )
            identity = None

        if identity is None:
            vcprint(
                "[AUTH][INFO] API key rejected",
                color="yellow",
                log_level="INFO",
            )
            return ctx

        if identity.kind == "personal":
            return await self._admit_personal_key(request, ctx, identity)

        claimed = (request.headers.get("x-organization-id") or "").strip()
        if claimed and claimed.lower() != str(identity.organization_id).lower():
            raise ApiKeyOrganizationMismatch(claimed, str(identity.organization_id))

        vcprint(
            f"[AUTH][INFO] API key accepted: user={identity.user_id} "
            f"org={identity.organization_id} key={identity.key_id or '?'}",
            color="green",
            log_level="INFO",
        )

        new_metadata = dict(ctx.metadata)
        new_metadata["api_key_id"] = identity.key_id
        new_metadata["api_key_expires_at"] = identity.expires_at
        if identity.key_name:
            new_metadata["api_key_name"] = identity.key_name
        if identity.limits is not None:
            new_metadata["api_key_limits"] = identity.limits

        return ctx.with_overrides(
            user_id=identity.user_id,
            auth_type="api_key",
            is_authenticated=True,
            organization_id=str(identity.organization_id),
            organization_admission="verified",
            claimed_organization_id=str(identity.organization_id),
            metadata=new_metadata,
        )

    async def _admit_personal_key(
        self, request: HTTPConnection, ctx: AppContext, identity: ApiKeyIdentity
    ) -> AppContext:
        """A personal key IS the person — admitted exactly as their own sign-in would be.

        The identity is the person's own ``auth.users`` row. The organization is NOT the
        key's to decide: it goes through :meth:`_resolve_organization`, the one resolver a
        signed-in person's request crosses — ``X-Organization-Id`` when sent, else the
        organization this key was deliberately configured with (carried as the claim a JWT
        would carry). Membership is verified there on every request, so a person removed
        from an organization is refused on the next call even while the key row is cached.

        The admin tier is deliberately NOT resolved: full admin access lives inside the
        admin apps, signed in (Arman, 2026-09-26/29); a key reaches everything the person
        can do as an ordinary member.
        """
        vcprint(
            f"[AUTH][INFO] personal API key accepted: user={identity.user_id} "
            f"key={identity.key_id or '?'}",
            color="green",
            log_level="INFO",
        )
        new_metadata = dict(ctx.metadata)
        new_metadata["api_key_id"] = identity.key_id
        new_metadata["api_key_kind"] = "personal"
        new_metadata["api_key_expires_at"] = identity.expires_at
        if identity.key_name:
            new_metadata["api_key_name"] = identity.key_name
        if identity.limits is not None:
            new_metadata["api_key_limits"] = identity.limits
        # The claims an RLS session is opened with. `organization_id` is the key's configured
        # organization — the same claim slot a JWT's organization rides in — so the resolver
        # below treats it exactly like a presented claim: verified, never trusted.
        new_metadata["jwt_claims"] = {
            "sub": identity.user_id,
            "role": "authenticated",
            "aud": "authenticated",
            "organization_id": str(identity.organization_id),
        }
        admitted = ctx.with_overrides(
            user_id=identity.user_id,
            auth_type="api_key",
            is_authenticated=True,
            metadata=new_metadata,
        )
        return await self._resolve_organization(request, admitted)
