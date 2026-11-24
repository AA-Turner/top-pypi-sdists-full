"""The per-token validation cache behind the JWT lane."""

from __future__ import annotations

import copy
import hashlib
import time
from typing import Any



from .types import (
    VerifiedToken,
)


class TokenCacheLane:
    """Mixin on ``AuthMiddleware``: SHA256(token) -> verified identity, TTL-bounded."""

    @staticmethod
    def _hash_token(token: str) -> str:
        # Full SHA256 hex; never store the raw token. Collisions are
        # computationally infeasible.
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _token_cache_lookup(
        self,
        token: str,
    ) -> (
        tuple[
            str,
            bool,
            str | None,
            dict[str, Any],
            str | None,
            int | None,
            str | None,
        ]
        | None
    ):
        """Return identity, claims, and JWT lifecycle metadata for a fresh
        entry. Expired entries are evicted on access."""
        if self._token_cache_ttl <= 0 or not self._token_cache:
            return None
        key = self._hash_token(token)
        entry = self._token_cache.get(key)
        if entry is None:
            return None
        (
            cache_expires_at,
            user_id,
            is_admin,
            email,
            jwt_claims,
            admin_level,
            jwt_expires_at,
            issuer,
        ) = entry
        if time.monotonic() >= cache_expires_at:
            self._token_cache.pop(key, None)
            return None
        return (
            user_id,
            is_admin,
            email,
            jwt_claims,
            admin_level,
            jwt_expires_at,
            issuer,
        )

    def _token_cache_insert(
        self,
        token: str,
        *,
        user_id: str,
        is_admin: bool,
        admin_level: str | None,
        email: str | None,
        jwt_claims: dict[str, Any],
        jwt_exp: int | None,
        jwt_issuer: str | None,
    ) -> None:
        """Store a successful validation. TTL is capped by the JWT's own
        ``exp`` so a cached entry can never outlive the token itself."""
        if self._token_cache_ttl <= 0 or self._token_cache_max_size <= 0:
            return
        now_mono = time.monotonic()
        ttl = self._token_cache_ttl
        if jwt_exp is not None:
            remaining = float(jwt_exp) - time.time()
            if remaining <= 0:
                return  # token already expired — don't pollute the cache
            ttl = min(ttl, remaining)
        # Opportunistic sweep when full: drop expired entries first, then
        # the oldest by expiry. Cheap because the cache is tiny.
        if len(self._token_cache) >= self._token_cache_max_size:
            expired_keys = [k for k, v in self._token_cache.items() if v[0] <= now_mono]
            for k in expired_keys:
                self._token_cache.pop(k, None)
            if len(self._token_cache) >= self._token_cache_max_size:
                # Drop the oldest entries until we're back under the cap.
                ordered = sorted(self._token_cache.items(), key=lambda kv: kv[1][0])
                drop_n = len(self._token_cache) - self._token_cache_max_size + 1
                for k, _ in ordered[:drop_n]:
                    self._token_cache.pop(k, None)
        self._token_cache[self._hash_token(token)] = (
            now_mono + ttl,
            user_id,
            is_admin,
            email,
            copy.deepcopy(jwt_claims),
            admin_level,
            jwt_exp,
            jwt_issuer,
        )

    @staticmethod
    def _verified_from_cache(
        token_value: str,
        cached: tuple[
            str,
            bool,
            str | None,
            dict[str, Any],
            str | None,
            int | None,
            str | None,
        ],
    ) -> VerifiedToken:
        (
            user_id,
            is_admin,
            email,
            jwt_claims,
            admin_level,
            expires_at,
            issuer,
        ) = cached
        return VerifiedToken(
            user_id=user_id,
            is_admin=is_admin,
            email=email,
            claims=copy.deepcopy(jwt_claims),
            token=token_value,
            admin_level=admin_level,
            expires_at=expires_at,
            issuer=issuer,
        )
