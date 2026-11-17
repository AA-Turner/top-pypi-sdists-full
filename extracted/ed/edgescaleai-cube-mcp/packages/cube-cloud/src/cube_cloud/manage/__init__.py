"""Management operations over the rbac-service: product tags (read and edit) now; customers, partners and users later.

One module underneath every surface that manages access (AGENTS.md rule 3). The
console's Manage section (docs/console-spec.md §4.30) calls it today; MCP tools for
the same people are meant to call the same functions later, so nothing here knows
about HTTP responses, React, or tool text. Each operation:

- takes the caller's VERIFIED address (`auth/api_keys.console_user_email` on the
  console) and refuses without one;
- authorizes before it reads anything (AGENTS.md rule 4), raising `NotPermitted`,
  which a surface renders as its own "not found";
- lets `rbac_service.RbacServiceError` through, which a surface renders as "could not
  read", never as an allow;
- returns plain, allowlisted dicts.

**Who may manage, today: EdgeScale staff,** decided by the rbac-service (scope `*`, any
EdgeScale grant), never by the Apollo profile. When customer or partner admins get
self-service, `require_staff` becomes a per-operation decision on the service and the
operations below narrow by its scope; the surfaces do not change shape.
"""

from __future__ import annotations

from cube_cloud.manage.access import NotPermitted, is_offered, offer, require_staff
from cube_cloud.manage.companies import COMPANY_FIELDS, list_companies
from cube_cloud.manage.products import PRODUCT_FIELDS, list_products
from cube_cloud.manage.tags import (
    SHARE_ROLES,
    InvalidInput,
    set_owner,
    share,
    unshare,
    writes_offered,
)

__all__ = [
    "COMPANY_FIELDS", "InvalidInput", "NotPermitted", "PRODUCT_FIELDS", "SHARE_ROLES", "is_offered",
    "list_companies", "list_products", "offer", "require_staff", "set_owner", "share", "unshare", "writes_offered",
]
