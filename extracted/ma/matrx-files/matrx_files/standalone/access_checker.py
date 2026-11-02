"""Inject the authoritative DB access policy into the standalone service.

The package's Python permission fallback (`cloud_sync/permissions.py::check_async`)
is a DELIBERATE SUBSET — owner / public / direct-grant / folder only. It cannot
see orgs, memberships, `platform.reachability`, or the contextual crawl-artifact
→ `web.site` container grant. In a HOSTED deployment aidream injects
`files.has_access_for` as the checker (`install_file_access_checker`), so the
async file gate is answered by the ONE authoritative DB policy. The standalone
microservice must do the IDENTICAL wiring — without it, every container-derived
file (e.g. a web-crawl screenshot an org member should see) is silently denied
with `has 'none'`, even though `files.has_access_for` would grant it.

Never "improve" the Python fallback into a second policy — fix the DB function
and inject it here. This module is the standalone twin of aidream's
`services/file_access/resolver.py`, using the package's own `matrx_files` DB
binding instead of the host's PRIMARY pool (independence-compliant).
"""

from __future__ import annotations

from matrx_orm import call_function

from matrx_files.cloud_sync.permissions import configure_access_checker

# matrx-utils speaks read/write/admin; the DB enum is viewer < editor < admin.
_LEVEL_TO_DB: dict[str, str] = {"read": "viewer", "write": "editor", "admin": "admin"}

# The package's registered matrx-orm config name (every files.* Model uses
# `_database = "matrx_files"`; bootstrap_db binds the pool under this name).
_DB = "matrx_files"


async def db_access_allowed(
    user_id: str,
    resource_type: str,
    resource_id: str,
    level: str = "read",
) -> bool:
    """True iff `user_id` may act on `resource_id` at `level`, per the DB policy.

    Files route through `files.has_access_for` (so a contextual system artifact
    resolves via its container, not its historical owner); everything else uses
    the generic `iam.has_access_for`. Identical shape to aidream's
    `file_access_allowed`, on the package's own DB binding.
    """
    if not user_id or not resource_id:
        return False
    try:
        db_level = _LEVEL_TO_DB[level]
    except KeyError:
        raise ValueError(
            f"unknown access level {level!r} — expected one of {sorted(_LEVEL_TO_DB)}"
        ) from None
    if resource_type == "file":
        return bool(
            await call_function(_DB, "files", "has_access_for", user_id, resource_id, db_level)
        )
    return bool(
        await call_function(
            _DB, "iam", "has_access_for", user_id, resource_type, resource_id, db_level
        )
    )


def install_standalone_access_checker() -> None:
    """Make the DB policy the single source of truth for the async file gate.

    Async only (`sync_checker=None`, matching aidream): the sync `require` path
    cannot borrow the async DB pool from a foreign loop, so it stays on the
    deny-more Python subset. The request path (`get_authorized_record_async` →
    `require_async`) is async and now consults the authoritative DB policy.
    """
    configure_access_checker(db_access_allowed, sync_checker=None)
