"""GUARD — a whole data export can be uploaded, and survives an interruption.

A person's Google Takeout, Slack workspace export or photo library is routinely
bigger than 5 GB, and uploading one takes long enough that something WILL
interrupt it: a laptop lid, a train tunnel, a server deploy. So two properties
have to hold together, and neither is worth anything alone:

1. the transport must accept the file at all, and when it refuses, the refusal
   must be a sentence naming what to do — not a number;
2. an upload interrupted at any point must resume from exactly where it stopped
   and assemble to byte-identical content.

Each test below has its failing half run for real rather than asserted, so the
guard cannot quietly stop guarding:

* ``test_the_old_ceiling_really_did_refuse_a_twelve_gigabyte_export`` builds a
  manager at the old 5 GB ceiling and watches it refuse the export;
* ``test_a_five_mib_chunk_on_a_huge_upload_is_refused_before_it_wastes_hours``
  shows the failure that used to arrive ten thousand chunks in.

SUT: the real ``TUSSessionManager`` and the real router. Only S3, the ORM layer
and the host RPCs are doubled (``tests/_tus_harness.py``). Expected bytes come
from ``hashlib`` over what the test sent.
"""

from __future__ import annotations

import hashlib

import pytest
from _tus_harness import MIN_PART, TusWorld, build_world, chunks_of
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.api.router_tus import build_tus_router
from matrx_files.cloud_sync.transports.tus import (
    DEFAULT_MAX_SIZE,
    S3_MAX_PARTS,
    ExceedsLength,
    PartTooSmall,
    TUSSessionManager,
)

OWNER = "11111111-1111-1111-1111-111111111111"
GB = 1024 * 1024 * 1024
OLD_CEILING = 5 * GB
TAKEOUT_BYTES = 12 * GB


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    return build_world(monkeypatch)


# ---------------------------------------------------------------------------
# 1. The ceiling
# ---------------------------------------------------------------------------


async def test_the_old_ceiling_really_did_refuse_a_twelve_gigabyte_export(
    world: TusWorld,
) -> None:
    """The failing half, executed. This is the block a real person hit."""
    old = TUSSessionManager(world.engine, max_size=OLD_CEILING, min_part_bytes=MIN_PART)
    with pytest.raises(ExceedsLength):
        await old.create_async(
            owner_id=OWNER,
            file_path="exports/takeout.tgz",
            upload_length=TAKEOUT_BYTES,
        )


async def test_a_twelve_gigabyte_export_is_accepted_now(world: TusWorld) -> None:
    created = await world.manager.create_async(
        owner_id=OWNER,
        file_path="exports/takeout.tgz",
        upload_length=TAKEOUT_BYTES,
    )
    assert created.upload_offset == 0
    assert created.upload_length == TAKEOUT_BYTES
    assert world.session_row(created.upload_id)["upload_length"] == TAKEOUT_BYTES


async def test_the_refusal_names_what_to_do_not_just_a_number(world: TusWorld) -> None:
    small = TUSSessionManager(world.engine, max_size=GB, min_part_bytes=MIN_PART)
    with pytest.raises(ExceedsLength) as excinfo:
        await small.create_async(
            owner_id=OWNER,
            file_path="exports/takeout.tgz",
            upload_length=TAKEOUT_BYTES,
        )
    message = str(excinfo.value)
    assert "12.9 GB" in message or "12.9" in message, "say how big the file actually is"
    assert "administrator" in message, "say who can change it"
    assert "quota" in message, (
        "say that this is not the storage quota — otherwise the person goes and "
        "deletes files for nothing"
    )
    assert "upload_length" not in message, "a person never reads a field name"


def test_the_default_ceiling_is_big_enough_for_a_real_export() -> None:
    assert DEFAULT_MAX_SIZE > OLD_CEILING
    assert DEFAULT_MAX_SIZE >= 64 * GB, (
        "a photo library or a multi-account Takeout runs to tens of gigabytes"
    )


# ---------------------------------------------------------------------------
# 2. Resume
# ---------------------------------------------------------------------------


async def test_an_interrupted_upload_resumes_and_assembles_byte_identically(
    world: TusWorld,
) -> None:
    """Interrupt after two chunks, restart the server, finish, compare hashes."""
    content = bytes(range(256)) * 40  # 10,240 bytes, every chunk distinguishable
    chunks = chunks_of(content, size=MIN_PART)

    created = await world.manager.create_async(
        owner_id=OWNER,
        file_path="exports/interrupted.bin",
        upload_length=len(content),
    )
    offset = 0
    for chunk in chunks[:2]:
        offset = (
            await world.manager.append_async(
                upload_id=created.upload_id,
                owner_id=OWNER,
                body=chunk,
                client_offset=offset,
            )
        ).new_offset

    interrupted_at = offset
    assert 0 < interrupted_at < len(content)

    # The server restarts: a brand-new manager, with only the durable row to go on.
    restarted = TUSSessionManager(world.engine, min_part_bytes=MIN_PART)
    session = await restarted.get_async(upload_id=created.upload_id, owner_id=OWNER)
    assert session is not None, "an in-flight upload must survive a restart"
    assert session.upload_offset == interrupted_at, (
        "resume must continue from the bytes the server really has, not from zero"
    )

    offset = session.upload_offset
    for chunk in chunks[2:]:
        offset = (
            await restarted.append_async(
                upload_id=created.upload_id,
                owner_id=OWNER,
                body=chunk,
                client_offset=offset,
            )
        ).new_offset

    result = await restarted.finalize_async(upload_id=created.upload_id, owner_id=OWNER)
    stored = world.object_at(world.session_row(created.upload_id)["key"])
    assert stored == content, "the resumed upload did not assemble to the original bytes"
    assert result.size_bytes == len(content)
    assert hashlib.sha256(stored).hexdigest() == hashlib.sha256(content).hexdigest()


async def test_resending_a_chunk_the_server_already_has_is_refused_by_offset(
    world: TusWorld,
) -> None:
    """A client that resumes from its own idea of the offset must be corrected."""
    from matrx_files.cloud_sync.transports.tus import OffsetMismatch

    content = b"Z" * (MIN_PART * 4)
    created = await world.manager.create_async(
        owner_id=OWNER, file_path="exports/dup.bin", upload_length=len(content)
    )
    await world.manager.append_async(
        upload_id=created.upload_id, owner_id=OWNER, body=content[:MIN_PART],
        client_offset=0,
    )
    with pytest.raises(OffsetMismatch):
        await world.manager.append_async(
            upload_id=created.upload_id, owner_id=OWNER, body=content[:MIN_PART],
            client_offset=0,
        )


# ---------------------------------------------------------------------------
# 3. Part sizing — the failure that used to arrive ten thousand chunks in
# ---------------------------------------------------------------------------


def test_part_sizing_keeps_a_huge_upload_inside_the_storage_part_limit(
    world: TusWorld,
) -> None:
    for size in (1 * GB, 50 * GB, 60 * GB, DEFAULT_MAX_SIZE):
        advised = world.manager.advise_part_bytes(size)
        parts = -(-size // advised)
        assert parts <= S3_MAX_PARTS, (
            f"a {size / GB:.0f} GB upload at the advised {advised / 1e6:.0f} MB chunk "
            f"would need {parts:,} parts, above the {S3_MAX_PARTS:,} storage allows"
        )
        assert advised >= world.manager.min_part_bytes


async def test_a_too_small_chunk_on_a_huge_upload_is_refused_before_it_wastes_hours(
    world: TusWorld,
) -> None:
    """The failing half: at a fixed 5 MiB chunk a 60 GB upload dies at part 10,001.

    60 GB in 5 MiB chunks is 12,288 parts, and storage accepts 10,000. It used
    to die at part 10,001 — hours in, with the bytes already sent. Now it is
    refused on the first chunk, with the chunk size to use.
    """
    manager = TUSSessionManager(world.engine, min_part_bytes=5 * 1024 * 1024)
    created = await manager.create_async(
        owner_id=OWNER, file_path="exports/huge.bin", upload_length=60 * GB
    )
    with pytest.raises(PartTooSmall) as excinfo:
        await manager.append_async(
            upload_id=created.upload_id,
            owner_id=OWNER,
            body=b"x" * (5 * 1024 * 1024),
            client_offset=0,
        )
    message = str(excinfo.value)
    assert "MB" in message and "resumes" in message, (
        "the refusal must say the size to use and that nothing is lost"
    )


# ---------------------------------------------------------------------------
# 4. What the server advertises is what it enforces
# ---------------------------------------------------------------------------


def test_options_advertises_the_ceiling_that_is_actually_enforced(
    world: TusWorld,
) -> None:
    configured = 40 * GB
    app = FastAPI()
    app.include_router(
        build_tus_router(
            file_manager_dep=lambda: world.file_manager,
            user_id_dep=lambda: OWNER,
            max_size=configured,
        )
    )
    response = TestClient(app).options("/files/upload/tus")
    assert response.status_code == 204
    assert response.headers["Tus-Max-Size"] == str(configured), (
        "a client told one ceiling and refused at another cannot tell policy from bug"
    )
