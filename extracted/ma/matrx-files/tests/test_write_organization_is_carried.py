"""A file write's ORGANIZATION is carried, never defaulted to an organization picked for the owner.

SUT: ``SyncEngine._resolve_write_organization_id{,_async}`` — the ONE funnel every
file write (managed_write, track_write, TUS finalize, presigned finalize, external
object adoption, upload_with_intent) passes through — over the real
``DatabaseClient`` and the insert constraints captured from Matrx Main
(``_files_db_double``).

Until 2026-09-17 the funnel ended in a per-user saved-organization lookup:
a write whose caller had dropped the organization landed SILENTLY in the owner's
own workspace instead of the tenant the person was working in — no error, no row
anywhere, and the file is then invisible to the organization it belongs to. That
RPC answers exactly one question ("which organization is this user's OWN
workspace") and is never the answer to "nobody passed one".

Law: common-docs/policies/context-is-carried-never-rebuilt.md (rule 4).
"""

from __future__ import annotations

import pytest
from _files_db_double import FilesDB, build_engine

USER = "user-id"
CARRIED_ORG = "org-carried-0001"
EXPLICIT_ORG = "org-explicit-0002"
PERSONAL_ORG = "org-personal-of-user-id"
FILE_PATH = "docs/report.pdf"
CONTENT = b"report bytes\n"


@pytest.fixture
def files_db():
    db = FilesDB()
    # The owner HAS a personal organization — the point is that nothing reaches
    # for it. A test that removed it would prove only that the lookup is absent.
    db.org_members.update({(USER, CARRIED_ORG), (USER, EXPLICIT_ORG), (USER, PERSONAL_ORG)})
    with db.bound():
        yield db


def _drop_the_carried_organization() -> None:
    """What a boundary defect looks like here: no context at all."""
    from matrx_utils import ctx as matrx_ctx

    matrx_ctx._context_getter = None


def _carry_an_organizationless_context() -> None:
    """The other shape: a context that exists but lost its organization."""
    from matrx_utils import ctx as matrx_ctx

    matrx_ctx._context_getter = lambda: matrx_ctx.SimpleUserContext(
        user_id=USER, is_authenticated=True, organization_id=None
    )


@pytest.mark.asyncio
async def test_the_write_lands_in_the_organization_the_request_carries(files_db):
    engine = build_engine(files_db, user_id=USER, organization_id=CARRIED_ORG)

    result = await engine.managed_write_async(FILE_PATH, CONTENT)

    assert files_db.files.rows[result.file_id]["organization_id"] == CARRIED_ORG


@pytest.mark.asyncio
async def test_an_explicit_organization_outranks_the_carried_one(files_db):
    engine = build_engine(files_db, user_id=USER, organization_id=CARRIED_ORG)

    result = await engine.managed_write_async(
        FILE_PATH,
        CONTENT,
        metadata={"organization_id": EXPLICIT_ORG},
    )

    assert files_db.files.rows[result.file_id]["organization_id"] == EXPLICIT_ORG


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "break_the_boundary",
    [_drop_the_carried_organization, _carry_an_organizationless_context],
    ids=["no-context-at-all", "context-without-an-organization"],
)
async def test_a_write_with_no_carried_organization_refuses_and_writes_nothing(
    files_db, break_the_boundary
):
    engine = build_engine(files_db, user_id=USER, organization_id=CARRIED_ORG)
    break_the_boundary()

    with pytest.raises(ValueError, match="never defaulted to an organization picked for the owner"):
        await engine.managed_write_async(FILE_PATH, CONTENT)

    assert files_db.live_files() == []
    assert PERSONAL_ORG not in {r.get("organization_id") for r in files_db.files.rows.values()}


def test_the_sync_twin_refuses_the_same_way(files_db):
    engine = build_engine(files_db, user_id=USER, organization_id=CARRIED_ORG)
    _drop_the_carried_organization()

    with pytest.raises(ValueError, match="never defaulted to an organization picked for the owner"):
        engine._resolve_write_organization_id(USER)

    assert files_db.live_files() == []
