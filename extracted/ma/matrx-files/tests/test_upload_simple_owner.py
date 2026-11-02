"""The buffered door files a save under the person the request carries, never ``''``.

Break (production, 2026-10-21 17:56 UTC onward): every paid media save (podcast
audio, xAI images, OpenAI audio, request snapshots) failed with
``invalid input syntax for type uuid: ""`` on
``SELECT * FROM files.files WHERE created_by = $1 AND file_path = $2``.
The process-wide cloud FileManager's ``CloudSyncConfig.user_id`` is empty by
design (the person comes from the request context), so callers pass
``user_id=fm.sync_engine.user_id`` == ``''``. 8f11a14e77 added a path lookup at
the top of ``upload_simple`` that used that raw argument before the engine
resolved it from the context.

SUT: ``FileService.upload_simple`` over the real ``SyncEngine`` and
``DatabaseClient`` on the files double; the double's path lookup refuses an
empty owner exactly as Postgres's uuid column does.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService

USER = "user-id"
PERSONAL_ORG = "org-personal-user-id"


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER, PERSONAL_ORG))
    with db.bound():
        yield db


@pytest.fixture
def engine(files_db):
    eng = build_engine(files_db, user_id=USER, organization_id=PERSONAL_ORG)
    # Production shape: the shared FileManager bakes NO user; the context carries it.
    eng._config.user_id = ""
    real = eng.db.get_file_by_path_async

    async def uuid_column(owner_id, file_path):
        if not owner_id:
            raise ValueError('invalid input syntax for type uuid: ""')
        return await real(owner_id, file_path)

    eng.db.get_file_by_path_async = uuid_column
    return eng


@pytest.fixture
def service(engine):
    return FileService(SimpleNamespace(sync_engine=engine))


async def test_empty_owner_argument_resolves_to_the_requests_person(files_db, service):
    result = await service.upload_simple(
        b"generated audio bytes",
        file_path="generations/audio/episode.wav",
        user_id="",  # what AIMediaHandler sent: fm.sync_engine.user_id
        auto_thumbnail=False,
        auto_rekey=False,
    )
    row = files_db.files.rows[str(result.file_id)]
    assert str(row["created_by"]) == USER


async def test_no_person_anywhere_is_refused_by_name_before_any_lookup(service):
    from matrx_utils import ctx as matrx_ctx

    from matrx_files.service import FileOwnerMissing

    matrx_ctx._context_getter = lambda: None
    with pytest.raises(FileOwnerMissing, match="no signed-in person"):
        await service.upload_simple(
            b"bytes",
            file_path="generations/audio/orphan.wav",
            user_id="",
            auto_thumbnail=False,
            auto_rekey=False,
        )
