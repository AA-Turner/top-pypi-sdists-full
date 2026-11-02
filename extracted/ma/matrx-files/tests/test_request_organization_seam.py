"""A verified X-Organization-Id reaches the write, in EVERY host shape (2026-09-19 outage).

SUT: the seam between "the auth boundary admitted an organization for this request" and
"the file write funnel knows which organization to write in".

The outage (`common-docs/projects/acquisition-frontier/own-files/VERIFICATION.md` §15/§16):
dropping 21 files on a fresh Rulebook fired 21 uploads to `files.matrxserver.com` and ALL 21
returned `400 matrx-files: this write carries no organization` — with a correct, membership-
VERIFIED `X-Organization-Id` on every request. `AuthMiddleware` pins the verified organization
on the **matrx-connect** `AppContext`; `SyncEngine._carried_organization_id` read the
**matrx-utils** ambient context; the two are joined only by a host calling
`matrx_utils.configure_context`, which the matrx-files standalone app never did.

Each test below fails on the pre-fix tree and passes after. Run with
`-p no:cacheprovider` from `packages/matrx-files`.

Breaks guarded, one per class:
  1. a host that wires ONLY matrx-connect (the standalone shape) cannot resolve an
     organization — the literal outage;
  2. the buffered upload edge stops resolving the organization itself and goes back to
     hoping a metadata dict was filled;
  3. `managed_write_async` ignores the explicit `organization_id=` thread and reads
     metadata instead;
  4. the standalone app boots with no organization seam at all and only discovers it when a
     person drags a file.
"""

from __future__ import annotations

import inspect
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


# ---------------------------------------------------------------------------
# Host shapes. `None` for a seam means "this host did not wire it".
# ---------------------------------------------------------------------------

ADMITTED_ORG = "0a000000-0000-4000-8000-0000000000aa"
OTHER_ORG = "0a000000-0000-4000-8000-0000000000bb"


class _FakeAppContext:
    def __init__(self, organization_id: str | None) -> None:
        self.user_id = "0b000000-0000-4000-8000-000000000001"
        self.is_authenticated = True
        self.organization_id = organization_id


@pytest.fixture
def host(monkeypatch):
    """Install one host shape: which of the two context seams exists, and what it carries."""
    from matrx_utils import ctx as matrx_ctx

    def install(*, matrx_utils_org: str | None, matrx_connect_org: str | None):
        monkeypatch.setattr(
            matrx_ctx,
            "_context_getter",
            (
                (
                    lambda: matrx_ctx.SimpleUserContext(
                        user_id="0b000000-0000-4000-8000-000000000001",
                        is_authenticated=True,
                        organization_id=matrx_utils_org,
                    )
                )
                if matrx_utils_org is not None
                else None
            ),
            raising=False,
        )
        fake_connect = types.ModuleType("matrx_connect")
        fake_connect.get_app_context = lambda: (
            _FakeAppContext(matrx_connect_org) if matrx_connect_org is not None else None
        )
        monkeypatch.setitem(sys.modules, "matrx_connect", fake_connect)

    return install


# ---------------------------------------------------------------------------
# 1. The literal outage: the standalone host wires only matrx-connect.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "matrx_utils_org,matrx_connect_org,expected",
    [
        # The matrx-files STANDALONE service (files.matrxserver.com) as it really
        # is: AuthMiddleware admitted the org onto the AppContext, and nothing
        # ever called matrx_utils.configure_context. THIS is the 400.
        pytest.param(None, ADMITTED_ORG, ADMITTED_ORG, id="standalone-connect-only"),
        # aidream: configure_context(try_get_app_context) joins both seams.
        pytest.param(ADMITTED_ORG, ADMITTED_ORG, ADMITTED_ORG, id="aidream-both-seams"),
        # A background task deliberately scoped with set_manual_context keeps
        # winning over whatever request context happens to be lying around.
        pytest.param(ADMITTED_ORG, OTHER_ORG, ADMITTED_ORG, id="manual-scope-wins"),
        # A request that genuinely named no organization is still None — never
        # a default, never an organization picked for the owner.
        pytest.param(None, None, None, id="no-organization-stays-none"),
    ],
)
def test_admitted_organization_is_readable_in_every_host_shape(
    host, matrx_utils_org, matrx_connect_org, expected
):
    host(matrx_utils_org=matrx_utils_org, matrx_connect_org=matrx_connect_org)
    from matrx_files.request_organization import admitted_organization_id

    assert admitted_organization_id() == expected


def test_write_funnel_resolves_the_admitted_org_on_a_connect_only_host(host):
    """The ONE write funnel, on the exact host shape that produced the 400."""
    host(matrx_utils_org=None, matrx_connect_org=ADMITTED_ORG)
    from matrx_files.cloud_sync.sync_engine import SyncEngine

    engine = object.__new__(SyncEngine)
    # No explicit org and no metadata org — exactly what the buffered upload
    # door passed before the fix. Branch 2 of the funnel must answer.
    assert engine._carried_organization_id() == ADMITTED_ORG


def test_write_funnel_refuses_and_never_defaults_when_nobody_named_an_org(host):
    """The refusal is preserved: no seam AND no explicit org is still a refusal."""
    host(matrx_utils_org=None, matrx_connect_org=None)
    from matrx_files.cloud_sync.sync_engine import SyncEngine

    engine = object.__new__(SyncEngine)
    assert engine._carried_organization_id() is None
    with pytest.raises(ValueError, match="carries no organization"):
        engine._resolve_write_organization_id("0b000000-0000-4000-8000-000000000001", None)


# ---------------------------------------------------------------------------
# 2-3. The organization is threaded EXPLICITLY from the edge, not fished out of
#      a metadata dict some other layer may not have filled.
# ---------------------------------------------------------------------------


def test_buffered_upload_edge_resolves_the_organization_once_and_threads_it():
    """`POST /files/upload` names the organization in the call, not in a dict."""
    source = Path(
        __import__("matrx_files").__file__
    ).parent / "api" / "router_files.py"
    text = source.read_text()
    upload = text[text.index("async def upload_file(") : text.index("@router.get(\"/sync/changes\"")]
    assert "admitted_organization_id()" in upload, (
        "the upload edge must resolve the request's organization itself — "
        "leaving it to an ambient read deep in the write path is the 2026-09-19 outage"
    )
    assert upload.count("organization_id=request_organization_id") == 2, (
        "BOTH upload doors (upload_simple and upload_with_intent) must be handed "
        "the edge-resolved organization explicitly"
    )


def test_tus_create_stamps_the_admitted_organization_on_the_session():
    """A resumable upload lands in the org it was OPENED in, not the finalizer's."""
    source = Path(
        __import__("matrx_files").__file__
    ).parent / "api" / "router_tus.py"
    text = source.read_text()
    create = text[text.index("async def tus_create(") :]
    assert "admitted_organization_id()" in create
    assert 'row_metadata["organization_id"]' in create


@pytest.mark.parametrize("func_name", ["managed_write_async"])
def test_write_path_accepts_an_explicit_organization(func_name):
    from matrx_files.cloud_sync.sync_engine import SyncEngine

    sig = inspect.signature(getattr(SyncEngine, func_name))
    assert "organization_id" in sig.parameters, (
        f"{func_name} must accept the organization explicitly; a write whose "
        "organization can only arrive through `metadata` depends on every "
        "intermediate layer remembering to copy it"
    )


def test_explicit_organization_outranks_the_metadata_dict():
    """Precedence, read off the one line that decides it."""
    source = (
        Path(__import__("matrx_files").__file__).parent
        / "cloud_sync"
        / "sync_engine.py"
    ).read_text()
    assert (
        "requested_org_id = organization_id or self._metadata_organization_id(metadata_dict)"
        in source
    ), "the explicit thread must be read BEFORE the metadata dict"


def test_upload_simple_threads_the_organization_through():
    from matrx_files.service import FileService

    sig = inspect.signature(FileService.upload_simple)
    assert "organization_id" in sig.parameters


# ---------------------------------------------------------------------------
# 4. A host with no seam at all says so at BOOT, not on the first drag-and-drop.
# ---------------------------------------------------------------------------


def test_standalone_host_wires_the_context_seam():
    source = (
        Path(__import__("matrx_files").__file__).parent / "standalone" / "app.py"
    ).read_text()
    assert "_configure_context_for_standalone()" in source
    assert "configure_context" in source
    assert "_assert_organization_seam()" in source


def test_boot_guard_refuses_a_host_with_no_organization_seam(monkeypatch):
    from matrx_files._config import IndependenceConfigError
    from matrx_files.standalone import app as standalone_app

    monkeypatch.setattr(
        standalone_app,
        "context_seam_status",
        lambda: {"matrx_utils_context": False, "matrx_connect_app_context": False},
        raising=False,
    )
    # The guard imports the status function locally; patch it at the source.
    import matrx_files.request_organization as request_organization

    monkeypatch.setattr(
        request_organization,
        "context_seam_status",
        lambda: {"matrx_utils_context": False, "matrx_connect_app_context": False},
    )
    with pytest.raises(IndependenceConfigError, match="NO organization context seam"):
        standalone_app._assert_organization_seam()


def test_boot_guard_passes_when_a_seam_exists(monkeypatch):
    import matrx_files.request_organization as request_organization
    from matrx_files.standalone import app as standalone_app

    monkeypatch.setattr(
        request_organization,
        "context_seam_status",
        lambda: {"matrx_utils_context": False, "matrx_connect_app_context": True},
    )
    standalone_app._assert_organization_seam()
