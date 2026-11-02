"""Permissions manager for the cloud sync layer.

Provides ACL support: owner-based, direct user (and org) grants on the
canonical ``iam.permissions`` table, folder-inherited permissions, and
shareable links with optional expiry and use limits. (The legacy
group-based ACL tier was removed in the 2026 DB canonicalization.)

Permission levels (ordered by power):
    read  — view / download the file
    write — read + modify / overwrite the file
    admin — write + manage permissions, delete the file

Usage::

    pm = PermissionsManager(db, user_id="current-user-uuid")

    # Grant read access to another user
    pm.grant("file", file_id, grantee_id="other-user", level="read")

    # Check access
    level = pm.check("file", file_id)  # returns "admin" | "write" | "read" | None

    # Create a share link (canonical platform.share_links; viewer/editor)
    link = pm.create_share_link("file", file_id, permission_level="viewer", max_uses=10)
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Literal

from .db import DatabaseClient

logger = logging.getLogger(__name__)

PermissionLevel = Literal["read", "write", "admin"]
ResourceType = Literal["file", "folder"]

_LEVEL_RANK = {"admin": 3, "write": 2, "read": 1}

# Appended to every denial produced by the standalone Python SUBSET resolver
# (no host-injected DB checker). This wording difference is load-bearing: a
# denial carrying this marker means the deployment is running WITHOUT the
# authoritative DB policy (`configure_access_checker` was never called) — a
# wiring defect to fix, never a real permission verdict to debug. The injected
# path's denials say "lacks '<level>' access" and never carry this marker.
# (2026-07-29: files.matrxserver.com served exactly this denial for crawl
# artifacts the DB policy grants, because the deployed build predated
# `install_standalone_access_checker`.)
_FALLBACK_DENIAL_MARKER = (
    " [python-subset-fallback: no authoritative DB access checker is injected"
    " on this deployment — see configure_access_checker]"
)

# The SYNC gate stays on the subset even on correctly-wired deployments (both
# hosts inject async-only: the DB pool can't answer from a foreign loop). Its
# marker must NOT claim the deployment is unwired — that sends a debugger
# hunting a wiring defect that doesn't exist.
_SYNC_FALLBACK_DENIAL_MARKER = (
    " [python-subset (sync path): synchronous file access never consults the DB"
    " policy — the async gate on this deployment may still be correctly injected]"
)


# ---------------------------------------------------------------------------
# THE authoritative access resolver (host-injected)
# ---------------------------------------------------------------------------
# The access policy has ONE implementation and it lives in the DATABASE
# (`iam.has_access_for(user_id, type, id, level)` — owner, org-admin, public,
# `internal` + org, explicit grants, memberships, `platform.reachability`
# transitive containers, super-admin, containment recursion). RLS calls the same
# body through `iam.has_access()` with `auth.uid()`.
#
# This package cannot reach the DB itself (no ORM dependency — it is the root of
# the graph), so the host INJECTS the resolver. When injected it is the single
# source of truth and the Python resolution below is NOT consulted at all.
#
# The Python fallback (owner -> public -> direct grant -> parent folder) exists
# ONLY so matrx-utils runs standalone. It is a deliberate SUBSET of the real
# policy: it cannot see orgs, memberships or reachability. NEVER treat it as the
# policy, and never "improve" it into a second implementation — fix the DB
# function instead. See db/migrations/0159_iam_has_access_for.sql.
AccessChecker = Callable[[str, str, str, str], Awaitable[bool]]
SyncAccessChecker = Callable[[str, str, str, str], bool]

_access_checker: AccessChecker | None = None
_sync_access_checker: SyncAccessChecker | None = None


def configure_access_checker(
    checker: AccessChecker | None,
    *,
    sync_checker: SyncAccessChecker | None = None,
) -> None:
    """Inject the host's authoritative access resolver.

    ``checker(user_id, resource_type, resource_id, level) -> bool`` where
    ``level`` is ``"read" | "write" | "admin"``. Once set, it decides every
    file/folder access question; the built-in Python fallback is bypassed.
    """
    global _access_checker, _sync_access_checker
    _access_checker = checker
    _sync_access_checker = sync_checker


def get_access_checker() -> AccessChecker | None:
    return _access_checker


def get_sync_access_checker() -> SyncAccessChecker | None:
    return _sync_access_checker


def _higher(a: str | None, b: str | None) -> str | None:
    """Return the higher of two permission levels."""
    if a is None:
        return b
    if b is None:
        return a
    return a if _LEVEL_RANK.get(a, 0) >= _LEVEL_RANK.get(b, 0) else b


def _is_expired(row: dict) -> bool:
    """Return True if the permission/link has expired."""
    exp = row.get("expires_at")
    if not exp:
        return False
    if isinstance(exp, str):
        exp = datetime.fromisoformat(exp.replace("Z", "+00:00"))
    return exp <= datetime.now(UTC)


def _is_contextual_system_artifact(record: dict) -> bool:
    """True when access must be derived from an external container.

    These records (web-crawl snapshots/screenshots) are system evidence owned
    by a container, not by the user whose id happens to sit in ``created_by``/
    ``owner_id``. For them the resolver SKIPS the owner and ``published_to_web``
    shortcuts and resolves via explicit ``iam.permissions`` grants
    plus the platform judge (``public.has_access_as`` — the canonical
    container-access evaluator), which ALWAYS runs. Folder inheritance is also
    skipped: their access is container-derived, never folder-derived.
    """
    metadata = record.get("metadata") or {}
    return bool(metadata.get("system_artifact") and metadata.get("artifact_domain") == "web_crawl")


class PermissionsManager:
    """Resolves and manages access control for cloud files and folders."""

    def __init__(self, db: DatabaseClient, user_id: str = "") -> None:
        self._db = db
        self._user_id = user_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str) -> None:
        self._user_id = value

    # ------------------------------------------------------------------
    # Permission checking
    # ------------------------------------------------------------------

    def _effective_uid(self, explicit: str | None) -> str:
        """Resolve user_id with the same priority as SyncEngine._resolve_user_id."""
        if explicit:
            return explicit
        if self._user_id:
            return self._user_id
        try:
            from matrx_utils.ctx import get_active_user_id

            return get_active_user_id() or ""
        except Exception:
            return ""

    def check(
        self,
        resource_type: ResourceType,
        resource_id: str,
        user_id: str | None = None,
    ) -> str | None:
        """Return the effective permission level for *user_id* on a resource.

        Resolution is done here against ``files.*`` + the canonical
        ``iam.permissions`` table (owner → public → explicit grant →
        folder inheritance → ``public.has_access_as`` platform judge for
        reachability / Shared Knowledge). The deprecated
        ``cld_get_effective_permission`` function is gone, and the
        JWT-based ``iam.has_access`` resolver cannot stand in for it
        alone: this layer talks to Postgres with the SERVICE-ROLE key,
        so ``auth.uid()`` is NULL and ``iam.has_access`` would deny
        everything. We resolve explicitly for a passed-in ``user_id``
        instead, including ``has_access_as(p_user=…)`` for cascades.
        (The user-group ACL tier is removed.)

        Contextual system artifacts (``_is_contextual_system_artifact``) skip
        the owner / public / folder tiers and resolve via explicit grants +
        the platform judge only.
        """
        uid = self._effective_uid(user_id)
        if not uid:
            return None

        # 1. Ownership check
        if resource_type == "file":
            record = self._db.get_file(resource_id)
        else:
            record = self._db.get_folder(resource_id)

        if not record:
            return None
        # Contextual system artifacts (web-crawl evidence) are container-owned:
        # historical created_by/owner ownership and published_to_web must
        # NOT confer access, and the platform judge always gets the question.
        contextual = resource_type == "file" and _is_contextual_system_artifact(record)
        level: str | None = None
        if not contextual:
            if record.get("owner_id") == uid:
                return "admin"
            if record.get("published_to_web"):
                level = "read"

        # 2. Direct user permission (iam.permissions, translated by db.py)
        perm = self._db.get_user_permission(resource_id, resource_type, uid)
        if perm and not _is_expired(perm):
            level = _higher(level, perm["permission_level"])

        # 3. Folder-inherited permission (for files only; contextual artifacts
        # are container-derived, never folder-derived — skipped for them)
        if resource_type == "file" and not contextual and record.get("parent_folder_id"):
            folder_level = self.check("folder", record["parent_folder_id"], uid)
            level = _higher(level, folder_level)

        # 4. Platform judge (reachability / Shared Knowledge data_store grants).
        # Viewer-only — library grants never confer write/admin via this path.
        # Contextual artifacts ALWAYS consult the judge; errors fail closed
        # (no level is added).
        if resource_type == "file" and (
            contextual or level is None or _LEVEL_RANK.get(level, 0) < _LEVEL_RANK["read"]
        ):
            try:
                if self._db.has_platform_viewer_access(uid, "file", resource_id):
                    level = _higher(level, "read")
            except Exception:
                logger.exception(
                    "has_platform_viewer_access failed for file=%s user=%s",
                    resource_id,
                    uid,
                )

        # Contextual system artifacts are VIEWER-CEILING everywhere (the DB
        # policy denies write/admin for them unconditionally). An explicit
        # iam.permissions grant must not let this fallback hand out write/admin
        # the authoritative policy would refuse — clamp, keeping the subset
        # strictly deny-more.
        if contextual and level is not None:
            level = "read"

        return level

    async def check_async(
        self,
        resource_type: ResourceType,
        resource_id: str,
        user_id: str | None = None,
    ) -> str | None:
        """Async version of :meth:`check` — same resolution, async client."""
        uid = self._effective_uid(user_id)
        if not uid:
            return None

        if resource_type == "file":
            record = await self._db.get_file_async(resource_id)
        else:
            record = await self._db.get_folder_async(resource_id)

        if not record:
            return None
        # Contextual system artifacts: skip owner/public shortcuts, skip folder
        # inheritance, ALWAYS ask the platform judge (see `check`).
        contextual = resource_type == "file" and _is_contextual_system_artifact(record)
        level: str | None = None
        if not contextual:
            if record.get("owner_id") == uid:
                return "admin"
            if record.get("published_to_web"):
                level = "read"

        perm = await self._db.get_user_permission_async(resource_id, resource_type, uid)
        if perm and not _is_expired(perm):
            level = _higher(level, perm["permission_level"])

        if resource_type == "file" and not contextual and record.get("parent_folder_id"):
            folder_level = await self.check_async("folder", record["parent_folder_id"], uid)
            level = _higher(level, folder_level)

        # Platform judge (reachability / Shared Knowledge). Viewer-only.
        # Contextual artifacts always consult it; errors fail closed.
        if resource_type == "file" and (
            contextual or level is None or _LEVEL_RANK.get(level, 0) < _LEVEL_RANK["read"]
        ):
            try:
                if await self._db.has_platform_viewer_access_async(uid, "file", resource_id):
                    level = _higher(level, "read")
            except Exception:
                logger.exception(
                    "has_platform_viewer_access_async failed for file=%s user=%s",
                    resource_id,
                    uid,
                )

        # Viewer-ceiling clamp for contextual artifacts — see `check`.
        if contextual and level is not None:
            level = "read"

        return level

    def require(
        self,
        resource_type: ResourceType,
        resource_id: str,
        minimum: PermissionLevel = "read",
        user_id: str | None = None,
    ) -> str:
        """Raise PermissionError unless the user holds at least ``minimum``.

        Delegates to the host-injected authoritative resolver (the DB policy)
        when one is configured; otherwise falls back to the standalone subset.
        """
        checker = get_sync_access_checker()
        if checker is not None:
            uid = self._effective_uid(user_id)
            if not uid or not checker(uid, resource_type, resource_id, minimum):
                raise PermissionError(
                    f"User '{uid or user_id or self._user_id}' lacks '{minimum}' "
                    f"access on {resource_type} '{resource_id}'."
                )
            return minimum

        level = self.check(resource_type, resource_id, user_id)
        if level is None or _LEVEL_RANK.get(level, 0) < _LEVEL_RANK[minimum]:
            raise PermissionError(
                f"User '{user_id or self._user_id}' requires '{minimum}' access "
                f"on {resource_type} '{resource_id}' but has '{level or 'none'}'."
                f"{_SYNC_FALLBACK_DENIAL_MARKER}"
            )
        return level

    async def require_async(
        self,
        resource_type: ResourceType,
        resource_id: str,
        minimum: PermissionLevel = "read",
        user_id: str | None = None,
    ) -> str:
        checker = get_access_checker()
        if checker is not None:
            uid = self._effective_uid(user_id)
            if not uid or not await checker(uid, resource_type, resource_id, minimum):
                raise PermissionError(
                    f"User '{uid or user_id or self._user_id}' lacks '{minimum}' "
                    f"access on {resource_type} '{resource_id}'."
                )
            return minimum

        level = await self.check_async(resource_type, resource_id, user_id)
        if level is None or _LEVEL_RANK.get(level, 0) < _LEVEL_RANK[minimum]:
            raise PermissionError(
                f"User '{user_id or self._user_id}' requires '{minimum}' access "
                f"on {resource_type} '{resource_id}' but has '{level or 'none'}'."
                f"{_FALLBACK_DENIAL_MARKER}"
            )
        return level

    # ------------------------------------------------------------------
    # Grant / revoke
    # ------------------------------------------------------------------

    def grant(
        self,
        resource_type: ResourceType,
        resource_id: str,
        grantee_id: str,
        level: PermissionLevel = "read",
        grantee_type: Literal["user", "group"] = "user",
        expires_at: str | None = None,
    ) -> dict:
        """Grant a permission.  Requires admin access on the resource."""
        self.require(resource_type, resource_id, "admin")
        return self._db.upsert_permission(
            {
                "resource_id": resource_id,
                "resource_type": resource_type,
                "grantee_id": grantee_id,
                "grantee_type": grantee_type,
                "permission_level": level,
                "granted_by": self._effective_uid(None) or None,
                "expires_at": expires_at,
            }
        )

    async def grant_async(
        self,
        resource_type: ResourceType,
        resource_id: str,
        grantee_id: str,
        level: PermissionLevel = "read",
        grantee_type: Literal["user", "group"] = "user",
        expires_at: str | None = None,
    ) -> dict:
        await self.require_async(resource_type, resource_id, "admin")
        return await self._db.upsert_permission_async(
            {
                "resource_id": resource_id,
                "resource_type": resource_type,
                "grantee_id": grantee_id,
                "grantee_type": grantee_type,
                "permission_level": level,
                "granted_by": self._effective_uid(None) or None,
                "expires_at": expires_at,
            }
        )

    def revoke(
        self,
        resource_type: ResourceType,
        resource_id: str,
        grantee_id: str,
        grantee_type: Literal["user", "group"] = "user",
    ) -> bool:
        """Revoke a permission.  Requires admin access on the resource."""
        self.require(resource_type, resource_id, "admin")
        return self._db.delete_permission(resource_id, resource_type, grantee_id, grantee_type)

    async def revoke_async(
        self,
        resource_type: ResourceType,
        resource_id: str,
        grantee_id: str,
        grantee_type: Literal["user", "group"] = "user",
    ) -> bool:
        await self.require_async(resource_type, resource_id, "admin")
        return await self._db.delete_permission_async(
            resource_id, resource_type, grantee_id, grantee_type
        )

    def list_permissions(self, resource_type: ResourceType, resource_id: str) -> list[dict]:
        """List all permission grants on a resource.  Requires admin access."""
        self.require(resource_type, resource_id, "admin")
        return self._db.list_permissions(resource_id, resource_type)

    async def list_permissions_async(
        self, resource_type: ResourceType, resource_id: str
    ) -> list[dict]:
        await self.require_async(resource_type, resource_id, "admin")
        return await self._db.list_permissions_async(resource_id, resource_type)

    # ------------------------------------------------------------------
    # Share links
    # ------------------------------------------------------------------

    def create_share_link(
        self,
        resource_type: ResourceType,
        resource_id: str,
        permission_level: Literal["viewer", "editor"] = "viewer",
        expires_at: str | None = None,
        max_uses: int | None = None,
        user_id: str | None = None,
    ) -> dict:
        """Create a share link (``platform.share_links``).

        Requires ``admin`` on the resource (the item level, not the
        organization-admin role — see THE SCOPE-QUALIFIED ADMIN RULE in
        common-docs/systems/platform/access/DECISIONS.md, 2026-09-10).

        The platform's levels are ``viewer`` / ``commenter`` / ``editor`` /
        ``admin`` (AI Matrx Data Doctrine R18; ``commenter`` is declared, not yet
        in the live enum as of 2026-09-10). This entry point deliberately CAPS a
        share link at ``editor`` — the canonical RPC ``public.create_share_link``
        itself accepts ``admin``. The cap is a product choice about links, not the
        vocabulary; see the CONVERGE note on ``_CreateShareLinkRequest``.
        """
        self.require(resource_type, resource_id, "admin", user_id)
        return self._db.create_share_link(
            {
                "resource_id": resource_id,
                "resource_type": resource_type,
                "permission_level": permission_level,
                "created_by": self._effective_uid(user_id) or None,
                "expires_at": expires_at,
                "max_uses": max_uses,
            }
        )

    async def create_share_link_async(
        self,
        resource_type: ResourceType,
        resource_id: str,
        permission_level: Literal["viewer", "editor"] = "viewer",
        expires_at: str | None = None,
        max_uses: int | None = None,
        user_id: str | None = None,
    ) -> dict:
        await self.require_async(resource_type, resource_id, "admin", user_id)
        return await self._db.create_share_link_async(
            {
                "resource_id": resource_id,
                "resource_type": resource_type,
                "permission_level": permission_level,
                "created_by": self._effective_uid(user_id) or None,
                "expires_at": expires_at,
                "max_uses": max_uses,
            }
        )

    def resolve_share_link(self, token: str) -> dict | None:
        """Atomically validate + consume one use of a share token.

        Delegates to the canonical ``iam.resolve_share_token`` resolver
        (revoked / expired / exhausted checks + use_count increment in one
        statement). Returns ``{resource_type, resource_id, permission_level}``
        or None when the token authorizes nothing.
        """
        return self._db.consume_share_link(token)

    async def resolve_share_link_async(self, token: str) -> dict | None:
        return await self._db.consume_share_link_async(token)

    async def resolve_share_child_file_async(self, token: str, file_id: str) -> dict | None:
        """Does this share token reach this child file of the record it shares?

        True only for a file attached to the shared record itself (today: a
        media part of a shared conversation's visible messages). Never consumes
        a use. See ``iam.share_link_child_file`` (access ladder T-19b).
        """
        return await self._db.share_link_child_file_async(token, file_id)

    def deactivate_share_link(self, token: str) -> bool:
        return self._db.deactivate_share_link(token)

    async def deactivate_share_link_async(self, token: str) -> bool:
        return await self._db.deactivate_share_link_async(token)

    def list_share_links(self, resource_type: ResourceType, resource_id: str) -> list[dict]:
        self.require(resource_type, resource_id, "admin")
        return self._db.list_share_links(resource_id, resource_type)

    async def list_share_links_async(
        self, resource_type: ResourceType, resource_id: str
    ) -> list[dict]:
        await self.require_async(resource_type, resource_id, "admin")
        return await self._db.list_share_links_async(resource_id, resource_type)

    # NOTE: user-group management (create_group / add_to_group / …) was
    # removed in the 2026 DB canonicalization — the cld_user_groups feature
    # is dead. File ACLs are direct user/org grants on iam.permissions.
