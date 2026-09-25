"""The team secret: a second lock on platform-lifecycle routes.

It used to be a global middleware gating every route but an exemption list, which
made the whole API -- `innoday login` included -- need a shared secret on top of
the user's own token. Identity is the Bearer token. The secret now guards only
the routes that create or destroy a platform user or organization (Tier C, see
tests/test_auth_tiers.py), plus `POST /api/v1/auth/sign-in-link`, the one
unauthenticated route that sends email (PF-455).
"""

import hmac
import os

from fastapi import HTTPException, Request


def require_team_secret(request: Request) -> None:
    """Route-level team-secret gate -- the only one there is. No-op when
    TEAM_ACCESS_SECRET is unset (local dev). Raises 401 on a missing/invalid
    header. Attach it as an additional dependency, beside the route's own auth:

        @router.post("/users", dependencies=[Depends(require_team_secret)])
    """
    secret = os.getenv("TEAM_ACCESS_SECRET")
    if not secret:
        return
    if not hmac.compare_digest(request.headers.get("X-Team-Secret", ""), secret):
        raise HTTPException(
            status_code=401, detail="Missing or invalid X-Team-Secret header"
        )
