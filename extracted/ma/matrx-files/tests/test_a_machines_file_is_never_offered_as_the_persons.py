"""A file a machine writes carries the machine-artifact marker from the first byte.

SUT: the ONE upload door — ``FileService.upload_for_organization`` / ``SyncEngine.managed_write_async``
over the real ``DatabaseClient`` and the insert constraints captured from Matrx Main
(``_files_db_double``), plus the TUS transport's own row insert. S3 and IAM RPCs are the only doubles.

WHY (2026-09-29, one-source-input fix round V3-C item 5). The person's pick lists — the Source
input's "Use existing → Files" and the organization inventory — read ONE database filter,
``platform._inventory_filter``, which hides a file whose ``metadata`` contains
``{"system_artifact": true}``. The page-capture landing's gzipped originals
(``page-captures-<org>/scrape_parsed_page/<host>/<hash>.json.gz``, 880 alive rows) and files under
``coding-sessions/`` never carried it, so they flooded those lists. The marker is now derived from
the path at the door (``matrx_files.user_visible.stamp_machine_artifact``), so no writer has to
remember it.

Breaks guarded:
* a page-capture original / a coding-session file / a TUS upload under a machine namespace lands
  without ``system_artifact`` (the live defect);
* a person's own upload, or a person's deliverable carried for an organization (an HR letter),
  is stamped and vanishes from their pick list;
* a writer's own ``artifact_domain`` (``web_crawl`` carries access meaning) is overwritten;
* a new carried root is added without saying whether its files are machine output.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService
from matrx_files.user_visible import (
    CARRIED_ROOTS,
    MACHINE_CARRIED_ROOTS,
    MACHINE_NAMESPACE_DOMAINS,
    MACHINE_NAMESPACES,
    PERSON_CARRIED_ROOTS,
    machine_artifact_marker,
    stamp_machine_artifact,
)

USER = "87a6e699-0000-4000-8000-000000000001"
ORG = "884d1ce8-0000-4000-8000-00000000000a"
ORIGINAL = b'{"url": "https://en.wikipedia.org/wiki/Recycling", "html": "<html>...</html>"}'


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER, ORG))
    with db.bound():
        yield db


@pytest.fixture
def engine(files_db):
    return build_engine(files_db, user_id=USER, organization_id=ORG)


@pytest.fixture
def service(engine):
    return FileService(SimpleNamespace(sync_engine=engine))


def _row(files_db: FilesDB, file_id: Any) -> dict[str, Any]:
    return {str(r["id"]): r for r in files_db.files.rows.values()}[str(file_id)]


def _hidden_from_pick_lists(row: dict[str, Any]) -> bool:
    """``platform._inventory_filter``'s metadata clause: ``metadata @> '{"system_artifact": true}'``."""
    return (row.get("metadata") or {}).get("system_artifact") is True


async def test_a_page_capture_original_is_a_machine_artifact(files_db, service):
    """The landing's exact request shape (content_processing/landing.py)."""
    result = await service.upload_for_organization(
        ORIGINAL,
        owner_id=USER,
        organization_id=ORG,
        root="page-captures",
        source_key="scrape_parsed_page",
        source_label="Web pages",
        sub_folders=["en-wikipedia-org"],
        file_name="b2a68df3bdafecff66ab0b65.json.gz",
        mime_type="application/gzip",
        published_to_web=False,
        metadata={"source_original": True, "source_kind": "scrape_parsed_page"},
    )
    row = _row(files_db, result.file_id)

    assert row["file_path"].startswith(f"page-captures-{ORG}/")
    assert _hidden_from_pick_lists(row)
    assert row["metadata"]["artifact_domain"] == "page_capture"
    # The writer's own metadata is kept, not replaced.
    assert row["metadata"]["source_original"] is True


async def test_a_coding_session_file_is_a_machine_artifact(files_db, engine):
    """A mirror placement under coding-sessions/ with no artifact kind (the 14 live leakers)."""
    result = await engine.managed_write_async(
        "coding-sessions/claude_code/a549016a-298d-4da6-b7d0-7523ae9cd2f9/notes/alpha.md",
        b"# alpha\n",
        user_id=USER,
        metadata={},
    )
    row = _row(files_db, result.file_id)

    assert _hidden_from_pick_lists(row)
    assert row["metadata"]["artifact_domain"] == "coding_session"


async def test_a_resumable_upload_under_a_machine_namespace_is_marked(monkeypatch):
    """The TUS transport inserts its own row; it must stamp the same marker."""
    from _tus_harness import build_world, upload_file

    world = build_world(monkeypatch)
    _, result = await upload_file(
        world,
        owner="tus-owner",
        path="coding-sessions/_probe/size-5000000.jsonl",
        content=b'{"line": 1}\n',
        metadata={},
    )
    row = world.files.rows[result.file_id]

    assert _hidden_from_pick_lists(row)


async def test_a_persons_upload_stays_pickable(files_db, engine):
    result = await engine.managed_write_async(
        "My Files/Recycling/intake-checklist.md",
        b"- weigh the load\n- photograph the manifest\n",
        user_id=USER,
        metadata={"note": "uploaded in the app"},
    )
    row = _row(files_db, result.file_id)

    assert not _hidden_from_pick_lists(row)
    assert "artifact_domain" not in row["metadata"]


async def test_a_persons_deliverable_carried_for_an_organization_stays_pickable(files_db, service):
    """An employment-verification letter is something a person asked for and may attach."""
    result = await service.upload_for_organization(
        b"%PDF-1.7 employment verification letter",
        owner_id=USER,
        organization_id=ORG,
        root="hr-letters",
        source_key="verification",
        source_label="Verification letters",
        file_name="verification-letter.pdf",
        mime_type="application/pdf",
        published_to_web=False,
    )
    row = _row(files_db, result.file_id)

    assert not _hidden_from_pick_lists(row)


def test_a_writers_own_domain_always_wins():
    crawl_path = f"web-crawls-{ORG}/site/body.html"
    stamped = stamp_machine_artifact(crawl_path, {"artifact_domain": "web_crawl", "web_site_id": "s"})
    assert stamped == {"artifact_domain": "web_crawl", "web_site_id": "s", "system_artifact": True}
    # A carried root whose domain carries access meaning never gets one invented for it.
    assert machine_artifact_marker(crawl_path) == {"system_artifact": True}
    # A person's path is returned untouched — the very same object.
    meta = {"a": 1}
    assert stamp_machine_artifact("My Files/a.md", meta) is meta
    # Only the FIRST segment names a machine namespace or a carried root.
    assert machine_artifact_marker("My Files/coding-sessions/x.md") == {}
    assert machine_artifact_marker("page-captures/guard/x") == {}
    assert machine_artifact_marker("/coding-sessions/x") != {}


def test_every_carried_root_says_whether_its_files_are_machine_output():
    """A new carried root must choose — the partition is exact."""
    machine, person = set(MACHINE_CARRIED_ROOTS), set(PERSON_CARRIED_ROOTS)
    assert not machine & person, f"a root is declared both ways: {sorted(machine & person)}"
    assert machine | person == set(CARRIED_ROOTS), (
        f"undeclared carried roots: {sorted(set(CARRIED_ROOTS) - machine - person)}; "
        f"unknown declared roots: {sorted((machine | person) - set(CARRIED_ROOTS))}"
    )
    assert set(MACHINE_NAMESPACE_DOMAINS) == set(MACHINE_NAMESPACES)
