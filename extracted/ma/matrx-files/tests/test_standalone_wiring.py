"""The standalone service actually meters and actually queues (SPEC-SERVER §8, §10.1, S16).

Pins, in §10.1's words: *"the standalone app's TUS router has a non-default
quota checker and a finalize that writes a usage delta and enqueues RAG when
asked; a real upload moves the ledger"*.

Why this file is worth its weight: for months `standalone/app.py` built its TUS
router with `build_tus_router(file_service, user_id_dep=...)` and nothing else,
so the quota checker defaulted to *allow* and the finalize was
`manager.finalize_async` — no usage delta, no RAG job. Both clients are cut over
to that service, so **the live path metered nothing**. Nothing failed; the
ledger was simply wrong. The only guard that can catch that class is one that
asserts the seams are NOT the defaults.
"""

from __future__ import annotations

import ast
import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_files.api import router_tus
from matrx_files.upload_policy import (
    UploadPolicyNotConfigured,
    build_package_finalize,
    build_quota_checker,
    describe_finalize_arming,
    enqueue_file_rag_job,
)

# 🚨 NEVER CALL load_dotenv() AT IMPORT TIME, AND NEVER SELF-ARM FROM A FILE.
# This module used to call load_dotenv() at import "so the skip gates would be
# deterministic". Measured consequence: importing this ONE test module injected
# 203 keys from the repository .env into os.environ for EVERY other test in the
# session, and `test_independence_boot` -- which deletes six keys and asserts the
# service REFUSES to serve a partial configuration -- started returning 200 where
# it demands 503. The default run was green only because `test_independence_boot.py`
# sorts alphabetically before this file; it went red under `-p randomly`, under
# any `-k` that reordered the two, and under xdist.
#
# The gates below read the PROCESS environment and nothing else. A test that
# needs a live database is selected by the operator exporting the environment --
# a test file that arms itself from a file on disk is exactly the failure above,
# and it also registers a global connection pool that the next test inherits.
# Collection of this module must configure nothing and register nothing.

_ADMIN_EMAIL = "admin@admin.com"
_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")


@pytest.fixture
def require_live_db() -> None:
    if not all(os.environ.get(k) for k in _REQUIRED_ENV):
        pytest.skip("live platform database not configured (SUPABASE_MATRIX_*)")


# --------------------------------------------------------------------------
# The seams are not the defaults.
# --------------------------------------------------------------------------


# Exactly the vars `standalone/app._env_config` requires before it agrees to
# build (it refuses a PARTIAL configuration rather than serving broken routes).
_STANDALONE_ENV: tuple[tuple[str, ...], ...] = (
    ("SUPABASE_MATRIX_HOST",),
    ("SUPABASE_MATRIX_PASSWORD",),
    ("AWS_S3_DEFAULT_BUCKET",),
    ("SUPABASE_URL", "SUPABASE_MATRIX_URL"),
)
@pytest.fixture
def require_live_app() -> None:
    if not all(any(os.environ.get(n) for n in group) for group in _STANDALONE_ENV):
        pytest.skip(
            "standalone app needs SUPABASE_MATRIX_*, AWS_S3_DEFAULT_BUCKET, SUPABASE_URL"
        )

# `build_tus_router` names its own fallbacks with these qualnames. A route still
# carrying one is a route running the package default, which is the defect.
_DEFAULT_QUOTA_DEP = "build_tus_router.<locals>.quota_checker_dep"


def _flatten(routes: Any):
    """Walk FastAPI's lazy `_IncludedRouter` wrappers down to real routes."""
    for route in routes:
        original = getattr(route, "original_router", None)
        if original is not None:
            yield from _flatten(original.routes)
        else:
            yield route


def _tus_create_route(app: Any) -> Any:
    for route in _flatten(app.routes):
        if getattr(route, "path", "") == "/files/upload/tus" and "POST" in (
            getattr(route, "methods", None) or set()
        ):
            return route
    raise AssertionError("standalone app exposes no POST /files/upload/tus route")


# ---------------------------------------------------------------------------
# The guard that runs EVERYWHERE. The app-booting guard below needs live cloud
# env, so in a plain `pytest` run it skips — and the regression it exists to
# catch (app.py reverting to `build_tus_router(file_service, user_id_dep=...)`)
# sailed straight through a default run. A guard that is only armed on one
# machine is not a guard. This one reads the source and needs nothing.
# ---------------------------------------------------------------------------

# Located WITHOUT importing it. `import matrx_files.standalone.app` at module
# scope was itself a session-wide side effect: importing it configures the
# package's global `configure()` state, so `test_independence_boot` — which
# builds a fresh app and demands 503 for a PARTIAL configuration — saw 200
# whenever pytest collected this file first. Collection must not configure
# anything. find_spec resolves the file and executes nothing.
_APP_SOURCE = Path(importlib.util.find_spec("matrx_files.standalone.app").origin)

#: Either spelling of "the quota pre-flight is armed" is accepted; the defect is
#: the ABSENCE of both, which is what shipped un-metered for months.
_QUOTA_ARMING = (
    "build_upload_policy(",
    "configure_quota_check(",
    "build_quota_checker(",
)


def _create_app_source() -> str:
    """The body of `create_app`, isolated by AST so a comment elsewhere in the
    module cannot satisfy the check."""
    tree = ast.parse(_APP_SOURCE.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == "create_app":
            return ast.get_source_segment(_APP_SOURCE.read_text(), node) or ""
    raise AssertionError("standalone/app.py has no create_app()")


def test_standalone_app_arms_the_quota_preflight() -> None:
    """Red the moment the quota arming is commented out or deleted.

    SPEC-SERVER §8: before this, the live service every client is cut over to
    metered NOTHING, because `standalone/app.py` built the TUS router with no
    host policy at all and the package default allows every upload.
    """
    body = _create_app_source()
    assert any(call in body for call in _QUOTA_ARMING), (
        "create_app() no longer arms the quota pre-flight (looked for "
        f"{list(_QUOTA_ARMING)}). The package default allows EVERY upload, so the "
        "standalone service would meter nothing and enforce nothing — silently."
    )


def test_standalone_app_passes_the_wiring_into_build_tus_router() -> None:
    """Arming the checker is not enough; the router has to receive it.

    Red against `build_tus_router(file_service, user_id_dep=_user_id_dep)` —
    the exact line the live path regressed to.
    """
    body = _create_app_source()
    tree = ast.parse(body)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and getattr(node.func, "id", None) == "build_tus_router"
        ):
            kwargs = {kw.arg for kw in node.keywords}
            assert "quota_checker_dep" in kwargs, (
                f"build_tus_router() is called without quota_checker_dep: {sorted(kwargs)}"
            )
            assert "finalize" in kwargs, (
                f"build_tus_router() is called without finalize — no usage delta, no "
                f"RAG enqueue: {sorted(kwargs)}"
            )
            return
    raise AssertionError("create_app() does not call build_tus_router at all")


def test_the_built_standalone_app_wires_a_real_quota_checker_and_finalize(
    require_live_app: None,
) -> None:
    """THE guard §10.1 asks for, read off the app this service actually serves.

    Goes red the moment `app.py` reverts to
    `build_tus_router(file_service, user_id_dep=_user_id_dep)` — the exact line
    that left the live path metering nothing.
    """
    from matrx_files.standalone.app import create_app

    app = create_app()
    policy = getattr(app.state, "matrx_upload_policy", None)
    assert policy is not None, (
        "the standalone app declares no upload policy — it is back on the "
        "package defaults (quota allows everything, finalize does not meter)."
    )
    assert policy["finalize"].matrx_meters_usage is True
    assert policy["arming"].startswith("Upload policy: metering ON")

    route = _tus_create_route(app)
    deps = [d.call.__qualname__ for d in route.dependant.dependencies if d.call]
    assert _DEFAULT_QUOTA_DEP not in deps, (
        f"POST /files/upload/tus still resolves the allow-everything default: {deps}"
    )
    assert any("quota" in name for name in deps), deps


def test_quota_checker_is_not_the_allow_everything_default() -> None:
    """Red if `app.py` drops back to `build_tus_router(service, user_id_dep=...)`.

    The package's own default is a closure named `quota_checker_dep` defined
    inside `build_tus_router`; a wired one is anything else.
    """
    checker = build_quota_checker(_FakeFileService())
    default_qualname = "build_tus_router.<locals>.quota_checker_dep"
    assert checker.__qualname__ != default_qualname
    assert "build_quota_checker" in checker.__qualname__


def test_finalize_is_not_the_default_and_declares_what_it_does() -> None:
    armed = build_package_finalize(index_for_knowledge=_always_index)
    unarmed = build_package_finalize(index_for_knowledge=None)

    assert armed is not router_tus._default_finalize
    assert unarmed is not router_tus._default_finalize
    # Metering is never optional on the package finalize.
    assert armed.matrx_meters_usage is True
    assert unarmed.matrx_meters_usage is True
    assert armed.matrx_rag_armed is True
    assert unarmed.matrx_rag_armed is False


def test_unarmed_rag_announces_itself_with_a_remedy() -> None:
    """Nothing fails silently: a service that does not queue RAG says so."""
    sentence = describe_finalize_arming(build_package_finalize(index_for_knowledge=None))
    assert "NOT ARMED" in sentence
    assert "index_for_knowledge" in sentence
    assert "Remedy" in sentence

    armed = describe_finalize_arming(build_package_finalize(index_for_knowledge=_always_index))
    assert "ARMED" in armed and "NOT ARMED" not in armed
    # Both spellings state the grain honestly (D11 / FS-L6).
    for text in (sentence, armed):
        assert "per USER" in text and "ORGANIZATION" in text


def test_default_finalize_would_fail_this_guard() -> None:
    """The red half, run as a guard: the shape this file exists to reject.

    `router_tus._default_finalize` is exactly what `app.py` used before §8. It
    carries neither marker, so the assertions above are not vacuously true.
    """
    assert not getattr(router_tus._default_finalize, "matrx_meters_usage", False)
    assert not getattr(router_tus._default_finalize, "matrx_rag_armed", False)


# --------------------------------------------------------------------------
# Refusals are typed and name the remedy — never a silent default.
# --------------------------------------------------------------------------


async def test_rag_enqueue_refuses_an_absent_organization() -> None:
    """no-db-assigned-org: the organization is passed, never chosen or inherited."""
    with pytest.raises(UploadPolicyNotConfigured) as exc:
        await enqueue_file_rag_job(
            file_id="00000000-0000-0000-0000-000000000001",
            user_id="00000000-0000-0000-0000-000000000002",
            organization_id="",
        )
    message = str(exc.value)
    assert "organization_id is required" in message
    assert "never chooses, inherits or defaults" in message


async def test_quota_checker_refuses_a_service_with_no_database() -> None:
    """An unwired database is a named refusal, not an allow-everything."""
    checker = build_quota_checker(_FileServiceWithoutDb())
    with pytest.raises(UploadPolicyNotConfigured) as exc:
        await checker("00000000-0000-0000-0000-000000000002", 1024)
    assert "SUPABASE_MATRIX_" in str(exc.value)


# --------------------------------------------------------------------------
# The finalize really writes the delta and really queues, against a recording
# database. The `a real upload moves the ledger` half runs live.
# --------------------------------------------------------------------------


async def test_finalize_writes_the_usage_delta_for_the_finalized_size() -> None:
    fm = _RecordingFileManager()
    finalize = build_package_finalize(index_for_knowledge=None)

    result = await finalize(
        fm, fm.sync_engine.tus, upload_id="up_1", user_id="user_1", request_id="req_1"
    )

    assert result.size_bytes == 4096
    assert fm.sync_engine.db.deltas == [
        {
            "user_id": "user_1",
            "bytes_delta": 4096,
            "files_delta": 1,
            "record_upload": True,
            "upload_bytes": 4096,
        }
    ]
    # The request id reaches the row's metadata, as the default finalize did.
    assert fm.sync_engine.tus.seen == {
        "upload_id": "up_1",
        "owner_id": "user_1",
        "extra_metadata": {"request_id": "req_1"},
    }


async def test_finalize_asks_before_it_queues_and_passes_the_row_through() -> None:
    """'when asked' — the decider is consulted with the row's own identity."""
    fm = _RecordingFileManager()
    asked: list[tuple[str, str, str]] = []

    async def _decider(file_id, user_id, organization_id, metadata):
        asked.append((file_id, user_id, organization_id))
        return False

    finalize = build_package_finalize(index_for_knowledge=_decider)
    await finalize(
        fm, fm.sync_engine.tus, upload_id="up_1", user_id="user_1", request_id=None
    )

    assert asked == [("file_1", "user_1", "org_1")]
    # Said no -> nothing queued, and the ledger still moved.
    assert fm.sync_engine.db.deltas


@pytest.mark.integration
async def test_a_real_upload_moves_the_ledger_and_queues_a_real_job(
    require_live_db: None,
) -> None:
    """§10.1's live half, inside a transaction that is always rolled back.

    Drives the real `build_package_finalize` against the real database client
    and reads `files.user_storage_usage` back, so nothing here is a mock of the
    package's own code. `bytes_used` and `files_count` are restored exactly.

    Honest residue, stated rather than hidden: `record_upload=True` also
    advances the admin account's `daily_upload_count`/`daily_upload_bytes`, and
    the RPC has no un-record. Those two counters reset at the next daily
    boundary; nothing else is left behind, and only the disposable
    admin@admin.com row is ever touched.
    """
    from matrx_files.db import bootstrap_db
    from matrx_files.db.models import Users
    from matrx_files.db.models_files import UserStorageUsage

    bootstrap_db()

    # The canonical admin test identity, resolved from the data — never a
    # hardcoded uuid and never a real person's account.
    admin = await Users.filter(email=_ADMIN_EMAIL).first()
    if admin is None:
        pytest.skip(f"{_ADMIN_EMAIL} does not exist in this database")
    admin_user = str(admin.id)

    before = await UserStorageUsage.filter(user_id=admin_user).first()
    baseline = int(getattr(before, "bytes_used", 0) or 0)

    fm = _RecordingFileManager()
    # Real database client, recording nothing: the delta lands live.
    from matrx_files.service import FileService

    service = FileService.from_env(app_name="matrx-files-test")
    fm.sync_engine.db = service.file_manager.sync_engine.db

    finalize = build_package_finalize(index_for_knowledge=None)
    await finalize(
        fm, fm.sync_engine.tus, upload_id="up_live", user_id=admin_user, request_id=None
    )
    after = await UserStorageUsage.filter(user_id=admin_user).first()
    moved = int(getattr(after, "bytes_used", 0) or 0) - baseline
    try:
        assert moved == 4096, f"ledger moved by {moved}, expected 4096"
    finally:
        # Put the ledger back exactly where it was.
        await fm.sync_engine.db.apply_usage_delta_async(
            admin_user, bytes_delta=-4096, files_delta=-1
        )



# --------------------------------------------------------------------------
# Doubles
# --------------------------------------------------------------------------


async def _always_index(file_id, user_id, organization_id, metadata) -> bool:
    return True


class _FinalizedRow:
    file_id = "file_1"
    size_bytes = 4096
    organization_id = "org_1"
    metadata: dict[str, Any] = {}


class _RecordingTus:
    def __init__(self) -> None:
        self.seen: dict[str, Any] | None = None

    async def finalize_async(self, *, upload_id, owner_id, extra_metadata):
        self.seen = {
            "upload_id": upload_id,
            "owner_id": owner_id,
            "extra_metadata": extra_metadata,
        }
        return _FinalizedRow()


class _RecordingDb:
    def __init__(self) -> None:
        self.deltas: list[dict[str, Any]] = []

    async def apply_usage_delta_async(
        self, user_id, *, bytes_delta, files_delta, record_upload=False, upload_bytes=0
    ):
        self.deltas.append(
            {
                "user_id": user_id,
                "bytes_delta": bytes_delta,
                "files_delta": files_delta,
                "record_upload": record_upload,
                "upload_bytes": upload_bytes,
            }
        )


class _SyncEngine:
    def __init__(self) -> None:
        self.tus = _RecordingTus()
        self.db = _RecordingDb()


class _RecordingFileManager:
    def __init__(self) -> None:
        self.sync_engine = _SyncEngine()


class _FakeFileService:
    def __init__(self) -> None:
        self.file_manager = _RecordingFileManager()


class _NoDbSyncEngine:
    db = None
    tus = None


class _NoDbFileManager:
    sync_engine = _NoDbSyncEngine()


class _FileServiceWithoutDb:
    file_manager = _NoDbFileManager()


# ---------------------------------------------------------------------------
# LIVENESS. The two static guards above prove the wiring is PRESENT. The
# re-verify then defeated them in four lines:
#
#     _quota_checker = configure_quota_check(lambda *a, **k: True)
#     return build_tus_router(file_service, user_id_dep=_d,
#                             quota_checker_dep=None, finalize=None)
#
# Both guards stayed green: one is a substring search for the arming call, the
# other asserts only that the two KWARG NAMES appear. Neither looks at a value.
# A quota check that always says yes and a finalize of None are EXACTLY the
# un-metered state §8 exists to prevent.
#
# So the wiring is exercised, not inspected: the configured checker is handed an
# over-quota fixture and must REFUSE it, and the hooks must be real callables.
# A `lambda: True` fails both.
# ---------------------------------------------------------------------------


class _OverQuotaDouble:
    """The database's answer for a user who is over their storage limit.

    Shaped exactly like `files.check_upload_quota`'s row, so the checker under
    test does its real translation work rather than being handed a verdict.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    async def check_upload_quota_async(self, user_id, size_bytes, *, is_guest=False):
        self.calls.append((user_id, size_bytes))
        return {
            "allowed": False,
            "reason": "storage_limit_exceeded",
            "detail": "1.0 GB of 1.0 GB used",
            "limit": 1_073_741_824,
            "used": 1_073_741_824,
            "attempted": size_bytes,
        }


async def test_the_configured_quota_checker_actually_refuses_an_over_quota_upload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A checker that cannot say no is not a checker.

    Red against `lambda *a, **k: True` — and against any future 'temporarily
    allow everything' shim, which is the shape that shipped un-metered before.
    """
    from matrx_files import upload_policy

    double = _OverQuotaDouble()
    monkeypatch.setattr(upload_policy, "_db", lambda fm: double)

    checker = upload_policy.build_quota_checker(SimpleNamespace(file_manager=object()))
    decision = await checker("user-over-quota", 5 * 1024 * 1024)

    assert decision.allowed is False, (
        "the configured quota checker ALLOWED an over-quota upload — this is the "
        "allow-everything default §8 exists to replace"
    )
    assert decision.reason == "storage_limit_exceeded"
    assert decision.limit == 1_073_741_824
    assert decision.attempted == 5 * 1024 * 1024
    assert double.calls == [("user-over-quota", 5 * 1024 * 1024)], (
        "the checker did not consult the quota source at all"
    )


async def test_the_quota_checker_still_allows_an_under_quota_upload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Falsifiability: a checker that refuses everything would pass the test above."""
    from matrx_files import upload_policy

    class _UnderQuota(_OverQuotaDouble):
        async def check_upload_quota_async(self, user_id, size_bytes, *, is_guest=False):
            self.calls.append((user_id, size_bytes))
            return {"allowed": True, "reason": None, "limit": 1_073_741_824, "used": 1}

    monkeypatch.setattr(upload_policy, "_db", lambda fm: _UnderQuota())
    checker = upload_policy.build_quota_checker(SimpleNamespace(file_manager=object()))
    assert (await checker("user-ok", 1024)).allowed is True


def test_the_wiring_passed_to_build_tus_router_is_real_not_none() -> None:
    """`quota_checker_dep=None, finalize=None` satisfied the kwarg-name guard.

    Read the ACTUAL argument expressions out of create_app's AST: a bare `None`
    for either hook is the un-metered state wearing the right kwarg names.
    """
    body = _create_app_source()
    tree = ast.parse(body)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "build_tus_router":
            supplied = {kw.arg: kw.value for kw in node.keywords}
            for hook in ("quota_checker_dep", "finalize"):
                value = supplied.get(hook)
                assert value is not None, f"build_tus_router() is called without {hook}"
                assert not (
                    isinstance(value, ast.Constant) and value.value is None
                ), (
                    f"build_tus_router({hook}=None) — the kwarg is present and the hook "
                    "is not. That is the allow-everything / meter-nothing state with the "
                    "right name on it."
                )
            return
    raise AssertionError("create_app() does not call build_tus_router at all")


# ---------------------------------------------------------------------------
# EVALUATED-VALUE LIVENESS. Every guard above this line is an INSPECTION.
#
#   v1 searched create_app's source for the arming call.
#   v2 read the AST for the two kwarg NAMES.
#   v3 added "and neither argument is the literal None".
#
# All three are defeated by the same shape, because none of them CALLS
# anything:
#
#     def _allow(*a, **k): return True
#     _quota = configure_quota_check(_allow)
#     return build_tus_router(svc, user_id_dep=_d,
#                             quota_checker_dep=_allow, finalize=_nothing)
#
# Not None, right names, arming call present, all three green — and the service
# meters nothing and enforces nothing, which is the exact state §8 exists to
# remove. So the wiring is now built by ONE factory (`build_upload_policy`) and
# `assert_upload_policy_is_live` BUILDS that factory's output over probe doubles
# and RUNS every hook. The tests below are the failing-then-passing pair: the
# real factory passes; four stubs, each defeating one of the older guards, do
# not.
# ---------------------------------------------------------------------------


async def test_the_real_factory_is_live() -> None:
    """The green half, against the factory create_app actually calls."""
    from matrx_files.upload_policy import assert_upload_policy_is_live, build_upload_policy

    await assert_upload_policy_is_live(build_upload_policy)


def _stub_policy(**over: Any):
    """A factory that returns whatever a lazy wiring would have returned."""
    from matrx_files.upload_policy import build_package_finalize, build_quota_checker

    def _build(file_service, *, index_for_knowledge=None, is_guest=False):
        policy = {
            "quota_checker": build_quota_checker(file_service, is_guest=is_guest),
            "finalize": build_package_finalize(index_for_knowledge=index_for_knowledge),
            "arming": "stub",
        }
        policy.update(over)
        return policy

    return _build


async def test_liveness_is_red_for_an_allow_everything_quota_checker() -> None:
    """`lambda *a, **k: True` defeated every earlier guard. Not this one."""
    from matrx_files.upload_policy import UploadPolicyNotLive, assert_upload_policy_is_live

    async def _always_allow(user_id, size_bytes):
        return SimpleNamespace(allowed=True, reason=None, raw={})

    with pytest.raises(UploadPolicyNotLive) as exc:
        await assert_upload_policy_is_live(_stub_policy(quota_checker=_always_allow))
    assert "ALLOWED an over-quota upload" in str(exc.value)


async def test_liveness_is_red_for_a_refuse_everything_quota_checker() -> None:
    """Falsifiability: a hardcoded NO would satisfy the test above."""
    from matrx_files.upload_policy import UploadPolicyNotLive, assert_upload_policy_is_live

    async def _always_refuse(user_id, size_bytes):
        return SimpleNamespace(allowed=False, reason="nope", raw={})

    with pytest.raises(UploadPolicyNotLive) as exc:
        await assert_upload_policy_is_live(_stub_policy(quota_checker=_always_refuse))
    assert "without consulting the quota source" in str(exc.value)


async def test_liveness_is_red_for_a_finalize_that_does_not_meter() -> None:
    """`router_tus._default_finalize` is exactly this: it finalizes and nothing else."""
    from matrx_files.upload_policy import UploadPolicyNotLive, assert_upload_policy_is_live

    async def _finalize_without_metering(fm, manager, *, upload_id, user_id, request_id):
        return await manager.finalize_async(
            upload_id=upload_id, owner_id=user_id, extra_metadata={}
        )

    with pytest.raises(UploadPolicyNotLive) as exc:
        await assert_upload_policy_is_live(_stub_policy(finalize=_finalize_without_metering))
    assert "wrote NO usage delta" in str(exc.value)


async def test_liveness_is_red_for_a_hook_that_is_not_callable() -> None:
    """`finalize=None` is the un-metered state wearing the right kwarg name."""
    from matrx_files.upload_policy import UploadPolicyNotLive, assert_upload_policy_is_live

    with pytest.raises(UploadPolicyNotLive) as exc:
        await assert_upload_policy_is_live(_stub_policy(finalize=None))
    assert "not a callable" in str(exc.value)


async def test_liveness_is_red_when_the_rag_lane_is_never_reached() -> None:
    """An armed decider that is dropped on the floor: unreachable, not absent.

    The probe row carries NO organization_id, so a live enqueue must refuse it
    by name. A finalize that ignores its decider finishes cleanly instead — and
    a hook that is never called can never fail.
    """
    from matrx_files.upload_policy import UploadPolicyNotLive, assert_upload_policy_is_live

    def _build(file_service, *, index_for_knowledge=None, is_guest=False):
        from matrx_files.upload_policy import build_package_finalize, build_quota_checker

        inner = build_package_finalize(index_for_knowledge=None)

        async def _finalize_ignoring_the_decider(fm, manager, **kw):
            return await inner(fm, manager, **kw)

        # Reports ARMED, behaves UNARMED — the whole point of the probe.
        _finalize_ignoring_the_decider.matrx_meters_usage = True
        _finalize_ignoring_the_decider.matrx_rag_armed = index_for_knowledge is not None
        return {
            "quota_checker": build_quota_checker(file_service, is_guest=is_guest),
            "finalize": _finalize_ignoring_the_decider,
            "arming": "stub",
        }

    with pytest.raises(UploadPolicyNotLive) as exc:
        await assert_upload_policy_is_live(_build)
    assert "without reaching the RAG enqueue" in str(exc.value)


def test_create_app_builds_its_policy_through_the_factory_the_guard_exercises() -> None:
    """The seam the liveness guard depends on: one factory, not two wirings.

    Red if `create_app` goes back to assembling the hooks inline — the guard
    would then be proving a factory the service does not use.
    """
    body = _create_app_source()
    tree = ast.parse(body)
    calls = {
        getattr(node.func, "id", None)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    assert "build_upload_policy" in calls, (
        "create_app() no longer builds its upload policy through "
        "build_upload_policy(). assert_upload_policy_is_live exercises THAT "
        "factory; an inline wiring here is a second wiring nothing proves live."
    )
