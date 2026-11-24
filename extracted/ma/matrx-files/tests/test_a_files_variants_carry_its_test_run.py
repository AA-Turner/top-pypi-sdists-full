"""A TEST RUN'S FILE AND ITS VARIANTS ARE STAMPED TOGETHER (CGU-10 AND-IMG13 #6, 2026-11-11).

Live (AND-V IMG12): of each stored picture's 3 variant rows, 2 carried no ``test_run_id`` — so
``platform.archive_test_run`` archived the picture and left its variants live. The variants are written by the
thumbnail job ``upload_simple`` fires after the master lands, through ``supervised_task`` → ``detached_task``,
which starts unstamped unless told the work is THIS request's own records (``carry_test_run``).

SUT: ``FileService.upload_simple`` over the real ``SyncEngine`` on the files double; the thumbnail job is
replaced by a probe that reads the test-run stamp it runs under. Drop ``carry_test_run=True`` at the thumbnail
call (or from ``supervised_task``) → red.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService
from matrx_files.standalone import test_stamp

USER = "user-id"
PERSONAL_ORG = "org-personal-user-id"
RUN = "6ee2de55-c7b6-46eb-9b6a-a28e4c6e7890"


@pytest.fixture
def service():
    db = FilesDB()
    db.org_members.add((USER, PERSONAL_ORG))
    with db.bound():
        yield FileService(SimpleNamespace(sync_engine=build_engine(db, user_id=USER, organization_id=PERSONAL_ORG)))


async def test_the_variants_job_runs_under_the_uploads_test_run(service, monkeypatch):
    import matrx_files.cloud_sync.processing as processing

    seen: list[str | None] = []
    done = asyncio.Event()

    async def probe(_fm, _file_id):
        seen.append(test_stamp.current_test_run_id())
        done.set()

    monkeypatch.setattr(processing, "generate_thumbnail_for_file", probe)
    token = test_stamp._current.set(RUN)
    try:
        await service.upload_simple(
            b"\x89PNG picture bytes",
            file_path="generations/images/picture.png",
            user_id=USER,
            mime_type="image/png",
            auto_thumbnail=True,
            auto_rekey=False,
        )
    finally:
        test_stamp._current.reset(token)
    await asyncio.wait_for(done.wait(), timeout=5)
    assert seen == [RUN], f"the variants job ran unstamped: {seen}"


async def test_without_a_test_run_nothing_is_stamped(service, monkeypatch):
    import matrx_files.cloud_sync.processing as processing

    seen: list[str | None] = []
    done = asyncio.Event()

    async def probe(_fm, _file_id):
        seen.append(test_stamp.current_test_run_id())
        done.set()

    monkeypatch.setattr(processing, "generate_thumbnail_for_file", probe)
    await service.upload_simple(
        b"\x89PNG picture bytes", file_path="generations/images/plain.png", user_id=USER,
        mime_type="image/png", auto_thumbnail=True, auto_rekey=False,
    )
    await asyncio.wait_for(done.wait(), timeout=5)
    assert seen == [None]
