"""The JWT lane: one verifier for every Supabase JWT (HTTP and out-of-band)."""

from __future__ import annotations

import asyncio
import copy
import logging
import time
from contextvars import ContextVar

import jwt
from matrx_utils import vcprint

from matrx_connect.context.app_context import AppContext
from ..authority_retry import call_authority
from ..session_authority import (
    CurrentSessionDecision,
    JwksUnavailable,
    SessionAuthorityUnavailable,
)

from .types import (
    JWKS_REFRESH_COOLDOWN_SECONDS,
    VerifiedToken,
)


#: Why THIS request's sign-in was refused, when the token was ours and readable (set by ``verify_token_raw``).
#: "session_ended": the login session behind the token is gone (signed out, or ended by a second-factor verify).
_REFUSAL: ContextVar[str | None] = ContextVar("matrx_token_refusal", default=None)

#: What a person (or a program) is told for each reason: a 401 that says WHY, never a bare "sign in".
TOKEN_REFUSALS: dict[str, str] = {
    "expired": "Your sign-in has expired. Refresh the session (or sign in again) and send the call again.",
    "session_ended": "This sign-in's session has ended (signed out, or replaced by a newer sign-in). Sign in again "
    "and send the call again.",
    "not_accepted": "The sign-in sent with this call was not accepted (unreadable, or not issued by this server). "
    "Sign in again and send the call again.",
}


def token_refusal_reason(token_value: str) -> str | None:
    """Why a token that failed verification was refused, read from its own claims (never trusted for access):
    expired, or a session the server already found ended. None when there is nothing more to say."""
    told = _REFUSAL.get()
    if told:
        return told
    try:
        claims = jwt.decode(token_value, options={"verify_signature": False})
    except jwt.InvalidTokenError:
        return None
    exp = claims.get("exp")
    if isinstance(exp, (int, float)) and exp <= time.time():
        return "expired"
    return None


def _reject_credential(reason: str, detail: str) -> None:
    """Log a caller's token that this verifier refused: a 401 for the caller, never a server failure.

    An unreadable header, an algorithm outside the allow-list (``alg='none'`` included), a missing
    ``kid`` is what the CALLER sent, decided before any key of ours is used. It stays visible at WARNING with a
    named reason so it can be traced, and out of the ERROR-only repair queue (86 ``alg='none'`` lines
    filed as server errors on 2026-11-12). Misconfiguration of THIS verifier stays at ERROR.
    """
    vcprint(
        f"[AUTH][REJECT] reason={reason}: {detail} Rejecting the credential (401).",
        color="yellow",
        log_level="WARNING",
    )


def refused_token_context(ctx: AppContext) -> AppContext:
    """The anonymous context for a presented-and-refused sign-in, carrying WHY when the token said (expired, ended)."""
    # A credential WAS presented and refused, so there is always something to say: the token's own
    # reason when it told us, else "not_accepted" (a 401 that drops the reason reads as "send a header").
    reason = _REFUSAL.get()
    if not reason or reason not in TOKEN_REFUSALS:
        reason = "not_accepted"
    metadata = dict(ctx.metadata)
    metadata["token_refused"] = {"reason": reason, "message": TOKEN_REFUSALS[reason]}
    return ctx.with_overrides(metadata=metadata)


class JwtLane:
    """Mixin on ``AuthMiddleware``: bearer parsing, ``verify_token_raw`` and JWKS signing keys."""

    async def _validate_token(
        self,
        authorization: str,
        fingerprint_id: str | None,
        ctx: AppContext,
    ) -> AppContext | None:
        try:
            scheme, token_value = authorization.split(None, 1)
            if scheme.lower() != "bearer":
                vcprint(
                    f"[AUTH][WARN] Non-bearer scheme rejected: {scheme!r}",
                    color="yellow",
                    log_level="WARNING",
                )
                return None
        except ValueError:
            vcprint(
                "[AUTH][WARN] Malformed authorization header", color="yellow", log_level="WARNING"
            )
            return None

        # NOTE (2026-05): static admin-token escape hatch removed. The only
        # accepted auth is a Supabase-signed JWT validated below. For local
        # dev / agent auth, hosts expose a dev-login endpoint that mints
        # real JWTs for real user_ids — see aidream/api/routers/dev_login.py.

        _REFUSAL.set(None)
        verified = await self.verify_token_raw(token_value)
        if verified is None:
            # Remember WHY for the refused branch (``AuthMiddleware``): still the same 401, now saying why.
            _REFUSAL.set(token_refusal_reason(token_value))
            return None

        new_metadata = dict(ctx.metadata)
        new_metadata["jwt_claims"] = verified.claims
        # exp is deliberately omitted from the selective claims projection.
        # Carry its verified value separately for credentials derived from
        # this exact login; never re-decode the raw bearer without verification.
        new_metadata["jwt_expires_at"] = verified.expires_at
        if verified.session_decision is not None:
            decision = verified.session_decision
            new_metadata["admin_admission"] = {
                "admitted": decision.admin_admitted,
                "mfa_required": decision.mfa_required,
                "reason": decision.reason,
                "current_admin_level": decision.current_admin_level,
            }
        return ctx.with_overrides(
            user_id=verified.user_id,
            auth_type="token",
            is_authenticated=True,
            # A Supabase anonymous user (guest token) is a verified JWT like any
            # other; only account-only work tells it apart (ctx.has_account).
            is_anonymous=verified.claims.get("is_anonymous") is True,
            is_admin=verified.is_admin,
            admin_level=verified.admin_level,
            email=verified.email,
            token=verified.token,
            fingerprint_id=fingerprint_id,
            metadata=new_metadata,
        )

    async def verify_token_raw(self, token_value: str) -> VerifiedToken | None:
        """Verify one token, coalescing concurrent cache misses by token hash."""
        cached = self._token_cache_lookup(token_value)
        if cached is not None:
            result = self._verified_from_cache(token_value, cached)
        else:
            result = await self._token_flights.do(
                self._hash_token(token_value),
                lambda: self._verify_token_raw_inner(token_value),
            )
        if result is None:
            return None
        # Current authority is NEVER cached with crypto/admin identity. Each
        # admission checks after the cache/single-flight, including warm hits.
        decision: CurrentSessionDecision | None = None
        if self._resolve_current_session is not None:
            try:
                resolve_session = self._resolve_current_session
                flight_key = "login:" + self._hash_token(token_value)
                authority = await call_authority(
                    lambda: self._session_flights.do(
                        flight_key,
                        lambda: resolve_session(result),
                        limit_seconds=self._session_resolve_timeout,
                    ),
                    attempt_timeout=self._session_resolve_timeout,
                    label="Current-session authority",
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "Current-session authority unavailable (%s)", type(exc).__name__
                )
                raise SessionAuthorityUnavailable("session authority unavailable") from exc
            if isinstance(authority, CurrentSessionDecision):
                decision = authority
            elif authority is True:
                # A boolean authority proved login, not current membership/MFA.
                # It must never preserve a cached administrator grant.
                decision = CurrentSessionDecision(True, None, False, None, "login_only")
            else:
                _REFUSAL.set("session_ended")
                return None
            if not decision.active:
                _REFUSAL.set("session_ended")
                return None
        # Each caller owns its claims mapping; a mutation in one request must
        # never leak through the shared flight or completed-result cache.
        return VerifiedToken(
            user_id=result.user_id,
            is_admin=decision.admin_admitted if decision is not None else result.is_admin,
            email=result.email,
            claims=copy.deepcopy(result.claims),
            token=result.token,
            admin_level=(decision.current_admin_level if decision.admin_admitted else None)
            if decision is not None else result.admin_level,
            expires_at=result.expires_at,
            issuer=result.issuer,
            session_decision=decision,
        )

    async def _verify_token_raw_inner(self, token_value: str) -> VerifiedToken | None:
        """Verify a raw Supabase JWT (no ``Bearer`` prefix) and resolve admin
        status. Returns a ``VerifiedToken`` on success, ``None`` on any failure.

        This is the single token-verification primitive: the HTTP
        ``_validate_token`` path and any out-of-band resource server (the MCP
        OAuth TokenVerifier) both call it, so the crypto, the lazy JWKS client,
        the token cache, and the admin resolver live in exactly one place.
        """
        if not self._jwt_secret and not self._jwks_url:
            vcprint(
                "[AUTH][ERROR] Neither jwt_secret nor jwks_url is set — "
                "JWT tokens cannot be validated.",
                color="red",
                log_level="ERROR",
            )
            return None

        # JWT structural pre-check.
        # A Supabase JWT is exactly three base64url segments separated by
        # dots (header.payload.signature). When the bearer token doesn't
        # match that shape, it isn't claiming to be a JWT — it's a
        # different bearer scheme that the host's downstream routers
        # authenticate themselves (e.g. AI Dream's sandbox-bridge service
        # token + ``X-Matrx-User-Id`` header pair, or any future
        # machine-to-machine integration that shares the
        # ``Authorization: Bearer …`` header). Skipping the decode
        # silently here prevents misleading
        # ``JWT validation FAILED: Not enough segments`` ERROR-level
        # noise on every such request, while still letting the request
        # fall through to whatever auth the route itself enforces.
        # Real JWT integrity / signature / audience / expiry failures
        # still surface loudly below — those are tokens that ARE
        # claiming to be JWTs and are genuinely broken.
        if token_value.count(".") != 2:
            return None

        # Scoped-capability tokens from a registered first-party issuer are
        # not user-login tokens — they are verified by the route that owns
        # their audience (matrx_connect.scoped_tokens). Fall through
        # silently instead of failing loudly on the audience check.
        if self._passthrough_issuers:
            try:
                unverified = jwt.decode(token_value, options={"verify_signature": False})
                if unverified.get("iss") in self._passthrough_issuers:
                    return None
            except jwt.InvalidTokenError:
                pass  # not even decodable — let the normal path report it

        # Hot path: a fresh cache entry skips the JWT decode AND the admin
        # DB lookup. pdf.js fires 5–6 HTTP Range requests against
        # /files/{id}/download in ~200ms for a single document open, each
        # carrying the same Bearer token — the cache collapses them to one
        # real validation.
        cached = self._token_cache_lookup(token_value)
        if cached is not None:
            return self._verified_from_cache(token_value, cached)

        try:
            # Peek at the unverified header to pick the verification key.
            # Symmetric (HS256) → shared secret; asymmetric (RS256/ES256)
            # → JWKS signing key resolved by ``kid``.
            try:
                unverified_header = jwt.get_unverified_header(token_value)
            except jwt.InvalidTokenError as exc:
                _reject_credential("header_unreadable", f"{type(exc).__name__}: {exc}")
                return None
            alg = unverified_header.get("alg", "HS256")

            allowed = list(self._jwt_algorithms)
            if alg not in allowed:
                _reject_credential(
                    "alg_not_allowed",
                    f"alg={alg!r} not in allow-list {allowed}."
                    f"{self._unverified_origin(token_value, unverified_header)}",
                )
                return None

            decode_key: object
            if alg == "HS256":
                if not self._jwt_secret:
                    vcprint(
                        "[AUTH][WARN] HS256 token rejected because jwt_secret "
                        "is not configured; rejecting.",
                        color="yellow",
                        log_level="WARNING",
                    )
                    return None
                decode_key = self._jwt_secret
            else:
                # Asymmetric — use JWKS.
                if not self._jwks_url:
                    vcprint(
                        f"[AUTH][ERROR] {alg} token received but jwks_url "
                        "is not configured; rejecting.",
                        color="red",
                        log_level="ERROR",
                    )
                    return None
                if self._jwks_client is None:
                    # Lazy build; PyJWKClient handles HTTP fetch + cache.
                    self._jwks_client = jwt.PyJWKClient(self._jwks_url)
                try:
                    kid_value = unverified_header.get("kid")
                    if not isinstance(kid_value, str) or not kid_value:
                        _reject_credential("kid_missing", f"{alg} token carries no kid.")
                        return None
                    kid = kid_value
                    signing_key = await self._jwks_flights.do(
                        kid,
                        lambda: self._get_signing_key(kid),
                    )
                except JwksUnavailable:
                    # The key endpoint could not be read (or is cooling down
                    # after a failed read): the token was never judged. Surface
                    # it as a retryable 503, never a 401 that signs people out.
                    raise
                except (jwt.PyJWKClientError, jwt.PyJWKClientConnectionError) as exc:
                    # An absent signing key is an authentication rejection, not
                    # an application crash. This is expected for stale sessions
                    # after a key rotation and for tokens issued by an unrelated
                    # project. Keep it visible for security/operator correlation,
                    # but out of the ERROR-only application-failure safety net.
                    vcprint(
                        f"[AUTH][WARN] JWKS key lookup rejected token for "
                        f"alg={alg}: {type(exc).__name__}: {exc}",
                        color="yellow",
                        log_level="WARNING",
                    )
                    return None
                decode_key = signing_key.key

            decode_kwargs: dict = {"algorithms": [alg]}
            if self._jwt_audience:
                decode_kwargs["audience"] = self._jwt_audience
            else:
                decode_kwargs["options"] = {"verify_aud": False}
            # Signature verification is CPU-bound (RSA/EC math); off the loop so a burst of
            # cold tokens never freezes every other request.
            decoded = await asyncio.to_thread(jwt.decode, token_value, decode_key, **decode_kwargs)
            user_id = decoded.get("sub", "")
            vcprint(f"[AUTH][INFO] JWT accepted: user={user_id}", color="green", log_level="INFO")

            # Resolve admin status. The tier resolver is preferred (it also
            # yields the level); is_admin is derived as ``level is not None``.
            # A host that only wired the boolean resolver still works.
            is_admin = False
            admin_level: str | None = None
            if self._admin_level_resolver and user_id:
                try:
                    admin_level = await self._admin_level_resolver(user_id)
                    is_admin = admin_level is not None
                except Exception as exc:
                    vcprint(
                        f"[AUTH][WARN] Admin tier check failed for user={user_id}: {exc}",
                        color="yellow",
                        log_level="WARNING",
                    )
            elif self._is_admin_resolver and user_id:
                try:
                    is_admin = await self._is_admin_resolver(user_id)
                except Exception as exc:
                    vcprint(
                        f"[AUTH][WARN] Admin check failed for user={user_id}: {exc}",
                        color="yellow",
                        log_level="WARNING",
                    )

            if is_admin:
                vcprint(
                    f"[AUTH][INFO] Admin confirmed from DB: user={user_id} "
                    f"level={admin_level or 'unknown'}",
                    color="green",
                    log_level="INFO",
                )

            # Stash the raw claims on metadata under a known key so
            # downstream resolvers (organization_id, custom scopes) can read
            # them without re-decoding. Strip the signature/exp metadata from
            # the snapshot — claims-only.
            jwt_claims = {
                k: v
                for k, v in decoded.items()
                if k not in ("iat", "exp", "nbf", "jti", "iss", "sub")
            }
            email = decoded.get("email")
            # Insert into the validation cache so subsequent requests with
            # the same Bearer token within the TTL window short-circuit the
            # JWT decode + admin DB lookup. ``exp`` is the JWT's own
            # expiry (if present) — the insert caps TTL at remaining
            # lifetime so a cached entry never outlives the token.
            self._token_cache_insert(
                token_value,
                user_id=user_id,
                is_admin=is_admin,
                admin_level=admin_level,
                email=email,
                jwt_claims=jwt_claims,
                jwt_exp=decoded.get("exp"),
                jwt_issuer=decoded.get("iss"),
            )

            return VerifiedToken(
                user_id=user_id,
                is_admin=is_admin,
                email=email,
                claims=copy.deepcopy(jwt_claims),
                token=token_value,
                admin_level=admin_level,
                expires_at=decoded.get("exp"),
                issuer=decoded.get("iss"),
            )
        except jwt.ExpiredSignatureError:
            # Expiry is normal session lifecycle, not a signature/integrity
            # incident. The HTTP boundary emits one compact 401 outcome; logging
            # a second red traceback-sized alarm here made routine refreshes look
            # like uncaught server failures. Out-of-band verifiers simply return
            # rejection and let their transport produce its normal challenge.
            return None
        except jwt.InvalidTokenError as e:
            # A JWT-shaped token whose signature or audience fails against OUR key stays at ERROR:
            # a wrong secret, a swapped key or an audience change would fail every sign-in here,
            # and that is a server regression (pinned by test_jwt_with_bad_signature_rejected_loudly).
            vcprint(
                f"[AUTH][ERROR] JWT validation FAILED: {type(e).__name__}: {e}",
                color="red",
                log_level="ERROR",
            )
            return None

    @staticmethod
    def _unverified_origin(token_value: str, header: dict[str, object]) -> str:
        """Who a rejected token claims to come from: issuer, kid and role, never the token.

        A rejected-algorithm line that names no caller cannot be traced to the client still
        holding the old token (275 a day on 2026-11-06, route unknown). These claims are read
        WITHOUT trusting them and only to be logged.
        """
        try:
            claims = jwt.decode(token_value, options={"verify_signature": False})
        except jwt.InvalidTokenError:
            claims = {}
        parts = {
            "iss": claims.get("iss"),
            "role": claims.get("role"),
            "aud": claims.get("aud"),
            "kid": header.get("kid"),
        }
        shown = " ".join(f"{k}={v!r}" for k, v in parts.items() if v)
        return f" Token claims (unverified): {shown}." if shown else ""

    async def _get_signing_key(self, kid: str) -> object:
        # PyJWKClient performs synchronous HTTP and owns mutable caches. Keep it
        # off the event loop, serialize access, and allow at most one forced
        # refresh per cooldown. Random unknown kids therefore cannot trigger an
        # outbound JWKS request each.
        async with self._jwks_lookup_lock:
            cached = self._jwks_keys.get(kid)
            if cached is not None:
                return cached

            now = time.monotonic()
            if not self._jwks_keys:
                if (
                    self._jwks_last_refresh
                    and now - self._jwks_last_refresh < JWKS_REFRESH_COOLDOWN_SECONDS
                ):
                    raise JwksUnavailable("JWKS refresh is cooling down after a failed fetch")
                # Set before I/O so a failed fetch is negatively cached for the
                # cooldown instead of every queued token retrying the network.
                self._jwks_last_refresh = now
                try:
                    signing_keys = await asyncio.to_thread(self._jwks_client.get_signing_keys)
                except Exception as exc:
                    raise JwksUnavailable("JWKS fetch failed") from exc
                self._jwks_keys.update({key.key_id: key for key in signing_keys if key.key_id})
            elif now - self._jwks_last_refresh >= JWKS_REFRESH_COOLDOWN_SECONDS:
                # A failed forced refresh is still a refresh attempt. Record it
                # before outbound I/O so queued unknown kids cannot each retry
                # the same failing endpoint. Keep the last known-good keys
                # unless the fetch succeeds.
                self._jwks_last_refresh = now
                try:
                    signing_keys = await asyncio.to_thread(
                        self._jwks_client.get_signing_keys,
                        True,
                    )
                except Exception as exc:
                    raise JwksUnavailable("JWKS refresh failed") from exc
                self._jwks_keys = {key.key_id: key for key in signing_keys if key.key_id}

            signing_key = self._jwks_keys.get(kid)
            if signing_key is None:
                raise jwt.PyJWKClientError(f'Unable to find a signing key that matches: "{kid}"')
            return signing_key
