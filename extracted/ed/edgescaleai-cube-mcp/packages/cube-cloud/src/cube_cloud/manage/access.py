"""Who may use the management operations. The rbac-service decides; this only asks it."""

from __future__ import annotations

import logging
import time

from cube_cloud import rbac_service
from cube_cloud.auth.api_keys import hash_email
from cube_cloud.config import settings
from cube_cloud.console import cache

logger = logging.getLogger(__name__)

# The shortest gap between two `fresh` reads one person can cause, per ECS task. A fresh
# read is one rbac-service call (and one audit row), never an Apollo read, so this caps
# what a staff member's page can ask for at one call per gap rather than one per request.
FRESH_FLOOR_SECONDS = 5.0
# hash_email(address) -> when that person last caused a fresh read (monotonic). Only
# verified EdgeScale addresses reach it, so it stays as small as the staff.
_fresh_at: dict[str, float] = {}


class NotPermitted(Exception):
    """The caller may not manage. Rendered by every surface as "not found", never 403."""


def is_offered(email: str | None) -> bool:
    """Whether to OFFER management to this caller: the stack serves it and the address is
    a verified EdgeScale one. Makes no call, so a surface can ask on every page load. A
    hint only; `require_staff` is the decision."""
    return rbac_service.is_enabled() and rbac_service.is_edgescale(email)


async def require_staff(email: str | None, *, fresh: bool = False) -> rbac_service.Catalog:
    """Raise `NotPermitted` unless the rbac-service answers `email` with scope `*`.

    The answer is the person's catalog, which also carries every product tag, so the
    product operations reuse it rather than asking twice. It is cached per person for
    `rbac_service_cache_ttl_seconds`: each `*` read writes an audit row on the service,
    and a revoked grant should take effect within that, not within a session. The slot
    is the address's hash, never the address: `console/cache.py` logs slot names, and a
    cleartext address would outlive the request in memory.

    The address check runs first so nobody else's request ever reaches the service.

    `fresh` asks for the service's answer now rather than a cached one: the page sends it
    after a tag edit, because the cache is per ECS task and an edit only clears the
    task that made it, so a reload served by another task could otherwise show the old
    tag. It is honored at most once per `FRESH_FLOOR_SECONDS` per person; inside that, the
    cached answer is at most that old.
    """
    if not is_offered(email):
        raise NotPermitted()
    slot = hash_email(email)
    if fresh:
        now = time.monotonic()
        if now - _fresh_at.get(slot, float("-inf")) >= FRESH_FLOOR_SECONDS:
            _fresh_at[slot] = now
            cache.drop("rbac-service", slot)
    answer = await cache.get_or_set(
        "rbac-service", slot, lambda: rbac_service.catalog(email),
        ttl=settings.rbac_service_cache_ttl_seconds,
    )
    if not answer.internal:
        # Every surface shows a refusal as "not found", so this line is the only place
        # that says why. The service's reason, never the address or the answer's items.
        logger.warning("manage: the rbac-service did not grant staff access (%s)",
                       answer.reason or ("no '*' in scope" if answer.allow else "denied, no reason given"))
        raise NotPermitted()
    return answer


# How long a "could not ask" access answer is held. Shorter than a real answer, so a
# recovered service shows the section soon; long enough that an outage does not make
# every page load wait out the service's timeout again.
ACCESS_FAILURE_TTL_SECONDS = 10.0

# The question that stands for "may edit product tags": may this person reassign a
# product the internal tenant owns? That takes `access` on internal, which the service
# gives an EdgeScale manager or admin and no one else; it is also the least any staff
# edit needs.
EDIT_ACTION, EDIT_COMPANY = "product.reassign", "internal"


async def offer(email: str | None) -> dict:
    """What a surface should OFFER this caller: `{"view": bool, "edit": bool}`.

    Both are the rbac-service's answers, not inferred here. `view` is `require_staff`
    (scope `*`, any EdgeScale grant), sharing its cached catalog. `edit` is asked only
    where this stack edits tags (`rbac_service_writes_enabled`) and the person can view:
    one `POST /v1/decide` for `EDIT_ACTION` on `EDIT_COMPANY`, which needs the key's
    `decide` scope.

    Still a hint: every read and write asks the service again. So when the service
    cannot be asked, the answer is no (hide), held `ACCESS_FAILURE_TTL_SECONDS`; a real
    answer is held `rbac_service_cache_ttl_seconds`, like the catalog. Raises
    `NotPermitted` only for a caller who is not offered management at all.
    """
    if not is_offered(email):
        raise NotPermitted()

    async def ask() -> dict:
        try:
            await require_staff(email)
        except NotPermitted:
            return {"view": False, "edit": False}
        except rbac_service.RbacServiceError as e:
            logger.warning("manage: could not ask the rbac-service whether to offer Manage (%s)", e)
            return {"view": False, "edit": False, "unknown": True}
        if not settings.rbac_service_writes_enabled:
            return {"view": True, "edit": False}
        try:
            edit = await rbac_service.may(email, EDIT_ACTION, EDIT_COMPANY)
        except rbac_service.KeyRefused as e:
            # Most likely the key lacks the `decide` scope: the edits work, but are not offered.
            logger.warning("manage: the rbac-service refused the edit question; is `decide` in the key's "
                           "scopes? (%s)", e)
            return {"view": True, "edit": False, "unknown": True}
        except rbac_service.RbacServiceError as e:
            logger.warning("manage: could not ask the rbac-service whether to offer tag edits (%s)", e)
            return {"view": True, "edit": False, "unknown": True}
        return {"view": True, "edit": edit}

    ttl = settings.rbac_service_cache_ttl_seconds
    answer = await cache.get_or_set(
        "manage-access", hash_email(email), ask, ttl=ttl,
        ttl_for=lambda a: ACCESS_FAILURE_TTL_SECONDS if a.get("unknown") else ttl,
    )
    return {"view": answer["view"], "edit": answer["edit"]}
