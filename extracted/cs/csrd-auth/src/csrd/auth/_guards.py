"""Authority-based access control guards for FastAPI."""

import logging
from collections.abc import Callable

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from csrd.context.platform import user_info_context
from csrd.models.claims import UserClaims

logger = logging.getLogger(__name__)


def _get_current_claims() -> UserClaims:
    """Retrieve the current user's claims from the request context.

    Raises ``HTTPException(403)`` if no claims are available (i.e. no
    authentication dependency has run yet for this request).
    """
    claims = user_info_context.get()
    if claims is None or not isinstance(claims, UserClaims):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="No authenticated user in request context",
        )
    result: UserClaims = claims
    return result


def require_authorities(*required: str) -> Callable:
    """FastAPI dependency factory that enforces authority requirements.

    Returns a dependency that checks ``UserClaims.authorities`` from the
    current request context.  All specified authorities must be present;
    if any are missing, a 403 Forbidden response is raised.

    Parameters
    ----------
    *required:
        One or more authority strings that must all be present in the
        user's claims.

    Usage
    -----
    Router-level (protects all routes on the router)::

        router = APIRouter(
            dependencies=[Depends(require_authorities("ADMIN"))],
        )

    Per-endpoint::

        @router.get("/sensitive")
        async def sensitive(
            _guard=Depends(require_authorities("ADMIN", "MANAGER")),
        ):
            ...
    """
    if not required:
        raise ValueError("require_authorities() requires at least one authority")

    async def _guard() -> None:
        claims = _get_current_claims()
        missing = set(required) - set(claims.authorities)
        if missing:
            logger.debug(
                "Authority check failed for sub=%s: missing %s (has %s)",
                claims.sub,
                sorted(missing),
                claims.authorities,
            )
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Insufficient authorities",
            )

    return _guard


def require_any_authority(*required: str) -> Callable:
    """FastAPI dependency factory that requires at least one of the given authorities.

    Unlike :func:`require_authorities` which requires **all** listed
    authorities, this requires that the user has **at least one**.

    Parameters
    ----------
    *required:
        One or more authority strings; the user must have at least one.
    """
    if not required:
        raise ValueError("require_any_authority() requires at least one authority")

    async def _guard() -> None:
        claims = _get_current_claims()
        if not set(required) & set(claims.authorities):
            logger.debug(
                "Authority check failed for sub=%s: has none of %s (has %s)",
                claims.sub,
                sorted(required),
                claims.authorities,
            )
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Insufficient authorities",
            )

    return _guard
