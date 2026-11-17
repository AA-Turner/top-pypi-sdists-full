"""The companies a tag edit can name: the rbac-service's enabled customers.

A tag edit picks a company from this list rather than taking one typed in, so nobody
reaches a confirmation for a company that does not exist. A company that is not here
has to be created on the rbac-service first (an admin call; nothing here creates one),
and the service refuses an owner or a share naming one anyway, so the list guides the
choice and the service still decides it.

`shared` and `internal` are not in the list: they are fixed names, not customers, and a
surface offers them itself where they apply (an owner, never a share).
"""

from __future__ import annotations

from cube_cloud import rbac_service
from cube_cloud.auth.api_keys import hash_email
from cube_cloud.config import settings
from cube_cloud.console import cache
from cube_cloud.manage.tags import _COMPANY, INTERNAL, SHARED, require_writes

# The fields a company carries out of this module (console rule: an allowlist, never the
# service's object passed through).
COMPANY_FIELDS = frozenset({"company", "display_name"})


async def list_companies(email: str | None) -> dict:
    """`{"companies": [{company, display_name}]}`: the enabled companies the rbac-service
    lets `email` see, sorted by key, for picking a tag edit's company.

    Offered only where tag edits are (`require_writes`: this stack edits tags and the
    caller is EdgeScale staff), since nothing else needs it and the list names every
    customer. Cached per person for `rbac_service_cache_ttl_seconds`, like the catalog:
    a company created on the service shows within that. A key without `customers:read`
    raises `rbac_service.KeyRefused`; any other failure `RbacServiceError`.
    """
    await require_writes(email)
    rows = await cache.get_or_set(
        "rbac-service-customers", hash_email(email), lambda: rbac_service.customers(email),
        ttl=settings.rbac_service_cache_ttl_seconds,
    )
    companies = [
        {"company": r["company"], "display_name": r["display_name"]}
        for r in rows
        if _COMPANY.match(r["company"]) and r["company"] not in (SHARED, INTERNAL)
    ]
    return {"companies": companies}
