"""The fingerprint guest lane."""

from __future__ import annotations

import hashlib

from starlette.requests import HTTPConnection, Request

from matrx_connect.context.app_context import AppContext

from .types import (
    _READ_METHODS,
)


class GuestLane:
    """Mixin on ``AuthMiddleware``: fingerprint -> host-resolved guest identity, and its signature."""

    def _is_incidental_request(self, request: Request | HTTPConnection) -> bool:
        if self._guest_mint_exempt is None:
            return False
        url = request.url
        return bool(
            self._guest_mint_exempt(
                getattr(request, "method", "POST"), url.path, url.query or ""
            )
        )

    def _sign_fingerprint(self, fingerprint: str, user_id: str) -> str:
        """HMAC-SHA256 signature of (fingerprint, user_id). 32-byte hex."""
        import hmac as _hmac

        msg = f"{fingerprint}|{user_id}".encode()
        return _hmac.new(self._guest_fp_secret, msg, hashlib.sha256).hexdigest()

    def verify_fingerprint_signature(
        self,
        fingerprint: str,
        user_id: str,
        signature: str,
    ) -> bool:
        import hmac as _hmac

        expected = self._sign_fingerprint(fingerprint, user_id)
        return _hmac.compare_digest(expected, signature or "")

    async def _guest_lane(
        self,
        request: Request | HTTPConnection,
        ctx: AppContext,
        fingerprint_id: str | None,
    ) -> AppContext | None:
        """Lane 5: fingerprint -> guest identity. None = the lane did not claim the request."""
        # 🚨 THE GUEST LANE EXISTS ONLY WHERE A HOST WIRED A RESOLVER. A
        # fingerprint is an unauthenticated, caller-chosen string; only
        # ``resolve_guest`` can turn it into a real ``auth.users`` identity.
        # Until 2026-09-26 a host with no resolver (the standalone matrx-files
        # and matrx-seo services, the hosted box) got ``user_id = fingerprint``
        # — so ``X-Guest-Fingerprint: <any user's uuid>`` with NO token read
        # that user's private files, and any non-uuid fingerprint 500'd with
        # InvalidTextRepresentationError. Without a resolver the header is
        # ignored for identity and the request stays anonymous (routes that
        # need a user answer 401). Guard:
        # tests/test_fingerprint_without_resolver_is_anonymous.py.
        mint_allowed = True
        if (
            fingerprint_id
            and self._resolve_guest
            and self._has_guest_identity is not None
            and (
                getattr(request, "method", "POST") in _READ_METHODS
                or self._is_incidental_request(request)
            )
        ):
            # A read (or an incidental write) from a fingerprint that never did
            # anything meaningful: no account.
            mint_allowed = await self._has_guest_identity(fingerprint_id)

        if fingerprint_id and self._resolve_guest and mint_allowed:
            user_id = await self._resolve_guest(
                fingerprint_id,
                ctx.ip_address,
                ctx.user_agent,
                route=f"{getattr(request, 'method', 'WS')} {request.url.path}",
            )

            # Sign the (fingerprint, user_id) pair so callers can verify
            # later (e.g. /files/migrate-guest-to-user proves the caller
            # was the guest at this UUID before they signed up).
            new_metadata = dict(ctx.metadata)
            try:
                new_metadata["guest_fingerprint_signature"] = self._sign_fingerprint(
                    fingerprint_id,
                    user_id,
                )
            except Exception:
                pass

            return ctx.with_overrides(
                auth_type="fingerprint",
                fingerprint_id=fingerprint_id,
                user_id=user_id,
                metadata=new_metadata,
            )

        return None
