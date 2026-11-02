"""The injected DB policy is THE access decision — not the Python fallback.

The file layer used to resolve access in Python (owner -> public -> direct grant
-> parent folder). That mirror is a strict SUBSET of the real policy
(`iam.has_access_for`): it cannot see orgs, org-admins, memberships or
`platform.reachability` containers, so it silently DENIED legitimately-shared
files. The host now injects the authoritative resolver.

These tests pin the contract:
  * when a checker is injected it decides — the Python path is not consulted;
  * a deny raises PermissionError (fail-closed), on the async AND sync gates;
  * the Python fallback still works when nothing is injected (standalone
    matrx-utils), and stays strictly deny-more: expired grants, under-level
    grants and org-scoped (`internal`) visibility never confer access;
  * `SyncEngine.get_authorized_record_async` asks the REAL gate for the level the
    caller requested — never skipping it for an owner or a shared organization
    (ORGANIZATION IS TENANCY, NEVER PERMISSION).
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from matrx_files.cloud_sync.permissions import (
    PermissionsManager,
    configure_access_checker,
)
from matrx_files.cloud_sync.sync_engine import SyncEngine


class _ExplodingDB:
    """Any Python-side resolution is a bug once a checker is injected."""

    def get_file(self, *a, **k):  # pragma: no cover - must never run
        raise AssertionError("Python fallback consulted despite an injected checker")

    async def get_file_async(self, *a, **k):  # pragma: no cover
        raise AssertionError("Python fallback consulted despite an injected checker")

    def get_user_permission(self, *a, **k):  # pragma: no cover
        raise AssertionError("Python fallback consulted despite an injected checker")

    async def get_user_permission_async(self, *a, **k):  # pragma: no cover
        raise AssertionError("Python fallback consulted despite an injected checker")


@pytest.fixture(autouse=True)
def _reset_checker():
    yield
    configure_access_checker(None, sync_checker=None)


def _pm() -> PermissionsManager:
    return PermissionsManager(_ExplodingDB(), user_id="u1")


async def test_injected_checker_decides_allow() -> None:
    seen: list[tuple] = []

    async def allow_all(user_id, rtype, rid, level):
        seen.append((user_id, rtype, rid, level))
        return True

    configure_access_checker(allow_all)
    pm = _pm()

    assert await pm.require_async("file", "f1", "read", "u1") == "read"
    # The policy question is forwarded verbatim — no Python pre-filtering.
    assert seen == [("u1", "file", "f1", "read")]


async def test_injected_checker_decides_deny_fail_closed() -> None:
    async def deny_all(user_id, rtype, rid, level):
        return False

    configure_access_checker(deny_all)
    pm = _pm()

    with pytest.raises(PermissionError):
        await pm.require_async("file", "f1", "read", "u1")


async def test_injected_checker_sees_every_level() -> None:
    asked: list[str] = []

    async def checker(user_id, rtype, rid, level):
        asked.append(level)
        return level != "admin"  # editor yes, admin no

    configure_access_checker(checker)
    pm = _pm()

    assert await pm.require_async("file", "f1", "write", "u1") == "write"
    with pytest.raises(PermissionError):
        await pm.require_async("file", "f1", "admin", "u1")
    assert asked == ["write", "admin"]


async def test_no_user_is_denied_even_with_permissive_checker() -> None:
    async def allow_all(user_id, rtype, rid, level):  # pragma: no cover
        raise AssertionError("must not consult the policy without an actor")

    configure_access_checker(allow_all)
    pm = PermissionsManager(_ExplodingDB(), user_id="")

    with pytest.raises(PermissionError):
        await pm.require_async("file", "f1", "read", None)


def test_sync_no_user_is_denied_even_with_permissive_sync_checker() -> None:
    def allow_all(user_id, rtype, rid, level):
        return True

    configure_access_checker(None, sync_checker=allow_all)
    pm = PermissionsManager(_ExplodingDB(), user_id="")

    with pytest.raises(PermissionError, match="lacks 'read' access on file 'f1'"):
        pm.require("file", "f1", "read", None)


def test_sync_checker_decides() -> None:
    configure_access_checker(None, sync_checker=lambda u, t, i, lvl: lvl == "read")
    pm = _pm()

    assert pm.require("file", "f1", "read", "u1") == "read"
    with pytest.raises(PermissionError):
        pm.require("file", "f1", "admin", "u1")


async def test_python_fallback_still_works_standalone() -> None:
    """No host injected → the package still resolves (subset) rather than crash."""

    class _DB:
        async def get_file_async(self, fid):
            return {"id": fid, "owner_id": "owner-1", "visibility": "personal"}

        async def get_user_permission_async(self, rid, rtype, uid):
            return {"permission_level": "read"} if uid == "grantee" else None

    configure_access_checker(None, sync_checker=None)
    pm = PermissionsManager(_DB(), user_id="")

    assert await pm.require_async("file", "f1", "read", "owner-1") == "admin"  # owner
    assert await pm.require_async("file", "f1", "read", "grantee") == "read"  # granted
    with pytest.raises(PermissionError):
        await pm.require_async("file", "f1", "read", "stranger")


class _FallbackDB:
    """Async fallback view of ONE file: its record, the caller's grant row (or
    None), and the platform judge's answer. No folder parent."""

    def __init__(self, record: dict, *, grant: dict | None = None, judge: bool = False):
        self._record = record
        self._grant = grant
        self._judge = judge

    async def get_file_async(self, fid):
        return self._record

    async def get_user_permission_async(self, rid, rtype, uid):
        return self._grant

    async def has_platform_viewer_access_async(self, uid, rtype, rid):
        return self._judge


def _private_file(**overrides) -> dict:
    record = {"id": "f1", "owner_id": "owner-1", "visibility": "personal"}
    record.update(overrides)
    return record


async def test_fallback_denies_an_expired_grant() -> None:
    pm = PermissionsManager(
        _FallbackDB(
            _private_file(),
            grant={"permission_level": "write", "expires_at": "2020-01-01T00:00:00Z"},
        )
    )

    with pytest.raises(PermissionError, match="but has 'none'"):
        await pm.require_async("file", "f1", "read", "grantee")


async def test_fallback_read_grant_does_not_satisfy_write() -> None:
    pm = PermissionsManager(_FallbackDB(_private_file(), grant={"permission_level": "read"}))

    assert await pm.require_async("file", "f1", "read", "grantee") == "read"
    with pytest.raises(PermissionError, match="requires 'write' access on file 'f1' but has 'read'"):
        await pm.require_async("file", "f1", "write", "grantee")


async def test_fallback_never_reads_org_scoped_visibility_as_access() -> None:
    """`internal` means org-scoped. The subset cannot see memberships, and org is
    tenancy, never permission — a non-owner without a grant is denied."""
    pm = PermissionsManager(
        _FallbackDB(_private_file(visibility="internal", organization_id="org-1"))
    )

    with pytest.raises(PermissionError, match="but has 'none'"):
        await pm.require_async("file", "f1", "read", "same-org-colleague")


async def test_fallback_keeps_the_higher_of_public_read_and_a_write_grant() -> None:
    pm = PermissionsManager(
        _FallbackDB(_private_file(visibility="public"), grant={"permission_level": "write"})
    )

    assert await pm.check_async("file", "f1", "grantee") == "write"
    assert await pm.require_async("file", "f1", "write", "grantee") == "write"


def _crawl_record(**overrides) -> dict:
    record = {
        "id": "crawl-file",
        "owner_id": "historical-owner",
        "visibility": "internal",
        "metadata": {
            "system_artifact": True,
            "artifact_domain": "web_crawl",
        },
    }
    record.update(overrides)
    return record


class _ContextualDB:
    """Fallback DB double for contextual-artifact resolution tests."""

    def __init__(self, record: dict, *, judge: bool, grant: str | None = None):
        self._record = record
        self._judge = judge
        self._grant = grant

    def get_file(self, fid):
        return self._record

    async def get_file_async(self, fid):
        return self._record

    def get_user_permission(self, rid, rtype, uid):
        return {"permission_level": self._grant} if self._grant else None

    async def get_user_permission_async(self, rid, rtype, uid):
        return self.get_user_permission(rid, rtype, uid)

    def has_platform_viewer_access(self, uid, rtype, rid):
        if isinstance(self._judge, Exception):
            raise self._judge
        return self._judge

    async def has_platform_viewer_access_async(self, uid, rtype, rid):
        return self.has_platform_viewer_access(uid, rtype, rid)


async def test_contextual_artifact_platform_judge_grants_read() -> None:
    """Container access (has_access_as) is THE path for crawl artifacts."""

    pm = PermissionsManager(_ContextualDB(_crawl_record(), judge=True), user_id="org-member")

    assert pm.check("file", "crawl-file", "org-member") == "read"
    assert await pm.check_async("file", "crawl-file", "org-member") == "read"
    assert pm.require("file", "crawl-file", "read", "org-member") == "read"
    assert await pm.require_async("file", "crawl-file", "read", "org-member") == "read"


async def test_contextual_artifact_judge_false_no_grant_denies() -> None:
    pm = PermissionsManager(_ContextualDB(_crawl_record(), judge=False), user_id="stranger")

    assert pm.check("file", "crawl-file", "stranger") is None
    assert await pm.check_async("file", "crawl-file", "stranger") is None
    with pytest.raises(PermissionError):
        pm.require("file", "crawl-file", "read", "stranger")
    with pytest.raises(PermissionError):
        await pm.require_async("file", "crawl-file", "read", "stranger")


async def test_contextual_artifact_owner_without_judge_or_grant_denied() -> None:
    """Historical created_by ownership must NOT leak back as authorization."""

    pm = PermissionsManager(
        _ContextualDB(_crawl_record(), judge=False), user_id="historical-owner"
    )

    assert pm.check("file", "crawl-file", "historical-owner") is None
    with pytest.raises(PermissionError):
        pm.require("file", "crawl-file", "read", "historical-owner")
    with pytest.raises(PermissionError):
        await pm.require_async("file", "crawl-file", "read", "historical-owner")


async def test_contextual_artifact_public_visibility_shortcut_skipped() -> None:
    """visibility=='public' must not shortcut contextual artifacts past the judge."""

    pm = PermissionsManager(
        _ContextualDB(_crawl_record(visibility="public"), judge=False), user_id="stranger"
    )

    assert pm.check("file", "crawl-file", "stranger") is None
    assert await pm.check_async("file", "crawl-file", "stranger") is None


async def test_contextual_artifact_explicit_grant_is_viewer_ceiling_clamped() -> None:
    """An explicit iam.permissions grant still confers access on a contextual
    artifact — but clamped to READ. The authoritative DB policy denies
    write/admin on system evidence unconditionally; the Python subset must
    stay deny-more, and before the clamp a 'write' grant here handed out a
    level the DB would refuse (2026-07-30 adversarial review, F4)."""
    pm = PermissionsManager(
        _ContextualDB(_crawl_record(), judge=False, grant="write"), user_id="grantee"
    )

    assert pm.check("file", "crawl-file", "grantee") == "read"
    assert await pm.check_async("file", "crawl-file", "grantee") == "read"


async def test_contextual_artifact_judge_error_fails_closed() -> None:
    pm = PermissionsManager(
        _ContextualDB(_crawl_record(), judge=RuntimeError("db down")),
        user_id="historical-owner",
    )

    assert pm.check("file", "crawl-file", "historical-owner") is None
    assert await pm.check_async("file", "crawl-file", "historical-owner") is None


# --------------------------------------------------------------------------
# SyncEngine.get_authorized_record_async — through the REAL gate
# --------------------------------------------------------------------------


def _authorizing_engine(record: dict, *, granted: tuple[str, ...], organization_id=None):
    """Engine view with the real PermissionsManager; the injected checker (the
    DB policy stand-in) grants `granted` levels to "caller" on this file only."""

    async def policy(user_id, rtype, rid, level):
        return (user_id, rtype, rid) == ("caller", "file", record["id"]) and level in granted

    configure_access_checker(policy)
    return SimpleNamespace(
        _db=SimpleNamespace(get_file_async=AsyncMock(return_value=record)),
        permissions=PermissionsManager(_ExplodingDB(), user_id=""),
        _organization_id=organization_id,
    )


async def test_authorized_record_denies_the_historical_owner_the_policy_refuses() -> None:
    record = {"id": "f1", "owner_id": "caller", "created_by": "caller"}
    engine = _authorizing_engine(record, granted=())

    with pytest.raises(PermissionError, match="lacks 'read' access on file 'f1'"):
        await SyncEngine.get_authorized_record_async(engine, "f1", user_id="caller", level="read")


async def test_authorized_record_enforces_the_requested_level() -> None:
    record = {"id": "f1", "owner_id": "someone-else"}
    engine = _authorizing_engine(record, granted=("read",))

    assert (
        await SyncEngine.get_authorized_record_async(engine, "f1", user_id="caller", level="read")
        is record
    )
    with pytest.raises(PermissionError, match="lacks 'admin' access on file 'f1'"):
        await SyncEngine.get_authorized_record_async(engine, "f1", user_id="caller", level="admin")


async def test_authorized_record_never_grants_by_shared_organization() -> None:
    record = {"id": "f1", "owner_id": "someone-else", "organization_id": "org-1"}
    engine = _authorizing_engine(record, granted=(), organization_id="org-1")

    with pytest.raises(PermissionError, match="lacks 'read' access on file 'f1'"):
        await SyncEngine.get_authorized_record_async(engine, "f1", user_id="caller", level="read")


def test_managed_read_never_bypasses_policy_for_owner() -> None:
    record = {
        "id": "f1",
        "owner_id": "historical-owner",
        "storage_uri": "s3://bucket/key",
    }
    engine = SimpleNamespace(
        _resolve_user_id=Mock(return_value="historical-owner"),
        _db=SimpleNamespace(get_file_by_path=Mock(return_value=record)),
        permissions=SimpleNamespace(require=Mock(side_effect=PermissionError)),
        _router=SimpleNamespace(read=Mock()),
    )

    with pytest.raises(PermissionError):
        SyncEngine.managed_read(engine, "artifact.html", user_id="historical-owner")

    engine.permissions.require.assert_called_once_with("file", "f1", "read", "historical-owner")
    engine._router.read.assert_not_called()
