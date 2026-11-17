"""The RBAC service: who owns each Apollo product, who it is shared with, and who may see it.

A separate EdgeScale service (repo `rbac-service`), decision-only: it never calls
Apollo. Not the Apollo/Teleport access layer this repo has long called "RBAC"
(`auth/apollo_rbac.py`, docs/rbac-architecture.md), which is why this package is
`rbac_service`.

Three rules hold for everything built on it, the console's Manage section first and the
MCP tools after:

1. **Every call goes through this package**, never straight to the service, so the key,
   the timeout and the fail-closed handling live in one place.
2. **Every call names a person**, the address `auth/api_keys.console_user_email`
   proved. The service decides on that person and audits under it; a call without one
   is a bug, not a service account.
3. **The service decides; this repo does not restate its rules.** A caller reads the
   answer (`allow`, `scope`) rather than re-deriving roles or tag semantics here.
"""

from __future__ import annotations

from cube_cloud.rbac_service.client import (
    Catalog,
    KeyRefused,
    RbacServiceError,
    Written,
    catalog,
    customers,
    declare,
    grant_share,
    is_edgescale,
    is_enabled,
    may,
    reassign,
    revoke_share,
    tag,
)

__all__ = [
    "Catalog", "KeyRefused", "RbacServiceError", "Written", "catalog", "customers", "declare", "grant_share",
    "is_edgescale", "is_enabled", "may", "reassign", "revoke_share", "tag",
]
